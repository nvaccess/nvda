# NVDA Remote Manual Test Suite

## Overview

Remote  enables remote assistance functionality between two computers running NVDA. It allows a user to connect to another computer running NVDA and either control the remote system or have their system controlled. This enables remote support, training, and collaboration between screen reader users. The add-on provides features such as speech relay, keyboard control, clipboard sharing, and braille support over remote connections.

## Environment Setup

### Host Configuration

* Windows 11 Pro
* Memory: at least 16GB
* Processor: at least 4 core
* NVDA Version: latest
* NVDA Remote Version: 2.6.4 (installed via addon store)

### Guest Configuration

* Another computer similar to the host or VMware Windows 11 Home running on the host with similar specs to the host computer
* Storage: 64GB disk
* Memory: 16GB
* Processor: 8 core
* NVDA Version: Custom build from <https://github.com/nvda-art/nvda> (remote branch)
* Base Position: latest

## Pre-Test Setup

1. Build signed launcher
2. Host: Run installed stock NVDA
3. Guest: Install signed launcher

## Connection Tests

### Direct Connection

1. Open NVDA Remote on the host
2. Press NVDA+alt+page-up to open the "Connect" dialog
3. Choose "Host" option
4. Set a password and wait for incoming connection
5. Open NVDA Remote on the guest
6. Press NVDA+alt+page-up to open the "Connect" dialog
7. Choose "Client" option
8. Enter the host's IP address and password
9. Verify connection status announcements or sounds
10. Test reversing roles (host becomes client, client becomes host)

### Control Server Connection

1. Open NVDA Remote on both systems
2. On both systems, press NVDA+alt+page-up to open the "Connect" dialog
3. Choose "Connect to Control Server" (nvdaremote.com)
4. Enter the same key on both systems
5. Set appropriate control permissions (Host controls guest, guest controls host)
6. Verify connection is established
7. Disconnect and retry with a different key
8. Verify behavior when server is unavailable
9. Test reconnection after temporary network interruption (by disabling networking or turning wifi off then back on again)
10. Test reversing roles (host becomes client, client becomes host)

## Version Compatibility Tests

### New Remote to New Remote

1. Install the new remote implementation on two test machines
2. Establish connection between the two instances
3. Test all control modes:
4. Verify all features work correctly compared to old plugin:
   1. Speech relay
   2. Remote keyboard input
   3. Clipboard transfer
   4. Braille routing
5. If possible, monitor CPU and memory usage during an extended session
6. Test connection stability during intensive screen reader usage

### New Remote Controlling Old Plugin

1. Install the new remote implementation on one machine
2. Install the 2.6.4 plugin on another machine
3. Test connecting from new remote to old plugin system
4. Verify backward compatibility of control features:
   1. Keyboard commands
   2. Speech relay
   3. Clipboard sharing
   4. Braille support
5. Test automatic reconnection behavior
6. Switch control directions and verify functionality

## Remote Control Features

### Keyboard Input

1. Connect two machines with remote control enabled
2. Test basic typing in a text editor
3. Test system shortcuts:
   1. Alt+Tab to switch applications
   2. Windows key to open start menu
   3. Alt+F4 to close applications
4. Test NVDA-specific shortcuts:
   1. NVDA+T to read title
   2. NVDA+F to read formatting
   3. NVDA+Tab for focus reporting
5. Verify modifier key combinations work properly:
   1. Shift+arrows for selection
   2. Ctrl+C and Ctrl+V for copy/paste
   3. Alt key combinations for menu navigation

## Speech and Braille

### Speech Relay

1. Connect two machines with remote control enabled
2. Navigate through various UI elements on controlled machine
3. Verify speech output on controlling machine
4. Test with different speech synthesizers:
   1. eSpeak NG
   2. Windows OneCore
   3. Any third-party synthesizer
5. Measure speech latency and note any issues
6. Test speech interruption behavior (press ctrl when speaking)
7. Verify speech settings respect on host/guest machines

### Braille Support

1. Connect a braille display to the controlling machine
2. Establish remote connection between machines
3. Verify braille output appears correctly
4. Test braille cursor routing functions
5. Test braille input commands
6. Verify braille display settings are respected
7. Test with different braille display models if available

## Special Features

### Clipboard Sharing

1. Connect two machines
2. Copy text on the controlling machine (Ctrl+C)
3. Push the clipboard text (NVDA+SHIFT+CTRL+C)
4. Paste text on the controlled machine (Ctrl+V)
5. Repeat in reverse direction
6. Test with various content types:
   1. Plain text
   2. Formatted text
   3. Large text (multiple paragraphs)
7. Verify handling of special characters
8. Test copying and pasting with keyboard shortcuts and context menus

## Error Handling

### Connection Issues

1. Establish remote connection between two machines
2. Temporarily disable network adapter on one machine
3. Verify appropriate error messages are displayed
4. Verify reconnection attempts occur automatically
5. Test behavior when connection times out
6. Verify recovery when network is restored
7. Test disconnection handling when one machine crashes

### Resource Usage

1. Establish remote connection between two machines
2. Monitor CPU usage during an extended session (30+ minutes)
3. Monitor memory consumption over time
4. Run resource-intensive applications during connection
5. Verify system stability under load
6. Document any performance degradation
7. Test with different NVDA logging levels

## Security Tests

### Authentication

1. Test connection with valid password
2. Attempt connection with invalid password
3. Test empty password behavior
