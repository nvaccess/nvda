# NVDA Add-on Runtime (ART) Design Document

## 1. Introduction

The NVDA Add-on Runtime (ART) moves NVDA add-ons from the core NVDA process to a separate process. This document describes the architecture and implementation plan for ART.

## 2. Goals

- Move add-ons to a separate process to improve NVDA stability
- Maintain compatibility with existing add-ons
- Support basic functionality (extension points, event handling) for the first version

## 3. Architecture

### 3.1 Process Architecture

ART uses a one-addon-per-process model where each enabled addon runs in its own isolated ART process:

1. NVDA Core Process: The main NVDA screen reader application
   - Manages the lifecycle of multiple add-on runtime processes (one per addon)
   - Maintains communication channels with each runtime process
   - Restarts individual runtime processes if they crash
   - Provides core screen reader functionality
   - Implements security validation for runtime communication

2. Regular Add-on Runtime Process (ART): Each addon gets its own ART process
   - Hosts exactly one addon with standard permissions in normal desktop sessions
   - Runs with limited but practical permissions
   - Has network access allowed to support add-ons that require online functionality
   - Has restricted file system access (limited to add-on's own directory)
   - Operates within an app container for isolation from the main system
   - Runs at low integrity level (IL_LOW)
   - Communicates with NVDA Core via secure, validated RPC channels
   - Cannot start new processes
   - Provides a Python environment where the single addon executes

3. Secure Desktop Add-on Runtime Process (SD-ART): Each addon gets its own SD-ART process in secure desktop
   - Hosts exactly one addon with highly restricted permissions in secure desktop sessions
   - Runs with minimal permissions (no network, no clipboard, strictly limited file system access)
   - Operates within a more restrictive app container than the regular ART
   - Also runs at low integrity level (IL_LOW)
   - Cannot create UI outside of NVDA
   - Cannot start new processes
   - Optimized for security-critical environments

### 3.2 Process Communication

All inter-process communication occurs via Pyro4 RPC with the following security measures:

- Binding Restriction: All RPC endpoints bind exclusively to loopback interface (127.0.0.1)
- Process Validation: The Windows Socket API is used to validate process identity
- Serialization: JSON serialization is used instead of Pickle to prevent code execution exploits
- Input Validation: All incoming data is validated using Pydantic before processing
- Message Size Limits: Maximum message sizes are enforced to prevent denial of service attacks

### 3.3 Data Flow Architecture

1. Event Flow:
   - System events originate in NVDA Core (via accessibility APIs)
   - Events are filtered and forwarded to relevant add-on runtimes
   - Add-ons process events and respond if necessary
   - Responses are validated before being processed by NVDA Core

2. Extension Point Flow:
   - Extension points in NVDA Core trigger calls to registered add-ons
   - NVDA Core tracks which add-ons have registered for which extension points
   - Add-on responses are validated and integrated into NVDA behavior

3. Audio Data Flow:
   - Add-ons generate audio data (e.g., synthesized speech)
   - PCM audio data is streamed to NVDA Core
   - NVDA Core handles playback through the audio subsystem

### 3.4 Process Lifecycle

1. Startup Sequence:
   - NVDA Core initializes
   - NVDA Core discovers enabled addons
   - For each enabled addon, NVDA Core launches a separate ART process (or SD-ART in secure desktop)
   - Each runtime process establishes a connection back to NVDA Core
   - NVDA Core validates each connection
   - Each ART process loads its assigned addon

2. Normal Operation:
   - Each addon runs in its own isolated runtime process
   - Communication follows the data flow patterns described above
   - NVDA monitors each runtime process health independently

3. Error Handling:
   - If an addon crashes, only its runtime process is affected
   - If a runtime process crashes, NVDA Core detects this and can restart just that process
   - Other addons continue running unaffected
   - During runtime restart, only the crashed addon is reloaded

4. Secure Desktop Transitions:
   - When transitioning to a secure desktop, NVDA Core launches SD-ART processes for each addon
   - Each addon gets its own SD-ART process with more restrictive permissions
   - Addons are isolated from each other even in secure desktop

### 3.5 Security Boundaries

The architecture establishes multiple security boundaries:

1. Process Boundary: Add-ons run in a separate process from NVDA Core
2. Integrity Level Boundary: Add-on runtimes operate at a lower integrity level than NVDA Core
3. App Container Boundary: Add-on runtimes run within app containers that restrict their capabilities
4. File System Boundary: Add-ons can only access their own directories
5. Network Boundary: SD-ART has no network access, ART has network access

These boundaries work together to create a defense-in-depth approach to protecting NVDA Core from potentially malicious or unstable add-ons.

## 4. Components

### 4.1 Package Structure

```
source/art/
├── __init__.py
├── manager.py                    # ARTManager - handles startup/shutdown/monitoring
├── core/                         # Services that run in NVDA Core process
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       ├── config.py             # ConfigService - exposes config.conf
│       ├── speech.py             # SpeechService - handles synth registration
│       ├── logging.py            # LoggingService - receives log messages
│       ├── events.py             # EventService - sends events to ART
│       └── navigation.py         # NavigationService - api.getFocusObject
└── runtime/                      # Code that runs in ART process
    ├── __init__.py
    ├── services/
    │   ├── __init__.py
    │   ├── addons.py             # AddOnLifecycleService
    │   ├── handlers.py           # ExtensionPointHandlerService
    │   └── extensionPoints.py    # ExtensionPointService
    └── proxies/                  # NVDA module proxies for add-ons
        ├── __init__.py
        ├── config.py             # Proxy for config module
        ├── speech.py             # Proxy for speech module
        ├── synthDriverHandler.py # Proxy for synthDriverHandler
        ├── globalVars.py         # Proxy for globalVars
        ├── logHandler.py         # Proxy for logHandler
        └── api.py                # Proxy for api module
```

### 4.2 NVDA Core Components

#### 4.2.1 ART Manager (`art.manager`)

- Starts and monitors the ART process
- Registers `art.core.services.*` with Pyro daemon
- Passes service URIs to ART process
- Starts/restarts the ART process if it crashes

#### 4.2.2 Core Services (`art.core.services.*`)

Services that run in NVDA Core and are exposed to ART via RPC:

- **ConfigService**: Exposes `config.conf` read/write access
- **SpeechService**: Handles synthesizer registration and audio streaming
- **LoggingService**: Receives log messages from ART
- **EventService**: Forwards NVDA events to ART
- **NavigationService**: Provides `api.getFocusObject`, `api.getNavigatorObject`

### 4.3 Add-on Runtime Components

#### 4.3.1 Runtime Services (`art.runtime.services.*`)

Services that run in the ART process:

- **AddOnLifecycleService**: Loads and manages add-ons
- **ExtensionPointHandlerService**: Executes extension point handlers
- **ExtensionPointService**: Tracks extension point registrations

#### 4.3.2 NVDA Module Proxies (`art.runtime.proxies.*`)

Proxy modules that make NVDA APIs available to add-ons:

- Added to Python path so `import config` finds `art.runtime.proxies.config`
- Each proxy forwards calls to appropriate `art.core.services.*` via RPC
- Maintains API compatibility with existing NVDA modules

#### 4.3.3 Import Redirection

```python
# In ART process startup
import sys
from pathlib import Path

# Add proxies to Python path
proxies_path = Path(__file__).parent / "art" / "runtime" / "proxies"
sys.path.insert(0, str(proxies_path))

# Now add-ons automatically get proxies when they import NVDA modules
```

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

- `loadAddon(addonPath)`: Loads the single addon assigned to this ART process
- `getLoadedAddon()`: Returns info about the loaded addon
- `getAddonInfo()`: Gets information about the loaded addon

#### 5.2.2 EventHandlerService

- `dispatchEvent(eventName, obj, **kwargs)`: Sends events to add-ons (mirrors `eventHandler.executeEvent` parameters)

#### 5.2.3 ExtensionPointService

- `registerHandler(addonId, extPointName, handlerId)`: Registers handler (calls `extensionPoints.HandlerRegistrar.register` via proxy)
- `invokeExtensionPoint(extPointName, *args, **kwargs)`: Calls handlers (invoked by NVDA core when an extension point is triggered)

## 6. Process Communication

### 6.1 Pyro4 Configuration

- Serializer: JSON (this was chosen to limit the possibility of Pickle security issues)
- Timeout: 2 seconds (is this too conservative?)
The Pyro4 RPC communication channel MUST be configured to bind exclusively to the loopback interface (e.g., `127.0.0.1`). Binding to any other network interface is prohibited.

### 6.2 Message Flow

```
Add-on (ART process)
    ↓ import config
art.runtime.proxies.config 
    ↓ RPC call
art.core.services.config (NVDA Core)
    ↓ direct access  
config.conf
```

- Method calls are serialized and sent via RPC
- Objects are serialized when possible
- Events flow from NVDA to add-ons via the EventHandlerService
- Extension point calls flow from NVDA to add-ons via the ExtensionPointService
- NVDA module access flows through proxy modules to core services

### 6.3 RPC Input Validation

All data received via RPC at service endpoints (both in NVDA Core receiving calls from ART, and ART receiving calls from NVDA Core) MUST be rigorously validated before use. Validation should include, but is not limited to: type checking, length/range constraints for strings and numbers, and sanitization appropriate for the data's intended use. Unexpected or invalid data must be rejected, and the event should be logged. Failure to validate inputs could lead to instability or security vulnerabilities in the receiving process. **Consideration should be given to using libraries like Pydantic to define data models and enforce these validation rules based on type hints and constraints.**

## 7. GUI System

### 7.1 Overview

ART has its own copy of wxPython, so add-ons can create GUI elements directly without serialization. Add-ons running in ART can use wx normally to create dialogs, message boxes, and other UI elements.

### 7.2 GUI Creation

Add-ons can use wx directly:

```python
# In add-on code running in ART
import wx

def showSettingsDialog(parent):
    dialog = wx.Dialog(parent, title="My Add-on Settings")
    # ... create controls normally
    dialog.ShowModal()
```

### 7.3 Integration with NVDA

Since ART runs in a separate process, GUI elements created by add-ons will appear as separate windows from NVDA's main interface. This is acceptable for add-on settings dialogs and similar functionality.

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
2. For each enabled addon, NVDA Core spawns a separate ART process with addon info.
3. Each ART process loads its assigned addon via AddOnLifecycleService.
4. Add-on initializes and registers event handlers/extension points (via proxied `register` calls).
5. Add-on Runtime signals ready status to NVDA Core.

## 11. Implementation Plan

### 11.1 Phase 1: Core Infrastructure

1. Reorganize existing code into `art.core` and `art.runtime` packages
2. Move services from `nvda_art.pyw` to `art.runtime.services`
3. Fix service discovery mechanism in ARTManager
4. Implement basic proxy modules in `art.runtime.proxies`

### 11.2 Phase 2: Essential Services

1. Implement `art.core.services.config` - ConfigService
2. Implement `art.core.services.logging` - LoggingService  
3. Implement `art.runtime.proxies.config` - config module proxy
4. Implement `art.runtime.proxies.logHandler` - logHandler module proxy
5. Test basic add-on loading with logging

### 11.3 Phase 3: Speech System

1. Implement `art.core.services.speech` - SpeechService
2. Implement `art.runtime.proxies.synthDriverHandler` - synthDriverHandler proxy
3. Implement `art.runtime.proxies.speech` - speech module proxy
4. Test synthesizer registration and basic speech

### 11.4 Phase 4: Vocalizer Integration

1. Implement remaining proxies (`globalVars`, `addonHandler`, etc.)
2. Add native DLL loading support
3. Implement file system access controls
4. Test full vocalizer add-on loading

### 11.5 Phase 5: Event System & Extension Points

1. Implement EventHandlerService
2. Implement event forwarding from NVDA to add-ons
3. Complete extension point system
4. Test with complex add-on interactions

### 11.6 Phase 6: Polish & Optimization

1. Performance optimization for RPC calls
2. Enhanced error handling and recovery
3. Additional proxy modules as needed

## 12. Error Handling

- ART process crashes: NVDA Core detects and restarts it
- Add-on crashes: Contained within ART process, logged
- RPC errors: Timeouts, retries for critical services

## 13. Startup Sequence

1. NVDA Core initializes (see `core.main`).
2. ARTManager creates and registers `art.core.services.*` with Pyro daemon.
3. For each enabled addon:
   - ARTManager starts a new ART process, passing addon info and service URIs
   - ART process connects to provided service URIs
   - ART process adds `art.runtime.proxies` to Python path for import redirection
   - ART process initializes `art.runtime.services.*` with addon context
   - ART process loads its assigned addon through AddOnLifecycleService
   - Addon imports NVDA modules, automatically getting proxies that communicate with NVDA Core
4. System is ready for user interaction with all addons running in isolation.

## 14. Security Model

### 14.1 Add-on Runtime Hosts

ART implements two different security models for add-on runtimes:

#### 14.1.1 Regular Add-on Runtime Host (ART)

- Limited file system access (restricted to the add-on's own directory)
- Network access allowed
- No ability to start new processes
- Running with low integrity level (IL_LOW, same as Internet downloaded files)
- Implemented using app container technology for sandboxing

#### 14.1.2 Secure Desktop Add-on Runtime Host (SD-ART)

- More restrictive than regular ART
- No network access whatsoever
- File system access limited to only its own directory
- No clipboard access
- No ability to start new processes
- No ability to create UI outside of NVDA
- No desktop access (can't access the active desktop)
- Also running with low integrity level and app container technology

### 14.2 Process Security Validation

To ensure that only legitimate ART processes can communicate with NVDA, and vice versa:

- NVDA will track the Process ID (PID) of each ART process it launches
- Connection validation will be implemented using the Windows Socket API to verify the source process
- This approach is similar to the secure desktop process validation already implemented in NVDA Remote

Based on the Pyro documentation provided, here's my suggested enhancement for the Communication Security section:

### 14.3 Communication Security

- All Pyro4 RPC communication will be bound exclusively to loopback interface (127.0.0.1)
- Input validation will be implemented using Pydantic to define data models and enforce validation rules
- Message size limits will be enforced to prevent DOS attacks
- HMAC signature verification will be implemented to ensure only legitimate NVDA Core and ART processes can communicate with each other
- The HMAC key will be generated during runtime initialization and securely shared between NVDA Core and ART processes
- This prevents malicious processes from connecting to either NVDA Core or ART services

#### 14.3.1 HMAC Key Exchange Process

When NVDA Core launches an ART process, it will:

1. Generate a cryptographically secure random key
2. Pass this key to the child process via standard input (stdin) immediately after process creation
3. The ART process will read this key from stdin during initialization
4. Both NVDA Core and the ART process will set their respective Pyro daemons' `_pyroHmacKey` property to this key
5. All subsequent RPC communications will include the HMAC signature for verification

This approach eliminates the need to store the shared secret in any persistent storage or configuration files, which could pose security risks. Each ART process will have its own unique HMAC key, known only to NVDA Core and that specific ART process. If the ART process needs to be restarted, a new key will be generated.

Since the key is passed via stdin, it never appears on the command line or in environment variables where it might be visible to other processes on the system. Both the Secure Desktop and Regular Add-on Runtime hosts will use this same mechanism for secure communication.

This security measure, combined with process validation using the Windows Socket API, provides a robust defense against unauthorized connections and ensures that only legitimate NVDA Core and ART processes can communicate with each other.

### 14.4 Audio Handling

- NVDA core will handle all audio processing
- Add-ons will send PCM audio data streams to NVDA for playback
- Audio generation capabilities remain in add-ons, but playback is controlled by NVDA

### 14.5 Add-on Isolation

- Version 1 does not implement isolation between add-ons within the same runtime
- Add-ons running in the same runtime process can potentially interact with each other
- Future versions may implement more granular isolation between add-ons

## 15. Future Enhancements (Post-Version 1)

- Permissions
- multiprocess runtime
