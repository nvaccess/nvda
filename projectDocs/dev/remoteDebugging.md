# Remote Debugging NVDA

Sometimes, it is not possible to effectively debug a running copy of NVDA, especially if you rely on NVDA or another screen reader for development.
In such cases, using a secondary machine to debug the running copy of NVDA can be helpful.
This document explains how to use [Visual Studio Code] (VS Code) to remotely debug NVDA.
It is recommended that you use the [Visual Studio Code Workspace Configuration for NVDA] when using VS Code as your IDE for NVDA development.

Note: keyboard shortcuts used in this guide assume you are using VS Code in English with a QWERTY keyboard, and that you haven't customised your keymap.
If they don't work, search the action in the Command Palette or Keyboard Shortcuts settings to find or change the key binding on your system.

## You will need

* Development machine: The machine with VS Code and all required extensions installed.
  * It is recommended that you use VS Code with the [Remote - Tunnels] extension installed.
  * To remotely debug NVDA, you must have the debug extension for the language you want to debug installed - [Python Debugger] for python and [C/C++] for C++.
    The [Python C++ Debugger] is recommended for debugging Python and C++ simultaneously.
  * Consider using the pre-configured NVDA VS Code workspace, which recommends all required extensions, and has other necessary settings configured.
  * Alternatively, you can use Visual Studio Code for the Web to debug the remote copy of NVDA in a web browser if you wish.
* Secondary machine: The machine with NVDA's source and the [NVDA dev environment] set up.
  This is the machine you will use to run the copy of NVDA being debugged.
  * As we are going to connect to VS Code, you will need to have VS Code installed.
    Alternatively, you can use the [VS Code Standalone CLI].

If you do not have (or do not want to use) two physical machines, you can use a virtual machine as the secondary machine.
Depending on the virtualisation software (hypervisor) in use, this may require hardware virtualisation support.
Without hardware virtualisation support, using a virtual machine will likely be slow, or may not be possible.

Instructions on how to create and use virtual machines are out of scope for this document.
Popular hypervisors for windows include [Oracle VM VirtualBox], [VMware Workstation] and [Microsoft Hyper-V].

## Workflow

### On the secondary machine

1. Open your NVDA repository in VS Code.
   E.g. in a terminal `cd` to the NVDA repo and run `code .`.
2. Set up a Remote tunnel so that another instance of VS code can control this one:
   1. Open the Command Palette (`control+shift+p`) and select "Remote Tunnels: Turn on Remote Tunnel Access...".
   2. Choose whether you want the tunnel to be open for this session (only when VS Code is open), or as a service (whenever you're logged in to this machine).
      * Installing the tunnel as a service will keep it active in the background, even when VS Code is closed.
        This option is not recommended.
   3. Choose how you will publish the tunnel.
      GitHub is probably easiest if you're already using GitHub for development.
      If you're not already logged in, log in when asked.
   4. A notification should appear informing you that your tunnel is available.
      Take note of the tunnel's name.

If you prefer, you can set up the tunnel [at the command line instead][CLI create tunnel].

* `code tunnel` to create a session tunnel.
* `code tunnel service install` to create a background service tunnel.

### On the development machine

1. Open VS Code.
2. Open the Remote Menu (`control+alt+o`) and choose "Connect to Tunnel...".
   * If you do not have the Remote-Tunnels extension installed, select "Tunnel" to install it.
3. Choose the account type you used to publish the tunnel from your secondary machine.
   If you're not already logged in, log in when prompted.
   Ensure you log in to the same account you used to publish the tunnel.
4. Select the tunnel that you created from your secondary machine.
   VS Code will let you know when you have connected.
   * The first time you connect, this may take some time as VS Code downloads necessary components.
   * Even if you have the required extensions installed locally, VS Code may prompt you to install them in the remote workspace.
     If prompted, proceed with the installation of the extensions.
5. Go to the Explorer view (`control+shift+e`), select "Open Folder" and browse to the NVDA repository on the secondary machine (or type its path).
6. VS Code on your development machine is now acting as a remote control for your secondary machine.
   Anything you do now will be carried out on your secondary machine.
7. With an appropriate `launch.json` (such as that in the NVDA VS Code workspace configuration) in the secondary machine's `.vscode` directory in the NVDA repository, you can now run and debug NVDA.
   NVDA will run on the secondary machine, and you can interact with the Debug view on the development machine.

If you prefer, you can also debug the remote copy of NVDA in a browser by entering the vscode.dev URL that was generated on the secondary machine.

### When you're done

When you're done, it's a good idea to disconnect from the remote tunnel on your development machine, and close the tunnel on your secondary machine.

* On your development machine, make sure you've saved any changes you have made, then open the Remote menu (`control+alt+o`) and choose "Close Remote Connection".
* On your secondary machine, open the Command Palette (`control+shift+p`) and run "Remote Tunnels: Turn off Remote Tunnel Access...".
  Press "Yes" when prompted.
  * If you created a session tunnel, closing VS Code without turning off remote tunnel access will close the tunnel until you open VS Code again.
  * If you created the tunnel as a service, the tunnel will continue to remain active in the background until you turn off remote tunnel access.
  * If you created the tunnel at the CLI, use `control+c` to close it.
    If you created it as a service, run `code tunnel kill` to close the tunnel, or `code tunnel service uninstall` to remove it.

## Example session: debug the date/time command

1. Set up your development and secondary machines as above, so that your development machine is now controlling your secondary machine.
2. On your development machine, navigate to `source/globalCommands.py`.
   Use the Explorer view (`control+shift+e`) to browse there, or the "Go to File..." command (`control+p`) to enter the path directly.
3. go to the date/time script (`script_dateTime`).
   Search (`control+f`) or use the breadcrumbs view (`control+shift+.`) to browse through the symbols in the file (you can type to filter in this list).
4. Insert a breakpoint (`f9`) in the `dateTime` script, for instance at the last line, and save the file (`control+s`).
5. Open the Debug view (`control+shift+d`) and ensure the appropriate debug launch configuration is selected.
   If you are using the pre-configured NVDA VS Code workspace, this is "NVDA (Python)".
   Note that to get to the launch selector, you need to press `rightArrow` when focused on the "Start Debugging" button.
   The selector is not currently reachable with tab.
6. Start debugging with the "Start Debugging" button (`f5`).
   NVDA should start up on your secondary machine.
7. On your secondary machine, execute the report time/date script (`NVDA+f12`).
   On your secondary machine, you will not hear anything, as NVDA will hit a breakpoint before it has the chance to speak.
   On your development machine, VS Code will let you know you have hit a breakpoint.
8. Now you can inspect NVDA's state (variables, stack frames etc) in the Debug view.
9. To continue debugging, run "Debug: Continue" (`f5`).
   On your secondary machine, NVDA should report the time.
10. To stop debugging, run "Debug: Stop" (`shift+f5`).
   When you're done with your breakpoint, toggle it off (`f9`) or remove it through the Debug view.

## Further reading

To learn more about debugging in VS Code, check out the following resources:

* [Debugging in Visual Studio Code](https://code.visualstudio.com/Docs/editor/debugging)
* [Debugging configurations for Python apps in Visual Studio Code](https://code.visualstudio.com/docs/python/debugging)
* [Debug C++ in Visual Studio Code](https://code.visualstudio.com/docs/cpp/cpp-debug)
* [Remote Tunnels documentation](https://code.visualstudio.com/docs/remote/tunnels)

[NVDA dev environment]: createDevEnvironment.md
[Visual Studio Code]: https://code.visualstudio.com/
[Remote - Tunnels]: https://marketplace.visualstudio.com/items?itemName=ms-vscode.remote-server
[Visual Studio Code Workspace Configuration for NVDA]: https://github.com/nvaccess/vscode-nvda
[Python C++ Debugger]: https://marketplace.visualstudio.com/items?itemName=benjamin-simmonds.pythoncpp-debug
[C/C++]: https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools
[Oracle VM VirtualBox]: https://www.virtualbox.org/
[VMware Workstation]: https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion
[Microsoft Hyper-V]: https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/about/
[Python Debugger]: https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy
[VS Code Standalone CLI]: https://code.visualstudio.com/docs/remote/tunnels#_alternative-downloads
[CLI create tunnel]: https://code.visualstudio.com/docs/editor/command-line#_create-remote-tunnel
