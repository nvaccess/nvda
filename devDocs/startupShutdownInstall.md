# NVDA Starting and Exiting outline

## Ways to start NVDA:

1. For an installed copy:
    1. Ctrl+Alt+N (Desktop shortcut)
    1. Automatically via Ease of Access on the Windows sign-in screen (at boot or signing out of a previous session)
    1. Automatically via Ease of Access on User Account Control (UAC) screens
    1. Via startup
1. For an installed copy, portable copy, installer:
    - By running the exe (see cli options too).
    This can be triggered by a user or external process such as an existing NVDA instance
    - test: `startupShutdownNVDA.Starts`
1. For source: eg runnvda.bat

## NVDA can be shutdown by:

1. UI within NVDA, with and without an ExitDialog prompt (uses `triggerNVDAExit`):
    1. NVDA+q
        - test: `startupShutdownNVDA.Quits from keyboard, Restarts`
    1. An unbound command to restart
    1. A prompt to restart from changing certain settings
    1. Via the NVDA menu -> Exit
        - test: `startupShutdownNVDA.Quits from menu`
1. A process sending `WM_QUIT`, eg a new NVDA process starting (uses `WM_QUIT`)
1. A handled crash (directly causes a new process to start, terminates unsafely)
    - test: `startupShutdownNVDA.Restarts on crash, Restarts on braille crash`
1. An unhandled crash (terminates unsafely)
1. An external command which kills the process (terminates unsafely) 
1. Windows shutting down (terminates unsafely)
    - On `wx.EVT_END_SESSION`, we save the config and play the exit sound. (Note: should this do more? NVDA may terminate unsafely directly after this)

## Safe exit hooks/triggers

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
* a windows message which can be sent across processes which will force the main loop to exit and close most NVDA windows.
* We subsequently run `triggerNVDAExit` to exit other required processes, and pump the queue to execute the shutdown.

## Technical startup and exit process

All the startup pathways execute nvda.pyw.

1. *Start nvda.pyw* 
1. MonkeyPatches are applied, the virtual environment is checked, starting arguments are parsed
1. We check for a running instance of NVDA by looking for a Message Window
    - terminate it if possible using `WM_QUIT` or forcing the process to exit. If this fails, abandon startup
1. We try to acquire the NVDA mutex
    - abandon startup if we can't
1. Initialise logging
1. Set the process to allow `WM_QUIT` messages
1. Start running `core.main()`
    1. Initialize config
    1. Play startup sound
    1. Set language, initialize NVDA modules and wx GUI
    1. Create the Message Window (used for `WM_QUIT`)
    1. Start the core pump (the timer that is fired inside the main loop when there is work to do)
    1. Start watchdog
    1. Notify postNvdaStartup
    1. Start the wx app main loop
    --- 
    1. *The main loop has exited via `triggerNVDAExit` or `WM_QUIT`*
    1. If `WM_QUIT` was used to exit the main loop, perform `triggerNVDAExit`
    1. Terminate gui
    1. Save config
    1. Terminate NVDA modules
    1. Play exit sound
    1. Destroy the message window
    1. Return to nvda.pyw
1. Notify ease of access of the shutdown
1. Release the Mutex
1. Exit nvda.pyw with `sys.exit`

### As a user, NVDA can be updated or installed:

1. Via a downloaded installer exe
1. Via the NVDA updater

### Technical installer/updater process:

1. 
