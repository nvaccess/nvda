# NVDA Starting and Exiting outline

## Ways to start NVDA:

1. For an installed copy:
    1. Ctrl+Alt+N (Desktop shortcut)
        - test: `startupShutdownNVDA.Starts from desktop shortcut`
    1. Automatically via Ease of Access on the Windows sign-in screen (at boot or signing out of a previous session)
    1. Automatically via Ease of Access on User Account Control (UAC) screens
    1. Automatically by Ease of Access after signing in to Windows
1. For an installed copy, portable copy, installer:
    1. An exiting instance of NVDA starting a new process (see shutting down procedures)
    1. By running the exe. 
        - This can be triggered by a user or external process such as an existing NVDA instance
        - test: `startupShutdownNVDA.Starts`
1. For source: eg runnvda.bat

## NVDA can be shutdown by:

1. UI within NVDA, with and without an ExitDialog prompt (uses `triggerNVDAExit`):
    1. NVDA+q
        - test: `startupShutdownNVDA.Quits from keyboard, Restarts`
    1. An input gesture to restart
    1. After changing some settings (eg installed add-ons or UI language), user prompted on dialog exit.
    1. Via the NVDA menu -> Exit
        - test: `startupShutdownNVDA.Quits from menu`
1. A process sending `WM_QUIT`, eg a new NVDA process starting
1. A handled crash (directly causes a new process to start, terminates unsafely)
    - test: `startupShutdownNVDA.Restarts on crash, Restarts on braille crash`
1. An unhandled crash (terminates unsafely)
    - requires manual testing/confirmation
1. An external command which kills the process (terminates unsafely) 
1. Windows shutting down (terminates unsafely) (uses `wx.EVT_END_SESSION`)

## Manual testing
Instructions for testing startup / shutdown.

### Start from shortcut
Prerequisites:
 - NVDA installed
 - Shortcut enabled during installation

Steps:
 1. Press (or emulate) Ctrl+Alt+N, observe NVDA starts up

Variation:
- At step 1. A version of NVDA is already running. Observe running version exits before installed version starts up.

### Windows Sign-in screen, automatic start
Prerequisites:
 - NVDA installed
 - Enable "Use NVDA during sign-in"

Steps:
 1. Sign out (not lock) Windows
 1. Observe NVDA announces the Windows sign-in screen

### UAC, automatic start
Prerequisites:
 - NVDA installed
 - An active Windows session (i.e. not signed out, locked)
 - The NVDA installed copy is running

Steps:
 1. Open the Start menu
 1. Type notepad
 1. Open context menu for notepad and choose `Run as Administrator`.
 1. When the UAC dialog appears, verify that NVDA launches on this secure desktop and reports the dialog.

### Windows Successful sign-in, automatic start
Prerequisites:
 - NVDA installed
 - Enable "Start NVDA after I sign in"

Steps:
 1. Start Windows
 1. Sign in
 1. Observe NVDA starts

### Running the *.exe

Steps:
 1. Press `win+r`
 1. Enter <path to nvda.exe>
 1. Press enter
 1. Observe NVDA starts

Variation:
- using an installer (launcher)
   -  eg: `C:\Users\username\Downloads\nvda_2021.1.exe`
- using an installed copy
   - just type `nvda` in place of the .exe
- using a portable copy
   - find and use the path to `nvda.exe`, located within the portable copy directory
   - the installer allows you to create an installed copy and a portable copy

### Running from source (runnvda.bat)
Prerequisites
- clone project and build NVDA (see [project readme](https://github.com/nvaccess/nvda/blob/master/readme.md#getting-the-source-code)).

Steps:
 1. Run `runnvda.bat` from cmd
 1. Observe NVDA starts

### An input gesture to restart

Prerequisite:
- Input gesture for "Restarts NVDA!" is assigned

Steps:
 1. Press (or emulate) the input gesture
 1. Observe that NVDA exits
 1. Observe that a new instance is started

## Technical notes

These notes are aimed at developers, wishing to understand technical aspects of the NVDA start and exit.

1. No more than one NVDA process instance should be running at the same time. Interactions with itself could cause severe issues, some (non-exhaustive list) examples of sub-systems where this would be a problem:
   - NVDA config files
   - Global (OS level) keyboard hook
   - Changed / incompatible in-process code
2. As such, we want to be able to detect running instances, cause them to exit, and confirm they have exited.

### Exit hooks/triggers

There are 3 ways that NVDA receives a request to exit:

- From internally calling [triggerNVDAExit](#When-exiting-from-triggerNVDAExit)
- Receiving [WM_QUIT](#When-exiting-from-WM_QUIT) Windows message
- Receiving [wx.EVT_END_SESSION](#When-exiting-from-wxEVT_END_SESSION) due to Windows session ending

### When exiting from `triggerNVDAExit`
* Called from within NVDA.
* A function in the core module
* Only executes the code once, uses a lock and flag to ensure this
* Uses a queue on the main thread to queue a safe shutdown
* Once the queued shutdown starts:
    1. the updateCheck is terminated
    1. watchdog is terminated
    1. globalPlugins and the brailleViewer are terminated, so we can close all windows safely
    1. All wx windows are closed
    1. Now that windows are closed, a new NVDA instance is started if requested

### When exiting from `WM_QUIT`
* [A Windows Message](https://docs.microsoft.com/en-us/windows/win32/winmsg/wm-quit) received from an external process, such as another NVDA process.
* NVDA accepts `WM_QUIT` messages from other processes and creates a [named window](https://docs.microsoft.com/en-us/windows/win32/learnwin32/creating-a-window#creating-the-window) that can be discovered.
* `WM_QUIT` is handled by `wx`, which force closes all wx windows (other UI features like the systray icon are not windows, and remain) and then exits the main loop.
`triggerNVDAExit` is a more expansive check than how wxWidgets handles `WM_QUIT`
* We subsequently run `triggerNVDAExit` to ensure that clean up code isn't missed, and pump the queue to execute it.
* Using a custom message has been considered:
  - Would allow custom handling (eg just `triggerNVDAExit`)
  - Unfortunately, older NVDA versions will only be aware of `WM_QUIT`, so we'd need to send `WM_QUIT` to these versions.
  - Sending the custom message, waiting for a timeout, then sending `WM_QUIT` adds a significant wait time
  - Identifying the running version (to selectively send the message) requires maintaining 2 message windows in NVDA (one for legacy behaviour) and adds complexity

### When exiting from `wx.EVT_END_SESSION`
* This is a [wxCloseEvent](https://docs.wxwidgets.org/3.0/classwx_close_event.html) triggered by a Windows session ending.
* On `wx.EVT_END_SESSION`, we save the config and play the exit sound.
* Other actions are not performed as we have limited time to perform an action for this event.
    * NVDA is expected to run as long as possible during the sign out process.
    * This is achieved through the [Windows API](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setprocessshutdownparameters), by setting the shutdown priority to the lowest reserved value for non-system applications, `0x100`.
    * [SHUTDOWN_NORETRY](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setprocessshutdownparameters) ensures that NVDA does not show up in the blocked shutdown list dialog.
    If it were, the user would have no way of reading the dialog and fixing the issue.

### Replacing an existing NVDA instance

With the requirement to only allow a single instance of NVDA, a new NVDA process must be able to replace an existing NVDA process.
NVDA will exit correctly in response to a [`WM_QUIT`](#When-exiting-from-WM_QUIT) Windows message, but the process must first be detected / identified in order to send the message.
For new NVDA process to detect an existing NVDA process, a named [message window](https://docs.microsoft.com/en-us/windows/win32/learnwin32/creating-a-window#creating-the-window) is used.
A new NVDA process searches for an existing NVDA window, and if it is detected, sends `WM_QUIT`.
The message window is created late during the start up, and destroyed early in exit and is not perfectly indicative of whether or not an NVDA process is running.
As such, we have a [MutEx](#MutEx) that ensures a newly started process blocks until any previous NVDA has finished exiting.

### MutEx

To confirm that another NVDA process is not running,
a [MutEx](https://docs.microsoft.com/en-us/windows/win32/sync/mutex-objects) is owned by the NVDA process.
NVDA will be blocked from starting until it can acquire the MutEx.
If it can not acquire the MutEx within a timeout, startup is aborted.
This is acquired as soon as possible and released by NVDA as late as possible.
When the NVDA process exits abnormally, Windows will release the MutEx.

### Unsafe restart

Called in the event of a crash. Exiting NVDA safely in the event of a crash could be improved, but it is limited as we cannot rely on other threads running or the state of NVDA.
