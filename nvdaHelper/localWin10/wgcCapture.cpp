/*
A part of NonVisual Desktop Access (NVDA)
Copyright (C) 2026 NV Access Limited, Cary-rowen
This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
*/

#include <algorithm>
#include <chrono>
#include <condition_variable>
#include <cstdint>
#include <exception>
#include <limits>
#include <memory>
#include <mutex>
#include <utility>
#include <vector>

#include <d3d11.h>
#include <dxgi.h>
#include <roapi.h>
#include <wil/resource.h>
#include <winrt/base.h>
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Graphics.Capture.h>
#include <winrt/Windows.Graphics.DirectX.h>
#include <winrt/Windows.Graphics.DirectX.Direct3D11.h>
#include <windows.graphics.capture.interop.h>
#include <windows.graphics.directx.direct3d11.interop.h>

#include <common/log.h>
#include "wgcCapture.h"

using namespace winrt;
using namespace winrt::Windows::Graphics::Capture;
using namespace winrt::Windows::Graphics::DirectX;
using namespace winrt::Windows::Graphics::DirectX::Direct3D11;

namespace {
using CaptureClock = std::chrono::steady_clock;
using CaptureDeadline = CaptureClock::time_point;

constexpr auto captureTimeout = std::chrono::seconds(2);
constexpr std::size_t bytesPerPixel = 4;
constexpr UINT defaultFeatureLevelCount = 0;
constexpr std::int32_t framePoolBufferCount = 1;

static_assert(sizeof(RGBQUAD) == bytesPerPixel);

struct D3DResources {
	com_ptr<ID3D11Device> device;
	com_ptr<ID3D11DeviceContext> context;
	IDirect3DDevice winrtDevice { nullptr };
};

struct FrameCaptureState {
	std::mutex mutex;
	std::condition_variable resultCondition;
	bool isAcceptingFrames { true };
	Direct3D11CaptureFrame frame { nullptr };
	std::exception_ptr error;
};

wil::unique_rouninitialize_call initializeWinRT() {
	const auto result = RoInitialize(RO_INIT_MULTITHREADED);
	if (result == RPC_E_CHANGED_MODE) {
		// The caller has already initialized this thread for another apartment type.
		return wil::unique_rouninitialize_call(false);
	}
	check_hresult(result);
	return {};
}

HRESULT createD3DDevice(
	D3D_DRIVER_TYPE driverType,
	com_ptr<ID3D11Device>& device,
	com_ptr<ID3D11DeviceContext>& context
) {
	return D3D11CreateDevice(
		nullptr,  // adapter
		driverType,
		nullptr,  // software rasterizer module
		D3D11_CREATE_DEVICE_BGRA_SUPPORT,
		nullptr,  // feature levels
		defaultFeatureLevelCount,
		D3D11_SDK_VERSION,
		device.put(),
		nullptr,  // selected feature level
		context.put()
	);
}

D3DResources createD3DResources() {
	D3DResources resources;
	auto result = createD3DDevice(D3D_DRIVER_TYPE_HARDWARE, resources.device, resources.context);
	if (result == DXGI_ERROR_UNSUPPORTED) {
		result = createD3DDevice(D3D_DRIVER_TYPE_WARP, resources.device, resources.context);
	}
	check_hresult(result);

	auto dxgiDevice = resources.device.as<IDXGIDevice>();
	com_ptr<IInspectable> inspectable;
	check_hresult(CreateDirect3D11DeviceFromDXGIDevice(dxgiDevice.get(), inspectable.put()));
	resources.winrtDevice = inspectable.as<IDirect3DDevice>();
	return resources;
}

GraphicsCaptureItem createItemForMonitor(HMONITOR monitor) {
	auto interopFactory = get_activation_factory<GraphicsCaptureItem, IGraphicsCaptureItemInterop>();
	GraphicsCaptureItem item { nullptr };
	check_hresult(interopFactory->CreateForMonitor(
		monitor,
		guid_of<GraphicsCaptureItem>(),
		put_abi(item)
	));
	return item;
}

struct CaptureMonitor {
	HMONITOR handle;
	RECT bounds;
};

struct MonitorCollection {
	std::vector<CaptureMonitor> monitors;
	std::exception_ptr error;
};

BOOL CALLBACK collectMonitor(
	HMONITOR monitor,
	HDC,
	LPRECT,
	LPARAM collectionAddress
) noexcept {
	auto& collection = *reinterpret_cast<MonitorCollection*>(collectionAddress);
	try {
		MONITORINFO monitorInfo { sizeof(monitorInfo) };
		if (!GetMonitorInfoW(monitor, &monitorInfo)) {
			throw_last_error();
		}
		collection.monitors.push_back({ monitor, monitorInfo.rcMonitor });
		return true;
	} catch (...) {
		collection.error = std::current_exception();
		return false;
	}
}

std::vector<CaptureMonitor> getMonitorsForRegion(RECT const& region) {
	MonitorCollection collection;
	if (!EnumDisplayMonitors(
		nullptr,
		&region,
		collectMonitor,
		reinterpret_cast<LPARAM>(&collection)
	)) {
		if (collection.error) {
			std::rethrow_exception(collection.error);
		}
		LOG_ERROR(L"wgcCapture: failed to enumerate monitors");
		return {};
	}
	return std::move(collection.monitors);
}

Direct3D11CaptureFrame captureFrame(
	D3DResources const& resources,
	GraphicsCaptureItem const& item,
	CaptureDeadline deadline
) {
	const auto itemSize = item.Size();
	if (itemSize.Width <= 0 || itemSize.Height <= 0) {
		LOG_ERROR(L"wgcCapture: capture item has invalid dimensions");
		return nullptr;
	}

	auto framePool = Direct3D11CaptureFramePool::CreateFreeThreaded(
		resources.winrtDevice,
		DirectXPixelFormat::B8G8R8A8UIntNormalized,
		framePoolBufferCount,
		itemSize
	);
	auto session = framePool.CreateCaptureSession(item);
	if (auto session2 = session.try_as<IGraphicsCaptureSession2>()) {
		session2.IsCursorCaptureEnabled(false);
	}

	auto state = std::make_shared<FrameCaptureState>();
	auto frameArrivedRevoker = framePool.FrameArrived(auto_revoke, [state](
		Direct3D11CaptureFramePool const& sender,
		winrt::Windows::Foundation::IInspectable const&
	) noexcept {
		bool shouldNotify = false;
		try {
			auto frame = sender.TryGetNextFrame();
			if (!frame) {
				return;
			}
			std::lock_guard<std::mutex> lock(state->mutex);
			if (state->isAcceptingFrames && !state->frame && !state->error) {
				state->frame = std::move(frame);
				shouldNotify = true;
			}
		} catch (...) {
			std::lock_guard<std::mutex> lock(state->mutex);
			if (state->isAcceptingFrames && !state->frame && !state->error) {
				state->error = std::current_exception();
				shouldNotify = true;
			}
		}
		if (shouldNotify) {
			state->resultCondition.notify_one();
		}
	});
	auto cleanup = wil::scope_exit([&]() noexcept {
		{
			std::lock_guard<std::mutex> lock(state->mutex);
			state->isAcceptingFrames = false;
		}
		try {
			frameArrivedRevoker.revoke();
		} catch (...) {
		}
		try {
			session.Close();
		} catch (...) {
		}
		try {
			framePool.Close();
		} catch (...) {
		}
	});

	session.StartCapture();
	Direct3D11CaptureFrame frame { nullptr };
	std::exception_ptr error;
	{
		std::unique_lock<std::mutex> lock(state->mutex);
		state->resultCondition.wait_until(lock, deadline, [&state]() {
			return state->frame || state->error;
		});
		state->isAcceptingFrames = false;
		frame = std::move(state->frame);
		error = std::move(state->error);
	}

	if (error) {
		std::rethrow_exception(error);
	}
	if (!frame) {
		LOG_ERROR(L"wgcCapture: timed out waiting for a capture frame");
		return nullptr;
	}
	return frame;
}

bool copyFramePixels(
	BYTE const* sourceBytes,
	std::size_t sourceRowPitch,
	unsigned int sourceWidth,
	unsigned int sourceHeight,
	RECT const& sourceBounds,
	RECT const& intersection,
	RECT const& request,
	unsigned int requestWidth,
	std::vector<RGBQUAD>& requestPixels
) {
	if (
		!sourceBytes
		|| sourceWidth == 0
		|| sourceHeight == 0
		|| sourceRowPitch < static_cast<std::size_t>(sourceWidth) * bytesPerPixel
	) {
		LOG_ERROR(L"wgcCapture: source pixels have invalid dimensions");
		return false;
	}

	const auto sourceBoundsWidth =
		static_cast<std::int64_t>(sourceBounds.right) - sourceBounds.left;
	const auto sourceBoundsHeight =
		static_cast<std::int64_t>(sourceBounds.bottom) - sourceBounds.top;
	if (sourceBoundsWidth <= 0 || sourceBoundsHeight <= 0) {
		LOG_ERROR(L"wgcCapture: capture source has invalid dimensions");
		return false;
	}

	// WGC frame dimensions can differ from screen coordinates, so map pixels proportionally.
	for (LONG screenY = intersection.top; screenY < intersection.bottom; ++screenY) {
		const auto sourceBoundsY = static_cast<std::uint64_t>(
			static_cast<std::int64_t>(screenY) - sourceBounds.top
		);
		const auto sourceY = std::min<std::uint64_t>(
			sourceBoundsY * sourceHeight / static_cast<std::uint64_t>(sourceBoundsHeight),
			sourceHeight - 1
		);
		auto sourceRow = sourceBytes + sourceY * sourceRowPitch;
		const auto requestY = static_cast<std::size_t>(
			static_cast<std::int64_t>(screenY) - request.top
		);
		for (LONG screenX = intersection.left; screenX < intersection.right; ++screenX) {
			const auto sourceBoundsX = static_cast<std::uint64_t>(
				static_cast<std::int64_t>(screenX) - sourceBounds.left
			);
			const auto sourceX = std::min<std::uint64_t>(
				sourceBoundsX * sourceWidth / static_cast<std::uint64_t>(sourceBoundsWidth),
				sourceWidth - 1
			);
			auto sourcePixel = sourceRow + sourceX * bytesPerPixel;
			const auto requestX = static_cast<std::size_t>(
				static_cast<std::int64_t>(screenX) - request.left
			);
			auto& destinationPixel = requestPixels[requestY * requestWidth + requestX];
			destinationPixel.rgbBlue = sourcePixel[0];
			destinationPixel.rgbGreen = sourcePixel[1];
			destinationPixel.rgbRed = sourcePixel[2];
			destinationPixel.rgbReserved = 0;
		}
	}
	return true;
}

bool copyWgcRegion(
	D3DResources const& resources,
	Direct3D11CaptureFrame const& frame,
	RECT const& sourceBounds,
	RECT const& intersection,
	RECT const& request,
	unsigned int requestWidth,
	std::vector<RGBQUAD>& requestPixels
) {
	auto surface = frame.Surface();
	auto dxgiSurfaceAccess =
		surface.as<::Windows::Graphics::DirectX::Direct3D11::IDirect3DDxgiInterfaceAccess>();
	com_ptr<ID3D11Texture2D> texture;
	check_hresult(dxgiSurfaceAccess->GetInterface(guid_of<ID3D11Texture2D>(), texture.put_void()));

	D3D11_TEXTURE2D_DESC textureDesc {};
	texture->GetDesc(&textureDesc);
	const auto contentSize = frame.ContentSize();
	if (
		contentSize.Width <= 0
		|| contentSize.Height <= 0
		|| textureDesc.Format != DXGI_FORMAT_B8G8R8A8_UNORM
	) {
		LOG_ERROR(L"wgcCapture: capture frame has an unsupported format or dimensions");
		return false;
	}
	const auto frameWidth = std::min(textureDesc.Width, static_cast<unsigned int>(contentSize.Width));
	const auto frameHeight = std::min(textureDesc.Height, static_cast<unsigned int>(contentSize.Height));
	if (frameWidth == 0 || frameHeight == 0) {
		LOG_ERROR(L"wgcCapture: capture frame has no usable pixels");
		return false;
	}

	auto stagingDesc = textureDesc;
	stagingDesc.BindFlags = 0;
	stagingDesc.CPUAccessFlags = D3D11_CPU_ACCESS_READ;
	stagingDesc.MiscFlags = 0;
	stagingDesc.Usage = D3D11_USAGE_STAGING;
	com_ptr<ID3D11Texture2D> stagingTexture;
	check_hresult(resources.device->CreateTexture2D(&stagingDesc, nullptr, stagingTexture.put()));
	resources.context->CopyResource(stagingTexture.get(), texture.get());

	D3D11_MAPPED_SUBRESOURCE mapped {};
	check_hresult(resources.context->Map(stagingTexture.get(), 0, D3D11_MAP_READ, 0, &mapped));
	auto unmap = wil::scope_exit([&]() noexcept {
		resources.context->Unmap(stagingTexture.get(), 0);
	});
	return copyFramePixels(
		static_cast<BYTE const*>(mapped.pData),
		mapped.RowPitch,
		frameWidth,
		frameHeight,
		sourceBounds,
		intersection,
		request,
		requestWidth,
		requestPixels
	);
}

void scaleImage(
	std::vector<RGBQUAD> const& source,
	unsigned int sourceWidth,
	unsigned int sourceHeight,
	RGBQUAD* destination,
	unsigned int destinationWidth,
	unsigned int destinationHeight
) {
	if (sourceWidth == destinationWidth && sourceHeight == destinationHeight) {
		std::copy(source.begin(), source.end(), destination);
		return;
	}
	for (unsigned int destinationY = 0; destinationY < destinationHeight; ++destinationY) {
		const auto sourceY = static_cast<std::size_t>(
			static_cast<std::uint64_t>(destinationY) * sourceHeight / destinationHeight
		);
		for (unsigned int destinationX = 0; destinationX < destinationWidth; ++destinationX) {
			const auto sourceX = static_cast<std::size_t>(
				static_cast<std::uint64_t>(destinationX) * sourceWidth / destinationWidth
			);
			destination[
				static_cast<std::size_t>(destinationY) * destinationWidth + destinationX
			] = source[sourceY * sourceWidth + sourceX];
		}
	}
}

bool hasValidPixelCount(unsigned int width, unsigned int height) {
	constexpr auto maxPixelCount =
		std::numeric_limits<std::size_t>::max() / sizeof(RGBQUAD);
	return width != 0
		&& height != 0
		&& width <= maxPixelCount / height;
}

bool createRequestRect(
	int screenX,
	int screenY,
	unsigned int width,
	unsigned int height,
	RECT& request
) {
	const auto right = static_cast<std::int64_t>(screenX) + width;
	const auto bottom = static_cast<std::int64_t>(screenY) + height;
	if (
		right > std::numeric_limits<LONG>::max()
		|| bottom > std::numeric_limits<LONG>::max()
	) {
		return false;
	}
	request = {
		static_cast<LONG>(screenX),
		static_cast<LONG>(screenY),
		static_cast<LONG>(right),
		static_cast<LONG>(bottom),
	};
	return true;
}

bool captureScreenRegion(
	int screenX,
	int screenY,
	unsigned int width,
	unsigned int height,
	RGBQUAD* image,
	unsigned int destinationWidth,
	unsigned int destinationHeight
) {
	if (
		!image
		|| !hasValidPixelCount(width, height)
		|| !hasValidPixelCount(destinationWidth, destinationHeight)
	) {
		LOG_ERROR(L"wgcCapture: invalid capture dimensions");
		return false;
	}
	RECT request {};
	if (!createRequestRect(screenX, screenY, width, height, request)) {
		LOG_ERROR(L"wgcCapture: capture region is outside the supported coordinate range");
		return false;
	}
	auto monitors = getMonitorsForRegion(request);
	if (monitors.empty()) {
		LOG_ERROR(L"wgcCapture: capture region does not intersect a monitor");
		return false;
	}

	[[maybe_unused]] const auto winRTInitialization = initializeWinRT();
	auto resources = createD3DResources();
	std::vector<RGBQUAD> requestPixels(
		static_cast<std::size_t>(width) * height,
		RGBQUAD {}
	);
	const auto captureDeadline = CaptureClock::now() + captureTimeout;
	for (auto const& monitor : monitors) {
		RECT intersection {
			std::max(request.left, monitor.bounds.left),
			std::max(request.top, monitor.bounds.top),
			std::min(request.right, monitor.bounds.right),
			std::min(request.bottom, monitor.bounds.bottom),
		};
		auto item = createItemForMonitor(monitor.handle);
		auto frame = captureFrame(resources, item, captureDeadline);
		if (!frame || !copyWgcRegion(
			resources,
			frame,
			monitor.bounds,
			intersection,
			request,
			width,
			requestPixels
		)) {
			return false;
		}
	}
	scaleImage(requestPixels, width, height, image, destinationWidth, destinationHeight);
	return true;
}
}

bool __stdcall wgcCapture_isSupported() {
	try {
		[[maybe_unused]] const auto winRTInitialization = initializeWinRT();
		if (!GraphicsCaptureSession::IsSupported()) {
			return false;
		}
		// The session API predates monitor capture, so also check the Win32 interop interface.
		[[maybe_unused]] const auto interopFactory =
			get_activation_factory<GraphicsCaptureItem, IGraphicsCaptureItemInterop>();
		return true;
	} catch (...) {
		return false;
	}
}

bool __stdcall wgcCapture_captureScreenRegion(
	int screenX,
	int screenY,
	unsigned int width,
	unsigned int height,
	RGBQUAD* image,
	unsigned int destinationWidth,
	unsigned int destinationHeight
) {
	try {
		return captureScreenRegion(
			screenX,
			screenY,
			width,
			height,
			image,
			destinationWidth,
			destinationHeight
		);
	} catch (hresult_error const& e) {
		LOG_ERROR(L"wgcCapture error: " << e.code() << L": " << e.message().c_str());
		return false;
	} catch (std::exception const& e) {
		LOG_ERROR(L"wgcCapture error: " << e.what());
		return false;
	} catch (...) {
		LOG_ERROR(L"wgcCapture: unknown exception");
		return false;
	}
}
