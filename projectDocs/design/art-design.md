# NVDA Add-on Runtime (ART) Design Document

## 1. Introduction

The NVDA Add-on Runtime (ART) moves NVDA add-ons from the core NVDA process to a separate process. This document describes the architecture and implementation plan for ART.

## 2. Goals

- Move add-ons to a separate process to improve NVDA stability
- Maintain compatibility with existing add-ons
- Support basic functionality (extension points, event handling) for the first version

## 3. Architecture

ART consists of two processes:

1. NVDA Core Process: Main NVDA screen reader application
2. Add-on Runtime Process: Hosts all add-ons in a single process

These processes communicate via Pyro4 RPC.

## 4. Components

### 4.1 NVDA Core Components

#### 4.1.1 ART Manager

- Starts and monitors the ART process
- Maintains communication with the ART process
- Starts/restarts the ART process if it crashes

#### 4.1.2 Service Proxies

- Extension Point Service Proxy
- Event Service Proxy

### 4.2 Add-on Runtime Components

#### 4.2.1 Runtime Manager

- Initializes the ART process
- Sets up Pyro4 server
- Loads add-ons
- Shuts down gracefully

#### 4.2.2 Add-on Host

- Loads add-on modules
- Manages add-on lifecycle (init, terminate)
- Routes events to add-ons

#### 4.2.3 Service Implementations

- Add-on Lifecycle Service
- Extension Point Service
- Event Handler Service

## 5. Services (Version 1 Minimum Set)

### 5.1 Core Services (exposed to add-ons)

#### 5.1.1 NavigationService

- `getFocusObject()`: Gets current focus object (proxies `api.getFocusObject`)
- `getNavigatorObject()`: Gets current navigator object (proxies `api.getNavigatorObject`)

#### 5.1.2 EventService

- `registerEventHandler(eventName, handlerId)`: Registers for NVDA events (related to `eventHandler.executeEvent` dispatch)
- `unregisterEventHandler(eventName, handlerId)`: Unregisters from events

#### 5.1.3 ExtensionPointProxyService

- `getExtensionPoint(name)`: Gets a proxy for an extension point (e.g., `inputCore.decide_executeGesture`)
- `registerExtensionPoint(name, type)`: Registers an add-on extension point (interacts with `extensionPoints` mechanism)

### 5.2 Add-on Services (exposed to NVDA core)

#### 5.2.1 AddOnLifecycleService

- `loadAddon(addonPath)`: Loads an add-on
- `unloadAddon(addonId)`: Unloads an add-on
- `getLoadedAddons()`: Lists loaded add-ons

#### 5.2.2 EventHandlerService

- `dispatchEvent(eventName, obj, **kwargs)`: Sends events to add-ons (mirrors `eventHandler.executeEvent` parameters)

#### 5.2.3 ExtensionPointService

- `registerHandler(addonId, extPointName, handlerId)`: Registers handler (calls `extensionPoints.HandlerRegistrar.register` via proxy)
- `invokeExtensionPoint(extPointName, *args, **kwargs)`: Calls handlers (invoked by NVDA core when an extension point is triggered)

## 6. Process Communication

### 6.1 Pyro4 Configuration

- Serializer: JSON (this was chosen to limit the possibility of Pickle security issues)
- Timeout: 2 seconds (is this too conservative?)
- **Binding:** The Pyro4 RPC communication channel MUST be configured to bind exclusively to the loopback interface (e.g., `127.0.0.1` for IPv4, `::1` for IPv6). Binding to any other network interface is prohibited.

### 6.2 Message Flow

- Method calls are serialized and sent via RPC
- Objects are serialized when possible
- Events flow from NVDA to add-ons via the EventHandlerService
- Extension point calls flow from NVDA to add-ons via the ExtensionPointService

### 6.3 RPC Input Validation

All data received via RPC at service endpoints (both in NVDA Core receiving calls from ART, and ART receiving calls from NVDA Core) MUST be rigorously validated before use. Validation should include, but is not limited to: type checking, length/range constraints for strings and numbers, and sanitization appropriate for the data's intended use. Unexpected or invalid data must be rejected, and the event should be logged. Failure to validate inputs could lead to instability or security vulnerabilities in the receiving process. **Consideration should be given to using libraries like Pydantic to define data models and enforce these validation rules based on type hints and constraints.**

## 7. GUI System

### 7.1 Overview

Add-ons need to create GUI elements in the NVDA process. Instead of attempting to serialize wxPython objects, ART uses a description-based approach where add-ons define the structure and NVDA renders it.

### 7.2 GUI Description Format

Add-ons create a JSON description of the intended GUI that mirrors guiHelper operations:

```json
{
  "dialog": {
    "id": "addonSettingsDialog_123",
    "title": "My Add-on Settings",
    "mainSizer": {
      "orientation": "VERTICAL"
    },
    "items": [
      {
        "type": "labeledControl",
        "label": "Setting:",
        "control": {
          "type": "TextCtrl",
          "id": "settingValue",
          "initialValue": "default"
        }
      },
      {
        "type": "checkBox",
        "id": "enableFeature",
        "label": "Enable Feature",
        "initialValue": false
      },
      {
        "type": "dialogDismissButtons",
        "standardButtons": ["OK", "Cancel"]
      }
    ]
  }
}
```

### 7.3 GUI Creation Process

1. Add-on creates a JSON description of the dialog
2. Add-on calls GUIService.createDialog() with the description
3. NVDA creates the dialog using `gui` helpers (e.g., similar logic to `gui.message.MessageDialog`)
4. NVDA shows the dialog to the user

### 7.4 Event Handling

1. User interacts with dialog (clicks button, changes value)
2. NVDA captures the event and widget ID
3. NVDA gathers current state of all controls in the dialog
4. NVDA sends an event message to the add-on with:
   - Dialog ID
   - Widget ID that triggered the event
   - Event type
   - Current state of all controls
5. Add-on processes the event and responds if needed

### 7.5 GUI Updates

Add-ons can send update messages to modify the GUI:

```json
{
  "dialogId": "addonSettingsDialog_123",
  "updates": [
    { "widgetId": "enableFeature", "property": "enabled", "value": false }
  ]
}
```

### 7.6 GUI Service Methods

- `createDialog(description)`: Creates and shows a dialog
- `updateDialog(dialogId, updates)`: Updates dialog elements
- `closeDialog(dialogId)`: Closes a dialog
- `getDialogState(dialogId)`: Gets current state of all controls

## 8. Extension Point System

### 8.1 Extension Point Types

ART supports all NVDA extension point types (defined in `extensionPoints`):

- Action: Notification of NVDA actions (`extensionPoints.Action`)
- Filter: Modifies data (`extensionPoints.Filter`)
- Decider: Influences NVDA decisions (`extensionPoints.Decider`)
- AccumulatingDecider: All handlers run (`extensionPoints.AccumulatingDecider`)
- Chain: Routes iterables (`extensionPoints.Chain`)

### 8.2 Extension Point Registration

1. Add-on calls extension point registration method (e.g., `someExtensionPoint.register(handler)`)
2. Add-on Runtime records registration (using a proxy for `extensionPoints.HandlerRegistrar.register`) and notifies NVDA Core
3. NVDA Core maintains map of extension points to registered add-ons

### 8.3 Extension Point Invocation

1. NVDA Core invokes an extension point
2. NVDA Core calls ExtensionPointService.invokeExtensionPoint()
3. Add-on Runtime calls registered handlers
4. Add-on Runtime returns results to NVDA Core

### 8.4 Add-on Access

Add-ons access extension points with the same API they use currently (proxied by ART):

```python
# In add-on code - unchanged from current pattern
# References actual extension points like:
# source.braille.filter_displaySize
# source.inputCore.decide_executeGesture
# source.config.post_configProfileSwitch
braille.filter_displaySize.register(self.myFilterFunction)
inputCore.decide_executeGesture.register(self.myDeciderFunction)
config.post_configProfileSwitch.register(self.myActionFunction)
```

## 9. Event System

### 9.1 Event Registration

1. Add-on registers for specific events
2. Add-on Runtime records registration
3. Add-on Runtime notifies NVDA Core of interest in these events

### 9.2 Event Dispatching

1. NVDA Core captures system events (focus changes, etc.) via handlers like `IAccessibleHandler`, `UIAHandler`.
2. NVDA Core queues events using `eventHandler.queueEvent`.
3. `eventHandler.executeEvent` eventually runs, which will call `EventHandlerService.dispatchEvent()` for ART.
4. Add-on Runtime routes events to registered add-ons.
5. Add-on processes the event.

### 9.3 Event Handler Implementation

Add-ons implement event handlers using the current pattern (defined by `eventHandler._EventExecuter.gen`):

```python
# In add-on code - unchanged from current pattern
def event_gainFocus(self, obj, nextHandler):
    # Handle event
    nextHandler()
```

## 10. Add-on Loading Process

1. NVDA Core discovers installed add-ons (using `addonHandler`).
2. NVDA Core calls AddOnLifecycleService.loadAddon() for each add-on.
3. Add-on Runtime imports the add-on module.
4. Add-on initializes (calling its `init` method) and registers event handlers/extension points (via proxied `register` calls).
5. Add-on Runtime returns success/failure to NVDA Core.

## 11. Implementation Plan

### 11.1 Phase 1: Basic Framework

1. Implement ART Manager in NVDA Core
2. Implement Runtime Manager in ART process
3. Set up Pyro4 communication
4. Implement basic process monitoring and restart

### 11.2 Phase 2: Extension Points

1. Implement ExtensionPointService
2. Implement extension point registration and invocation

### 11.3 Phase 3: Event System

1. Implement EventHandlerService
2. Implement event forwarding from NVDA to add-ons

### 11.4 Phase 4: GUI System

1. Implement GUI description format
2. Implement GUI service for dialog creation
3. Implement event feedback system

### 11.5 Phase 5: Testing

1. Test with simple add-ons
2. Verify extension point operation
3. Test GUI interaction
4. Address compatibility issues

## 12. Error Handling

- ART process crashes: NVDA Core detects and restarts it
- Add-on crashes: Contained within ART process, logged
- RPC errors: Timeouts, retries for critical services

## 13. Startup Sequence

1. NVDA Core initializes (see `core.main`).
2. NVDA Core starts ART process.
3. ART process initializes and connects back to NVDA Core.
4. NVDA Core loads configured add-ons through AddOnLifecycleService (part of `addonHandler.loadAddons`).
5. System is ready for user interaction.

## 14. Future Enhancements (Post-Version 1)

- Permissions
- multiprocess runtime
