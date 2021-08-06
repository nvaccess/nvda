# NVDA Starting and Exiting outline

## Ways to start NVDA:

1. For an installed copy:
    1. Ctrl+Alt+N (Desktop shortcut)
    1. Automatically via Ease of Access on the Windows sign-in screen (at boot or signing out of a previous session)
    1. Automatically via Ease of Access on User Account Control (UAC) screens
    1. Automatically by Ease of Access after signing in to Windows
1. For an installed copy, portable copy, installer:
    1. An exiting instance of NVDA starting a new process (see shutting down procedures)
    1. By running the exe (see cli options too).
    This can be triggered by a user or external process such as an existing NVDA instance
    - test: `startupShutdownNVDA.Starts`
1. For source: eg runnvda.bat

## NVDA can be shutdown by:

1. UI within NVDA, with and without an ExitDialog prompt (uses `triggerNVDAExit`):
    1. NVDA+q
        - test: `startupShutdownNVDA.Quits from keyboard, Restarts`
    1. An input gesture to restart
    1. A prompt to restart from changing certain settings
    1. Via the NVDA menu -> Exit
        - test: `startupShutdownNVDA.Quits from menu`
1. A process sending `WM_QUIT`, eg a new NVDA process starting (uses `WM_QUIT`)
1. A handled crash (directly causes a new process to start, terminates unsafely)
    - test: `startupShutdownNVDA.Restarts on crash, Restarts on braille crash`
1. An unhandled crash (terminates unsafely)
1. An external command which kills the process (terminates unsafely) 
1. Windows shutting down (terminates unsafely) (uses `wx.EVT_END_SESSION`)

## Exit hooks/triggers

### In process: `triggerNVDAExit`
* A function in the core module
* Only executes the code once, uses a lock and flag to ensure this
* Uses a queue on the main thread to queue a safe shutdown
* Once the queued shutdown starts:
    1. the updateCheck is terminated
    1. watchdog is terminated
    1. addons and the brailleViewer are terminated, so we can close all windows safely
    1. All NVDA windows are closed
    1. Now that windows are closed, a new NVDA instance is started if requested

### Out of process: `WM_QUIT`
* [a windows message](https://docs.microsoft.com/en-us/windows/win32/winmsg/wm-quit) which can be sent across processes which will force the main loop to exit and close most NVDA windows.
* We subsequently run `triggerNVDAExit` to ensure that clean up code isn't missed, and pump the queue to execute it.
* Changing to using a custom message, which would allow a custom handling (eg just `triggerNVDAExit`), requires compatibility with messaging older NVDA versions that are only aware of `WM_QUIT`.

### Out of process: `wx.EVT_END_SESSION`
- This is a [wxCloseEvent](https://docs.wxwidgets.org/3.0/classwx_close_event.html) triggered by a Windows session ending.
- On `wx.EVT_END_SESSION`, we save the config and play the exit sound.
- Other actions are not performed as we have limited time to perform an action for this event. With NVDA being killed off very last, Windows may include NVDA in the Block shutdown dialog, but the user won't be able to read it if we are shutting down.

## Technical startup and exit notes

## The Message Window

So that a new NVDA process can end a running NVDA process, NVDA accepts [WM_QUIT](#Out-of-process-WM_QUIT) messages from other processes and creates a window that can be discovered.
The Windows API allows us to find a process by searching for a named window, NVDA creates a window for accepting messages with a fixed name.

Starting up is blocked by checking for an existing NVDA window and sending `WM_QUIT`.
The message window is created late during the start up, and destroyed early in exit and is not perfectly indicative of whether or not an NVDA process is running. As such, we have a [MutEx](#MutEx) that ensures a newly started process blocks until any previous NVDA has finished exiting.

## MutEx

Preventing multiple copies. Note detects unusual shutdown of prior instance via "abandoned" mutex.

## Unsafe restart

Called in the event of a crash. Exiting NVDA safely in the event of a crash could be improved, but it is limited as we cannot rely on other threads running or the state of NVDA.

### As a user, NVDA can be updated or installed:

1. Via a downloaded installer exe
1. Via the NVDA updater

### Technical installer/updater process:

1. 
