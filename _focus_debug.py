"""Check which UIA element has focus in HWP - critical for TextInfo routing."""
import comtypes
import comtypes.client

UIAutomationCore = comtypes.client.GetModule("UIAutomationCore.dll")
from comtypes.gen.UIAutomationClient import *

uia = comtypes.CoCreateInstance(
    CUIAutomation._reg_clsid_,
    interface=IUIAutomation,
    clsctx=comtypes.CLSCTX_INPROC_SERVER,
)

# Get the currently focused element
focused = uia.GetFocusedElement()
if not focused:
    print("ERROR: No focused element")
    exit(1)

print("=== Focused Element ===")
print(f"  Name: '{focused.CurrentName}'")
print(f"  ClassName: '{focused.CurrentClassName}'")
print(f"  ControlType: {focused.CurrentControlType}")
print(f"  AutomationId: '{focused.CurrentAutomationId}'")
print(f"  ProcessId: {focused.CurrentProcessId}")

# Walk up the tree to see parent chain
print("\n=== Parent Chain ===")
walker = uia.CreateTreeWalker(uia.CreateTrueCondition())
elem = focused
for depth in range(8):
    if not elem:
        break
    name = (elem.CurrentName or "")[:60]
    cls = elem.CurrentClassName or ""
    ctrl = elem.CurrentControlType
    ctrl_names = {50004: "Edit", 50025: "Custom", 50032: "Window", 50033: "Pane",
                  50030: "Document", 50037: "TitleBar", 50017: "StatusBar"}
    ctrl_str = ctrl_names.get(ctrl, str(ctrl))
    marker = " <<< FOCUS" if depth == 0 else ""
    print(f"  {'  ' * depth}[{ctrl_str}] cls='{cls}' '{name}'{marker}")
    
    if cls == "HwpMainEditWnd":
        print(f"  {'  ' * depth}  ^^^ THIS is HwpMainEditWnd")
    
    parent = walker.GetParentElement(elem)
    if parent and parent.CurrentProcessId == focused.CurrentProcessId:
        elem = parent
    else:
        break
