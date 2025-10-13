/*
A part of NonVisual Desktop Access (NVDA)
Copyright (C) 2023-2026 NV Access Limited, Leonard de Ruijter
This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
*/

#include <uiAutomationClient.h>
#include <winrt/windows.foundation.h>
#include <winrt/windows.foundation.collections.h>
#include <winrt/windows.ui.uiautomation.core.h>
#include <atlcomcli.h>
#include <common/log.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

using namespace winrt::Windows::Foundation;
using namespace winrt::Windows::UI::UIAutomation;
using namespace winrt::Windows::UI::UIAutomation::Core;

inline py::module get_ctypes_module() {
	static py::module ctypes = py::module::import("ctypes");
	return ctypes;
}

inline py::object get_ctypes_POINTER_func() {
	static py::object ctypes_POINTER   = get_ctypes_module().attr("POINTER");
	return ctypes_POINTER;
}

inline py::object get_ctypes_addressof_func() {
	static py::object ctypes_addressof   = get_ctypes_module().attr("addressof");
	return ctypes_addressof;
}

inline py::object get_comtypes_module() {
	static py::module comtypes = py::module::import("comtypes");
	return comtypes;
}

inline py::object get_comtypes_GUID_class() {
	static py::object comtypes_GUID = get_comtypes_module().attr("GUID");
	return comtypes_GUID;
}

inline py::object get_comtypes_IUnknown_class() {
	static py::object comtypes_IUnknown = get_comtypes_module().attr("IUnknown");
	static py::object ptr = get_ctypes_POINTER_func()(comtypes_IUnknown);
	return ptr;
}

inline py::object get_comtypes_IUIAutomationElement_class() {
	static py::module  UIAHandler = py::module::import("UIAHandler");
	static py::object comtypes_IUIAutomationElement = UIAHandler.attr("IUIAutomationElement");
	static py::object ptr = get_ctypes_POINTER_func()(comtypes_IUIAutomationElement);
	return ptr;
}

inline py::object get_comtypes_IUIAutomationTextRange_class() {
	static py::module  UIAHandler = py::module::import("UIAHandler");
	static py::object comtypes_IUIAutomationTextRange = UIAHandler.attr("IUIAutomationTextRange");
	static py::object ptr = get_ctypes_POINTER_func()(comtypes_IUIAutomationTextRange);
	return ptr;
}

inline void* getcomTypesIUnknownPointerAddress(const py::object& obj) {
	if(!py::isinstance(obj, get_comtypes_IUnknown_class())) {
		throw std::invalid_argument("Not a COM object");
	}
	std::size_t h = py::hash(obj);
	if(h == 0) {
		throw std::invalid_argument("Invalid COM object");
	}
	return reinterpret_cast<void*>(h);
}

inline py::object IInspectableToPythonObject(IInspectable const& insp) {
	if(!insp) {
		return py::none();
	}

	// ───── Simple scalar PropertyValue ────────────────────────────────
	auto pv = insp.try_as<IPropertyValue>();
	if(pv) {
		switch(pv.Type()) {
			case PropertyType::Int32:
			return py::int_(pv.GetInt32());
			case PropertyType::Int64:
			return py::int_(pv.GetInt64());
			case PropertyType::UInt64:
			return py::int_(static_cast<long long>(pv.GetUInt64()));
			case PropertyType::Double:
			return py::float_(pv.GetDouble());
			case PropertyType::Single:
			return py::float_(pv.GetSingle());
			case PropertyType::Boolean:
			return py::bool_(pv.GetBoolean());
			case PropertyType::String:
			return py::str(winrt::to_string(pv.GetString()));
			case PropertyType::Guid: {
				GUID guid = pv.GetGuid();
				py::object guidObj = get_comtypes_GUID_class()();
				std::uintptr_t addr = get_ctypes_addressof_func()(guidObj).cast<std::uintptr_t>();
				GUID* pyGuidPtr = reinterpret_cast<GUID*>(addr);
				*pyGuidPtr = guid;
				return guidObj;
			}
			default:
				throw py::value_error("Unsupported PropertyType");
		}
	}

	// ───── Vector<IInspectable> ➜ list ───────────────────────────────
	auto vec = insp.try_as<winrt::Windows::Foundation::Collections::IVector<winrt::Windows::Foundation::IInspectable>>();
	if(vec) {
		py::list out;
		for(IInspectable const& item : vec) {
			out.append(IInspectableToPythonObject(item));
		}
		return out;
	}

	// ───── Map<hstring,IInspectable> ➜ dict ──────────────────────────
	auto stringMap = insp.try_as<winrt::Windows::Foundation::Collections::IMap<winrt::hstring, winrt::Windows::Foundation::IInspectable>>();
	if(stringMap) {
		py::dict d;
		for(auto it = stringMap.First(); it.HasCurrent(); it.MoveNext()) {
			auto cur	= it.Current();
			d[py::str(winrt::to_string(cur.Key()))] = IInspectableToPythonObject(cur.Value());
		}
		return d;
	}

	auto element = insp.try_as<IUIAutomationElement>();
	if(element) {
		IUIAutomationElement* pElement {nullptr};
		element.copy_to(&pElement);
		auto raw = reinterpret_cast<std::uintptr_t>(pElement);
		return get_comtypes_IUIAutomationElement_class()(raw);
	}

	auto textRange = insp.try_as<IUIAutomationTextRange>();
	if(textRange) {
		IUIAutomationTextRange* pTextRange {nullptr};
		textRange.copy_to(&pTextRange);
		auto raw = reinterpret_cast<std::uintptr_t>(pTextRange);
		return get_comtypes_IUIAutomationTextRange_class()(raw);
	}

	return py::none();
}

class RemoteOperationResult {
	private:
	AutomationRemoteOperationResult m_results {nullptr};

	public:
	RemoteOperationResult(AutomationRemoteOperationResult results) : m_results(results) {
		if(!m_results) {
			throw std::invalid_argument("Invalid AutomationRemoteOperationResult");
		}
	}

	int getErrorLocation() {
		return m_results.ErrorLocation();
	}

	HRESULT getExtendedError() {
		return m_results.ExtendedError();
	}

	int getStatus() {
		auto status = m_results.Status();
		return static_cast<int>(status);
	}

	bool hasOperand(int arg_registerID) {
		return m_results.HasOperand(AutomationRemoteOperationOperandId{arg_registerID});
	}

	py::object getOperand(int arg_registerID) {
		auto operand = m_results.GetOperand(AutomationRemoteOperationOperandId{arg_registerID});
		if(!operand) {
			throw std::runtime_error("Invalid operand ID");
		}
		return IInspectableToPythonObject(operand);
	}

};


class RemoteOperation {
	private:
		CoreAutomationRemoteOperation m_operation {CoreAutomationRemoteOperation()};

	public:
	RemoteOperation() = default;

	void importElement(int arg_registerID, py::object arg_pElement) {
		if(!py::isinstance(arg_pElement, get_comtypes_IUIAutomationElement_class())) {
			throw std::invalid_argument("Not a valid AutomationElement");
		}
		AutomationElement element {nullptr};
		winrt::copy_from_abi(element, getcomTypesIUnknownPointerAddress(arg_pElement));
		if(!element) {
			throw std::runtime_error("Invlid AutomationElement");
		}
		m_operation.ImportElement(AutomationRemoteOperationOperandId{arg_registerID}, element);
	}

	void importTextRange(int arg_registerID, py::object arg_pTextRange) {
				if(!py::isinstance(arg_pTextRange, get_comtypes_IUIAutomationTextRange_class())) {
			throw std::invalid_argument("Not a valid AutomationTextRange");
		}
		AutomationTextRange textRange {nullptr};
		winrt::copy_from_abi(textRange, getcomTypesIUnknownPointerAddress(arg_pTextRange));
		if(!textRange) {
			throw std::runtime_error("Invalid AutomationTextRange");
		}
		m_operation.ImportTextRange(AutomationRemoteOperationOperandId{arg_registerID}, textRange);
	}

	void addToResults(int arg_registerID) {
		m_operation.AddToResults(AutomationRemoteOperationOperandId{arg_registerID});
	}

	bool isOpcodeSupported(uint32_t arg_opcode) {
		return m_operation.IsOpcodeSupported(arg_opcode);
	}

	RemoteOperationResult execute(py::bytes bytecode) {
		std::string_view buf = bytecode;
		auto results = m_operation.Execute(winrt::array_view<const std::uint8_t>(
			reinterpret_cast<const std::uint8_t*>(buf.data()),
			static_cast<uint32_t>(buf.size())
		));
		if(!results) {
			throw std::runtime_error("Invalid AutomationRemoteOperationResult");
		}
		return RemoteOperationResult(results);
	}

};

PYBIND11_MODULE(_lowLevel, m) {
	m.doc() = "WinRT CoreAutomationRemoteOperation bridge for NVDA";

	py::class_<RemoteOperationResult>(m, "RemoteOperationResult")
		.def_property_readonly("errorLocation", &RemoteOperationResult::getErrorLocation)
		.def_property_readonly("extendedError", &RemoteOperationResult::getExtendedError)
		.def_property_readonly("status", &RemoteOperationResult::getStatus)
		.def("hasOperand", &RemoteOperationResult::hasOperand)
		.def("getOperand", &RemoteOperationResult::getOperand);

	py::class_<RemoteOperation>(m, "RemoteOperation")
		.def(py::init<>())
		.def("importElement", &RemoteOperation::importElement)
		.def("importTextRange", &RemoteOperation::importTextRange)
		.def("addToResults", &RemoteOperation::addToResults)
		.def("isOpcodeSupported", &RemoteOperation::isOpcodeSupported)
		.def("execute", &RemoteOperation::execute,
			py::arg("bytecode"));
}
