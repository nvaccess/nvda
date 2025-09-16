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

Inter-process communication uses Pyro5 RPC. Security measures include:

- Authenticated Encryption: XSalsa20-Poly1305 encryption with unique per-addon keys
- Binding Restriction: All RPC endpoints bind exclusively to loopback interface (127.0.0.1)
- Process Validation: The Windows Socket API is used to validate process identity
- Serialization: msgpack serialization is used instead of Pickle to prevent code execution exploits
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
    │   └── synth.py              # SynthService - synthesizer implementation
    └── proxies/                  # NVDA module proxies for add-ons
        ├── __init__.py
        ├── config.py             # Proxy for config module
        ├── speech.py             # Proxy for speech module
        ├── synthDriverHandler.py # Proxy for synthDriverHandler
        ├── globalVars.py         # Proxy for globalVars module
        ├── logHandler.py         # Proxy for logHandler module
        ├── languageHandler.py    # Proxy for languageHandler module
        ├── nvwave.py             # Proxy for nvwave module
        ├── ui.py                 # Proxy for ui module
        ├── addonHandler.py       # Proxy for addonHandler module
        ├── appModules.py         # Proxy for appModules module
        ├── brailleDisplayDrivers.py # Proxy for brailleDisplayDrivers
        ├── extensionPoints.py    # Proxy for extensionPoints module
        ├── globalPlugins.py      # Proxy for globalPlugins module
        ├── synthDrivers.py       # Proxy for synthDrivers module
        └── visionEnhancementProviders.py # Proxy for visionEnhancementProviders
```

### 4.2 NVDA Core Components

#### 4.2.1 ART Manager (`art.manager`)

The ART Manager handles process management with the following architecture:

**ARTManager Class**:
- **Core Service Management**: Starts Pyro5 daemon and registers all core services
- **Multi-Process Coordination**: Manages multiple `ARTAddonProcess` instances (one per addon)
- **Service Discovery**: Maintains URIs for all core services and distributes them to ART processes
- **Global Access**: Provides `getARTManager()` for system-wide access to ART services

**ARTAddonProcess Class**:
- **Subprocess Management**: Uses `SubprocessManager` with `ProcessConfig` for robust process control
- **JSON Handshake Protocol**: Implements bi-directional communication during startup
- **Service Connection**: Establishes Pyro5 proxy connections to ART services
- **Error Recovery**: Handles process crashes and communication failures
- **Secure Desktop Integration**: Detects and configures SD-ART mode automatically

**Process Configuration**:
- **Executable**: `nvda_art.exe` (built from `nvda_art.pyw`)
- **Creation Flags**: `CREATE_NO_WINDOW` for hidden console
- **Communication**: Bidirectional pipes for JSON handshake
- **Timeout Handling**: 10-second handshake timeout with graceful failure

**Key Features**:
- **One-Addon-Per-Process**: Each addon runs in complete isolation
- **Automatic Restart**: Failed processes can be restarted without affecting others
- **Service Proxy Management**: Automatic connection to ART services with retry logic
- **Detailed Logging**: Process lifecycle and communication logging

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

- **AddOnLifecycleService**: Loads and manages the assigned add-on
- **SynthService**: Manages synthesizer driver instances, handles speech requests, voice management, and audio streaming
- **ExtensionPointHandlerService**: Executes extension point handlers (integrated in nvda_art.pyw)
- **ExtensionPointService**: Tracks extension point registrations (integrated in nvda_art.pyw)

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

### 6.1 Pyro5 Configuration

- Serializer: encrypted (EncryptedSerializer wrapping msgpack for authenticated encryption)
- Timeout: 10 seconds with 3 retries
- Threading: Thread server type with 16 thread pool size
- Host: 127.0.0.1 (loopback only)
- Port: 0 (auto-assigned)

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

### 6.4 Encrypted Communication

ART encrypts all RPC communication between NVDA Core and ART processes using XSalsa20-Poly1305 authenticated encryption. This addresses the fundamental security gap in the original design where sensitive data like configuration settings, speech text, and addon interactions were transmitted as plaintext over local network sockets.

The implementation uses PyNaCl's SecretBox with unique ephemeral 32-byte keys generated for each addon. NVDA Core generates a unique key and serializer ID for each ART process, using incremental serializer IDs starting at 20. Each addon receives its unique encryption configuration during the JSON handshake. The EncryptedSerializer wraps Pyro5's msgpack serializer transparently - addons see no difference in API behavior, but all RPC calls are automatically encrypted with unique nonces to prevent replay attacks.

This per-addon encryption provides complete traffic isolation between addons. Addon A cannot decrypt communication from Addon B, as each uses different encryption keys and serializer IDs. Pyro5's serializer_id mechanism automatically routes messages to the correct encrypted serializer without performance overhead. The encryption overhead is negligible compared to RPC serialization costs, while eliminating several attack vectors including inter-process eavesdropping, message tampering, cross-addon attacks, and RPC injection attempts. Keys exist only in memory during the NVDA session, providing forward secrecy if the system is compromised later.

The encrypted serializer handles Pyro5's network layer quirks, including automatic conversion of bytearray objects to bytes for compatibility with PyNaCl's C bindings. Each message includes authentication data that prevents modification, ensuring that compromised processes cannot inject malicious RPC calls into the communication stream.

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

## 11. Synthesizer Architecture

The `SynthService` in each ART process manages synthesizer drivers and handles speech requests from NVDA Core. It deserializes speech sequences containing text and speech commands like `IndexCommand` (speech bookmarks), `CharacterModeCommand` (character-by-character mode), `BreakCommand` (pauses), `LangChangeCommand` (language switching), and `PitchCommand`/`RateCommand`/`VolumeCommand` for audio parameter changes.

The service includes a dynamic property system that adapts to any synthesizer. The service uses `__getattr__` to generate getter and setter methods for any synthesizer property:

```python
# Automatic method generation for any synthesizer property
def __getattr__(self, name: str):
    if name.startswith('set') and len(name) > 3:
        # Handles set{PropertyName}(value) -> synth.property = value
    elif name.startswith('getCurrent') and len(name) > 10:
        # Handles getCurrent{PropertyName}() -> synth.property
```

The service supports synthesizer-specific properties like `setInflection(value)` / `getCurrentInflection()` or `setVariant(value)` / `getCurrentVariant()` without hardcoding each one.

Voice management includes validation (`isValidVoice()`), default selection (`getDefaultVoice()`), and dynamic discovery (`getAvailableVoices()`) with locale support. Audio data streams from the ART process to NVDA Core for playback.

When an addon loads a synthesizer driver, the driver registers with `SynthService.setSynthInstance()`. The `SynthService` then becomes a proxy for all synthesizer operations, with NVDA Core communicating via `SpeechService` RPC calls.

## 12. Entry Points and Integration

NVDA initializes ART in `source/core.py`:

```python
# Initialize ART Manager (Add-on Runtime)
try:
    from art.manager import ARTManager
    log.debug("Initializing ART Manager")
    artManager = ARTManager()
    artManager.start()
    log.info("ART Manager initialized")
except Exception:
    log.error("Failed to initialize ART Manager", exc_info=True)
```

The build system produces `nvda_art.exe` with this py2exe configuration:

```python
{
    "script": "nvda_art.pyw",
    "dest_base": "nvda_art", 
    "icon_resources": [(1, "images/nvda.ico")],
    "other_resources": [_genManifestTemplate(shouldHaveUIAccess=False)],
    "version_info": {...}
}
```

The ART process entry point `nvda_art.pyw` reads JSON from stdin in production or accepts command line arguments for development.

```python
def getStartupInfo() -> Tuple[Optional[dict], bool]:
    is_cli_mode = len(sys.argv) > 1
    if is_cli_mode:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("--addon-path", required=True)
        parser.add_argument("--addon-name")
        parser.add_argument("--debug", action="store_true")
        # ...
    else:
        # Read JSON from stdin
        startup_line = sys.stdin.readline().strip()
        startup_data = json.loads(startup_line)
        # ...
```

Process configuration uses `CREATE_NO_WINDOW` for hidden console and pipes for communication:

```python
ART_CONFIG = ProcessConfig(
    name="NVDA ART",
    sourceScriptPath=Path("../source/nvda_art.pyw"),
    builtExeName="nvda_art.exe",
    popenFlags={
        "creationflags": subprocess.CREATE_NO_WINDOW,
        "bufsize": 0,
        "stdin": subprocess.PIPE,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
    },
)
```

Pyro5 configuration binds to loopback with msgpack serialization:

```python
# In nvda_art.pyw
Pyro5.config.SERIALIZER = "msgpack"
Pyro5.config.COMMTIMEOUT = 0.0
Pyro5.config.HOST = "127.0.0.1"
Pyro5.config.THREADPOOL_SIZE = 16
Pyro5.config.SERVERTYPE = "thread"
```

NVDA Core registers services like `ConfigService` and `LoggingService` with a Pyro5 daemon, then distributes the URIs to ART processes. Each ART process registers its own services like `AddOnLifecycleService` and `SynthService`.

The proxy module system injects NVDA module proxies into `sys.modules`:

```python
PROXY_MODULE_REGISTRY = {
    "ui": ui,
    "config": config,
    "logHandler": logHandler,
    "globalVars": globalVars,
    "speech": speech,
    # ... more modules
}

for module_name, module_obj in PROXY_MODULE_REGISTRY.items():
    sys.modules[module_name] = module_obj
```

Addons can use `import config` to get the proxy implementation.

## 13. SD-ART Implementation Status

SD-ART (Secure Desktop Add-on Runtime) detection is implemented but we don't enforce security restrictions yet.

When NVDA launches an ART process, it detects secure desktop mode using `utils.security.isRunningOnSecureDesktop()` and passes this information via the startup handshake:

```python
# In ARTAddonProcess._startProcessWithHandshake()
startup_data = {
    "config": {
        "secureDesktop": self._isRunningOnSecureDesktop(),
    }
}

# In nvda_art.pyw
is_secure_desktop = config.get("secureDesktop", False)
if is_secure_desktop:
    art_logger.info("=== SD-ART MODE: Running on Secure Desktop ===")
os.environ["NVDA_ART_SECURE_DESKTOP"] = "1" if is_secure_desktop else "0"
```

Currently, SD-ART processes are detected and labeled but run with the same permissions as regular ART. We haven't implemented the security restrictions from the original design (no network access, restricted file system access, no clipboard access, app container technology, low integrity level, UI creation restrictions).

To complete SD-ART, we need to implement app containers, integrity levels, and the planned security restrictions.

## 14. Implementation Plan

### 14.1 Phase 1: Core Infrastructure

1. Reorganize existing code into `art.core` and `art.runtime` packages
2. Move services from `nvda_art.pyw` to `art.runtime.services`
3. Fix service discovery mechanism in ARTManager
4. Implement basic proxy modules in `art.runtime.proxies`

### 14.2 Phase 2: Essential Services

1. Implement `art.core.services.config` - ConfigService
2. Implement `art.core.services.logging` - LoggingService  
3. Implement `art.runtime.proxies.config` - config module proxy
4. Implement `art.runtime.proxies.logHandler` - logHandler module proxy
5. Test basic add-on loading with logging

### 14.3 Phase 3: Speech System

1. Implement `art.core.services.speech` - SpeechService
2. Implement `art.runtime.proxies.synthDriverHandler` - synthDriverHandler proxy
3. Implement `art.runtime.proxies.speech` - speech module proxy
4. Test synthesizer registration and basic speech

### 14.4 Phase 4: Vocalizer Integration

1. Implement remaining proxies (`globalVars`, `addonHandler`, etc.)
2. Add native DLL loading support
3. Implement file system access controls
4. Test full vocalizer add-on loading

### 14.5 Phase 5: Event System & Extension Points

1. Implement EventHandlerService
2. Implement event forwarding from NVDA to add-ons
3. Complete extension point system
4. Test with complex add-on interactions

### 14.6 Phase 6: Polish & Optimization

1. Performance optimization for RPC calls
2. Enhanced error handling and recovery
3. Additional proxy modules as needed

## 15. Error Handling

- ART process crashes: NVDA Core detects and restarts it
- Add-on crashes: Contained within ART process, logged
- RPC errors: Timeouts, retries for critical services

## 16. Startup Sequence

### 16.1 NVDA Core Initialization
1. **NVDA Core initializes** (see `core.main`)
2. **ARTManager creation** and registration as global instance
3. **Core Services Setup**:
   - Creates Pyro5 daemon on loopback interface (127.0.0.1:0)
   - Registers all core services: `ConfigService`, `LoggingService`, `SpeechService`, `GlobalVarsService`, `NVWaveService`, `LanguageHandlerService`, `UIService`
   - Starts core daemon thread for RPC request handling
   - Stores service URIs for distribution to ART processes

### 16.2 ART Process Startup (Per Addon)

#### 16.2.1 Process Creation
1. **ARTAddonProcess instantiation** with addon spec and core service URIs
2. **Subprocess launch** via `SubprocessManager` using `nvda_art.exe`
3. **JSON handshake initiation**:
   ```json
   // NVDA Core → ART Process
   {
     "addon": {"name": "addonName", "path": "/path/to/addon"},
     "core_services": {"config": "PYRO:uri", "logging": "PYRO:uri"},
     "config": {"debug": false, "secureDesktop": false}
   }
   ```

#### 16.2.2 ART Process Initialization
1. **Entry point**: `nvda_art.pyw` main function
2. **Mode detection**: CLI vs handshake mode based on command line arguments
3. **Startup data parsing**: JSON deserialization and configuration extraction
4. **Environment setup**: Debug mode, secure desktop detection, path configuration
5. **Proxy module installation**: Injection of NVDA module proxies into `sys.modules`
6. **ARTRuntime creation**: Service registration and Pyro5 daemon startup

#### 16.2.3 Service Registration
1. **ART Services**: `AddOnLifecycleService`, `ExtensionPointHandlerService`, `ExtensionPointService`, `SynthService`
2. **Pyro5 daemon startup** with msgpack serialization and thread-based server
3. **Response generation**:
   ```json
   // ART Process → NVDA Core
   {
     "status": "ready",
     "addon_name": "addonName",
     "art_services": {"addon_lifecycle": "PYRO:uri", "synth": "PYRO:uri"}
   }
   ```

#### 16.2.4 Addon Loading
The ART process connects to NVDA Core services, loads the addon via `AddOnLifecycleService.loadAddonIfNeeded()`, and activates proxy modules. The addon registers extension point handlers and becomes available for RPC calls.

### 16.3 System Ready State
Each addon runs in its own ART process with bidirectional RPC communication to NVDA Core. Core services are accessible from all ART processes, and existing addon APIs work through proxies.

## 17. Security Model

### 17.1 Add-on Runtime Hosts

ART implements two security models. Regular ART allows network access but restricts file system access to the addon's directory and prevents starting new processes. SD-ART is more restrictive, blocking network access, clipboard access, UI creation outside NVDA, and desktop access. Both are designed to run with low integrity level (IL_LOW) and app container technology, though these restrictions are not yet fully implemented.

### 17.2 Process Security

NVDA Core tracks the Process ID (PID) of each ART process it launches and maintains full control over process creation, monitoring, and termination. Additional security measures like Windows Socket API validation and cryptographic process authentication were considered but not implemented. The current approach relies on the operating system's process security model and controlled process creation.

### 17.3 Communication Security

All Pyro5 RPC communication binds exclusively to the loopback interface (127.0.0.1) with random ports, preventing external access. ART processes are launched directly by NVDA Core with PID tracking and a bidirectional JSON handshake with 10-second timeout.

The system uses authenticated encryption for all RPC messages via XSalsa20-Poly1305, with unique per-addon keys providing message confidentiality and integrity. Underlying serialization uses msgpack instead of Pickle to prevent code execution exploits. Each addon runs in a separate process with isolated memory space, providing crash isolation so addon failures don't affect NVDA Core or other addons.

#### 17.3.2 Process Lifecycle Security  
- **Parent-Child Relationship**: ART processes are launched directly by NVDA Core
- **Process Tracking**: NVDA Core tracks Process IDs (PIDs) of launched ART processes
- **Handshake Protocol**: Bidirectional JSON handshake ensures proper initialization
- **Timeout Protection**: 10-second handshake timeout prevents hung processes

#### 17.3.3 Serialization Security
- **msgpack Serialization**: Uses msgpack instead of Pickle to prevent code execution exploits
- **Structured Data**: All RPC calls use defined data structures
- **No Code Injection**: Serialization format prevents arbitrary code execution

#### 17.3.4 Access Control via Process Model
- **Process Isolation**: Each addon runs in separate process with isolated memory space
- **Service Boundary**: Clear separation between NVDA Core and addon code
- **Crash Isolation**: Addon crashes do not affect NVDA Core or other addons


#### 17.3.6 Security Philosophy
The current security model relies on:
1. **Process Isolation**: Operating system process boundaries provide primary security
2. **Network Isolation**: Loopback-only communication prevents external access  
3. **Authenticated Encryption**: XSalsa20-Poly1305 provides message confidentiality and integrity
4. **Serialization Safety**: Safe serialization prevents code injection
5. **Lifecycle Management**: Controlled process creation and monitoring

This approach provides practical security for the intended use case while maintaining simplicity and performance.

### 17.4 Audio Handling

- NVDA core will handle all audio processing
- Add-ons will send PCM audio data streams to NVDA for playback
- Audio generation capabilities remain in add-ons, but playback is controlled by NVDA

### 17.5 Add-on Isolation

- Version 1 does not implement isolation between add-ons within the same runtime
- Add-ons running in the same runtime process can potentially interact with each other
- Future versions may implement more granular isolation between add-ons

## 18. Future Enhancements (Post-Version 1)

- Permissions
- multiprocess runtime
