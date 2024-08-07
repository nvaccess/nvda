# Remote Debugging NVDA

Sometimes it is not possible to effectively debug a running copy of NVDA, particularly if you rely on NVDA or another screen reader for development.
In these cases, it is helpful to use a secondary machine to debug the running copy of NVDA.
This document explains how to use [Visual Studio Code] (VS Code) to remotely debug NVDA.
It is recommended that you use the [Visual Studio Code Workspace Configuration for NVDA] when using VS Code as your IDE for NVDA development.

## You will need

* Development machine: The machine with VS Code and all required extensions installed.
  * It is recommended that you use VS Code with the [Remote - Tunnels] extension installed.
  * To remotely debug NVDA, you must have the debug extension for the language you want to debug installed--[Python Debugger] for python and [C/C++] for C++.
    The [Python C++ Debugger] is recommended for debugging Python and C++ at the same time.
  * Consider using the pre-configured NVDA VS Code workspace, which will recommend all required addons, and has other required settings configured.
  * Alternatively, you can use Visual Studio Code for the Web to debug the remote copy of NVDA in a web browser if you wish.
* Secondary machine: The machine with NVDA's source and the [NVDA dev environment] set up.
  This is the machine you will use to run the copy of NVDA being debugged.
  * As we are going to connect to VS Code, you will need to have VS Code installed.
    Alternatively, you canuse the [VS Code Standalone CLI].

If you do not have (or do not want to use) two physical machines, you can use a virtual machine as the secondary machine.
Depending on the virtualisation software (hypervisor) in use, this may require hardware virtualisation support.
Without hardware virtualisation support, using a virtual machine will likely be slow, or may not be possible.

Instructions on how to create and use virtual machines are out of scope for this document.
Popular hypervisors for windows include [Oracle VM VirtualBox], [VMware Workstation] and [Microsoft Hyper-V].

## Workflow

### On the secondary machine

1. Open your NVDA repository in VS Code.
   E.g. in a terminal `cd` to the NVDA repo and run `code .`.
2. Set up a Remote tunnel so that another VS code can control this VS code:  
   1. Open the Command Palette (`Ctrl`+`Shift`+`P`) and select "Remote Tunnels: Turn on Remote Tunnel Access...".
   2. Choose whether you want the tunnel to be open for this session (only when VS Code is open), or as a service (whenever you're logged in to this machine).
      * Installing the tunnel as a service will result in the tunnel continuing to remain active in the background.
        This option is not recommended.
   3. Choose how you will publish the tunnel.
      GitHub is probably easiest if you're already using GitHub for development.
      If you're not already logged in, log in when asked.
   4. A notification should appear informing you that your tunnel is available.
      Take note of the tunnel's name.

If you prefer, you can set up the tunnel [at the command line instead](https://code.visualstudio.com/docs/editor/command-line#_create-remote-tunnel).

* `code tunnel` to create a session tunnel.
* `code tunnel service install` to create a background service tunnel.

### On the development machine

1. Open VS Code.
2. Open the Remote Menu (`Ctrl`+`Alt`+`O`) and choose "Connect to Tunnel...".
   * If you do not have the Remote-Tunnels extension installed, select "Tunnel" to install it.
3. Choose the account type you used to publish the tunnel from your secondary machine.
   If you're not already logged in, log in when asked.
   Make sure you log in to the same account you used to publish the tunnel.
4. Select the tunnel that you created from your secondary machine.
   VS Code will let you know when you have connected.
   * The first time you connect, this may take some time as VS Code downloads necessary components.
   * Even if you have the required extensions installed locally, VS Code may prompt you to install them in the remote workspace.
     If prompted, procede with the installation of the extensions.
5. Go to the Explorer view (`Ctrl`+`Shift`+`E`), select "Open Folder" and browse to the NVDA repository on the development machine (or type its path).
6. VS Code on your development machine is now acting as a remote control for your secondary machine.
   Anything you do now will be carried out on your development machine.
7. With an appropriate `launch.json` (such as that in the NVDA VS Code workspace configuration) in the secondary machine's `.vscode` directory in the NVDA repository, you can now run and debug NVDA.
   NVDA will run on the secondary machine, and you can interact with the Debug view on the development machine.

If you prefer, you can also debug the remote copy of NVDA in a browser by entering the vscode.dev URL that was generated on the secondary machine.

### When you're done

When you're done, it's a good idea to disconnect from the remote tunnel on your development machine, and close the tunnel on your secondary machine.

* On your development machine, make sure you've saved any changes you have made, then open the Remote menu (`Ctrl`+`Alt`+`O`) and choose "Close Remote Connection".
* On your secondary machine, open the Command Palette (`Ctrl`+`Shift`+`P`) and run "Remote Tunnels: Turn off Remote Tunnel Access...".
  Press "Yes" when prompted.
  * If you chose to create a session tunnel, closing VS Code without turning off remote tunnel access will close the tunnel until you open VS Code again.
  * If you created the tunnel as a service, the tunnel will continue to remain active in the background until you turn off remote tunnel access.
  * If you created the tunnel at the CLI, `Ctrl`+`C` to close it.
    If you created it as a service, run `code tunnel kill` to stop the service, or `code tunnel service uninstall` to remove it.

## Further reading

The following resources may be of use:

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
