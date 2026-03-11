// wgcCapture.cpp
// Windows Graphics Capture + Windows.Media.Ocr integration for NVDA.
// CreateForWindow captures from the DWM compositor, before the
// Magnification API color transform, so OCR works with screen curtain.

#include <wrl/wrappers/corewrappers.h>
#include <winrt/base.h>
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Foundation.Collections.h>
#include <winrt/Windows.System.h>
#include <winrt/Windows.Graphics.Capture.h>
#include <winrt/Windows.Graphics.DirectX.h>
#include <winrt/Windows.Graphics.DirectX.Direct3D11.h>
#include <winrt/Windows.Graphics.Imaging.h>
#include <winrt/Windows.Media.Ocr.h>
#include <winrt/Windows.Globalization.h>
#include <winrt/Windows.Data.Json.h>
#include <winrt/Windows.Storage.Streams.h>
#include <windows.graphics.capture.interop.h>
#include <windows.graphics.capture.h>
#include <d3d11.h>
#include <dxgi.h>
#include <atomic>
#include <common/log.h>
#include "wgcCapture.h"

#pragma comment(lib, "d3d11.lib")
#pragma comment(lib, "dxgi.lib")

using namespace winrt;
using namespace Windows::Foundation;
using namespace Windows::Graphics;
using namespace Windows::Graphics::Capture;
using namespace Windows::Graphics::DirectX;
using namespace Windows::Graphics::DirectX::Direct3D11;
using namespace Windows::Graphics::Imaging;
using namespace Windows::Media::Ocr;
using namespace Windows::Globalization;
using namespace Windows::Data::Json;

class WgcCapture {
private:
	OcrEngine m_ocrEngine{ nullptr };
	wgcCapture_Callback m_callback;
	IDirect3DDevice m_device{ nullptr };
	com_ptr<ID3D11Device> m_d3dDevice;
	std::atomic<bool> m_cancelled{ false };

	void createDevice() {
		check_hresult(D3D11CreateDevice(
			nullptr,
			D3D_DRIVER_TYPE_HARDWARE,
			nullptr,
			D3D11_CREATE_DEVICE_BGRA_SUPPORT,
			nullptr, 0,
			D3D11_SDK_VERSION,
			m_d3dDevice.put(),
			nullptr,
			nullptr
		));

		auto dxgiDevice = m_d3dDevice.as<IDXGIDevice>();
		com_ptr<IInspectable> inspectable;
		check_hresult(CreateDirect3D11DeviceFromDXGIDevice(
			dxgiDevice.get(), inspectable.put()));
		m_device = inspectable.as<IDirect3DDevice>();
	}

	GraphicsCaptureItem createItemForWindow(HWND hwnd) {
		auto interopFactory = get_activation_factory<
			GraphicsCaptureItem,
			IGraphicsCaptureItemInterop>();

		GraphicsCaptureItem item{ nullptr };
		check_hresult(interopFactory->CreateForWindow(
			hwnd,
			guid_of<GraphicsCaptureItem>(),
			put_abi(item)
		));
		return item;
	}

	hstring serializeOcrResult(OcrResult const& result) {
		JsonArray jLines;
		for (auto const& line : result.Lines()) {
			JsonArray jWords;
			for (auto const& word : line.Words()) {
				JsonObject jWord;
				auto rect = word.BoundingRect();
				jWord.Insert(L"x",
					JsonValue::CreateNumberValue(rect.X));
				jWord.Insert(L"y",
					JsonValue::CreateNumberValue(rect.Y));
				jWord.Insert(L"width",
					JsonValue::CreateNumberValue(rect.Width));
				jWord.Insert(L"height",
					JsonValue::CreateNumberValue(rect.Height));
				jWord.Insert(L"text",
					JsonValue::CreateStringValue(word.Text()));
				jWords.Append(jWord);
			}
			jLines.Append(jWords);
		}
		return jLines.Stringify();
	}

	// Convert a SoftwareBitmap to BGRA8 format suitable for OCR
	SoftwareBitmap toBgra8(SoftwareBitmap const& bitmap) {
		return SoftwareBitmap::Convert(
			bitmap,
			BitmapPixelFormat::Bgra8,
			BitmapAlphaMode::Premultiplied
		);
	}

	// Crop a BGRA8 bitmap to the specified region (clamped to bounds)
	SoftwareBitmap cropBitmap(
		SoftwareBitmap const& src,
		unsigned int regionX,
		unsigned int regionY,
		unsigned int regionW,
		unsigned int regionH)
	{
		unsigned int bmpW = src.PixelWidth();
		unsigned int bmpH = src.PixelHeight();
		unsigned int cx = min(regionX, bmpW);
		unsigned int cy = min(regionY, bmpH);
		unsigned int cw = min(regionW, bmpW - cx);
		unsigned int ch = min(regionH, bmpH - cy);

		if (cw == 0 || ch == 0) {
			return nullptr;
		}

		auto srcBuffer = src.LockBuffer(BitmapBufferAccessMode::Read);
		auto srcRef = srcBuffer.CreateReference();
		auto srcAccess = srcRef.as<
			Windows::Foundation::IMemoryBufferByteAccess>();

		BYTE* srcData = nullptr;
		UINT32 srcCapacity = 0;
		check_hresult(srcAccess->GetBuffer(&srcData, &srcCapacity));
		int srcStride = srcBuffer.GetPlaneDescription(0).Stride;

		SoftwareBitmap dst(
			BitmapPixelFormat::Bgra8, cw, ch,
			BitmapAlphaMode::Premultiplied);

		auto dstBuffer = dst.LockBuffer(BitmapBufferAccessMode::Write);
		auto dstRef = dstBuffer.CreateReference();
		auto dstAccess = dstRef.as<
			Windows::Foundation::IMemoryBufferByteAccess>();

		BYTE* dstData = nullptr;
		UINT32 dstCapacity = 0;
		check_hresult(dstAccess->GetBuffer(&dstData, &dstCapacity));
		int dstStride = dstBuffer.GetPlaneDescription(0).Stride;

		constexpr int bytesPerPixel = 4;  // BGRA8
		for (unsigned int row = 0; row < ch; ++row) {
			BYTE* srcRow = srcData
				+ (cy + row) * srcStride
				+ cx * bytesPerPixel;
			BYTE* dstRow = dstData + row * dstStride;
			memcpy(dstRow, srcRow, cw * bytesPerPixel);
		}

		dstRef.Close();
		dstBuffer.Close();
		srcRef.Close();
		srcBuffer.Close();

		return dst;
	}

public:
	WgcCapture(
		OcrEngine const& engine,
		wgcCapture_Callback callback
	) : m_ocrEngine(engine), m_callback(callback), m_cancelled(false) {
		createDevice();
	}

	void markCancelled() {
		m_cancelled.store(true, std::memory_order_release);
	}

	fire_and_forget recognizeWindow(
		HWND hwnd,
		bool useRegion,
		unsigned int regionX,
		unsigned int regionY,
		unsigned int regionW,
		unsigned int regionH)
	{
		try {
			co_await resume_background();

			if (m_cancelled.load(std::memory_order_acquire)) {
				co_return;
			}

			if (!IsWindow(hwnd)) {
				LOG_ERROR(L"wgcCapture: invalid HWND");
				if (!m_cancelled.load(std::memory_order_acquire)) {
					m_callback(nullptr);
				}
				co_return;
			}

			auto item = createItemForWindow(hwnd);
			auto framePool =
				Direct3D11CaptureFramePool::CreateFreeThreaded(
					m_device,
					DirectXPixelFormat::B8G8R8A8UIntNormalized,
					1,
					item.Size()
				);

			auto session = framePool.CreateCaptureSession(item);

			// Hide yellow border on Win11 (no-op on Win10)
			if (auto session3 =
					session.try_as<IGraphicsCaptureSession3>()) {
				session3.IsBorderRequired(false);
			}

			session.StartCapture();

			Direct3D11CaptureFrame frame{ nullptr };
			for (int attempt = 0; attempt < 20 && !frame; ++attempt) {
				frame = framePool.TryGetNextFrame();
				if (!frame) {
					co_await resume_after(
						std::chrono::milliseconds(50));
				}
			}

			session.Close();
			framePool.Close();

			if (!frame) {
				LOG_ERROR(L"wgcCapture: no frame received");
				if (!m_cancelled.load(std::memory_order_acquire)) {
					m_callback(nullptr);
				}
				co_return;
			}

			auto surface = frame.Surface();
			auto fullBitmap =
				co_await SoftwareBitmap::CreateCopyFromSurfaceAsync(
					surface,
					BitmapAlphaMode::Premultiplied
				);
			frame.Close();

			SoftwareBitmap ocrBitmap{ nullptr };

			if (useRegion) {
				auto converted = toBgra8(fullBitmap);
				ocrBitmap = cropBitmap(
					converted, regionX, regionY, regionW, regionH);
				if (!ocrBitmap) {
					LOG_ERROR(
						L"wgcCapture: region out of bounds");
					if (!m_cancelled.load(std::memory_order_acquire)) {
						m_callback(nullptr);
					}
					co_return;
				}
			} else {
				ocrBitmap = toBgra8(fullBitmap);
			}

			unsigned int maxDim = m_ocrEngine.MaxImageDimension();
			unsigned int ocrW = ocrBitmap.PixelWidth();
			unsigned int ocrH = ocrBitmap.PixelHeight();
			if (ocrW > maxDim || ocrH > maxDim) {
				LOG_WARNING(
					L"wgcCapture: bitmap %ux%u exceeds "
					L"MaxImageDimension %u, OCR may fail",
					ocrW, ocrH, maxDim);
			}

			auto ocrResult =
				co_await m_ocrEngine.RecognizeAsync(ocrBitmap);

			if (m_cancelled.load(std::memory_order_acquire)) {
				co_return;
			}

			auto json = serializeOcrResult(ocrResult);
			m_callback(json.c_str());

		} catch (winrt::hresult_error const& ex) {
			LOG_ERROR(
				L"wgcCapture error: 0x%08X %s",
				ex.code(),
				ex.message().c_str()
			);
			if (!m_cancelled.load(std::memory_order_acquire)) {
				m_callback(nullptr);
			}
		} catch (...) {
			LOG_ERROR(L"wgcCapture: unknown exception");
			if (!m_cancelled.load(std::memory_order_acquire)) {
				m_callback(nullptr);
			}
		}
	}
};


// ---- Exported C functions ----

bool __stdcall wgcCapture_isSupported() {
	try {
		if (!GraphicsCaptureSession::IsSupported()) {
			return false;
		}
		auto interopFactory = get_activation_factory<
			GraphicsCaptureItem,
			IGraphicsCaptureItemInterop>();
		return interopFactory != nullptr;
	} catch (...) {
		return false;
	}
}

WgcCapture_H __stdcall wgcCapture_initialize(
	const wchar_t* language,
	wgcCapture_Callback callback)
{
	if (!callback) {
		LOG_ERROR(L"wgcCapture_initialize: null callback");
		return nullptr;
	}

	try {
		winrt::init_apartment(winrt::apartment_type::multi_threaded);

		OcrEngine engine{ nullptr };
		if (language && language[0] != L'\0') {
			engine = OcrEngine::TryCreateFromLanguage(
				Language{ language });
		} else {
			engine =
				OcrEngine::TryCreateFromUserProfileLanguages();
		}

		if (!engine) {
			LOG_ERROR(
				L"wgcCapture_initialize: "
				L"failed to create OcrEngine");
			return nullptr;
		}

		return static_cast<WgcCapture_H>(
			new WgcCapture(engine, callback));

	} catch (winrt::hresult_error const& ex) {
		LOG_ERROR(
			L"wgcCapture_initialize error: 0x%08X %s",
			ex.code(), ex.message().c_str());
		return nullptr;
	} catch (...) {
		LOG_ERROR(
			L"wgcCapture_initialize: unknown exception");
		return nullptr;
	}
}

void __stdcall wgcCapture_recognizeWindow(
	WgcCapture_H handle, HWND hwnd)
{
	if (!handle || !hwnd) return;
	static_cast<WgcCapture*>(handle)->recognizeWindow(
		hwnd, false, 0, 0, 0, 0);
}

void __stdcall wgcCapture_recognizeWindowRegion(
	WgcCapture_H handle, HWND hwnd,
	unsigned int x, unsigned int y,
	unsigned int width, unsigned int height)
{
	if (!handle || !hwnd) return;
	if (width == 0 || height == 0) return;
	static_cast<WgcCapture*>(handle)->recognizeWindow(
		hwnd, true, x, y, width, height);
}

void __stdcall wgcCapture_terminate(WgcCapture_H handle) {
	if (!handle) return;
	auto* instance = static_cast<WgcCapture*>(handle);
	// Mark cancelled so the coroutine stops calling back into Python.
	// The Python side is responsible for calling terminate only after the
	// recognition callback has fired (matching the uwpOcr pattern),
	// so by this point the coroutine has completed and delete is safe.
	instance->markCancelled();
	delete instance;
}
