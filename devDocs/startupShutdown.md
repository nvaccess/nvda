# NVDA Starting and Exiting outline

## Ways to start NVDA:

1. For an installed copy:
    1. Ctrl+Alt+N (Desktop shortcut)
        - can be tested by:
            1. Set the NVDA config to ensure the welcome dialog loads on startup
            1. Have an existing NVDA process running with a known handle
            1. Press (or emulate) Ctrl+Alt+N
            1. Ensure the known process ends
            1. Wait until the welcome dialog loads
    1. Automatically via Ease of Access on the Windows sign-in screen (at boot or signing out of a previous session)
        - manual testing required
    1. Automatically via Ease of Access on User Account Control (UAC) screens
        - manual testing required
    1. Automatically by Ease of Access after signing in to Windows
        - manual testing required
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
        - to test:
            1. Configure NVDA to load the Welcome dialog on start
            1. assign the input gesture to restart
            1. trigger the input gesture
            1. if the exit dialog is turned on, ensure it loads and is accepted
            1. ensure the existing process is killed and the Welcome dialog loads
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

## Technical notes

These notes are aimed at developers, wishing to understand technical aspects of the NVDA start and exit.

1. We want only one NVDA instance running at a time, so that it can't interact with itself.
2. As such, we want to be able to detect running instances, cause them to exit, and confirm they have exited.

### Exit hooks/triggers

There are 3 ways that the NVDA exit process:

- [triggerNVDAExit](#When-exiting-from-triggerNVDAExit)
- [WM_QUIT](#When-exiting-from-WM_QUIT)
- [wx.EVT_END_SESSION](#When-exiting-from-wxEVT_END_SESSION)

### When exiting from `triggerNVDAExit`
* Called from within NVDA.
* A function in the core module
* Only executes the code once, uses a lock and flag to ensure this
* Uses a queue on the main thread to queue a safe shutdown
* Once the queued shutdown starts:
    1. the updateCheck is terminated
    1. watchdog is terminated
    1. addons and the brailleViewer are terminated, so we can close all windows safely
    1. All wx windows are closed
    1. Now that windows are closed, a new NVDA instance is started if requested

### When exiting from `WM_QUIT`
* [A Windows Message](https://docs.microsoft.com/en-us/windows/win32/winmsg/wm-quit) received from an external process, such as another NVDA process.
* NVDA accepts `WM_QUIT` messages from other processes and creates a [named window](https://docs.microsoft.com/en-us/windows/win32/learnwin32/creating-a-window#creating-the-window) that can be discovered.
* Will force the main loop to exit and close most wx Windows.
* We subsequently run `triggerNVDAExit` to ensure that clean up code isn't missed, and pump the queue to execute it.
* Using a custom message has been considered:
  - Would allow custom handling (eg just `triggerNVDAExit`)
  - Unfortunately, older NVDA versions will only be aware of `WM_QUIT`, so we'd need to send `WM_QUIT` to these versions.
  - Sending the custom message, waiting for a timeout, then sending `WM_QUIT` adds a significant wait time
  - Identifying the running version (to selectively send the message) requires maintaining 2 message windows in NVDA (one for legacy behaviour) and adds complexity

### When exiting from `wx.EVT_END_SESSION`
* This is a [wxCloseEvent](https://docs.wxwidgets.org/3.0/classwx_close_event.html) triggered by a Windows session ending.
* On `wx.EVT_END_SESSION`, we save the config and play the exit sound.
* Other actions are not performed as we have limited time to perform an action for this event. With NVDA being killed off very last, Windows may include NVDA in the Block shutdown dialog, but the user won't be able to read it if we are shutting down.

### Replacing an existing NVDA instance

With the requirement to only allow a single instance of NVDA, a new NVDA process must be able to replace an existing NVDA process.
NVDA will exit correctly in response to a `[`WM_QUIT`](#When-exiting-from-WM_QUIT) Windows message, but the process must first be detected / identified in order to send the message.
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
