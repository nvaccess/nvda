# NVDA NVDA_VERSION User Guide

[TOC]

<!-- KC:title: NVDA NVDA_VERSION Commands Quick Reference -->



## Introduction {#Introduction}

Welcome to NVDA!

NonVisual Desktop Access (NVDA) is a free and open source screen reader for the Microsoft Windows operating system.
Providing feedback via synthetic speech and Braille, it enables blind or vision impaired people to access computers running Windows for no more cost than a sighted person.
NVDA is developed by [NV Access](https://www.nvaccess.org/), with contributions from the community.

### General Features {#GeneralFeatures}

NVDA allows blind and vision impaired people to access and interact with the Windows operating system and many third party applications.

A short video demonstration, ["What is NVDA?"](https://www.youtube.com/watch?v=tCFyyqy9mqo) is available from the NV Access YouTube channel.

Major highlights include:

* Support for popular applications including web browsers, email clients, internet chat programs and office suites
* Built-in speech synthesizer supporting over 80 languages
* Reporting of textual formatting where available such as font name and size, style and spelling errors
* Automatic announcement of text under the mouse and optional audible indication of the mouse position
* Support for many refreshable braille displays, including the ability to detect many of them automatically as well as braille input on braille displays with a braille keyboard
* Ability to run entirely from a USB flash drive or other portable media without the need for installation
* Easy to use talking installer
* Translated into 54 languages
* Support for modern Windows Operating Systems including both 32 and 64 bit variants
* Ability to run during Windows sign-in and [other secure screens](#SecureScreens).
* Announcing controls and text while using touch gestures
* Support for common accessibility interfaces such as Microsoft Active Accessibility, Java Access Bridge, IAccessible2 and UI Automation
* Support for Windows Command Prompt and console applications
* The ability to highlight the system focus

### System Requirements {#SystemRequirements}

* Operating Systems: all 32-bit and 64-bit editions of Windows 8.1, Windows 10, Windows 11, and all Server Operating Systems starting from Windows Server 2012 R2.
  * both AMD64 and ARM64 variants of Windows are supported.
* at least 150 MB of storage space.

### Internationalization {#Internationalization}

It is important that people anywhere in the world, no matter what language they speak, get equal access to technology.
Besides English, NVDA has been translated into 54 languages including: Afrikaans, Albanian, Amharic, Arabic, Aragonese, Bulgarian, Burmese, Catalan, Chinese (simplified and traditional), Croatian, Czech, Danish, Dutch, Farsi, Finnish, French, Galician, Georgian, German (Germany and Switzerland), Greek, Hebrew, Hindi, Hungarian, Icelandic, Irish, Italian, Japanese, Kannada, Korean, Kyrgyz, Lithuanian, Macedonian, Mongolian, Nepali, Norwegian, Polish, Portuguese (Brazil and Portugal), Punjabi, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish (Colombia and Spain), Swedish, Tamil, Thai, Turkish, Ukrainian and Vietnamese.

### Speech Synthesizer Support {#SpeechSynthesizerSupport}

Apart from providing its messages and interface in several languages, NVDA can also enable the user to read content in any language, as long as they have a speech synthesizer that can speak that language.

NVDA is bundled with [eSpeak NG](https://github.com/espeak-ng/espeak-ng), a free, open-source, multi-lingual speech synthesizer.

Information about other speech synthesizers that NVDA supports can be found in the [Supported Speech Synthesizers](#SupportedSpeechSynths) section.

### Braille support {#BrailleSupport}

For users that own a refreshable braille display, NVDA can output its information in braille.
NVDA uses the open source braille translator [LibLouis](https://liblouis.io/) to generate braille sequences from text.
Both uncontracted and contracted braille input via a braille keyboard is also supported.
Furthermore, NVDA will detect many braille displays automatically by default.
Please see the [Supported Braille Displays](#SupportedBrailleDisplays) section for information about the supported braille displays.

NVDA supports braille codes for many languages, including contracted, uncontracted and computer braille codes.

### License and Copyright {#LicenseAndCopyright}

NVDA is copyright NVDA_COPYRIGHT_YEARS NVDA contributors.

NVDA is available under the GNU General Public License version 2, with two special exceptions.
The exceptions are outlined in the license document under the sections "Non-GPL Components in Plugins and Drivers" and "Microsoft Distributable Code".
NVDA also includes and uses components which are made available under different free and open source licenses.
You are free to share or change this software in any way you like as long as it is accompanied by the license and you make all source code available to anyone who wants it.
This applies to both original and modified copies of this software, plus any derivative works.

For further details, you can [view the full license.](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
For details regarding exceptions, access the license document from the NVDA menu under the "help" section.

## NVDA Quick Start Guide {#NVDAQuickStartGuide}

This quick start guide contains three main sections: downloading, initial setup, and running NVDA.
These are followed by information on adjusting preferences, using add-ons, participating in the community and getting help.
The information in this guide is condensed from other parts of the NVDA User Guide.
Please refer to the full User Guide for more detailed information on each topic.

### Downloading NVDA {#GettingAndSettingUpNVDA}

NVDA is completely free for anyone to use.
There is no license key to worry about or expensive subscription to pay.
NVDA is updated, on average, four times per year.
The latest version of NVDA is always available from the "Download" page of the [NV Access website](NVDA_URL).

NVDA works with all recent versions of Microsoft Windows.
Check the [System Requirements](#SystemRequirements) for full details.

#### Steps for Downloading NVDA {#StepsForDownloadingNVDA}

These steps assume some familiarity with navigating a web page.

* Open your web browser (Press the `Windows` key, type the word "internet" without quotes, and press `enter`)
* Load the NV Access download page (Press `alt+d`, type the following address and press `enter`):
https://www.nvaccess.org/download
* Activate the "download" button
* The browser may or may not prompt for an action after downloading, and then start the download
* Depending on the browser, the file may run automatically after it downloads
* If the file needs to be manually launched, press `alt+n` to move to the notification area, then `alt+r` to run the file (or the steps for your browser)

### Setting up NVDA {#SettingUpNVDA}

Running the file you have just downloaded will start a temporary copy of NVDA.
You will then be asked if you want to install NVDA, create a portable copy or just continue using the temporary copy.

NVDA does not need access to the Internet to run or install once the launcher is downloaded.
If available, an internet connection does enable NVDA to check for updates periodically.

#### Steps for running the downloaded launcher {#StepsForRunningTheDownloadLauncher}

The setup file is named "nvda_2022.1.exe" or similar.
The year and version changes between updates to reflect the current release.

1. Run the downloaded file.
Music plays while a temporary copy of NVDA loads.
Once loaded, NVDA will speak throughout the rest of the process.
1. The NVDA Launcher window appears with the license agreement.
Press `downArrow` to read the license agreement if desired.
1. Press `tab` to move to the "I agree" checkbox, then press the `spacebar` to check it.
1. Press `tab` to move through the options, then press `enter` on the desired option.

The options are:

* "Install NVDA on this computer": This is the main option most users want for easy use of NVDA.
* "Create portable copy": This allows NVDA to be setup in any folder without installing.
This is useful on computers without admin rights, or on a memory stick to carry with you.
When selected, NVDA walks through the steps to create a portable copy.
The main thing NVDA needs to know is the folder to setup the portable copy in.
* "Continue running": This keeps the temporary copy of NVDA running.
This is useful for testing features in a new version before installing it.
When selected, the launcher window closes and the temporary copy of NVDA continues running until it is exited or the PC is shut down.
Note that changes to settings are not saved.
* "Cancel": This closes NVDA without performing any action.

If you plan to always use NVDA on this computer, you will want to choose to install NVDA.
Installing NVDA will allow for additional functionality such as automatic starting after sign-in, the ability to read the Windows sign-in and [secure screens](#SecureScreens).
These cannot be done with portable and temporary copies.
For full details of the limitations when running a portable or temporary copy of NVDA, please see [Portable and temporary copy restrictions](#PortableAndTemporaryCopyRestrictions).

Installing also offers to create Start Menu and desktop shortcuts, and allow NVDA to be started with `control+alt+n`.

#### Steps for installing NVDA from the launcher {#StepsForInstallingNVDAFromTheLauncher}

These steps walk through the most common setup options.
For more details on the options available, please see [Installation options](#InstallingNVDA).

1. From the launcher, ensure the checkbox to agree to the license is checked.
1. `Tab` to, and activate the "Install NVDA on this computer" button.
1. Next, are options to use NVDA during Windows sign-in and to create a desktop shortcut.
These are checked by default.
If desired, press `tab` and `spaceBar` to change any of these options, or leave them at the default.
1. Press `enter` to continue.
1. A Windows "User Account Control (UAC)" dialog appears asking "Do you want to allow this app to make changes to your PC?".
1. Press `alt+y` to accept the UAC prompt.
1. A progress bar fills up as NVDA installs.
During this process NVDA sounds an increasingly higher pitched beep.
This process is often fast and may not be noticed.
1. A dialog box appears confirm that the install of NVDA has been successful.
The message advises to "Press OK to start the installed copy".
Press `enter` to start the installed copy.
1. The "Welcome to NVDA" dialog appears, and NVDA reads a welcome message.
The focus is on the "Keyboard Layout" drop-down.
By default, "Desktop" keyboard layout uses the number pad for some function.
If desired, press `downArrow` to choose "Laptop" keyboard layout to reassign number pad functions to other keys.
1. Press `tab` to move to "Use `capsLock` as an NVDA modifier key".
`Insert` is set as the NVDA modifier key by default.
Press `spaceBar` to select `capsLock` as an alternate modifier key.
Note that the keyboard layout is set separately from the NVDA modifier key.
The NVDA key and keyboard layout can be changed later from the Keyboard Settings.
1. Use `tab` and `spaceBar` to adjust the other options on this screen.
These set whether NVDA starts automatically.
1. Press `enter` to close the dialog box with NVDA now running.

### Running NVDA {#RunningNVDA}

The full NVDA user guide has all the NVDA commands, split up into different sections for reference.
The tables of commands are also available in the "Commands Quick Reference".
The "Basic Training for NVDA" NVDA training module has each command in more depth with step-by-step activities.
"Basic Training for NVDA" is available from the [NV Access Shop](http://www.nvaccess.org/shop).

Here are some basic commands which are used frequently.
All commands are configurable, so these are the default keystrokes for these functions.

#### The NVDA Modifier Key {#NVDAModifierKey}

The default NVDA modifier key is either the `numpadZero`, (with `numLock` off), or the `insert` key, near the `delete`, `home` and `end` keys.
The NVDA modifier key can also be set to the `capsLock` key.

#### Input Help {#InputHelp}

To learn and practice the location of keys, press `NVDA+1` to turn Input help on.
While in input help mode, performing any input gesture (such as pressing a key or performing a touch gesture) will report the action and describe what it does (if anything).
The actual commands will not execute while in input help mode.

#### Starting and stopping NVDA {#StartingAndStoppingNVDA}

| Name |Desktop key |Laptop key |Description|
|---|---|---|---|
|Start NVDA |`control+alt+n` |`control+alt+n` |Starts or restarts NVDA|
|Exit NVDA |`NVDA+q`, then `enter` |`NVDA+q`, then `enter` |Exits NVDA|
|Pause or restart speech |`shift` |`shift` |Instantly pauses speech. Pressing it again will continue speaking where it left off|
|Stop speech |`control` |`control` |Instantly stops speaking|

#### Reading text {#ReadingText}

| Name |Desktop key |Laptop key |Description|
|---|---|---|---|
|Say all |`NVDA+downArrow` |`NVDA+a` |Starts reading from the current position, moving it along as it goes|
|Read current line |`NVDA+upArrow` |`NVDA+l` |Reads the line. Pressing twice spells the line. Pressing three times spells the line using character descriptions (Alpha, Bravo, Charlie, etc)|
|Read selection |`NVDA+shift+upArrow` |`NVDA+shift+s` |Reads any selected text. Pressing twice will spell the information. Pressing three times will spell it using character description|
|Read clipboard text |`NVDA+c` |`NVDA+c` |Reads any text on the clipboard. Pressing twice will spell the information. Pressing three times will spell it using character description|

#### Reporting location and other information {#ReportingLocation}

| Name |Desktop key |Laptop key |Description|
|---|---|---|---|
|Window title |`NVDA+t` |`NVDA+t` |Reports the title of the currently active window. Pressing twice will spell the information. Pressing three times will copy it to the clipboard|
|Report focus |`NVDA+tab` |`NVDA+tab` |Reports the current control which has focus.  Pressing twice will spell the information. Pressing three times will spell it using character description|
|Read window |`NVDA+b` |`NVDA+b` |Reads the entire current window (useful for dialogs)|
|Read status bar |`NVDA+end` |`NVDA+shift+end` |Reports the Status Bar if NVDA finds one. Pressing twice will spell the information. Pressing three times will copy it to the clipboard|
|Read time |`NVDA+f12` |`NVDA+f12` |Pressing once reports the current time, pressing twice reports the date. The time and date are reported in the format specified in Windows settings for the system tray clock.|
|Report text formatting |`NVDA+f` |`NVDA+f` |Reports text formatting. Pressing twice shows the information in a window|
|Report link destination |`NVDA+k` |`NVDA+k` |Pressing once speaks the destination URL of the link at the current caret or focus position. Pressing twice shows it in a window for more careful review|

#### Toggle which information NVDA reads {#ToggleWhichInformationNVDAReads}

| Name |Desktop key |Laptop key |Description|
|---|---|---|---|
|Speak typed characters |`NVDA+2` |`NVDA+2` |When enabled, NVDA will announce all characters you type on the keyboard.|
|Speak typed words |`NVDA+3` |`NVDA+3` |When enabled, NVDA will announce word you type on the keyboard.|
|Speak command keys |`NVDA+4` |`NVDA+4` |When enabled, NVDA will announce all non-character keys you type on the keyboard. This includes key combinations such as control plus another letter.|
|Enable mouse tracking |`NVDA+m` |`NVDA+m` |When enabled, NVDA will announce the text currently under the mouse pointer, as you move it around the screen. This allows you to find things on the screen, by physically moving the mouse, rather than trying to find them through object navigation.|

#### The synth settings ring {#TheSynthSettingsRing}

| Name |Desktop key |Laptop key |Description|
|---|---|---|---|
|Move to next synth setting |`NVDA+control+rightArrow` |`NVDA+shift+control+rightArrow` |Moves to the next available speech setting after the current, wrapping around to the first setting again after the last|
|Move to previous synth setting |`NVDA+control+leftArrow` |`NVDA+shift+control+leftArrow` |Moves to the next available speech setting before the current, wrapping around to the last setting after the first|
|Increment current synth setting |`NVDA+control+upArrow` |`NVDA+shift+control+upArrow` |increases the current speech setting you are on. E.g. increases the rate, chooses the next voice, increases the volume|
|Increment the current synth setting in larger steps |`NVDA+control+pageUp` |`NVDA+shift+control+pageUp` |Increases the value of the current speech setting you're on in larger steps. e.g. when you're on a voice setting, it will jump forward every 20 voices; when you're on slider settings (rate, pitch, etc) it will jump forward the value up to 20%|
|Decrement current synth setting |`NVDA+control+downArrow` |`NVDA+shift+control+downArrow` |decreases the current speech setting you are on. E.g. decreases the rate, chooses the previous voice, decreases the volume|
|Decrement the current synth setting in larger steps |`NVDA+control+pageDown` |`NVDA+shift+control+pageDown` |Decreases the value of the current speech setting you're on in larger steps. e.g. when you're on a voice setting, it will jump backward every 20 voices; when you're on a slider setting, it will jump backward the value up to 20%.|

It is also possible to set the first or last value of the current synth setting by assign custom gestures in [Input Gestures dialog](#InputGestures), under the speech category.
This means, for example, when you're on a rate setting, it will set the rate to 0 or 100.
When you're on a voice setting, it will set the first or last voice.

#### Web navigation {#WebNavigation}

The full list of Single Letter Navigation keys is in the [Browse Mode](#BrowseMode) section of the user guide.

| Command |Keystroke |Description|
|---|---|---|
|Heading |`h` |Move to the next heading|
|Heading level 1, 2, or 3 |`1`, `2`, `3` |Move to the next heading at the specified level|
|Form field |`f` |Move to the next form field (edit box, button, etc)|
|Link |`k` |Move to the next link|
|Landmark |`d` |Move to the next landmark|
|List |`l` |Move to the next list|
|Table |`t` |Move to the next table|
|Move backwards |`shift+letter` |Press `shift` and any of the above letters to move to the previous element of that type|
|Elements list |`NVDA+f7` |Lists various types of elements, such as links and headings|

### Preferences {#Preferences}

Most NVDA functions can be enabled or changed via the NVDA settings.
Settings, and other options, are available via NVDA's menu.
To open NVDA's menu, press `NVDA+n`.
To open NVDA's general settings dialog directly, press `NVDA+control+g`.
Many settings screens have keystrokes to open them directly, such as `NVDA+control+s` for synthesizer, or `NVDA+control+v` for other voice options.

### Add-ons {#Addons}
Add-ons are programs which provide new or changed functionality for NVDA.
Add-ons are developed by the NVDA community, or external companies and are unaffiliated with NV Access.
As with any software, it is important to trust the developer of an add-on before using it.
Please refer to [Installing Add-ons](#AddonStoreInstalling) for ways to verify add-ons prior to installation.

The first time the Add-on Store is opened, NVDA displays a warning about add-ons.
Add-ons are not vetted by NV Access and may have unrestricted functionality and access to information.
Press `spacebar` if you have read the warning and do not need to see it next time.
Press `tab` to reach the "OK" button, then `enter` to accept the warning and proceed to the Add-on Store.
The "[Add-ons and the Add-on Store](#AddonsManager)" section of the User Guide contains information about every feature of the Add-on Store.

The Add-on Store is available from the Tools menu.
Press `NVDA+n` to open the NVDA menu, then `t` for tools, then `a` for Add-on Store.
When the Add-on Store opens, it shows "Available add-ons" if no add-ons are installed.
When add-ons are installed, the Add-on Store opens to the "Installed add-ons" tab.

#### Available add-ons {#AvailableAddons}
When the window first opens, add-ons may take a few seconds to load.
NVDA will read the name of the first add-on once the list of add-ons finishes loading.
Available add-ons are listed alphabetically in a multi-column list.
To browse the list and find out about a specific add-on:

1. Use the arrow keys or press the first letter of an add-on name to move around the list.
1. Press `tab` once to move to a description of the currently selected add-on.
1. Use the [reading keys](#ReadingText) or arrow keys to read the full description.
1. Press `tab` to the "Actions" button, which can be used to install the add-on, among other actions.
1. Press `tab` to "Other Details", which lists details such as the publisher, version and homepage.
1. To return to the list of add-ons, press `alt+a`, or `shift+tab` until reaching the list.

#### Searching for add-ons {#SearchingForAddons}
As well as browsing all available add-ons, it is possible to filter the add-ons shown.
To search, press `alt+s` to jump to the "Search" field and type the text to search for.
Searching checks for matches in the add-on ID, display name, publisher, author and description fields.
The list updates while typing the search terms.
Once done, press `tab` to go to the filtered list of add-ons and browse the results.

#### Installing add-ons {#InstallingAddons}

To install an add-on:

1. With the focus on an add-on you would like to install, press `enter`.
1. The actions menu opens with a list of actions; the first action is "Install".
1. To install the add-on, press `i` or `downArrow` to "Install" and press `enter`.
1. The focus returns to the add-on in the list and NVDA will read the details about the add-on.
1. The "Status" information reported by NVDA changes from "Available" to "Downloading".
1. Once the add-on has finished downloading, it will change to "Downloaded. Pending install".
1. Repeat with any other add-ons you would like to install at the same time.
1. Once finished, press `tab` until the focus is on the "Close" button, then press `enter`.
1. The downloaded add-ons will start the installation process once the Add-on Store is closed.
During the installation process, add-ons may display dialogs that you will need to respond to.
1. When the add-ons have been installed, a dialog appears advising that changes were made, and you must restart NVDA for the add-on installation to complete.
1. Press `enter` to restart NVDA.

#### Managing installed add-ons {#ManagingInstalledAddons}
Press `control+tab` to move between the tabs of the Add-on Store.
The tabs include: "Installed add-ons", "Updatable add-ons", "Available add-ons" and "Installed incompatible add-ons".
Each of the tabs are set out similar to each other, as a list of add-ons, a panel for more details on the selected add-on, and a button to perform actions for the selected add-on.
The actions menu of installed add-ons includes "Disable" and "Remove" rather than "Install".
Disabling an add-on stops NVDA from loading it, but leaves it installed.
To re-enable a disabled add-on, activate "Enable" from the actions menu.
After enabling, disabling, or removing add-ons, you will be prompted to restart NVDA when closing the Add-on Store.
These changes will only take effect once NVDA is restarted.
Note that in the Add-on Store window `escape` works the same as the Close button.

#### Updating add-ons {#UpdatingAddons}
When an update to an add-on you have installed is available, it will be listed in the "Updatable add-ons" tab.
Press `control+tab` to get to this tab from anywhere in the Add-on Store.
The status of the add-on will be listed as "Update available".
The list will display the currently installed version and the available version.
Press `enter` on the add-on to open the actions list; choose "Update".

### Community {#Community}

NVDA has a vibrant user community.
There is a main [English language email list](https://nvda.groups.io/g/nvda) and a page full of [local language groups](https://github.com/nvaccess/nvda/wiki/Connect).
NV Access, makers of NVDA, are active on [Twitter](https://twitter.com/nvaccess) and [Facebook](https://www.facebook.com/NVAccess).
NV Access also have a regular [In-Process blog](https://www.nvaccess.org/category/in-process/).

There is also an [NVDA Certified Expert](https://certification.nvaccess.org/) program.
This is an online exam you can complete to demonstrate your skills in NVDA.
[NVDA Certified Experts](https://certification.nvaccess.org/) can list their contact and relevant business details.

### Getting help {#GettingHelp}

To get help for NVDA, press `NVDA+n` to open the menu, then `h` for help.
From this submenu you can access the User Guide, a quick reference of commands, history of new features and more.
These first three options open in the default web browser.
There is also more comprehensive Training Material available in the [NV Access Shop](https://www.nvaccess.org/shop).

We recommend starting with the "Basic Training for NVDA module".
This module covers concepts from getting started up to browsing the web and using object navigation.
It is available in:

* [Electronic text](https://www.nvaccess.org/product/basic-training-for-nvda-ebook/), which includes Word DOCX, Web page HTML, eBook ePub and Kindle KFX formats.
* [Human-read, MP3 audio](https://www.nvaccess.org/product/basic-training-for-nvda-downloadable-audio/)
* [Hard-copy UEB Braille](https://www.nvaccess.org/product/basic-training-for-nvda-braille-hard-copy/) with delivery included anywhere in the world.

Other modules, and the discounted [NVDA Productivity Bundle](https://www.nvaccess.org/product/nvda-productivity-bundle/), are available in the [NV Access Shop](https://www.nvaccess.org/shop/).

NV Access also sells [telephone support](https://www.nvaccess.org/product/nvda-telephone-support/), either in blocks, or as part of the [NVDA Productivity Bundle](https://www.nvaccess.org/product/nvda-productivity-bundle/).
Telephone support includes local numbers in Australia and the USA.

The [email user groups](https://github.com/nvaccess/nvda/wiki/Connect) are a great source of community help, as are [certified NVDA experts](https://certification.nvaccess.org/).

You can make bug reports or feature requests via [GitHub](https://github.com/nvaccess/nvda/blob/master/projectDocs/issues/readme.md).
The [contribution guidelines](https://github.com/nvaccess/nvda/blob/master/.github/CONTRIBUTING.md) contain valuable information for contributing to the community.

## More Setup Options {#MoreSetupOptions}
### Installation Options {#InstallingNVDA}

If installing NVDA directly from the downloaded NVDA launcher, press the Install NVDA button.
If you have already closed this dialog or are wanting to install from a portable copy, please choose the Install NVDA menu item found under Tools in the NVDA menu.

The installation dialog that appears will confirm whether you wish to install NVDA and will also tell you whether this installation will be updating a previous install.
Pressing the Continue button will start installing NVDA.
There are also a few options in this dialog which are explained below.
Once the installation has completed, a message will appear telling you that it was successful.
Pressing OK at this point will restart the newly installed copy of NVDA.

#### Incompatible add-ons warning {#InstallWithIncompatibleAddons}

If you have add-ons already installed there may also be a warning that incompatible add-ons will be disabled.
Before you're able to press the Continue button you will have to use the checkbox to confirm that you understand that these add-ons will be disabled.
There will also be a button present to review the add-ons that will be disabled.
Refer to the [incompatible add-ons dialog section](#incompatibleAddonsManager) for more help on this button.
After installation, you are able to re-enable incompatible add-ons at your own risk from within the [Add-on Store](#AddonsManager).

#### Use NVDA during sign-in {#StartAtWindowsLogon}

This option allows you to choose whether or not NVDA should automatically start while at the Windows sign-in screen, before you have entered a password.
This also includes User Account Control and [other secure screens](#SecureScreens).
This option is enabled by default for fresh installations.

#### Create Desktop Shortcut (ctrl+alt+n) {#CreateDesktopShortcut}

This option allows you to choose whether or not NVDA should create a shortcut on the desktop to start NVDA.
If created, this shortcut will also be assigned a shortcut key of `control+alt+n`, allowing you to start NVDA at any time with this keystroke.

#### Copy Portable Configuration to Current User Account {#CopyPortableConfigurationToCurrentUserAccount}

This option allows you to choose whether or not NVDA should copy the user configuration from the currently running NVDA into the configuration for the currently logged on  user, for the installed copy of NVDA.
This will not copy the configuration for any other users of this system nor to the system configuration for use during Windows sign-in and [other secure screens](#SecureScreens).
This option is only available when installing from a portable copy, not when installing directly from the downloaded Launcher package.

### Creating a Portable Copy {#CreatingAPortableCopy}

If creating a portable copy directly from the NVDA download package, press the Create Portable Copy button.
If you have already closed this dialog or you are running an installed copy of NVDA, choose the Create Portable copy menu item found under Tools in the NVDA menu.

The Dialog that appears allows you to choose where the portable copy should be created.
This can be a directory on your hard drive or a location on a USB thumb drive or other portable media.
There is also an option to choose whether NVDA should copy the logged on user's current NVDA configuration for use  with the newly created portable copy.
This option is only available when creating a portable copy from an installed copy, not when creating from the download package.
Pressing Continue will create the portable copy.
Once creation is complete, a message will appear telling you it was successful.
Press OK to dismiss this dialog.

### Portable and Temporary Copy Restrictions {#PortableAndTemporaryCopyRestrictions}

If you want to take NVDA with you on a USB thumb drive or other writable media, then you should choose to create a portable copy.
The installed copy is also able to create a portable copy of itself at any time.
The portable copy also has the ability to install itself on any computer at a later time.
However, if you wish to copy NVDA onto read-only media such as a CD, you should just copy the download package.
Running the portable version directly from read-only media is not supported at this time.

The [NVDA installer](#StepsForRunningTheDownloadLauncher) can be used as a temporary copy of NVDA.
Temporary copies prevent saving NVDA settings.
This includes disabling usage of the [Add-on Store](#AddonsManager).

Portable and temporary copies of NVDA have the following restrictions:

* The inability to automatically start during and/or after log-on.
* The inability to interact with applications running with administrative privileges, unless of course NVDA itself has been run also with these privileges (not recommended).
* The inability to read User Account Control (UAC) screens when trying to start an application with administrative privileges.
* The inability to support input from a touchscreen.
* The inability to provide features such as browse mode and speaking of typed characters in Windows Store apps.
* Audio ducking is not supported.

## Using NVDA {#GettingStartedWithNVDA}
### Launching NVDA {#LaunchingNVDA}

If you have installed NVDA with the installer, then starting NVDA is as simple as either pressing control+alt+n, or choosing NVDA from the NVDA menu under Programs on the Start Menu.
Additionally you can type NVDA into the Run dialog and press Enter.
If NVDA is already running, it will be restarted.
You can also pass some [command line options](#CommandLineOptions) which allows you to quit (-q), disable add-ons (--disable-addons), etc.

For installed copies, NVDA stores the configuration in the roaming application data folder of the current user by default (e.g. "`C:\Users\<user>\AppData\Roaming`").
It is possible to change this in a way that NVDA loads its configuration from the local application data folder instead.
Consult the section about [system wide parameters](#SystemWideParameters) for more details.

To start the portable version, go to the directory you unpacked NVDA to, and press enter or double click on nvda.exe.
If NVDA was already running, it will automatically stop before starting the portable version.

As NVDA starts, you will first hear an ascending set of tones (telling you that NVDA is loading).
Depending on how fast your computer is, or if you are running NVDA off a USB key or other slow media, it may take a little while to start.
If it is taking an extra-long time to start, NVDA should say "Loading NVDA. Please wait..."

If you don't hear any of this, or you hear the Windows error sound, or a descending set of tones, then this means that NVDA has an error, and you will need to possibly report a bug to the developers.
Please check out the NVDA website for how to do this.

#### Welcome Dialog {#WelcomeDialog}

When NVDA starts for the first time, you will be greeted by a dialog box which provides you with some basic information about the NVDA modifier key and the NVDA menu.
(Please see further sections about these topics.)
The dialog box also contains a combo box and three checkboxes.
The combo box lets you select the keyboard layout.
The first checkbox lets you control if NVDA should use the Caps Lock as an NVDA modifier key.
The second specifies whether NVDA should start automatically after you log on to Windows and is only available for installed copies of NVDA.
The third lets you control if this Welcome dialog should appear each time NVDA starts.

#### Data usage statistics dialog {#UsageStatsDialog}

Starting from NVDA 2018.3, the user is asked if they want to allow usage data to be sent to NV Access in order to help improve NVDA in the future.
When starting NVDA for the first time, a dialog will appear which will ask you if you want to accept sending data to NV Access while using NVDA.
You can read more info about the data gathered by NV Access in the general settings section, [Allow NV Access to gather NVDA usage statistics](#GeneralSettingsGatherUsageStats).
Note: pressing on "yes" or "no" will save this setting and the dialog will never appear again unless you reinstall NVDA.
However, you can enable or disable the data gathering process manually in NVDA's general settings panel. For changing this setting manually, you can check or uncheck the checkbox called [Allow the NVDA project to gather NVDA usage statistics](#GeneralSettingsGatherUsageStats).

### About NVDA keyboard commands {#AboutNVDAKeyboardCommands}
#### The NVDA Modifier Key {#TheNVDAModifierKey}

Most NVDA-specific keyboard commands consist of pressing a particular key called the NVDA modifier key in conjunction with one or more other keys.
Notable exceptions to this are the text review commands for the desktop keyboard layout which just use the numpad keys by themselves, but there are some other exceptions as well.

NVDA can be configured so that the numpad Insert, Extended Insert and/or Caps Lock key can be used as the NVDA modifier key.
By default, both the numpad Insert and Extended Insert keys are set as NVDA modifier keys.

If you wish to cause one of the NVDA modifier keys to behave as it usually would if NVDA were not running (e.g. you wish to turn Caps Lock on when you have set Caps Lock to be an NVDA modifier key), you can press the key twice in quick succession.

#### Keyboard Layouts {#KeyboardLayouts}

NVDA currently comes with two sets of key commands (known as keyboard layouts): the desktop layout and the laptop layout.
By default, NVDA  is set to use the Desktop layout, though you can switch to the Laptop layout in the Keyboard category of the [NVDA Settings](#NVDASettings) dialog, found under Preferences in the NVDA menu.

The Desktop layout makes heavy use of the numpad (with Num Lock off).
Although most laptops do not have a physical numpad, some laptops can emulate one by holding down the FN key and pressing letters and numbers on the right-hand side of the keyboard (7, 8, 9, u, i, o, j, k, l, etc.).
If your laptop cannot do this or does not allow you to turn Num Lock off, you may want to switch to the Laptop layout instead.

### NVDA Touch Gestures {#NVDATouchGestures}

If you are running NVDA on a device with a touchscreen, you can also control NVDA directly via touch commands.
While NVDA is running, unless touch interaction support is disabled, all touch input will go directly to NVDA.
Therefore, actions that can be performed normally without NVDA will not work.
<!-- KC:beginInclude -->
To toggle touch interaction support, press NVDA+control+alt+t.
<!-- KC:endInclude -->
You can also enable or disable [touch interaction support](#TouchSupportEnable) from the Touch Interaction category of the NVDA settings.

#### Exploring the Screen {#ExploringTheScreen}

The most basic action you can perform with the touch screen is to announce the control or text at any point on the screen.
To do this, place one finger anywhere on the screen.
You can also keep your finger on the screen and move it around to read other controls and text that your finger moves over.

#### Touch Gestures {#TouchGestures}

When NVDA commands are described later in this user guide, they may list a touch gesture which can be used to activate that command with the touchscreen.
Following are some instructions on how to perform the various touch gestures.

##### Taps {#Taps}

Tap the screen quickly with one or more fingers.

Tapping once with one  finger is simply known as a tap.
Tapping with 2 fingers at the same time is a 2-finger tap and so on.

If the same tap is performed one or more times again in quick succession, NVDA will instead treat this as a multi-tap gesture.
Tapping twice will result in a double-tap.
Tapping 3 times will result in a triple-tap and so on.
Of course, these multi-tap gestures also recognize how many fingers were used, so it's possible to have gestures like a 2-finger triple-tap, a 4-finger tap, etc.

##### Flicks {#Flicks}

Quickly swipe your finger across the screen.

There are 4 possible flick gestures depending on the direction: flick left, flick right, flick up and flick down.

Just like taps, more than one finger can be used to perform the gesture.
Therefore, gestures such as 2-finger flick up and 4-finger flick left are all possible.

#### Touch Modes {#TouchModes}

As there are many more NVDA commands than possible touch gestures, NVDA has several touch modes you can switch between which make certain subsets of commands available.
The two modes are text mode and object mode.
Certain NVDA commands listed in this document may have a touch mode listed in brackets after the touch gesture.
For example, flick up (text mode) means that the command will be performed if you flick up, but only while in text mode.
If the command does not have a mode listed, it will work in any mode.

<!-- KC:beginInclude -->
To toggle touch modes, perform a 3-finger tap.
<!-- KC:endInclude -->

#### Touch keyboard {#TouchKeyboard}

The touch keyboard is used to enter text and commands from a touchscreen.
When focused on an edit field, you can bring up the touch keyboard by double-tapping the touch keyboard icon on the bottom of the screen.
For tablets such as Microsoft Surface Pro, the touch keyboard is always available when the keyboard is undocked.
To dismiss the touch keyboard, double-tap the touch keyboard icon or move away from the edit field.

While the touch keyboard is active, to locate keys on the touch keyboard, move your finger to where the touch keyboard is located (typically at the bottom of the screen), then move around the keyboard with one finger.
When you find the key you wish to press, double-tap the key or lift your finger, depending on options chosen from the [Touch Interaction Settings category](#TouchInteraction) of the NVDA Settings.

### Input Help Mode {#InputHelpMode}

Many NVDA commands are mentioned throughout the rest of this user guide, but an easy way to explore all the different commands is to turn on input help.

To turn on input help, press NVDA+1.
To turn it off, press NVDA+1 again.
While in input help, performing any input gesture (such as pressing a key or performing a touch gesture) will report the action and describe what it does (if anything).
The actual  commands will not execute while in input help mode.

### The NVDA menu {#TheNVDAMenu}

The NVDA menu allows you to control NVDA's settings, access help, save/revert your configuration, Modify speech dictionaries, access additional tools and exit NVDA.

To get to the NVDA menu from anywhere in Windows while NVDA is running, you may do any of the following:

* press `NVDA+n` on the keyboard.
* Perform a 2-finger double-tap on the touch screen.
* Access the system tray by pressing `Windows+b`, `downArrow` to the NVDA icon, and press `enter`.
* Alternatively, access the system tray by pressing `Windows+b`, `downArrow` to the NVDA icon, and open the context menu by pressing the `applications` key located next to the right control key on most keyboards.
On a keyboard without an `applications` key, press `shift+f10` instead.
* Right-click on the NVDA icon located in the Windows system tray

When the menu comes up, You can use the arrow keys to navigate the menu, and the `enter` key to activate an item.

### Basic NVDA commands {#BasicNVDACommands}

<!-- KC:beginInclude -->

| Name |Desktop key |Laptop key |Touch |Description|
|---|---|---|---|---|
|Starts or restarts NVDA |Control+alt+n |Control+alt+n |none |Starts or restarts NVDA from the Desktop, if this Windows shortcut is enabled during NVDA's installation process. This is a Windows specific shortcut and therefore it cannot be reassigned in the input gestures dialog.|
|Stop speech |Control |control |2-finger tap |Instantly stops speaking|
|Pause Speech |shift |shift |none |Instantly pauses speech. Pressing it again will continue speaking where it left off (if pausing is supported by the current synthesizer)|
|NVDA Menu |NVDA+n |NVDA+n |2-finger double-tap |Pops up the NVDA menu to allow you to access preferences, tools, help, etc.|
|Toggle Input Help Mode |NVDA+1 |NVDA+1 |none |Pressing any key in this mode will report the key, and the description of any NVDA command associated with it|
|Quit NVDA |NVDA+q |NVDA+q |none |Exits NVDA|
|Pass next key through |NVDA+f2 |NVDA+f2 |none |Tells NVDA to pass the next key press straight through to the active application - even if it is normally treated as an NVDA key command|
|Toggle application sleep mode on and off |NVDA+shift+s |NVDA+shift+z |none |sleep mode disables all NVDA commands and speech/braille output for the current application. This is most useful in applications that provide their own speech or screen reading features. Press this command again to disable sleep mode - note that NVDA will only retain the Sleep Mode setting until it is restarted.|

<!-- KC:endInclude -->

### Reporting System Information {#ReportingSystemInformation}

<!-- KC:beginInclude -->

| Name |key |Description|
|---|---|---|
|Report date/time |NVDA+f12 |Pressing once reports the current time, pressing twice reports the date|
|Report battery status |NVDA+shift+b |Reports the battery status i.e. whether AC power is in use or the current charge percentage.|
|Report clipboard text |NVDA+c |Reports the Text on the clipboard if there is any.|

<!-- KC:endInclude -->

### Speech modes {#SpeechModes}

The speech mode governs how screen content, notifications, responses to commands, and other output is spoken during operation of NVDA.
The default mode is "talk", which speaks in situations that are expected when using a screen reader.
However, under certain circumstances, or when running particular programs, you may find one of the other speech modes valuable.

The four available speech modes are:

* Talk (Default): NVDA will speak normally in reaction to screen changes, notifications, and actions such as moving the focus, or issuing commands.
* On-demand: NVDA will only speak when you use commands with a reporting function (e.g. report the title of the window); but it will not speak in reaction to actions such as moving the focus or the cursor.
* Off: NVDA will not speak anything, however unlike sleep mode, it will silently react to commands.
* Beeps: NVDA will replace normal speech with short beeps.

The Beeps mode may be useful when some very verbose output is scrolling in a terminal window, but you don't care what it is, only that it is continuing to scroll; or in other circumstances when the fact that there is output is more relevant than the output itself.

The On-demand mode may be valuable when you don't need constant feedback about what is happening on screen or on the computer, but you periodically need to check particular things using review commands, etc.
Examples include while recording audio, when using screen magnification, during a meeting or a call, or as an alternative to beeps mode.

A gesture allows cycling through the various speech modes:
<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Cycle Speech Mode |`NVDA+s` |Cycles between speech modes.|

<!-- KC:endInclude -->

If you only need to switch between a limited subset of speech modes, see [Modes available in the Cycle speech mode command](#SpeechModesDisabling) for a way to disable unwanted modes.

## Navigating with NVDA {#NavigatingWithNVDA}

NVDA allows you to explore and navigate the system in several ways, including both normal interaction and review.

### Objects {#Objects}

Each Application and the operating system itself consist of many objects.
An object is a single item such as a piece of text, button, checkbox, slider, list or editable text field.

### Navigating with the System Focus {#SystemFocus}

The system focus, also known simply as the focus, is the [object](#Objects) which receives keys typed on the keyboard.
For example, if you are typing into an editable text field, the editable text field has the focus.

The most common way of navigating around Windows with NVDA is to simply move the system focus using standard Windows keyboard commands, such as pressing tab and shift+tab to move forward and back between controls, pressing alt to get to the menu bar and then using the arrows to navigate menus, and using alt+tab to move between running applications.
As you do this, NVDA will report information about the object with focus, such as its name, type, value, state, description, keyboard shortcut and positional information.
When [Visual Highlight](#VisionFocusHighlight) is enabled, the location of the current system focus is also exposed visually.

There are some key commands that are useful when moving with the System focus:
<!-- KC:beginInclude -->

| Name |Desktop key |Laptop key |Description|
|---|---|---|---|
|Report current focus |NVDA+tab |NVDA+tab |announces the current object or control that has the System focus. Pressing twice will spell the information|
|Report title |NVDA+t |NVDA+t |Reports the title of the currently active window. Pressing twice will spell the information. Pressing three times will copy it to the clipboard|
|Read active window |NVDA+b |NVDA+b |reads all the controls in the currently active window (useful for dialogs)|
|Report Status Bar |NVDA+end |NVDA+shift+end |Reports the Status Bar if NVDA finds one. Pressing twice will spell the information. Pressing three times will copy it to the clipboard|
|Report Shortcut Key |`shift+numpad2` |`NVDA+control+shift+.` |Reports the shortcut (accelerator) key of the currently focused object|

<!-- KC:endInclude -->

### Navigating with the System Caret {#SystemCaret}

When an [object](#Objects) that allows navigation and/or editing of text is [focused](#SystemFocus), you can move through the text using the system caret, also known as the edit cursor.

When the focus is on an object that has the system caret, you can use the arrow keys, page up, page down, home, end, etc. to move through the text.
You can also change the text if the control supports editing.
NVDA will announce as you move by character, word and line, and will also announce as you select and unselect text.

NVDA provides the following key commands in relation to the system caret:
<!-- KC:beginInclude -->

| Name |Desktop key |Laptop key |Description|
|---|---|---|---|
|Say all |NVDA+downArrow |NVDA+a |Starts reading from the current position of the system caret, moving it along as it goes|
|Read current line |NVDA+upArrow |NVDA+l |Reads the line where the system caret is currently situated. Pressing twice spells the line. Pressing three times spells the line using character descriptions.|
|Read current text selection |NVDA+Shift+upArrow |NVDA+shift+s |Reads any currently selected text|
|Report text formatting |NVDA+f |NVDA+f |Reports the formatting of the text where the caret is currently situated. Pressing twice shows the information in browse mode|
|Report link destination |`NVDA+k` |`NVDA+k` |Pressing once speaks the destination URL of the link at the current caret or focus position. Pressing twice shows it in a window for more careful review|
|Report caret location |NVDA+numpadDelete |NVDA+delete |Reports information about the location of the text or object at the position of system caret. For example, this might include the percentage through the document, the distance from the edge of the page or the exact screen position. Pressing twice may provide further detail.|
|Next sentence |alt+downArrow |alt+downArrow |Moves the caret to the next sentence and announces it. (only supported in Microsoft Word and Outlook)|
|Previous sentence |alt+upArrow |alt+upArrow |Moves the caret to the previous sentence and announces it. (only supported in Microsoft Word and Outlook)|

When within a table, the following key commands are also available:

| Name |Key |Description|
|---|---|---|
|Move to previous column |control+alt+leftArrow |Moves the system caret to the previous column (staying in the same row)|
|Move to next column |control+alt+rightArrow |Moves the system caret to the next column (staying in the same row)|
|Move to previous row |control+alt+upArrow |Moves the system caret to the previous row (staying in the same column)|
|Move to next row |control+alt+downArrow |Moves the system caret to the next row (staying in the same column)|
|Move to first column |control+alt+home |Moves the system caret to the first column (staying in the same row)|
|Move to last column |control+alt+end |Moves the system caret to the last column (staying in the same row)|
|Move to first row |control+alt+pageUp |Moves the system caret to the first row (staying in the same column)|
|Move to last row |control+alt+pageDown |Moves the system caret to the last row (staying in the same column)|
|Say all in column |`NVDA+control+alt+downArrow` |Reads the column vertically from the current cell downwards to the last cell in the column.|
|Say all in row |`NVDA+control+alt+rightArrow` |Reads the row horizontally from the current cell rightwards to the last cell in the row.|
|Read entire column |`NVDA+control+alt+upArrow` |Reads the current column vertically from top to bottom without moving the system caret.|
|Read entire row |`NVDA+control+alt+leftArrow` |Reads the current row horizontally from left to right without moving the system caret.|

<!-- KC:endInclude -->

### Object Navigation {#ObjectNavigation}

Most of the time, you will work with applications using commands which move the [focus](#SystemFocus) and the [caret](#SystemCaret).
However, sometimes, you may wish to explore the current application or the Operating System without moving the focus or caret.
You may also wish to work with [objects](#Objects) that cannot be accessed normally using the keyboard.
In these cases, you can use object navigation.

Object navigation allows you to move between and obtain information about individual [objects](#Objects).
When you move to an object, NVDA will report it similarly to the way it reports the system focus.
For a way to review all text as it appears on the screen, you can instead use [screen review](#ScreenReview).

Rather than having to move back and forth between every single object on the system, the objects are organized hierarchically.
This means that some objects contain other objects and you must move inside them to access the objects they contain.
For example, a list contains list items, so you must move inside the list in order to access its items.
If you have moved to a list item, moving next and previous will take you to other list items in the same list.
Moving to a list item's containing object will take you back to the list.
You can then move past the list if you wish to access other objects.
Similarly, a toolbar contains controls, so you must move inside the toolbar to access the controls in the toolbar.

If you yet prefer to move back and forth between every single object on the system, you can use commands to move to the previous/next object in a flattened view.
For example, if you move to the next object in this flattened view and the current object contains other objects, NVDA will automatically move to the first object that it contains.
Alternatively, if the current object doesn't contain any objects, NVDA will move to the next object at the current level of the hierarchy.
If there is no such next object, NVDA will try to find the next object in the hierarchy based on containing objects until there are no more objects to move to.
The same rules apply to moving backwards in the hierarchy.

The object currently being reviewed is called the navigator object.
Once you navigate to an object, you can review its content using the [text review commands](#ReviewingText) while in [Object review mode](#ObjectReview).
When [Visual Highlight](#VisionFocusHighlight) is enabled, the location of the current navigator object is also exposed visually.
By default, the navigator object moves along with the System focus, though this behaviour can be toggled on and off.

Note: Braille following Object Navigation can be configured via [Braille Tether](#BrailleTether).

To navigate by object, use the following commands:

<!-- KC:beginInclude -->

| Name |Desktop key |Laptop key |Touch |Description|
|---|---|---|---|---|
|Report current object |NVDA+numpad5 |NVDA+shift+o |none |Reports the current navigator object. Pressing twice spells the information, and pressing 3 times copies this object's name and value to the clipboard.|
|Move to containing object |NVDA+numpad8 |NVDA+shift+upArrow |flick up (object mode) |Moves to the object containing the current navigator object|
|Move to previous object |NVDA+numpad4 |NVDA+shift+leftArrow |none |Moves to the object before the current navigator object|
|Move to previous object in flattened view |NVDA+numpad9 |NVDA+shift+[ |flick left (object mode) |Moves to the previous object in a flattened view of the object navigation hierarchy|
|Move to next object |NVDA+numpad6 |NVDA+shift+rightArrow |none |Moves to the object after the current navigator object|
|Move to next object in flattened view |NVDA+numpad3 |NVDA+shift+] |flick right (object mode) |Moves to the next object in a flattened view of the object navigation hierarchy|
|Move to first contained object |NVDA+numpad2 |NVDA+shift+downArrow |flick down (object mode) |Moves to the first object contained by the current navigator object|
|Move to focus object |NVDA+numpadMinus |NVDA+backspace |none |Moves to the object that currently has the system focus, and also places the review cursor at the position of the System caret, if it is showing|
|Activate current navigator object |NVDA+numpadEnter |NVDA+enter |double-tap |Activates the current navigator object (similar to clicking with the mouse or pressing space when it has the system focus)|
|Move System focus or caret to current review position |NVDA+shift+numpadMinus |NVDA+shift+backspace |none |pressed once Moves the System focus to the current navigator object, pressed twice moves the system caret to the position of the review cursor|
|Report review cursor location |NVDA+shift+numpadDelete |NVDA+shift+delete |none |Reports information about the location of the text or object at the review cursor. For example, this might include the percentage through the document, the distance from the edge of the page or the exact screen position. Pressing twice may provide further detail.|
|Move review cursor to status bar |none |none |none |Reports the Status Bar if NVDA finds one. It also moves the navigator object to this location.|

<!-- KC:endInclude -->

Note: numpad keys require the Num Lock to be turned off to work properly.

### Reviewing Text {#ReviewingText}

NVDA allows you to read the contents of the [screen](#ScreenReview), current [document](#DocumentReview) or current [object](#ObjectReview) by character, word or line.
This is mostly useful in places (including Windows command consoles) where there is no [system caret](#SystemCaret).
For example, you might use it to review the text of a long information message in a dialog.

When moving the review cursor, the System caret does not follow along, so you can review text without losing your editing position.
However, by default, when the System caret moves, the review cursor follows along.
This can be toggled on and off.

Note: Braille following the review cursor can be configured via [Braille Tether](#BrailleTether).

The following commands are available for reviewing text:
<!-- KC:beginInclude -->

| Name |Desktop key |Laptop key |Touch |Description|
|---|---|---|---|---|
|Move to top line in review |shift+numpad7 |NVDA+control+home |none |Moves the review cursor to the top line of the text|
|Move to previous line in review |numpad7 |NVDA+upArrow |flick up (text mode) |Moves the review cursor to the previous line of text|
|Report current line in review |numpad8 |NVDA+shift+. |none |Announces the current line of text where the review cursor is positioned. Pressing twice spells the line. Pressing three times spells the line using character descriptions.|
|Move to next line in review |numpad9 |NVDA+downArrow |flick down (text mode) |Move the review cursor to the next line of text|
|Move to bottom line in review |shift+numpad9 |NVDA+control+end |none |Moves the review cursor to the bottom line of text|
|Move to previous word in review |numpad4 |NVDA+control+leftArrow |2-finger flick left (text mode) |Moves the review cursor to the previous word in the text|
|Report current word in review |numpad5 |NVDA+control+. |none |Announces the current word in the text where the review cursor is positioned. Pressing twice spells the word. Pressing three times spells the word using character descriptions.|
|Move to next word in review |numpad6 |NVDA+control+rightArrow |2-finger flick right (text mode) |Move the review cursor to the next word in the text|
|Move to start of line in review |shift+numpad1 |NVDA+home |none |Moves the review cursor to the start of the current line in the text|
|Move to previous character in review |numpad1 |NVDA+leftArrow |flick left (text mode) |Moves the review cursor to the previous character on the current line in the text|
|Report current character in review |numpad2 |NVDA+. |none |Announces the current character on the line of text where the review cursor is positioned. Pressing twice reports a description or example of that character. Pressing three times reports the numeric value of the character in decimal and hexadecimal.|
|Move to next character in review |numpad3 |NVDA+rightArrow |flick right (text mode) |Move the review cursor to the next character on the current line of text|
|Move to end of line in review |shift+numpad3 |NVDA+end |none |Moves the review cursor to the end of the current line of text|
|Move to previous page in review |`NVDA+pageUp` |`NVDA+shift+pageUp` |none |Moves the review cursor to the previous page of text if supported by the application|
|Move to next page in review |`NVDA+pageDown` |`NVDA+shift+pageDown` |none |Moves the review cursor to the next page of text if supported by the application|
|Say all with review |numpadPlus |NVDA+shift+a |3-finger flick down (text mode) |Reads from the current position of the review cursor, moving it as it goes|
|Select then Copy from review cursor |NVDA+f9 |NVDA+f9 |none |Starts the select then copy process from the current position of the review cursor. The actual action is not performed until you tell NVDA where the end of the text range is|
|Select then Copy to review cursor |NVDA+f10 |NVDA+f10 |none |On the first press, text is selected from the position previously set as start marker up to and including the review cursor's current position. If the system caret can reach the text, it will be moved to the selected text. After pressing this key stroke a second time, the text will be copied to the Windows clipboard|
|Move to marked start for copy in review |NVDA+shift+f9 |NVDA+shift+f9 |none |Moves the review cursor to the position previously set start marker for copy|
|Report text formatting |NVDA+shift+f |NVDA+shift+f |none |Reports the formatting of the text where the review cursor is currently situated. Pressing twice shows the information in browse mode|
|Report current symbol replacement |None |None |none |Speaks the symbol where the review cursor is positioned. Pressed twice, shows the symbol and the text used to speak it in browse mode.|

<!-- KC:endInclude -->

Note: numpad keys require the Num Lock to be turned off to work properly.

A good way to remember the basic text review commands  when using the Desktop layout  is to think of them as being in a grid of three by three, with top to bottom being line, word and character and left to right being previous, current and next.
The layout is illustrated as follows:

| . {.hideHeaderRow} |. |.|
|---|---|---|
|Previous line |Current line |Next line|
|Previous word |Current word |Next word|
|Previous character |Current character |Next character|

### Review Modes {#ReviewModes}

NVDA's [text review commands](#ReviewingText) can review content within the current navigator object, current document or screen, depending on the review mode selected.

The following commands switch between review modes:
<!-- KC:beginInclude -->

| Name |Desktop key |Laptop key |Touch |Description|
|---|---|---|---|---|
|Switch to next review mode |NVDA+numpad7 |NVDA+pageUp |2-finger flick up |switches to the next available review mode|
|Switch to previous review mode |NVDA+numpad1 |NVDA+pageDown |2-finger flick down |switches to the previous available review mode|

<!-- KC:endInclude -->

#### Object Review {#ObjectReview}

While in object review mode, you are able to only review the content of the current [navigator object](#ObjectNavigation).
For objects such as editable text fields or other basic text controls, this will generally be the text content.
For other objects, this may be the name and/or value.

#### Document Review {#DocumentReview}

When the [navigator object](#ObjectNavigation) is within a browse mode document (e.g. web page) or other complex document (e.g. a Lotus Symphony document), it is possible to switch to the document review mode.
The document review mode allows you to review the text of the entire document.

When switching from object review to document review, the review cursor is placed in the document at the position of the navigator object.
When moving around the document with review commands, the navigator object is automatically updated to the object found at the current review cursor position.

Note that NVDA will switch to document review from object review automatically when moving around browse mode documents.

#### Screen Review {#ScreenReview}

The screen review mode allows you to review the text of the screen as it appears visually within the current application.
This is similar to the screen review or mouse cursor functionality in many other Windows screen readers.

When switching to screen review mode, the review cursor is placed at the screen position of the current [navigator object](#ObjectNavigation).
When moving around the screen with review commands, the navigator object is automatically updated to the object found at the screen position of the review cursor.

Note that in some newer applications, NVDA may not see some or all text displayed on the screen due to the use of newer screen drawing technologies which are impossible to support at this time.

### Navigating with the Mouse {#NavigatingWithTheMouse}

When you move the mouse, NVDA by default reports the text that is directly under the mouse pointer as the pointer moves over it.
Where supported, NVDA will read the surrounding paragraph of text, though some controls may only read by line.

NVDA can be configured to also announce the type of [object](#Objects) under the mouse as it moves (e.g. list, button, etc.).
This may be useful for totally blind users, as sometimes, the text isn't enough.

NVDA provides a way for users to understand where the mouse is located relative to the dimensions of the screen by playing the current mouse coordinates as audio beeps.
The higher the mouse is on the screen, the higher the pitch of the beeps.
The further left or right the mouse is located on the screen, the further left or right the sound will be played (assuming the user has stereo speakers or headphones).

These extra mouse features are not turned on by default in NVDA.
If you wish to take advantage of them, you can configure them from the [Mouse settings](#MouseSettings) category of the [NVDA Settings](#NVDASettings) dialog, found in the NVDA Preferences menu.

Although a physical mouse or trackpad should be used to navigate with the mouse, NVDA provides some commands related to the mouse:
<!-- KC:beginInclude -->

| Name |Desktop key |Laptop key |Touch |Description|
|---|---|---|---|---|
|Left mouse button click |numpadDivide |NVDA+[ |none |Clicks the left mouse button once. The common double click can be performed by pressing this key twice in quick succession|
|Left mouse button lock |shift+numpadDivide |NVDA+control+[ |none |Locks the left mouse button down. Press again to release it. To drag the mouse, press this key to lock the left button down and then move the mouse either physically or use one of the other mouse routing commands|
|Right mouse click |numpadMultiply |NVDA+] |tap and hold |Clicks the right mouse button once, mostly used to open context menu at the location of the mouse.|
|Right mouse button lock |shift+numpadMultiply |NVDA+control+] |none |Locks the right mouse button down. Press again to release it. To drag the mouse, press this key to lock the right button down and then move the mouse either physically or use one of the other mouse routing commands|
|Move mouse to current navigator object |NVDA+numpadDivide |NVDA+shift+m |none |Moves the mouse to the location of the current navigator object and review cursor|
|Navigate to the object under the mouse |NVDA+numpadMultiply |NVDA+shift+n |none |Set the navigator object to the object located at the position of the mouse|

<!-- KC:endInclude -->

## Browse Mode {#BrowseMode}

Complex read-only documents such as web pages are browsed in NVDA using browse mode.
This includes documents in the following applications:

* Mozilla Firefox
* Microsoft Internet Explorer
* Mozilla Thunderbird
* HTML messages in Microsoft Outlook
* Google Chrome
* Microsoft Edge
* Adobe Reader
* Foxit Reader
* Supported books in Amazon Kindle for PC

Browse mode is also optionally available for Microsoft Word documents.

In browse mode, the content of the document is made available in a flat representation that can be navigated with the cursor keys as if it were a normal text document.
All of NVDA's [system caret](#SystemCaret) key commands will work in this mode; e.g. say all, report formatting, table navigation commands, etc.
When [Visual Highlight](#VisionFocusHighlight) is enabled, the location of the virtual browse mode caret is also exposed visually.
Information such as whether text is a link, heading, etc. is reported along with the text as you move.

Sometimes, you will need to interact directly with controls in these documents.
For example, you will need to do this for editable text fields and lists so that you can type characters and use the cursor keys to work with the control.
You do this by switching to focus mode, where almost all keys are passed to the control.
When in Browse mode, by default, NVDA will automatically switch to focus mode if you tab to or click on a particular control that requires it.
Conversely, tabbing to or clicking on a control that does not require focus mode will switch back to browse mode.
You can also press enter or space to switch to focus mode on controls that require it.
Pressing escape will switch back to browse mode.
In addition, you can manually force focus mode, after which it will remain in effect until you choose to disable it.

<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Toggle browse/focus modes |NVDA+space |Toggles between focus mode and browse mode|
|Exit focus mode |escape |Switches back to browse mode if focus mode was previously switched to automatically|
|Refresh browse mode document |NVDA+f5 |Reloads the current document content (useful if certain content seems to be missing from the document. Not available in Microsoft Word and Outlook.)|
|Find |NVDA+control+f |Pops up a dialog in which you can type some text to find in the current document. See [searching for text](#SearchingForText) for more information.|
|Find next |NVDA+f3 |Finds the next occurrence of the text in the document that you previously searched for|
|Find previous |NVDA+shift+f3 |Finds the previous occurrence of the text in the document you previously searched for|

<!-- KC:endInclude -->

### Single Letter Navigation {#SingleLetterNavigation}

While in browse mode, for quicker navigation, NVDA also provides single character keys to jump to certain fields in the document.
Note that not all of these commands are supported in every type of document.

<!-- KC:beginInclude -->
The following keys by themselves jump to the next available element, while adding the shift key causes them to jump to the previous element:

* h: heading
* l: list
* i: list item
* t: table
* k: link
* n: nonLinked text
* f: form field
* u: unvisited link
* v: visited link
* e: edit field
* b: button
* x: checkbox
* c: combo box
* r: radio button
* q: block quote
* s: separator
* m: frame
* g: graphic
* d: landmark
* o: embedded object (audio and video player, application, dialog, etc.)
* 1 to 6: headings at levels 1 to 6 respectively
* a: annotation (comment, editor revision, etc.)
* `p`: text paragraph
* w: spelling error

To move to the beginning or end of containing elements such as lists and tables:

| Name |Key |Description|
|---|---|---|
|Move to start of container |shift+comma |Moves to the start of the container (list, table, etc.) where the caret is positioned|
|Move past end of container |comma |Moves past the end of the container (list, table, etc.) where the caret is positioned|

<!-- KC:endInclude -->

Some web applications such as Gmail, Twitter and Facebook use single letters as shortcut keys.
If you want to use these while still being able to use your cursor keys to read in browse mode, you can temporarily disable NVDA's single letter navigation keys.
<!-- KC:beginInclude -->
To toggle single letter navigation on and off for the current document, press NVDA+shift+space.
<!-- KC:endInclude -->

#### Text paragraph navigation command {#TextNavigationCommand}

You can jump to the next or previous text paragraph by pressing `p` or `shift+p`.
Text paragraphs are defined by a group of text that appears to be written in complete sentences.
This can be useful to find the beginning of readable content on various webpages, such as:

* News websites
* Forums
* Blog posts

These commands can also be helpful for skipping certain kinds of clutter, such as:

* Ads
* Menus
* Headers

Please note, however, that while NVDA tries its best to identify text paragraphs, the algorithm is not perfect and at times can make mistakes.
Additionally, this command is different from paragraph navigation commands `control+downArrow/upArrow`.
Text paragraph navigation only jumps between text paragraphs, while paragraph navigation commands take the cursor to the previous/next paragraphs regardless of whether they contain text or not.

#### Other navigation commands {#OtherNavigationCommands}

In addition to the quick navigation commands listed above, NVDA has commands that have no default keys assigned.
To use these commands, you first need to assign gestures to them using the [Input Gestures dialog](#InputGestures).
Here is a list of available commands:

* Article
* Figure
* Grouping
* Tab
* Menu item
* Toggle button
* Progress bar
* Math formula
* Vertically aligned paragraph
* Same style text
* Different style text

Keep in mind that there are two commands for each type of element, for moving forward in the document and backward in the document, and you must assign gestures to both commands in order to be able to quickly navigate in both directions.
For example, if you want to use the `y` / `shift+y` keys to quickly navigate through tabs, you would do the following:

1. Open input gestures dialog from browse mode.
1. Find "moves to the next tab" item in the Browse mode section.
1. Assign `y` key for found gesture.
1. Find "moves to the previous tab" item.
1. Assign `shift+y` for found gesture.

### The Elements List {#ElementsList}

The elements list provides access to a list of various types of elements in the document as appropriate for the application.
For example, in web browsers, the elements list can list links, headings, form fields, buttons or landmarks.
Radio buttons allow you to switch between the different types of elements.
An edit field is also provided in the dialog which allows you to filter the list to help you search for a particular item on the page.
Once you have chosen an item, you can use the provided buttons in the dialog to move to or activate that item.
<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Browse mode elements list |NVDA+f7 |Lists various types of elements in the current document|

<!-- KC:endInclude -->

### Searching for text {#SearchingForText}

This dialog allows you to search for terms in the current document.
In the "Type the text you wish to find" field, the text to be found can be entered.
The "Case sensitive" checkbox makes the search consider uppercase and lowercase letters differently.
For example, with "Case sensitive" selected you can find "NV Access" but not "nv access".
Use the following keys for performing searches:
<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Find text |NVDA+control+f |Opens the  search dialog|
|Find next |NVDA+f3 |searches the next occurrence of the current search term|
|Find previous |NVDA+shift+f3 |searches the previous  occurrence of the current search term|

<!-- KC:endInclude -->

### Embedded Objects {#ImbeddedObjects}

Pages can include rich content using technologies such as Oracle Java and HTML5, as well as applications and dialogs.
Where these are encountered in browse mode, NVDA will report "embedded object", "application" or "dialog", respectively.
You can quickly move to them using the o and shift+o embedded object single letter navigation keys.
To interact with these objects, you can press enter on them.
If it is accessible, you can then tab around it and interact with it like any other application.
A key command is provided to return to the original page containing the embedded object:
<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Move to containing browse mode document |NVDA+control+space |Moves the focus out of the current embedded object and into the document that contains it|

<!-- KC:endInclude -->

### Native Selection Mode {#NativeSelectionMode}

By default when selecting text with the `shift+arrow` keys in Browse Mode, a selection is only made within NVDA's Browse Mode representation of the document, and not within the application itself.
This means that the selection is not visible on screen, and copying text with `control+c` will only copy NVDA's plain text representation of the content. i.e. formatting of tables, or whether something is a link will not be copied.
However, NVDA has a Native Selection Mode which can be turned on in particular Browse Mode documents (so far only Mozilla Firefox) which causes the document's native selection to follow NVDA's Browse Mode selection.

<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Toggle Native Selection Mode on and off |`NVDA+shift+f10` |Toggles native selection mode on and off|

<!-- KC:endInclude -->

When Native Selection Mode is turned on, copying the selection with `control+c` will also use the application's own copy functionality, meaning that rich content will be copied to the clipboard, rather than plain text.
This means that pasting this content into a program such as Microsoft Word or Excel, formatting such as tables, or whether something is a link will be included.
Please note however that in native selection mode, some accessible labels or other information that NVDA generates in Browse Mode will not be included.
Also, although the application will try its best to match the native selection to NVDA's Browse Mode selection, it may not always be completely accurate.
However, for scenarios where you wish to copy an entire table or paragraph of rich content, this feature should prove useful.

## Reading Mathematical Content {#ReadingMath}

NVDA can read and navigate mathematical content on the web and in other applications, providing access in both speech and braille.
However, in order for NVDA to read and interact with mathematical content, you will first need to install a Math component for NvDA.
There are several NVDA add-ons available in the NVDA Add-on Store that provide support for math, including the [MathCAT NVDA add-on](https://nsoiffer.github.io/MathCAT/) and [Access8Math](https://github.com/tsengwoody/Access8Math).
Please refer to the [Add-on Store section](#AddonsManager) to learn how to browse and install available add-ons in NVDA.
NVDA also can make use of the older [MathPlayer](https://info.wiris.com/mathplayer-info) software from Wiris if found on your system, though this software is no longer maintained.

### Supported math content {#SupportedMathContent}

With an appropriate math component installed, NVDA supports the following types of mathematical content:

* MathML in Mozilla Firefox, Microsoft Internet Explorer and Google Chrome.
* Microsoft Word 365 Modern Math Equations via UI automation:
NVDA is able to read and interact with math equations in Microsoft Word 365/2016 build 14326 and higher.
Note however that any previously created MathType equations must be first converted to Office Math.
This can be done by selecting each and choosing "Equation Options", then "Convert to Office Math" in the context menu.
Ensure your version of MathType is the latest version before doing this.
Microsoft Word provides linear symbol-based navigation through the equations itself and supports inputting math using several syntaxes, including LateX.
For further details, please see [Linear format equations using UnicodeMath and LaTeX in Word](https://support.microsoft.com/en-us/office/linear-format-equations-using-unicodemath-and-latex-in-word-2e00618d-b1fd-49d8-8cb4-8d17f25754f8)
* Microsoft Powerpoint, and older versions of Microsoft Word:
NVDA can read and navigate MathType equations in both Microsoft Powerpoint and Microsoft word.
MathType needs to be installed in order for this to work.
The trial version is sufficient.
It can be downloaded from the [MathType presentation page](https://www.wiris.com/en/mathtype/).
* Adobe Reader:
Note that this is not an official standard yet, so there is currently no publicly available software that can produce this content.
* Kindle Reader for PC:
NVDA can read and navigate Math in Kindle for PC for books with accessible math.

When reading a document, NVDA will speak any supported mathematical content where it occurs.
If you are using a braille display, it will also be displayed in braille.

### Interactive Navigation {#InteractiveNavigation}

If you are working primarily with speech, in most cases, you will probably wish to examine the expression in smaller segments, rather than hearing the entire expression at once.

If you are in browse mode, you can do this by moving the cursor to the mathematical content and pressing enter.

If you are not in browse mode:

1. move the review cursor to the mathematical content.
By default, the review cursor follows the system caret, so you can usually use the system caret to move to the desired content.
1. Then, activate the following command:

<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Interact with math content |NVDA+alt+m |Begins interaction with math content.|

<!-- KC:endInclude -->

At this point, NVDA will enter Math mode, where you can use commands such as the arrow keys to explore the expression.
For example, you can move through the expression with the left and right arrow keys and zoom into a portion of the expression such as a fraction using the down arrow key.

When you wish to return to the document, simply press the escape key.

For more information on available commands and preferences for reading and navigating within math content, please refer to the documentation for your particular math component you have installed.

* [MathCAT documentation](https://nsoiffer.github.io/MathCAT/users.html)
* [Access8Math documentation](https://github.com/tsengwoody/Access8Math)
* [MathPlayer documentation](https://docs.wiris.com/mathplayer/en/mathplayer-user-manual.html)

Sometimes mathematical content might be displayed as a button or other type of element which, when activated, can display a dialog or more information related to the formula.
To activate the button or the element containing the formula, press ctrl+enter.

### Installing MathPlayer {#InstallingMathPlayer}

Although it is generally recommended to use one of the newer NVDA add-ons to support math in NVDA, in certain limited scenarios MathPlayer may still be a more suitable choice.
E.g. MathPlayer may support a particular language or Braille code that is unsupported in newer add-ons.
MathPlayer is available for free from the Wiris website.
[Download MathPlayer](https://downloads.wiris.com/mathplayer/MathPlayerSetup.exe).
After installing MathPlayer, you will need to restart NVDA.
Please note that information about MathPlayer may state that it is only for older browsers such as Internet Explorer 8.
This is only referring to using MathPlayer to display mathematical content visually, and can be ignored by those using it to read or navigate math with NVDA.

## Braille {#Braille}

If you own a braille display, NVDA can display information in braille.
If your braille display has a Perkins-style keyboard, you can also enter contracted or uncontracted braille.
Braille can also be displayed on screen using the [Braille Viewer](#BrailleViewer) instead of, or at the same time as, using a physical braille display.

Please see the [Supported Braille Displays](#SupportedBrailleDisplays) section for information about the supported braille displays.
This section also contains information about what displays support NVDA's automatic background braille display detection functionality.
You can configure braille using the [Braille category](#BrailleSettings) of the [NVDA Settings](#NVDASettings) dialog.

### Control Type, State and Landmark abbreviations {#BrailleAbbreviations}

In order to fit as much information as possible on a braille display, the following abbreviations have been defined to indicate control type and state as well as landmarks.

| Abbreviation |Control type|
|---|---|
|app |application|
|art |article|
|bqt |block quote|
|btn |button|
|drbtn |drop down button|
|spnbtn |spin button|
|splbtn |split button|
|tgbtn |toggle button|
|cap |caption|
|cbo |combo box|
|chk |checkbox|
|dlg |dialog|
|doc |document|
|edt |editable text field|
|pwdedt |password edit|
|embedded |embedded object|
|enote |end note|
|fig |figure|
|fnote |foot note|
|gra |graphic|
|grp |grouping|
|hN |heading at level n, e.g. h1, h2.|
|hlp |help balloon|
|lmk |landmark|
|lnk |link|
|vlnk |visited link|
|lst |list|
|mnu |menu|
|mnubar |menu bar|
|mnubtn |menu button|
|mnuitem |menu item|
|pnl |panel|
|prgbar |progress bar|
|bsyind |busy indicator|
|rbtn |radio button|
|scrlbar |scroll bar|
|sect |section|
|stbar |status bar|
|tabctl |tab control|
|tbl |table|
|cN |table column number n, e.g. c1, c2.|
|rN |table row number n, e.g. r1, r2.|
|term |terminal|
|tlbar |tool bar|
|tltip |tool tip|
|tv |tree view|
|tvbtn |tree view button|
|tvitem |tree view item|
|lv N |a tree view item has a hierarchical level N|
|wnd |window|
|⠤⠤⠤⠤⠤ |separator|
|mrkd |marked content|

The following state indicators are also defined:

| Abbreviation |Control state|
|---|---|
|... |displayed when an object supports autocompletion|
|⢎⣿⡱ |displayed when an object (e.g. a toggle button) is pressed|
|⢎⣀⡱ |displayed when an object (e.g. a toggle button) is not pressed|
|⣏⣿⣹ |displayed when an object (e.g. a checkbox) is checked|
|⣏⣸⣹ |displayed when an object (e.g. a checkbox) is half checked|
|⣏⣀⣹ |displayed when an object (e.g. a checkbox) is not checked|
|- |displayed when an object (e.g. a tree view item) is collapsible|
|+ |displayed when an object (e.g. a tree view item) is Expandable|
|*** |displayed when a protected control or document is encountered|
|clk |displayed when an object is clickable|
|cmnt |displayed when there is a comment for a spreadsheet cell or piece of text in a document|
|frml |displayed when there is a formula on a spreadsheet cell|
|invalid |displayed when an invalid entry has been made|
|ldesc |displayed when an object (usually a graphic) has a long description|
|mln |displayed when an edit field allows typing multiple lines of text such as comment fields on websites|
|req |displayed when a required form field is encountered|
|ro |displayed when an object (e.g. an editable text field) is read-only|
|sel |displayed when an object is selected|
|nsel |displayed when an object is not selected|
|sorted asc |displayed when an object is sorted ascending|
|sorted desc |displayed when an object is sorted descending|
|submnu |displayed when an object has a popup (usually a sub-menu)|

Finally, the following abbreviations for landmarks are defined:

| Abbreviation |Landmark|
|---|---|
|bnnr |banner|
|cinf |content info|
|cmpl |complementary|
|form |form|
|main |main|
|navi |navigation|
|srch |search|
|rgn |region|

### Braille Input {#BrailleInput}

NVDA supports entry of both uncontracted and contracted braille via a braille keyboard.
You can select the translation table used to translate braille into text using the [Input table](#BrailleSettingsInputTable) setting in the Braille category of the [NVDA Settings](#NVDASettings) dialog.

When uncontracted braille is being used, text is inserted as soon as it is entered.
When using contracted braille, text is inserted when you press space or enter at the end of a word.
Note that translation can only reflect the braille word you are typing and cannot consider existing text.
For example, if you are using a braille code that begins numbers with a number sign and you press backspace to move to the end of a number, you will need to type the number sign again to enter additional numbers.

<!-- KC:beginInclude -->
Pressing dot 7 erases the last entered braille cell or character.
Dot 8 translates any braille input and presses the enter key.
Pressing dot 7 + dot 8 translates any braille input, but without adding a space or pressing enter.
<!-- KC:endInclude -->

#### Inputting keyboard shortcuts {#BrailleKeyboardShortcuts}

NVDA supports inputting keyboard shortcuts and emulating keypresses using the braille display.
This emulation comes in two forms: assigning a Braille input directly to some key press and using the virtual modifier keys.

Commonly-used keys, such as the arrow keys or pressing Alt to reach menus, can be mapped directly to Braille inputs.
The driver for each Braille display comes pre-equipped with some of these assignments.
You can change these assignments or add new emulated keys from the [Input Gestures dialog](#InputGestures).

While this approach is useful for commonly-pressed or unique keys (such as Tab), you may not want to assign a unique set of keys to each keyboard shortcut.
To allow emulating keypresses where modifier keys are held down, NVDA provides commands to toggle the control, alt, shift, windows, and NVDA keys, along with commands for some combinations of those keys.
To use these toggles, first press the command (or sequence of commands) for the modifier keys you want pressed.
Then input the character that's part of the keyboard shortcut you want to input.
For example, to produce control+f, use the "Toggle control key" command and then type an f,
and to input control+alt+t, use either the "Toggle control key" and "Toggle alt key" commands, in either order, or the "Toggle control and alt keys" command, followed by typing a t.

If you accidentally toggle modifier keys, running the toggle command again will remove the modifier.

When typing in contracted Braille, using the modifier toggle keys will cause your input to be translated just as if you had pressed dots 7+8.
In addition, the emulated keypress cannot reflect Braille typed before the modifier key was pressed.
This means that, to type alt+2 with a Braille code that uses a number sign, you must first toggle Alt and then type a number sign.

## Vision {#Vision}

While NVDA is primarily aimed at blind or vision impaired people who primarily use speech and/or braille to operate a computer, it also provides built-in facilities to change the contents of the screen.
Within NVDA, such a visual aid is called a vision enhancement provider.

NVDA offers several built-in vision enhancement providers which are described below.
Additional vision enhancement providers can be provided in [NVDA add-ons](#AddonsManager).

NVDA's vision settings can be changed in the [vision category](#VisionSettings) of the [NVDA Settings](#NVDASettings) dialog.

### Visual Highlight {#VisionFocusHighlight}

Visual Highlight can help to identify the [system focus](#SystemFocus), [navigator object](#ObjectNavigation) and [browse mode](#BrowseMode) positions.
These positions are highlighted with a coloured rectangle outline.

* Solid blue highlights a combined navigator object and system focus location (e.g. because [the navigator object follows the system focus](#ReviewCursorFollowFocus)).
* Dashed blue highlights just the system focus object.
* Solid pink highlights just the navigator object.
* Solid yellow highlights the virtual caret used in browse mode (where there is no physical caret such as in web browsers).

When Visual Highlight is enabled in the [vision category](#VisionSettings) of the [NVDA Settings](#NVDASettings) dialog, you can [change whether or not to highlight the focus, navigator object or browse mode caret](#VisionSettingsFocusHighlight).

### Screen Curtain {#VisionScreenCurtain}

As a blind or vision impaired user, it is often not possible or necessary to see the contents of the screen.
Furthermore, it might be hard to ensure that there isn't someone looking over your shoulder.
For this situation, NVDA contains a feature called "Screen Curtain" which can be enabled to make the screen black.

You can enable the Screen Curtain in the [vision category](#VisionSettings) of the [NVDA Settings](#NVDASettings) dialog.

<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Toggles the state of the screen curtain |`NVDA+control+escape` |Enable to make the screen black or disable to show the contents of the screen. Pressed once, screen curtain is enabled until you restart NVDA. Pressed twice, screen curtain is enabled until you disable it.|

<!-- KC:endInclude -->

When the Screen Curtain is active some tasks directly based on what appears on the screen such as performing [OCR](#Win10Ocr) or taking a screenshot cannot be achieved.

Due to a change in the Windows Magnification API, Screen Curtain had to be updated to support the newest versions of Windows.
Use NVDA 2021.2 to activate Screen Curtain with Windows 10 21H2 (10.0.19044) or later.
For security purposes, when using a new version of Windows, get visual confirmation that the Screen Curtain makes the screen entirely black.

Please note that while Windows Magnifier is running and inverted screen colors are being used, the screen curtain cannot be enabled.

## Content Recognition {#ContentRecognition}

When authors don't provide sufficient information for a screen reader user to determine the content of something, various tools can be used to attempt to recognize the content from an image.
NVDA supports the optical character recognition (OCR) functionality built into Windows 10 and later to recognize text from images.
Additional content recognizers can be provided in NVDA add-ons.

When you use a content recognition command, NVDA recognizes content from the current [navigator object](#ObjectNavigation).
By default, the navigator object follows the system focus or browse mode cursor, so you can usually just move the focus or browse mode cursor where desired.
For example, if you move the browse mode cursor to a graphic, recognition will recognize content from the graphic by default.
However, you may wish to use object navigation directly to, for example, recognize the content of an entire application window.

Once recognition is complete, the result will be presented in a document similar to browse mode, allowing you to read the information with cursor keys, etc.
Pressing enter or space will activate (normally click) the text at the cursor if possible.
Pressing escape dismisses the recognition result.

### Windows OCR {#Win10Ocr}

Windows 10 and later includes OCR for many languages.
NVDA can use this to recognize text from images or inaccessible applications.

You can set the language to use for text recognition in the [Windows OCR category](#Win10OcrSettings) of the [NVDA Settings](#NVDASettings) dialog.
Additional languages can be installed by opening the Start menu, choosing Settings, selecting Time & Language -> Region & Language and then choosing Add a language.

When you want to monitor constantly changing content, such as when watching a video with subtitles, you can optionally enable automatic refresh of the recognized content.
This can also be done in the [Windows OCR category](#Win10OcrSettings) of the [NVDA Settings](#NVDASettings) dialog.

Windows OCR may be partially or fully incompatible with [NVDA vision enhancements](#Vision) or other external visual aids. You will need to disable these aids before proceeding to a recognition.

<!-- KC:beginInclude -->
To recognize the text in the current navigator object using Windows OCR, press NVDA+r.
<!-- KC:endInclude -->

## Application Specific Features {#ApplicationSpecificFeatures}

NVDA provides its own extra features  for some applications to make certain tasks easier or to provide access to functionality which is not otherwise accessible to screen reader users.

### Microsoft Word {#MicrosoftWord}
#### Automatic Column and Row Header Reading {#WordAutomaticColumnAndRowHeaderReading}

NVDA is able to automatically announce appropriate row and column headers when navigating around tables in Microsoft Word.
This requires that the Report Table row / column headers option in NVDA's Document Formatting settings, found in the [NVDA Settings](#NVDASettings) dialog, be turned on.

If you use [UIA to access Word documents](#MSWordUIA), which is default in recent versions of Word and Windows, the cells of the first row will automatically be considered as column headers; similarly, the cells of the first column will automatically be considered as row headers.

On the contrary, if you do not use [UIA to access Word documents](#MSWordUIA), you will have to indicate to NVDA which row or column contains the headers in any given table.
After moving to the first cell in the column or row containing the headers, use one of the following commands:
<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Set column headers |NVDA+shift+c |Pressing this once tells NVDA this is the first header cell in the row that contains column headers, which should be automatically announced when moving between columns below this row. Pressing twice will clear the setting.|
|Set row headers |NVDA+shift+r |Pressing this once tells NVDA this is the first header cell in the column that contains row headers, which should be automatically announced when moving between rows after  this column. Pressing twice will clear the setting.|

<!-- KC:endInclude -->
These settings will be stored in the document as bookmarks compatible with other screen readers such as JAWS.
This means that users of other screen readers who open this document at a later date will automatically  have the row and column headers already set.

#### Browse Mode in Microsoft Word {#BrowseModeInMicrosoftWord}

Similar to the web, Browse mode can be used in Microsoft Word to allow you to use features such as Quick navigation and the Elements List.
<!-- KC:beginInclude -->
To toggle Browse mode on and off in Microsoft Word, press NVDA+space.
<!-- KC:endInclude -->
For further information about Browse mode and Quick Navigation, see the [Browse Mode section](#BrowseMode).

##### The Elements List {#WordElementsList}

<!-- KC:beginInclude -->
While in Browse mode in Microsoft Word, you can access the Elements List by pressing NVDA+f7.
<!-- KC:endInclude -->
The Elements List can list headings, links, annotations (which includes comments and track changes) and errors (currently limited to spelling errors).

#### Reporting Comments {#WordReportingComments}

<!-- KC:beginInclude -->
To report any comments at the current caret position, press NVDA+alt+c.
<!-- KC:endInclude -->
All comments for the document, along with other tracked changes, can also be listed in the NVDA Elements List  when selecting Annotations as the type.

### Microsoft Excel {#MicrosoftExcel}
#### Automatic Column and Row Header Reading {#ExcelAutomaticColumnAndRowHeaderReading}

NVDA is able to automatically announce appropriate row and column headers when navigating around Excel worksheets.
This firstly requires that the Report Table row / column headers option in NVDA's Document Formatting settings, found in the [NVDA Settings](#NVDASettings) dialog, be turned on.
Secondly, NVDA needs to know which row or column contains the headers.
After moving to the first cell in the column or row containing the headers, use one of the following commands:
<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Set column headers |NVDA+shift+c |Pressing this once tells NVDA this is the first header cell in the row that contains column headers, which should be automatically announced when moving between columns below this row. Pressing twice will clear the setting.|
|Set row headers |NVDA+shift+r |Pressing this once tells NVDA this is the first header cell in the column that contains row headers, which should be automatically announced when moving between rows after  this column. Pressing twice will clear the setting.|

<!-- KC:endInclude -->
These settings will be stored in the workbook as defined name ranges compatible with other screen readers such as JAWS.
This means that users of other screen readers who open this workbook at a later date will automatically  have the row and column headers already set.

#### The Elements List {#ExcelElementsList}

Similar to the web, NVDA has an Elements List for Microsoft Excel that allows you to list and access several different types of information.
<!-- KC:beginInclude -->
To access the Elements List in Excel, press NVDA+f7.
<!-- KC:endInclude -->
The various types of information available in the Elements List are:

* Charts: This lists all charts in the active worksheet.
Selecting a chart and pressing enter or the Move to button focuses the chart for navigating and reading with the arrow keys.
* Comments: This lists all cells in the active worksheet containing comments.
The cell address along with its comments are shown for each cell.
Pressing enter or the Move To button when on a listed comment will move directly to that cell.
* Formulas: This lists all cells in the worksheet containing a formula.
The cell address along with its formula are shown for each cell.
Pressing enter or the Move To button on a listed formula will move directly to that cell.
* Sheets: This lists all sheets in the workbook.
Pressing f2 when on a listed sheet allows you to rename the sheet.
Pressing enter or the Move To button while on the listed sheet will switch to that sheet.
* Form fields: This lists all form fields in the active worksheet.
For each form field, the Elements List shows the alternative text of the field along with the addresses of the cells it covers.
Selecting a form field and pressing enter or the Move to button moves to that field in browse mode.

#### Reporting Notes {#ExcelReportingComments}

<!-- KC:beginInclude -->
To report any notes for the currently focused cell, press NVDA+alt+c.
In Microsoft 2016, 365 and newer, the classic comments in Microsoft Excel have been renamed to "notes".
<!-- KC:endInclude -->
All notes for the worksheet can also be listed in the NVDA Elements List after pressing NVDA+f7.

NVDA can also display a specific dialog for adding or editing a certain note.
NVDA overrides the native MS Excel notes editing region due to accessibility constraints, but the key stroke for displaying the dialog is inherited from MS Excel and therefore works also without NVDA running.
<!-- KC:beginInclude -->
To add or edit a certain note, in a focused cell, press shift+f2.
<!-- KC:endInclude -->

This key stroke does not appear and cannot be changed in NVDA's input gesture dialog.

Note: it is possible to open the note editing region in MS Excel also from the context menu of any cell of the work sheet.
However, this will open the inaccessible note editing region and not the NVDA specific note editing dialog.

In Microsoft Office 2016, 365 and newer, a new style comment dialog has been added.
This dialog is accessible and provides more features such as replying to comments, etc.
It can also be opened from the context menu of a certain cell.
The comments added to the cells via the new style comment dialog are not related to "notes".

#### Reading Protected Cells {#ExcelReadingProtectedCells}

If a workbook has been protected, it may not be possible to move focus to particular cells that have been locked for editing.
<!-- KC:beginInclude -->
To allow moving to locked cells, switch to Browse Mode by pressing NVDA+space, and then use standard Excel movement commands such as the arrow keys to move around all cells on the current worksheet.
<!-- KC:endInclude -->

#### Form Fields {#ExcelFormFields}

Excel worksheets can include form fields.
You can access these using the Elements List or the f and shift+f form field single letter navigation keys.
Once you move to a form field in browse mode, you can press enter or space to either activate it or switch to focus mode so you can interact with it, depending on the control.
For further information about Browse mode and single letter navigation, see the [Browse Mode section](#BrowseMode).

### Microsoft PowerPoint {#MicrosoftPowerPoint}

<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Toggle speaker notes reading |control+shift+s |When in a running slide show, this command will toggle between the speaker notes for the slide and the content for the slide. This only affects what NVDA reads, not what is displayed on screen.|

<!-- KC:endInclude -->

### foobar2000 {#Foobar2000}

<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Report remaining time |control+shift+r |Reports the remaining time of the currently playing track, if any.|
|Report elapsed time |control+shift+e |Reports the elapsed time of the currently playing track, if any.|
|Report track length |control+shift+t |Reports the length of the currently playing track, if any.|

<!-- KC:endInclude -->

Note: The above shortcuts work only with the default formatting string for foobar's status line.

### Miranda IM {#MirandaIM}

<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Report recent message |NVDA+control+1-4 |Reports one of the recent messages, depending on the number pressed; e.g. NVDA+control+2 reads the second most recent message.|

<!-- KC:endInclude -->

### Poedit {#Poedit}

NVDA offers enhanced support for Poedit 3.4 or newer.

<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Report notes for translators |`control+shift+a` |Reports any notes for translators. If pressed twice, presents the notes in browse mode|
|Report Comment |`control+shift+c` |Reports any comment in the comments window. If pressed twice, presents the comment in browse mode|
|Report Old Source Text |`control+shift+o` |Reports the old source text, if any. If pressed twice, presents the text in browse mode|
|Report Translation Warning |`control+shift+w` |Reports a translation warning, if any. If pressed twice, presents the warning in browse mode|

<!-- KC:endInclude -->

### Kindle for PC {#Kindle}

NVDA supports reading and navigating books in Amazon Kindle for PC.
This functionality is only available in Kindle books designated with "Screen Reader: Supported" which you can check on the details page for the book.

Browse mode is used to read books.
It is enabled automatically when you open a book or focus the book area.
The page will be turned automatically as appropriate when you move the cursor or use the say all command.
<!-- KC:beginInclude -->
You can manually turn to the next page with the pageDown key and turn to the previous page with the pageUp key.
<!-- KC:endInclude -->

Single letter navigation is supported for links and graphics, but only within the current page.
Navigating by link also includes footnotes.

NVDA provides early support for reading and interactive navigation of mathematical content for books with accessible math.
Please see the [Reading Mathematical Content](#ReadingMath) section for further information.

#### Text Selection {#KindleTextSelection}

Kindle allows you to perform various functions on selected text, including obtaining a dictionary definition, adding notes and highlights, copying the text to the clipboard and searching the web.
To do this, first select text as you normally would in browse mode; e.g. by using shift and the cursor keys.
<!-- KC:beginInclude -->
Once you have selected text, press the applications key or shift+f10 to show the available options for working with the selection.
<!-- KC:endInclude -->
If you do this with no text selected, options will be shown for the word at the cursor.

#### User Notes {#KindleUserNotes}

You can add a note regarding a word or passage of text.
To do this, first select the relevant text and access the selection options as described above.
Then, choose Add Note.

When reading in browse mode, NVDA refers to these notes as comments.

To view, edit or delete a note:

1. Move the cursor to the text containing the note.
1. Access the options for the selection as described above.
1. Choose Edit Note.

### Azardi {#Azardi}

<!-- KC:beginInclude -->
When in the table view of added books:

| Name |Key |Description|
|---|---|---|
|Enter |enter |Opens the selected book.|
|Context menu |applications |Opens the context menu for the selected book.|

<!-- KC:endInclude -->

### Windows Console {#WinConsole}

NVDA provides support for the Windows command console used by Command Prompt, PowerShell, and the Windows Subsystem for Linux.
The console window is of fixed size, typically much smaller than the buffer that holds the output.
As new text is written, the content scroll upwards and previous text is no longer visible.
On Windows versions before Windows 11 22H2, text in the console that is not visibly displayed in the window is not accessible with NVDA's text review commands.
Therefore, it is necessary to scroll the console window to read earlier text.
In newer versions of the console and in Windows Terminal, it is possible to review the entire text buffer freely without the need to scroll the window.
<!-- KC:beginInclude -->
The following built-in Windows Console keyboard shortcuts may be useful when [reviewing text](#ReviewingText) with NVDA in older versions of Windows Console:

| Name |Key |Description|
|---|---|---|
|Scroll up |control+upArrow |Scrolls the console window up, so earlier text can be read.|
|Scroll down |control+downArrow |Scrolls the console window down, so later text can be read.|
|Scroll to start |control+home |Scrolls the console window to the beginning of the buffer.|
|Scroll to end |control+end |Scrolls the console window to the end of the buffer.|

<!-- KC:endInclude -->

## Configuring NVDA {#ConfiguringNVDA}

Most configuration can be performed using dialog boxes accessed through the Preferences sub-menu of the NVDA menu.
Many of these settings can be found in the multi-page [NVDA Settings dialog](#NVDASettings).
In all dialog boxes, press the OK button to accept any changes you have made.
To cancel any changes, press the Cancel button or the escape key.
For certain dialogs, you can press the Apply button to let the settings take effect immediately without closing the dialog.
Most NVDA dialogs support context help.
<!-- KC:beginInclude -->
When in a dialog, pressing `f1` opens the User Guide at the paragraph related to the focused setting or the current dialog.
<!-- KC:endInclude -->
Some settings can also be changed using shortcut keys, which are listed where relevant in the sections below.

### NVDA Settings {#NVDASettings}

<!-- KC:settingsSection: || Name | Desktop key | Laptop key | Description | -->
NVDA provides many configuration parameters that can be changed using the settings dialog.
To make it easier to find the kind of settings you want to change, the dialog displays a list of configuration categories to choose from.
When you select a category, all of the settings related to it will be shown in the dialog.
To move between categories, use `tab` or `shift+tab` to reach the list of categories, and then use the up and down arrow keys to navigate the list.
From anywhere in the dialog, you may also move forward one category by pressing `ctrl+tab`, or back one category by pressing `shift+ctrl+tab`.

Once you change one or more settings, the settings can be applied using the apply button, in which case the dialog will stay open, allowing you to change more settings or choose another category.
If you want to save your settings and close the NVDA Settings dialog, you can use the OK button.

Some settings categories have dedicated shortcut keys.
If pressed, the shortcut key will open the NVDA Settings dialog directly to that particular category.
By default, not all categories can be accessed with keyboard commands.
If you frequently access categories that do not have dedicated shortcut keys, you may wish to use the [Input Gestures dialog](#InputGestures) to add a custom gesture such as a keyboard command or touch gesture for that category.

The settings categories found in the NVDA Settings dialog will be outlined below.

#### General {#GeneralSettings}

<!-- KC:setting -->

##### Open General settings {#OpenGeneralSettings}

Key: `NVDA+control+g`

The General category of the NVDA Settings dialog sets NVDA's overall behaviour such as interface language and whether or not it should check for updates.
This category contains the following options:

##### Language {#GeneralSettingsLanguage}

This is a combo box which allows you to select the language that NVDA's user interface and messages should be shown in.
There are many languages, however the default option is "User Default, Windows".
This option tells NVDA to use the language that Windows is currently set to.

Please note that NVDA must be restarted when changing the language.
When the confirmation dialog appears, select "restart now" or "restart later" if you wish to use the new language now or at a later time, respectively. If "restart later" is selected, the configuration must be saved (either manually or using the save on exit functionality).

##### Save configuration on exit {#GeneralSettingsSaveConfig}

This option is a checkbox that, when checked, tells NVDA to automatically save the current configuration when you exit NVDA.

##### Show exit options when exiting NVDA {#GeneralSettingsShowExitOptions}

This option is a checkbox that allows you to choose whether or not a dialog appears when you exit NVDA that asks what action you want to perform.
When checked, a dialog will appear when you attempt to exit NVDA asking whether you want to exit, restart, restart with add-ons disabled or install pending updates (if any).
When unchecked, NVDA will exit immediately.

##### Play sounds when starting or exiting NVDA {#GeneralSettingsPlaySounds}

This option is a checkbox that, when checked, tells NVDA to play sounds when it starts or exits.

##### Logging level {#GeneralSettingsLogLevel}

This is a combo box that lets you choose how much NVDA will log as it's running.
Generally users should not need to touch this as not too much is logged.
However, if you wish to provide information in a bug report, or enable or disable logging altogether, then it may be a useful option.

The available logging levels are:

* Disabled: Apart from a brief startup message, NVDA will not log anything while it runs.
* Info: NVDA will log basic information such as startup messages and information useful for developers.
* Debug warning: Warning messages that are not caused by severe errors will be logged.
* Input/output: Input from keyboard and braille displays, as well as speech and braille output will be logged.
If you are concerned about privacy, do not set the logging level to this option.
* Debug: In addition to info, warning, and input/output messages, additional debug messages will be logged.
Just like input/output, if you are concerned about privacy, you should not set the logging level to this option.

##### Start NVDA after I sign in {#GeneralSettingsStartAfterLogOn}

If this option is enabled, NVDA will start automatically as soon as you sign in to Windows.
This option is only available for installed copies of NVDA.

##### Use NVDA during sign-in (requires administrator privileges) {#GeneralSettingsStartOnLogOnScreen}

If you sign in to Windows by providing a user name and password, then enabling this option will make NVDA start automatically at the sign-in screen when Windows starts.
This option is only available for installed copies of NVDA.

##### Use currently saved settings during sign-in and on secure screens (requires administrator privileges) {#GeneralSettingsCopySettings}

Pressing this button copies your currently saved NVDA user configuration to NVDA's system configuration directory, so that NVDA will use it during sign-in and when running on User Account Control (UAC) and other [secure screens](#SecureScreens).
To make sure that all your settings are transferred, make sure to save your configuration first with control+NVDA+c or Save configuration in the NVDA menu.
This option is only available for installed copies of NVDA.

##### Automatically check for updates to NVDA {#GeneralSettingsCheckForUpdates}

If this is enabled, NVDA will automatically check for updated versions and inform you when an update is available.
You can also manually check for updates by selecting Check for updates under Help in the NVDA menu.
When manually or automatically checking for updates, it is necessary for NVDA to send some information to the update server in order to receive the correct update for your system.
The following information is always sent:

* Current NVDA version
* Operating System version
* Whether the Operating System is 64 or 32 bit

##### Allow NV Access to gather NVDA usage statistics {#GeneralSettingsGatherUsageStats}

If this is enabled, NV Access will use the information from update checks in order to track  the number of NVDA users including particular demographics such as Operating system and country of origin.
Note that although your IP address will be used to calculate your country during the update check, the IP address is never kept.
Apart from the mandatory information required to check for updates, the following extra information is also currently sent:

* NVDA interface language
* Whether this copy of NVDA is portable or installed
* Name of the current speech synthesizer in use (including the name of the add-on the driver comes from)
* Name of the current Braille display in use (including the name of the add-on the driver comes from)
* The current output Braille table (if Braille is in use)

This information greatly aides NV Access to prioritize future development of NVDA.

##### Notify for pending updates on startup {#GeneralSettingsNotifyPendingUpdates}

If this is enabled, NVDA will inform you when there is a pending update on startup, offering you the possibility to install it.
You can also manually install the pending update from the Exit NVDA dialog (if enabled),  from the NVDA menu, or when you perform a new check from the Help menu.

#### Speech Settings {#SpeechSettings}

<!-- KC:setting -->

##### Open Speech settings {#OpenSpeechSettings}

Key: `NVDA+control+v`

The Speech category in the NVDA Settings dialog contains options that lets you change the speech synthesizer as well as voice characteristics for the chosen synthesizer.
For a quicker alternative way of controlling speech parameters from anywhere, please see the [Synth Settings Ring](#SynthSettingsRing) section.

The Speech Settings category contains the following options:

##### Change synthesizer {#SpeechSettingsChange}

The first option in the Speech Settings category is the Change... button. This button activates the [Select Synthesizer](#SelectSynthesizer) dialog, which allows you to select the active speech synthesizer and output device.
This dialog opens on top of the NVDA Settings dialog.
Saving or dismissing the settings in the Select Synthesizer dialog will return you to the NVDA Settings dialog.

##### Voice {#SpeechSettingsVoice}

The Voice option is a combo box listing all the voices of the current synthesizer that you have installed.
You can use the arrow keys to listen to all the various choices.
Left and Up arrow take you up in the list, while right and down arrow move you down in the list.

##### Variant {#SpeechSettingsVariant}

If you are using the Espeak NG synthesizer which is packaged with NVDA, this is a combo box that allows you to select the Variant the synthesizer should speak with.
ESpeak NG's Variants are rather like voices, as they provide slightly different attributes to the eSpeak NG voice.
Some variants will sound like a male, some like a female, and some even like a frog.
If using a third-party synthesizer, you may also be able to change this value if your chosen voice supports it.

##### Rate {#SpeechSettingsRate}

This option allows you to change the rate of your voice.
This is a slider that goes from 0 to 100 - 0 being the slowest, 100 being the fastest.

##### Rate boost {#SpeechSettingsRateBoost}

Enabling this option will significantly increase the speech rate, if supported by the current synthesizer.

##### Pitch {#SpeechSettingsPitch}

This option allows you to change the pitch of the current voice.
It is a slider which goes from 0 to 100 - 0 being the lowest pitch and 100 being the highest.

##### Volume {#SpeechSettingsVolume}

This option is a slider which goes from 0 to 100 - 0 being the lowest volume and 100 being the highest.

##### Inflection {#SpeechSettingsInflection}

This option is a slider that lets you choose how much inflection (rise and fall in pitch) the synthesizer should use to speak with.

##### Automatic Language switching {#SpeechSettingsLanguageSwitching}

This checkbox allows you to toggle whether NVDA should switch speech synthesizer languages automatically if the text being read specifies its language.
This option is enabled by default.

##### Automatic Dialect switching {#SpeechSettingsDialectSwitching}

This checkbox allows you to toggle whether or not dialect changes should be made, rather than just actual language changes.
For example, if reading in an English U.S. voice but a document specifies that some text is in English U.K., then the synthesizer will switch accents if this option is enabled.
This option is disabled by default.

<!-- KC:setting -->

##### Punctuation/Symbol Level {#SpeechSettingsSymbolLevel}

Key: NVDA+p

This allows you to choose the amount of punctuation and other symbols that should be spoken as words.
For example, when set to all, all symbols will be spoken as words.
This option applies to all synthesizers, not just the currently active synthesizer.

##### Trust voice's language when processing characters and symbols {#SpeechSettingsTrust}

On by default, this option tells NVDA if the current voice's language can be trusted when processing symbols and characters.
If you find that NVDA is reading punctuation in the wrong language for a particular synthesizer or voice, you may wish to turn this off to force NVDA to use its global language setting instead.

##### Include Unicode Consortium data (including emoji) when processing characters and symbols {#SpeechSettingsCLDR}

When this checkbox is checked, NVDA will include additional symbol pronunciation dictionaries when pronouncing characters and symbols.
These dictionaries contain descriptions for symbols (particularly emoji) that are provided by the [Unicode Consortium](https://www.unicode.org/consortium/) as part of their [Common Locale Data Repository](http://cldr.unicode.org/).
If you want NVDA to speak descriptions of emoji characters based on this data, you should enable this option.
However, if you are using a speech synthesizer that supports speaking emoji descriptions natively, you may wish to turn this off.

Note that manually added or edited character descriptions are saved as part of your user settings.
Therefore, if you change the description of a particular emoji, your custom description will be spoken for that emoji regardless of whether this option is enabled.
You can add, edit or remove symbol descriptions in NVDA's [punctuation/symbol pronunciation dialog](#SymbolPronunciation).

To toggle Unicode Consortium data inclusion from anywhere, please assign a custom gesture using the [Input Gestures dialog](#InputGestures).

##### Capital pitch change percentage {#SpeechSettingsCapPitchChange}

This edit field allows you to type the amount that the pitch of the voice will change when speaking a capital letter.
This value is a percentage, where a negative value lowers the pitch and a positive value raises it.
For no pitch change you would use 0.
Usually, NVDA raises the pitch slightly for any capital letter, but some synthesizers may not support this well.
In case pitch change for capitals is not supported, consider [Say "cap" before capitals](#SpeechSettingsSayCapBefore) and/or [ Beep for capitals](#SpeechSettingsBeepForCaps) instead.

##### Say "cap" before capitals {#SpeechSettingsSayCapBefore}

This setting is a checkbox that, when checked, tells NVDA to say the word "cap" before any capital letter when spoken as an individual character such as when spelling.

##### Beep for capitals {#SpeechSettingsBeepForCaps}

If this checkbox is checked, NVDA will make a small beep each time it encounters a capitalized character by itself.

##### Use spelling functionality if supported {#SpeechSettingsUseSpelling}

Some words consist of only one character, but the pronunciation is different depending on whether the character is being spoken as an individual character (such as when spelling) or a word.
For example, in English, "a" is both a letter and a word and is pronounced differently in each case.
This option allows the synthesizer to differentiate between these two cases if the synthesizer supports this.
Most synthesizers do support it.

This option should generally be enabled.
However, some Microsoft Speech API synthesizers do not implement this correctly and behave strangely when it is enabled.
If you are having problems with the pronunciation of individual characters, try disabling this option.

##### Delayed descriptions for characters on cursor movement {#delayedCharacterDescriptions}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Enabled, Disabled|
|Default |Disabled|

When this setting is checked, NVDA will say the character description when you move by characters.

For example, while reviewing a line by characters, when the letter "b" is read NVDA will say "Bravo" after a 1 second delay.
This can be useful if it is hard to distinguish between pronunciation of symbols, or for hearing impaired users.

The delayed character description will be cancelled if other text is spoken during that time, or if you press the `control` key.

##### Modes available in the Cycle speech mode command {#SpeechModesDisabling}

This checkable list allows selecting which [speech modes](#SpeechModes) are included when cycling between them using `NVDA+s`.
Modes which are unchecked are excluded.
By default all modes are included.

For example if you do not need to use "beeps" and "off" mode you should uncheck these two, and keep both "talk" and "on-demand" checked.
Note that it is necessary to check at least two modes.

#### Select Synthesizer {#SelectSynthesizer}

<!-- KC:setting -->

##### Open Select Synthesizer dialog {#OpenSelectSynthesizer}

Key: `NVDA+control+s`

The Synthesizer dialog, which can be opened by activating the Change... button in the speech category of the NVDA settings dialog, allows you to select which Synthesizer NVDA should use to speak with.
Once you have selected your synthesizer of choice, you can press Ok and NVDA will load the selected Synthesizer.
If there is an error loading the synthesizer, NVDA will notify you with a message, and continue using the previous synthesizer.

##### Synthesizer {#SelectSynthesizerSynthesizer}

This option allows you to choose the synthesizer you wish NVDA to use for speech output.

For a list of the Synthesizers that NVDA supports, please see the [Supported Speech Synthesizers](#SupportedSpeechSynths) section.

One special item that will always appear in this list is "No speech", which allows you to use NVDA with no speech output whatsoever.
This may be useful for someone who wishes to only use NVDA with braille, or perhaps to sighted developers who only wish to use the Speech Viewer.

#### Synth settings ring {#SynthSettingsRing}

If you wish to quickly change speech settings without going to the Speech category of the NVDA settings dialog, there are some NVDA key commands that allow you to move through the most common speech settings from anywhere while running NVDA:
<!-- KC:beginInclude -->

| Name |Desktop key |Laptop key |Description|
|---|---|---|---|
|Move to next synth setting |NVDA+control+rightArrow |NVDA+shift+control+rightArrow |Moves to the next available speech setting after the current, wrapping around to the first setting again after the last|
|Move to previous synth setting |NVDA+control+leftArrow |NVDA+shift+control+leftArrow |Moves to the next available speech setting before the current, wrapping around to the last setting after the first|
|Increment current synth setting |NVDA+control+upArrow |NVDA+shift+control+upArrow |increases the current speech setting you are on. E.g. increases the rate, chooses the next voice, increases the volume|
|Increment the current synth setting in a larger step |`NVDA+control+pageUp` |`NVDA+shift+control+pageUp` |Increases the value of the current speech setting you're on in larger steps. e.g. when you're on a voice setting, it will jump forward every 20 voices; when you're on slider settings (rate, pitch, etc) it will jump forward the value up to 20%|
|Decrement current synth setting |NVDA+control+downArrow |NVDA+shift+control+downArrow |decreases the current speech setting you are on. E.g. decreases the rate, chooses the previous voice, decreases the volume|
|Decrement the current synth setting in a larger step |`NVDA+control+pageDown` |`NVDA+shift+control+pageDown` |Decreases the value of the current speech setting you're on in larger steps. e.g. when you're on a voice setting, it will jump backward every 20 voices; when you're on a slider setting, it will jump backward the value up to 20%|

<!-- KC:endInclude -->

#### Braille {#BrailleSettings}

The Braille category in the NVDA Settings dialog contains options that let you change several aspects of braille input and output.
This category contains the following options:

##### Change braille display {#BrailleSettingsChange}

The Change... button in the Braille category of the NVDA Settings dialog activates the [Select Braille Display](#SelectBrailleDisplay) dialog, which allows you to select the active braille display.
This dialog opens on top of the NVDA Settings dialog.
Saving or dismissing the settings in the Select Braille Display dialog will return you to the NVDA Settings dialog.

##### Output Table {#BrailleSettingsOutputTable}

The next option you will come to in this category is the braille output table combo box.
In this combo box, you will find braille tables for different languages, braille standards and grades.
The chosen table will be used to translate text into braille to be presented on your braille display.
You can move from braille table to braille table in the list by using the arrow keys.

##### Input Table {#BrailleSettingsInputTable}

Complementary to the previous option, the next setting you will find is the braille input table combo box.
The chosen table will be used to translate braille entered on your braille display's Perkins-style keyboard into text.
You can move from braille table to braille table in the list by using the arrow keys.

Note that this option is only useful if your braille display has a Perkins-style keyboard and this feature is supported by the braille display driver.
If input is not supported on a display which does have a braille keyboard, this will be noted in the [Supported Braille Displays](#SupportedBrailleDisplays) section.

<!-- KC:setting -->

##### Braille mode {#BrailleMode}

Key: `NVDA+alt+t`

This option allows you to select between the available braille modes.

Currently, two braille modes are supported, "follow cursors" and "display speech output".

When follow cursors is selected, the braille display will follow either the system focus/caret or the navigator object/review cursor, depending on what braille is tethered to.

When display speech output is selected, the braille display will show what NVDA speaks, or would have spoken if speech mode was set to "talk".

##### Expand to computer braille for the word at the cursor {#BrailleSettingsExpandToComputerBraille}

This option allows the word that is under the cursor to be displayed in non-contracted computer braille.

##### Show Cursor {#BrailleSettingsShowCursor}

This option allows the braille cursor to be turned on and off.
It applies to the system caret and review cursor, but not to the selection indicator.

##### Blink Cursor {#BrailleSettingsBlinkCursor}

This option allows the braille cursor to blink.
If blinking is turned off, the braille cursor will constantly be in the "up" position.
The selection indicator is not affected by this option, it is always dots 7 and 8 without blinking.

##### Cursor Blink Rate (ms) {#BrailleSettingsBlinkRate}

This option is a numerical field that allows you to change the blink rate of the cursor in milliseconds.

##### Cursor Shape for Focus {#BrailleSettingsCursorShapeForFocus}

This option allows you to choose the shape (dot pattern) of the braille cursor when braille is tethered to focus.
The selection indicator is not affected by this option, it is always dots 7 and 8 without blinking.

##### Cursor Shape for Review {#BrailleSettingsCursorShapeForReview}

This option allows you to choose the shape (dot pattern) of the braille cursor when braille is tethered to review.
The selection indicator is not affected by this option, it is always dots 7 and 8 without blinking.

##### Show Messages {#BrailleSettingsShowMessages}

This is a combobox that allows you to select if NVDA should display braille messages and when they should disappear automatically.

To toggle show messages from anywhere, please assign a custom gesture using the [Input Gestures dialog](#InputGestures).

##### Message Timeout (sec) {#BrailleSettingsMessageTimeout}

This option is a numerical field that controls how long NVDA messages are displayed on the braille display.
The NVDA message is immediately dismissed when pressing a routing key on the braille display, but appears again when pressing a corresponding key which triggers the message.
This option is shown only if "Show Messages" is set to "Use timeout".

<!-- KC:setting -->

##### Tether Braille {#BrailleTether}

Key: NVDA+control+t

This option allows you to choose whether the braille display will follow the system focus / caret, the navigator object / review cursor, or both.
When "automatically" is selected, NVDA will follow the system focus and caret by default.
In this case, when the navigator object or the review cursor position is changed by means of explicit user interaction, NVDA will tether to review temporarily, until the focus or the caret changes.
If you want it to follow the focus and caret only, you need to configure braille to be tethered to focus.
In this case, braille will not follow the NVDA navigator during object navigation or the review cursor during review.
If you want braille to follow object navigation and text review instead, you need to configure braille to be tethered to review.
In this case, Braille  will not follow system focus and system caret.

##### Move system caret when routing review cursor {#BrailleSettingsReviewRoutingMovesSystemCaret}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Default (Never), Never, Only when tethered automatically, Always|
|Default |Never|

This setting determines if the system caret should also be moved with a routing button press.
This option is set to Never by default, meaning that routing will never move the caret when routing the review cursor.

When this option is set to Always, and [braille tethering](#BrailleTether) is set to "automatically" or "to review", pressing a cursor routing key will also move the system caret or focus when supported.
When the current review mode is [Screen Review](#ScreenReview), there is no physical caret.
In this case, NVDA tries to focus the object under the text you're routing to.
The same applies to [object review](#ObjectReview).

You can also set this option to only move the caret when tethered automatically.
In that case, pressing a cursor routing key will only move the system caret or focus when NVDA is tethered to the review cursor automatically, whereas no movement will occur when manually tethered to the review cursor.

This option is shown only if "[tether braille](#BrailleTether)" is set to "automatically" or "to review".

To toggle move system caret when routing review cursor from anywhere, please assign a custom gesture using the [Input Gestures dialog](#InputGestures).

##### Read by Paragraph {#BrailleSettingsReadByParagraph}

If enabled, braille will be displayed by paragraphs instead of lines.
Also, the next and previous line commands will move by paragraph accordingly.
This means that you do not have to scroll the display at the end of each line even where more text would fit on the display.
This may allow for more fluent reading of large amounts of text.
It is disabled by default.

##### Avoid splitting words when possible {#BrailleSettingsWordWrap}

If this is enabled, a word which is too large to fit at the end of the braille display will not be split.
Instead, there will be some blank space at the end of the display.
When you scroll the display, you will be able to read the entire word.
This is sometimes called "word wrap".
Note that if the word is too large to fit on the display even by itself, the word must still be split.

If this is disabled, as much of the word as possible will be displayed, but the rest will be cut off.
When you scroll the display, you will then be able to read the rest of the word.

Enabling this may allow for more fluent reading, but generally requires you to scroll the display more.

##### Focus context presentation {#BrailleSettingsFocusContextPresentation}

This option allows you to choose what context information NVDA will show on the braille display when an object gets focus.
Context information refers to the hierarchy of objects containing the focus.
For example, when you focus a list item, this list item is part of a list.
This list might be contained by a dialog, etc.
Please consult the section about [object navigation](#ObjectNavigation) for more information about the hierarchy that applies to objects in NVDA.

When set to fill display for context changes, NVDA will try to display as much context information as possible on the braille display, but only for the parts of the context that have changed.
For the example above, this means that when changing focus to the list, NVDA will show the list item on the braille display.
Furthermore, if there is enough space left on the braille display, NVDA will try to show that the list item is part of a list.
If you then start moving through the list with your arrow keys, it is assumed that you are aware that you are still in the list.
Thus, for the remaining list items you focus, NVDA will only show the focused list item on the display.
In order for you to read the context again (i.e. that you are in a list and that the list is part of a dialog), you will have to scroll your braille display back.

When this option is set to always fill the display, NVDA will try to show as much context information as possible on the braille display, regardless of whether you have seen the same context information before.
This has the advantage that NVDA will fit as much information as possible on the display.
However, the downside is that there is always a difference in the position where the focus starts on the braille display.
This can make it difficult to skim a long list of items, for example, as you will need to continually move your finger to find the start of the item.
This was the default behaviour for NVDA 2017.2 and before.

When you set the focus context presentation option to only show the context information when scrolling back, NVDA never shows context information on your braille display by default.
Thus, in the example above, NVDA will display that you focused a list item.
However, in order for you to read the context (i.e. that you are in a list and that the list is part of a dialog), you will have to scroll your braille display back.

To toggle focus context presentation from anywhere, please assign a custom gesture using the [Input Gestures dialog](#InputGestures).

##### Interrupt speech while scrolling {#BrailleSettingsInterruptSpeech}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Default (Enabled), Enabled, Disabled|
|Default |Enabled|

This setting determines if speech should be interrupted when the Braille display is scrolled backwards/forwards.
Previous/next line commands always interrupt speech.

On-going speech might be a distraction while reading Braille.
For this reason the option is enabled by default, interrupting speech when scrolling braille.

Disabling this option allows speech to be heard while simultaneously reading Braille.

##### Show selection {#BrailleSettingsShowSelection}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Default (Enabled), Enabled, Disabled|
|Default |Enabled|

This setting determines if selection indicator (dots 7 and 8) is shown by the braille display.
The option is enabled by default so the selection indicator is shown.
The selection indicator might be a distraction while reading.
Disabling this option may improve readability.

To toggle show selection from anywhere, please assign a custom gesture using the [Input Gestures dialog](#InputGestures).

#### Select Braille Display {#SelectBrailleDisplay}

<!-- KC:setting -->

##### Open Select Braille Display dialog {#OpenSelectBrailleDisplay}

Key: `NVDA+control+a`

The Select Braille Display dialog, which can be opened by activating the Change... button in the Braille category of the NVDA settings dialog, allows you to select which Braille display NVDA should use for braille output.
Once you have selected your braille display of choice, you can press Ok and NVDA will load the selected display.
If there is an error loading the display driver, NVDA will notify you with a message, and continue using the previous display, if any.

##### Braille Display {#SelectBrailleDisplayDisplay}

This combo box presents you with several options depending on what braille display drivers are available on your system.
Move between these options with the arrow keys.

The automatic option will allow NVDA to search for many supported braille displays in the background.
When this feature is enabled and you connect a supported display using USB or bluetooth, NVDA will automatically connect with this display.

No braille means that you are not using braille.

Please see the [Supported Braille Displays](#SupportedBrailleDisplays) section for more information about supported braille displays and which of these support automatic detection in the background.

##### Displays to detect automatically {#SelectBrailleDisplayAutoDetect}

When braille display is set to "Automatic", the check boxes in this list control allows you to enable and disable display drivers that will be involved in the automatic detection process.
This allows you to exclude braille display drivers you do not use on a regular basis.
For example, if you only own a display that requires the Baum driver to function, you may leave the Baum driver enabled whereas the other drivers can be disabled.

By default, all drivers that support automatic detection are enabled.
Any driver added, for example in a future version of NVDA or in an add-on, will also be enabled by default.

You may consult the documentation for your braille display in the section [Supported Braille Displays](#SupportedBrailleDisplays) to check whether the driver supports automatic detection of displays.

##### Port {#SelectBrailleDisplayPort}

This option, if available, allows you to choose what port or type of connection will be used to communicate with the braille display you have selected.
It is a combo box containing the possible choices for your braille display.

By default, NVDA employs automatic port detection, which means the connection with the braille device will be established automatically by scanning for available USB and bluetooth devices on your system.
However, for some braille displays, you may be able to explicitly choose what port should be used.
Common options are "Automatic" (which tells NVDA to employ the default automatic port selection procedure), "USB", "Bluetooth" and legacy serial communication ports if your braille display supports this type of communication.

This option won't be available if your braille display only supports automatic port detection.

You may consult the documentation for your braille display in the section [Supported Braille Displays](#SupportedBrailleDisplays) to check for more details on the supported types of communication and available ports.

Please note: If you connect multiple Braille Displays to your machine at the same time which use the same driver (E.g. connecting two Seika displays),
it is currently impossible to tell NVDA which display to use.
Therefore it is recommended to only connect one Braille Display of a given type / manufacturer to your machine at a time.

#### Audio {#AudioSettings}

<!-- KC:setting -->

##### Open Audio settings {#OpenAudioSettings}

Key: `NVDA+control+u`

The Audio category in the NVDA Settings dialog contains options that let you change several aspects of audio output.

##### Output device {#SelectSynthesizerOutputDevice}

This option allows you to choose the audio device that NVDA should instruct the selected synthesizer to speak through.

<!-- KC:setting -->

##### Audio Ducking Mode {#SelectSynthesizerDuckingMode}

Key: `NVDA+shift+d`

This option allows you to choose if NVDA should lower the volume of other applications while NVDA is speaking, or all the time while NVDA is running.

* No Ducking: NVDA will never lower the volume of other audio.
* Duck when outputting speech and sounds: NVDA will only lower the volume of other audio when NVDA is speaking or playing sounds. This may not work for all synthesizers.
* Always duck: NVDA will keep the volume of other audio lower the whole time NVDA is running.

This option is only available if NVDA has been installed.
It is not possible to support audio ducking for portable and temporary copies of NVDA.

##### Volume of NVDA sounds follows voice volume {#SoundVolumeFollowsVoice}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Disabled, Enabled|
|Default |Disabled|

When this option is enabled, the volume of NVDA sounds and beeps will follow the volume setting of the voice you are using.
If you decrease the volume of the voice, the volume of sounds will decrease.
Similarly, if you increase the volume of the voice, the volume of sounds will increase.
This option is not available if you have started NVDA with [WASAPI disabled for audio output](#WASAPI) in Advanced Settings.

##### Volume of NVDA sounds {#SoundVolume}

This slider allows you to set the volume of NVDA sounds and beeps.
This setting only takes effect when "Volume of NVDA sounds follows voice volume" is disabled.
This option is not available if you have started NVDA with [WASAPI disabled for audio output](#WASAPI) in Advanced Settings.

##### Sound split {#SelectSoundSplitMode}

The sound split feature allows users to make use of their stereo output devices, such as headphones and speakers.
Sound split makes it possible to have NVDA speech in one channel (e.g. left) and have all other applications play their sounds in the other channel (e.g. right).
By default sound split is disabled.
A gesture allows cycling through the various sound split modes:
<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Cycle Sound Split Mode |`NVDA+alt+s` |Cycles between sound split modes.|

<!-- KC:endInclude -->

By default this command will cycle between the following modes:

* Sound split disabled: NVDA does not apply any sound split processing.
* NVDA on the left and applications on the right: NVDA will speak in the left channel, while other applications will play sounds in the right channel.
* NVDA on the left and applications in both channels: NVDA will speak in the left channel, while other applications will play sounds in  both left and right channels.

There are more advanced sound split modes available in NVDA setting combo box.
Among these modes, "NVDA in both channels and applications in both channels" forces all the sounds to be directed in both channels.
This mode may differ from "Sound split disabled" mode in case other audio processing interfers with channel volumes.

Please note, that sound split doesn't work as a mixer.
For example, if an application is playing a stereo sound track while sound split is set to "NVDA on the left and applications on the right", then you will only hear the right channel of the sound track, while the left channel of the sound track will be muted.

This option is not available if you have started NVDA with [WASAPI disabled for audio output](#WASAPI) in Advanced Settings.

Please note, that if NVDA crashes, then it won't be able to restore application sounds volume, and those applications might still output sound only in one channel after NVDA crash.
In order to mitigate this, please restart NVDA and select the mode "NVDA in both channels and applications in both channels".

##### Customizing Sound split modes {#CustomizeSoundSplitModes}

This checkable list allows selecting which sound split modes are included when cycling between them using `NVDA+alt+s`.
Modes which are unchecked are excluded.
By default only three modes are included.

* Sound split disabled.
* NVDA on the left and applications on the right.
* NVDA on the left and applications in both channels.

Note that it is necessary to check at least one mode.
This option is not available if you have started NVDA with [WASAPI disabled for audio output](#WASAPI) in Advanced Settings.

##### Time to keep audio device awake after speech {#AudioAwakeTime}

This edit box specifies how long NVDA keeps the audio device awake after speech ends.
This allows NVDA to avoid certain speech glitches like dropped parts of words.
This can happen due to audio devices (especially Bluetooth and wireless devices) entering standby mode.
This might also be helpful in other use cases, such as when running NVDA inside a virtual machine (e.g. Citrix Virtual Desktop), or on certain laptops.

Lower values may allow audio to be cut-off more often, as a device may enter standby mode too soon, causing the start of the following speech to be clipped.
Setting the value too high may cause the battery of the sound output device to discharge faster, as it stays active for longer while no sound is being sent.

You can set the time to zero in order to disable this feature.

#### Vision {#VisionSettings}

The Vision category in the NVDA Settings dialog allows you to enable, disable and configure [visual aids](#Vision).

Note that the available options in this category could be extended by [NVDA add-ons](#AddonsManager).
By default, this settings category contains the following options:

##### Visual Highlight {#VisionSettingsFocusHighlight}

The check boxes in the Visual Highlight grouping control the behaviour of NVDA's built-in [Visual Highlight](#VisionFocusHighlight) facility.

* Enable Highlighting: Toggles Visual Highlight on and off.
* Highlight system focus: toggles whether the [system focus](#SystemFocus) will be highlighted.
* Highlight navigator object: toggles whether the [navigator object](#ObjectNavigation) will be highlighted.
* Highlight browse mode cursor: Toggles whether the [virtual browse mode cursor](#BrowseMode) will be highlighted.

Note that checking and unchecking the "Enable Highlighting" check box wil also change the state of the tree other check boxes accordingly.
Therefore, if "Enable Highlighting" is off and you check this check box, the other tree check boxes will also be checked automatically.
If you only want to highlight the focus and leave the navigator object and browse mode check boxes unchecked, the state of the "Enable Highlighting" check box will be half checked.

##### Screen Curtain {#VisionSettingsScreenCurtain}

You can enable the [Screen Curtain](#VisionScreenCurtain) by checking the "Make screen black (immediate effect)" check box.
A warning that your screen will become black after activation will be displayed.
Before continuing (selecting "Yes"), ensure you have enabled speech / braille and will be able to control your computer without the use of the screen.
Select "No" if you no longer wish to enable the Screen Curtain.
If you are sure, you can choose the Yes button to enable the screen curtain.
If you no longer want to see this warning message every time, you can change this behaviour in the dialog that displays the message.
You can always restore the warning by checking the "Always show a warning when loading Screen Curtain" check box next to the "Make screen black" check box.

By default, sounds are played when the Screen Curtain is toggled.
When you want to change this behaviour, you can uncheck the "Play sound when toggling Screen Curtain" check box.

##### Settings for third party visual aids {#VisionSettingsThirdPartyVisualAids}

Additional vision enhancement providers can be provided in [NVDA add-ons](#AddonsManager).
When these providers have adjustable settings, they will be shown in this settings category in separate groupings.
For the supported settings per provider, please refer to the documentation for that provider.

#### Keyboard {#KeyboardSettings}

<!-- KC:setting -->

##### Open Keyboard settings {#OpenKeyboardSettings}

Key: `NVDA+control+k`

The Keyboard category in the NVDA Settings dialog contains options that set how NVDA behaves as you use and type on your keyboard.
This settings category contains the following options:

##### Keyboard layout {#KeyboardSettingsLayout}

This combo box lets you choose what type of keyboard layout NVDA should use. Currently the two that come with NVDA are Desktop and Laptop.

##### Select NVDA Modifier Keys {#KeyboardSettingsModifiers}

The checkboxes in this list control what keys can be used as [NVDA modifier keys](#TheNVDAModifierKey). The following keys are available to choose from:

* The Caps Lock key
* The insert key on the number pad
* The extended insert key (usually found above the arrow keys, near home and end)

If no key is chosen as the NVDA key it may be impossible to access many NVDA commands, therefore you are required to check at least one of the modifiers.

<!-- KC:setting -->

##### Speak Typed Characters {#KeyboardSettingsSpeakTypedCharacters}

Key: NVDA+2

When enabled, NVDA will announce all characters you type on the keyboard.

<!-- KC:setting -->

##### Speak Typed Words {#KeyboardSettingsSpeakTypedWords}

Key: NVDA+3

When enabled, NVDA will announce all words you type on the keyboard.

##### Speech interrupt for typed characters {#KeyboardSettingsSpeechInteruptForCharacters}

If on, this option will cause speech to be interrupted each time a character is typed. This is on by default.

##### Speech interrupt for Enter key {#KeyboardSettingsSpeechInteruptForEnter}

If on, this option will cause speech to be interrupted each time the Enter key is pressed. This is on by default.

##### Allow skim reading in Say All {#KeyboardSettingsSkimReading}

If on, certain navigation commands (such as quick navigation in browse mode or moving by line or paragraph) do not stop Say All, rather Say All jumps to the new position and continues reading.

##### Beep if Typing Lowercase Letters when Caps Lock is On {#KeyboardSettingsBeepLowercase}

When enabled, a warning beep will be heard if a letter is typed with the shift key while Caps Lock is on.
Generally, typing shifted letters with Caps Lock is unintentional and is usually due to not realizing that Caps Lock is enabled.
Therefore, it can be quite helpful to be warned about this.

<!-- KC:setting -->

##### Speak Command Keys {#KeyboardSettingsSpeakCommandKeys}

Key: NVDA+4

When enabled, NVDA will announce all non-character keys you type on the keyboard. This includes key combinations such as control plus another letter.

##### Play sound for spelling errors while typing {#KeyboardSettingsAlertForSpellingErrors}

When enabled, a short buzzer sound will be played when a word you type contains a spelling error.
This option is only available if reporting of spelling errors is enabled in NVDA's [Document Formatting Settings](#DocumentFormattingSettings), found in the NVDA Settings dialog.

##### Handle keys from other applications {#KeyboardSettingsHandleKeys}

This option allows the user to control if key presses generated by applications such as on-screen keyboards and speech recognition software should be processed by NVDA.
This option is on by default, though certain users may wish to turn this off, such as those typing Vietnamese with the UniKey typing software as it will  cause incorrect character input.

#### Mouse {#MouseSettings}

<!-- KC:setting -->

##### Open Mouse settings {#OpenMouseSettings}

Key: `NVDA+control+m`

The Mouse category in the NVDA Settings dialog allows NVDA to track the mouse, play mouse coordinate beeps and sets other mouse usage options.
This category contains the following options:

##### Report Mouse Shape Changes {#MouseSettingsShape}

A checkbox, that when checked means that NVDA will announce the shape of the mouse pointer each time it changes.
The mouse pointer in Windows changes shape to convey certain information such as when something is editable, or when something is loading etc.

<!-- KC:setting -->

##### Enable mouse tracking {#MouseSettingsTracking}

Key: NVDA+m

When enabled, NVDA will announce the text currently under the mouse pointer, as you move it around the screen. This allows you to find things on the screen, by physically moving the mouse, rather than trying to find them through object navigation.

##### Text unit resolution {#MouseSettingsTextUnit}

If NVDA is set to announce the text under the mouse as you move it, this option allows you to choose exactly how much text will be spoken.
The options are character, word, line and paragraph.

To toggle text unit resolution from anywhere, please assign a custom gesture using the [Input Gestures dialog](#InputGestures).

##### Report object when mouse enters it {#MouseSettingsRole}

If this checkbox is checked, NVDA will announce information about objects as the mouse moves inside them.
This includes the role (type) of the object as well as states (checked/pressed), cell coordinates in tables, etc.
Note that the announcement of some object details might be dependent on how other settings are set, such as in the [object presentation](#ObjectPresentationSettings) or [Document Formatting](#DocumentFormattingSettings) categories.

##### Play audio coordinates when mouse moves {#MouseSettingsAudio}

Checking this checkbox makes NVDA play beeps as the mouse moves, so that the user can work out where the mouse is in regards to the dimensions of the screen.
The higher the mouse is on the screen, the higher the pitch of the beeps.
The further left or right the mouse is located on the screen, the further left or right the sound will be played (assuming the user has stereo speakers or headphones).

##### Brightness controls audio coordinates volume {#MouseSettingsBrightness}

If the "play audio coordinates when mouse moves" checkbox is checked, then checking this checkbox means that the volume of the audio coordinates beeps is controlled by how bright the screen is under the mouse.
This setting is unchecked by default.

##### Ignore mouse input from other applications {#MouseSettingsHandleMouseControl}

This option allows the user to ignore mouse events (including mouse movement and button presses) generated by other applications such as TeamViewer and other remote control software.
This option is unchecked by default.
If you check this option and you have the "Enable mouse tracking" option enabled, NVDA will not announce what is under the mouse if the mouse is moved by another application.

#### Touch Interaction {#TouchInteraction}

This settings category, only available on computers with touch capabilities, allows you to configure how NVDA interacts with touchscreens.
This category contains the following options:

##### Enable touch interaction support {#TouchSupportEnable}

This checkbox enables NVDA's touch interaction support.
If enabled, you can use your fingers to navigate and interact with items on screen using a touchscreen device.
If disabled, touchscreen support will be disabled as though NVDA is not running.
This setting can also be toggled using NVDA+control+alt+t.

##### Touch typing mode {#TouchTypingMode}

This checkbox allows you to specify the method you wish to use when entering text using the touch keyboard.
If this checkbox is checked, when you locate a key on the touch keyboard, you can lift your finger and the selected key will be pressed.
If this is unchecked, you need to double-tap on the key of the touch keyboard to press the key.

#### Review Cursor {#ReviewCursorSettings}

The Review Cursor category in the NVDA Settings dialog is used to configure NVDA's review cursor behaviour.
This category contains the following options:

<!-- KC:setting -->

##### Follow System Focus {#ReviewCursorFollowFocus}

Key: NVDA+7

When enabled, The review cursor will always be placed in the same object as the current system focus whenever the focus changes.

<!-- KC:setting -->

##### Follow System Caret {#ReviewCursorFollowCaret}

Key: NVDA+6

When enabled, the review cursor will automatically be moved to the position of the System caret each time it moves.

##### Follow mouse cursor {#ReviewCursorFollowMouse}

When enabled, the review cursor will follow the mouse as it moves.

##### Simple Review mode {#ReviewCursorSimple}

When enabled, NVDA will filter the hierarchy of objects that can be navigated to exclude objects that aren't of interest to the user; e.g. invisible objects and objects used only for layout purposes.

To toggle simple review mode from anywhere, please assign a custom gesture using the [Input Gestures dialog](#InputGestures).

#### Object Presentation {#ObjectPresentationSettings}

<!-- KC:setting -->

##### Open Object Presentation settings {#OpenObjectPresentationSettings}

Key: `NVDA+control+o`

The Object Presentation category in the NVDA Settings dialog is used to set how much information NVDA will present about controls such as description, position information and so on.
These options don't typically apply to browse mode.
These options typically apply to focus reporting and NVDA object navigation, but not reading text content e.g. browse mode.

##### Report tooltips {#ObjectPresentationReportToolTips}

A checkbox that when checked tells NVDA to report tooltips as they appear.
Many Windows and controls show a small message (or tooltip) when you move the mouse pointer over them, or sometimes when you move the focus to them.

##### Report notifications {#ObjectPresentationReportNotifications}

This checkbox, when checked, tells NVDA to report help balloons and toast notifications as they appear.

* Help Balloons are like tooltips, but are usually larger in size, and are associated with system events such as a network cable being unplugged, or perhaps to alert you about Windows security issues.
* Toast notifications have been introduced in Windows 10 and appear in the notification centre in the system tray, informing about several events (i.e. if an update has been downloaded, a new e-mail arrived in your inbox, etc.).

##### Report Object Shortcut Keys {#ObjectPresentationShortcutKeys}

When this checkbox is checked, NVDA will include the shortcut key that is associated with a certain object or control when it is reported.
For example the File menu on a menu bar may have a shortcut key of alt+f.

##### Report object position information {#ObjectPresentationPositionInfo}

This option lets you choose whether you wish to have an object's position (e.g. 1 of 4) reported when moving to the object with the focus or object navigation.

##### Guess Object Position Information when unavailable {#ObjectPresentationGuessPositionInfo}

If reporting of object position information is turned on, this option allows NVDA to guess object position information when it is otherwise unavailable for a particular control.

When on, NVDA will report position information for more controls such as menus and toolbars, however this information may be slightly inaccurate.

##### Report Object descriptions {#ObjectPresentationReportDescriptions}

Uncheck this checkbox if you don't wish to have the description reported along with objects (i.e. search suggestions, reporting of whole dialog window right after the dialog opens, etc.).

<!-- KC:setting -->

##### Progress bar output {#ObjectPresentationProgressBarOutput}

Key: NVDA+u

This option controls how NVDA reports progress bar updates to you.

It has the following options:

* Off: Progress bars will not be reported as they change.
* Speak: This option tells NVDA to speak the progress bar in percentages. Each time the progress bar changes, NVDA will speak the new value.
* Beep: This tells NVDA to beep each time the progress bar changes. The higher the beep, the closer the progress bar is to completion.
* Beep and speak: This option tells NVDA to both beep and speak when a progress bar updates.

##### Report background progress bars {#ObjectPresentationReportBackgroundProgressBars}

This is an option that, when checked, tells NVDA to keep reporting a progress bar, even if it is not physically in the foreground.
If you minimize or switch away from a window that contains a progress bar, NVDA will keep track of it, allowing you to do other things while NVDA tracks the progress bar.

<!-- KC:setting -->

##### Report dynamic content changes {#ObjectPresentationReportDynamicContent}

Key: NVDA+5

Toggles the announcement of new content in particular objects such as terminals and the history control in chat programs.

##### Play a sound when auto-suggestions appear {#ObjectPresentationSuggestionSounds}

Toggles announcement of appearance of auto-suggestions, and if enabled, NVDA will play a sound to indicate this.
Auto-suggestions are lists of suggested entries based on text entered into certain edit fields and documents.
For example, when you enter text into the search box in Start menu in Windows Vista and later, Windows displays a list of suggestions based on what you typed.
For some edit fields such as search fields in various Windows 10 apps, NVDA can notify you that a list of suggestions has appeared when you type text.
The auto-suggestions list will close once you move away from the edit field, and for some fields, NVDA can notify you of this when this happens.

#### Input Composition {#InputCompositionSettings}

The Input Composition category allows you to control how NVDA reports the input of Asian characters, such as with IME or Text Service input methods.
Note that due to the fact that input methods vary greatly by available features and by how they convey information, it will most likely be necessary to configure these options differently for each input method to get the most efficient typing experience.

##### Automatically report all available candidates {#InputCompositionReportAllCandidates}

This option, which is on by default,  allows you to choose whether or not all visible candidates should be reported automatically when a candidate list appears or its page is changed.
Having this option on for pictographic input methods such as Chinese New ChangJie or Boshiami is useful, as you can automatically hear all symbols and their numbers and you can choose one right away.
However, for phonetic input methods such as Chinese New Phonetic, it may be more useful to turn this option off, as all the symbols will sound the same and you will have to use the arrow keys to navigate the list items individually to gain more information  from the character descriptions for each candidate.

##### Announce Selected Candidate {#InputCompositionAnnounceSelectedCandidate}

This option, which is on by default, allows you to choose whether NVDA should announce the selected candidate when a candidate list appears or when the selection is changed.
For input methods where the selection can be changed with the arrow keys  (such as Chinese New Phonetic) this is necessary, but for some input methods it may be more efficient typing with this option turned off.
Note that even with this option off, the review cursor will still be placed on the selected candidate allowing you to use object navigation / review to manually read this or other candidates.

##### Always include short character descriptions for candidates {#InputCompositionCandidateIncludesShortCharacterDescription}

This option, which is on by default, allows you to choose whether or not NVDA should provide a short description for each character in a candidate, either when it's selected or when it's automatically read when the candidate list appears.
Note that for locales such as Chinese, the announcement of extra character descriptions for the selected candidate is not affected by this option.
This option may be useful for Korean and Japanese input methods.

##### Report changes to the reading string {#InputCompositionReadingStringChanges}

Some input methods such as Chinese New Phonetic and New ChangJie have a reading string (sometimes known as a precomposition string).
You can choose whether or not NVDA should announce new characters being typed into this reading string with this option.
This option is on by default.
Note some older input methods such as Chinese ChangJie may not use the reading string to hold precomposition characters, but instead use the composition string directly. Please see the next option for configuring reporting of the composition string.

##### Report changes to the composition string {#InputCompositionCompositionStringChanges}

After reading or precomposition data has been combined into a valid pictographic symbol, most input methods place this symbol into a composition string for temporary storage along with other combined symbols before they are finally inserted into the document.
This option allows you to choose whether or not NVDA should report new symbols as they appear  in the composition string.
This option is on by default.

#### Browse Mode {#BrowseModeSettings}

<!-- KC:setting -->

##### Open Browse Mode settings {#OpenBrowseModeSettings}

Key: `NVDA+control+b`

The Browse Mode category in the NVDA Settings dialog is used to configure NVDA's behaviour when you read and navigate complex documents such as web pages.
This category contains the following options:

##### Maximum Number of Characters on One Line {#BrowseModeSettingsMaxLength}

This field sets the maximum length of a line in browse mode (in characters).

##### Maximum Lines Per Page {#BrowseModeSettingsPageLines}

This field sets the amount of lines you will move by when pressing page up or page down while in browse mode.

<!-- KC:setting -->

##### Use screen layout {#BrowseModeSettingsScreenLayout}

Key: NVDA+v

This option allows you to specify whether browse mode should place clickable content (links, buttons and fields) on its own line, or if it should keep it in the flow of text as it is visually shown.
Note that this option doesn't apply to Microsoft Office apps such as Outlook and Word, which always use screen layout.
When screen layout is enabled, page elements will stay as they are visually shown.
For example, a visual line of multiple links will be presented in speech and braille as multiple links on the same line.
If it is disabled, then page elements will be placed on their own lines.
This may be easier to understand during line by line page navigation and make items easier to interact with for some users.

##### Enable browse mode on page load {#BrowseModeSettingsEnableOnPageLoad}

This checkbox toggles whether browse mode should be automatically enabled when loading a page.
When this option is disabled, browse mode can still be manually activated on pages or in documents where browse mode is supported.
See the [Browse Mode section](#BrowseMode) for a list of applications supported by browse mode.
Note that this option does not apply to situations where browse mode is always optional, e.g. in Microsoft Word.
This option is enabled by default.

##### Automatic Say All on page load {#BrowseModeSettingsAutoSayAll}

This checkbox toggles the automatic reading of a page after it loads in browse mode.
This option is enabled by default.

##### Include layout tables {#BrowseModeSettingsIncludeLayoutTables}

This option affects how NVDA handles tables used purely for layout purposes.
When on, NVDA will treat these as normal tables, reporting them based on [Document Formatting Settings](#DocumentFormattingSettings) and locating them with quick navigation commands.
When off, they will not be reported nor found with quick navigation.
However, the content of the tables will still be included as normal text.
This option is turned off by default.

To toggle inclusion of layout tables from anywhere, please assign a custom gesture using the [Input Gestures dialog](#InputGestures).

##### Configuring reporting of fields such as links and headings {#BrowseModeLinksAndHeadings}

Please see the options in the [Document Formatting category](#DocumentFormattingSettings) of the [NVDA Settings](#NVDASettings) dialog to configure the fields that are reported when navigating, such as links, headings and tables.

##### Automatic focus mode for focus changes {#BrowseModeSettingsAutoPassThroughOnFocusChange}

This option allows focus mode to be invoked if focus changes.
For example, when on a web page, if you press tab and you land on a form, if this option is checked, focus mode will automatically be invoked.

##### Automatic focus mode for caret movement {#BrowseModeSettingsAutoPassThroughOnCaretMove}

This option, when checked, allows NVDA to enter and leave focus mode when using arrow keys.
For example, if arrowing down a web page and you land on an edit box, NVDA will automatically bring you into focus mode.
If you arrow out of the edit box, NVDA will put you back in browse mode.

##### Audio indication of Focus and Browse modes {#BrowseModeSettingsPassThroughAudioIndication}

If this option is enabled, NVDA will play special sounds when it switches between browse mode and focus mode, rather than speaking the change.

##### Trap non-command gestures from reaching the document {#BrowseModeSettingsTrapNonCommandGestures}

Enabled by default, this option allows you to choose if gestures (such as key presses) that  do not result in an NVDA command and are not considered to be a command key in general, should be trapped from going through to the document you are currently focused on.
As an example, if enabled and the letter j was pressed, it would be trapped from reaching the document, even though it is not a quick navigation command nor is it likely to be a command in the application itself.
In this case NVDA will tell Windows to play a default sound whenever a key which gets trapped is pressed.

<!-- KC:setting -->

##### Automatically set system focus to focusable elements {#BrowseModeSettingsAutoFocusFocusableElements}

Key: NVDA+8

Disabled by default, this option allows you to choose if the system focus should automatically be set to elements that can take the system focus (links, form fields, etc.) when navigating content with the browse mode caret.
Leaving this option disabled will not automatically focus focusable elements when they are selected with the browse mode caret.
This might result in faster browsing experience and better responsiveness in browse mode.
The focus will yet be updated to the particular element when interacting with it (e.g. pressing a button, checking a check box).
Enabling this option may improve support for some websites at the cost of performance and stability.

#### Document Formatting {#DocumentFormattingSettings}

<!-- KC:setting -->

##### Open Document Formatting settings {#OpenDocumentFormattingSettings}

Key: `NVDA+control+d`

Most of the options in this category are for configuring what type of formatting you wish to have reported as you move the cursor around documents.
For example, if you check the report font name checkbox, each time you arrow onto text with a different font, the name of the font will be announced.

The document formatting options are organized into groups.
You can configure reporting of:

* Font
  * Font name
  * Font size
  * Font attributes
  * Superscripts and subscripts
  * Emphasis
  * Highlighted (Marked) text
  * Style
  * Colours
* Document information
  * Comments
  * Bookmarks
  * Editor revisions
  * Spelling errors
* Pages and spacing
  * Page numbers
  * Line numbers
  * Line indentation reporting [(Off, Speech, Tones, Both Speech and Tones)](#DocumentFormattingSettingsLineIndentation)
  * Ignore blank lines for line indentation reporting
  * Paragraph indentation (e.g. hanging indent, first line indent)
  * Line spacing (single, double, etc.)
  * Alignment
* Table information
  * Tables
  * Row/column headers (Off, Rows, Columns, Rows and columns)
  * Cell coordinates
  * Cell borders (Off, Styles, Both Colours and Styles)
* Elements
  * Headings
  * Links
  * Graphics
  * Lists
  * Block quotes
  * Groupings
  * Landmarks
  * Articles
  * Frames
  * Figures and captions
  * Clickable

To toggle these settings from anywhere, please assign custom gestures using the [Input Gestures dialog](#InputGestures).

##### Report formatting changes after the cursor {#DocumentFormattingDetectFormatAfterCursor}

If enabled, this setting tells NVDA to try and detect all the formatting changes on a line as it reports it, even if doing this may slow down NVDA's performance.

By default, NVDA will detect the formatting at the position of the System caret / Review Cursor, and in some instances may detect formatting on the rest of the line, only if it is not going to cause a performance decrease.

Enable this option while proof reading documents in applications such as WordPad, where formatting is important.

##### Line indentation reporting {#DocumentFormattingSettingsLineIndentation}

This option allows you to configure how indentation at the beginning of lines is reported.
The Report line indentation with combo box has four options.

* Off: NVDA will not treat indentation specially.
* Speech: If speech is selected, when the  amount of indentation changes, NVDA will say something like "twelve space" or "four tab."
* Tones: If Tones is selected, when the  amount of  indentation changes, tones indicate the amount of change in indent.
The tone will increase in pitch every space, and for a tab, it will increase in pitch the equivalent of 4 spaces.
* Both Speech and Tones: This option reads indentation using both of the above methods.

If you tick the "Ignore blank lines for line indentation reporting" checkbox, then indentation changes won't be reported for blank lines.
This may be useful when reading a document where blank lines are used to separate indented bloks of text, such as in programming source code.

#### Document Navigation {#DocumentNavigation}

This category allows you to adjust various aspects of document navigation.

##### Paragraph Style {#ParagraphStyle}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Default (Handled by application), Handled by application, Single line break, Multi line break|
|Default |Handled by application|

This combo box allows you to select the paragraph style to be used when navigating by paragraphs with `control+upArrow` and `control+downArrow`.
The available paragraph styles are:

* Handled by application: NVDA will let the application determine the previous or next paragraph, and NVDA will read the new paragraph when navigating.
This style works best when the application supports paragraph navigation natively, and is the default.
* Single line break: NVDA will attempt to determine the previous or next paragraph using a single line break as the paragraph indicator.
This style works best when reading documents in an application which does not natively support paragraph navigation, and paragraphs in the document are marked by a single press of the `enter` key.
* Multi line break: NVDA will attempt to determine the previous or next paragraph using at least one blank line (two presses of the `enter` key) as the paragraph indicator.
This style works best when working with documents which use block paragraphs.
Note that this paragraph style cannot be used in Microsoft Word or Microsoft Outlook, unless you are using UIA to access Microsoft Word controls.

You may toggle through the available paragraph styles from anywhere by assigning a key in the [Input Gestures dialog](#InputGestures).

#### Windows OCR Settings {#Win10OcrSettings}

The settings in this category allow you to configure [Windows OCR](#Win10Ocr).
This category contains the following options:

##### Recognition language {#Win10OcrSettingsRecognitionLanguage}

This combo box allows you to choose the language to be used for text recognition.
To cycle through available languages from anywhere, please assign a custom gesture using the [Input Gestures dialog](#InputGestures).

##### Periodically refresh recognized content {#Win10OcrSettingsAutoRefresh}

When this checkbox is enabled, NVDA will automatically refresh the recognized content when a recognition result has focus.
This can be very useful when you want to monitor constantly changing content, such as when watching a video with subtitles.
The refresh takes place every one and a half seconds.
This option is disabled by default.

#### Advanced Settings {#AdvancedSettings}

Warning! The settings in this category are for advanced users and may cause NVDA to not function correctly if configured in the wrong way.
Only make changes to these settings if you are sure you know what you are doing or if you have been specifically instructed to by an NVDA developer.

##### Making changes to advanced settings {#AdvancedSettingsMakingChanges}

In order to make changes to the advanced settings, the controls must be enabled by confirming, with the checkbox, that you understand the risks of modifying these settings

##### Restoring the default settings {#AdvancedSettingsRestoringDefaults}

The button restores the default values for the settings, even if the confirmation checkbox is not ticked.
After changing settings you may wish to revert to the default values.
This may also be the case if you are unsure if the settings have been changed.

##### Enable loading custom code from Developer Scratchpad Directory {#AdvancedSettingsEnableScratchpad}

When developing add-ons for NVDA, it is useful to be able to test code as you are writing it.
This option when enabled, allows NVDA to load custom appModules, globalPlugins, brailleDisplayDrivers, synthDrivers and vision enhancement providers, from a special developer scratchpad directory in your NVDA user configuration directory.
As their equivalents in add-ons, these modules are loaded when starting NVDA or, in the case of appModules and globalPlugins, when [reloading plugins](#ReloadPlugins).
This option is off by default, ensuring that no untested code is ever run in NVDA with out the user's explicit knowledge.
If you wish to distribute custom code to others, you should package it as an NVDA add-on.

##### Open Developer Scratchpad Directory {#AdvancedSettingsOpenScratchpadDir}

This button opens the directory where you can place custom code while developing it.
This button is only enabled if NVDA is configured to enable loading custom code from the Developer Scratchpad Directory.

##### Registration for UI Automation events and property changes {#AdvancedSettingsSelectiveUIAEventRegistration}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Automatic, Selective, Global|
|Default |Automatic|

This option changes how NVDA registers for events fired by the Microsoft UI Automation accessibility API.
The registration for UI Automation events and property changes combo box has three options:

* Automatic: "selective" on Windows 11 Sun Valley 2 (version 22H2) and later, "global" otherwise.
* Selective: NVDA will limit event registration to the system focus for most events.
If you suffer from performance issues in one or more applications, We recommend you to try this functionality to see whether performance improves.
However, on older versions of Windows, NVDA may have trouble tracking focus in some controls (such as the task manager and emoji panel).
* Global: NVDA registers for many UIA events that are processed and discarded within NVDA itself.
While focus tracking is more reliable in more situations, performance is significantly degraded, especially in applications like Microsoft Visual Studio.

##### Use UI automation to access Microsoft Word document controls {#MSWordUIA}

Configures whether or not NVDA should use the UI Automation accessibility API to access Microsoft Word documents, rather than the older Microsoft Word object model.
This applies to documents in Microsoft word itself, plus messages in Microsoft Outlook.
This setting contains the following values:

* Default (where suitable)
* Only where necessary: where the Microsoft Word object model is not  available at all
* Where suitable: Microsoft Word version 16.0.15000 or higher, or where the Microsoft Word object model is unavailable
* Always: where ever UI automation is available in Microsoft word (no matter how complete).

##### Use UI automation to access Microsoft Excel spreadsheet controls when available {#UseUiaForExcel}

When this option is enabled, NVDA will try to use the Microsoft UI Automation accessibility API in order to fetch information from Microsoft Excel Spreadsheet controls.
This is an experimental feature, and some features of Microsoft Excel may not be available in this mode.
For instance, NVDA's Elements List for listing formulas and comments, and Browse mode quick navigation to jump to form fields on a spreadsheet features are not available.
However, for basic spreadsheet navigating / editing, this option may provide a vast performance improvement.
We still do not recommend that the majority of users turn this on by default, though we do welcome users of Microsoft Excel build 16.0.13522.10000 or higher to test this feature and provide feedback.
Microsoft Excel's UI automation implementation is ever changing, and versions of Microsoft Office older than 16.0.13522.10000 may not expose enough information for this option to be of any use.

##### Use enhanced event processing {#UIAEnhancedEventProcessing}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Default (Enabled), Disabled, Enabled|
|Default |Enabled|

When this option is enabled, NVDA should remain responsive when being flooded with many UI Automation events, e.g. large amounts of text in a terminal.
After changing this option, you will need to restart NVDA for the change to take effect.

##### Windows Console support {#AdvancedSettingsConsoleUIA}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Automatic, UIA when available, Legacy|
|Default |Automatic|

This option selects how NVDA interacts with the Windows Console used by command prompt, PowerShell, and the Windows Subsystem for Linux.
It does not affect the modern Windows Terminal.
In Windows 10 version 1709, Microsoft [added support for its UI Automation API to the console](https://devblogs.microsoft.com/commandline/whats-new-in-windows-console-in-windows-10-fall-creators-update/), bringing vastly improved performance and stability for screen readers that support it.
In situations where UI Automation is unavailable or known to result in an inferior user experience, NVDA's legacy console support is available as a fallback.
The Windows Console support combo box has three options:

* Automatic: Uses UI Automation in the version of Windows Console included with Windows 11 version 22H2 and later.
This option is recommended and set by default.
* UIA when available: Uses UI Automation in consoles if available, even for versions with incomplete or buggy implementations.
While this limited functionality may be useful (and even sufficient for your usage), use of this option is entirely at your own risk and no support for it will be provided.
* Legacy: UI Automation in the Windows Console will be completely disabled.
The legacy fallback will always be used even in situations where UI Automation would provide a superior user experience.
Therefore, selecting this option is not recommended unless you know what you are doing.

##### Use UIA with Microsoft Edge and other Chromium based browsers when available {#ChromiumUIA}

Allows specifying when UIA will be used when it is available in Chromium based browsers such as Microsoft Edge.
UIA support for Chromium based browsers is early in development and may not provide the same level of access as IA2.
The combo box has the following options:

* Default (Only when necessary): The NVDA default, currently this is "Only when necessary". This default may change in the future as the technology matures.
* Only when necessary: When NVDA is unable to inject into the browser process in order to use IA2 and UIA is available, then NVDA will fall back to using UIA.
* Yes: If the browser makes UIA available, NVDA will use it.
* No: Don't use UIA, even if NVDA is unable to inject in process. This may be useful for developers debugging issues with IA2 and want to ensure that NVDA does not fall back to UIA.

##### Annotations {#Annotations}

This group of options is used to enable features which add experimental support for ARIA annotations.
Some of these features may be incomplete.

<!-- KC:beginInclude -->
To "Report summary of any annotation details at the system caret", press NVDA+d.
<!-- KC:endInclude -->

The following options exist:

* "Report 'has details' for structured annotations": enables reporting if the text or control has further details.
* "Report aria-description always":
  When the source of `accDescription` is aria-description, the description is reported.
  This is useful for annotations on the web.
  Note:
  * There are many sources for `accDescription` several have mixed or unreliable semantics.
    Historically AT has not been able to differentiate sources of `accDescription` typically it wasn't spoken due to the mixed semantics.
  * This option is in very early development, it relies on browser features not yet widely available.
  * Expected to work with Chromium 92.0.4479.0+

##### Report live regions {#BrailleLiveRegions}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Default (Enabled), Disabled, Enabled|
|Default |Enabled|

This option selects whether NVDA reports changes in some dynamic web content in Braille.
Disabling this option is equivalent to NVDA's behaviour in versions 2023.1 and earlier, which only reported these content changes in speech.

##### Speak passwords in all enhanced terminals {#AdvancedSettingsWinConsoleSpeakPasswords}

This setting controls whether characters are spoken by [speak typed characters](#KeyboardSettingsSpeakTypedCharacters) or [speak typed words](#KeyboardSettingsSpeakTypedWords) in situations where the screen does not update (such as password entry) in some terminal programs, such as the Windows Console with UI automation support enabled and Mintty.
For security purposes, this setting should be left disabled.
However, you may wish to enable it if you experience performance issues or instability with typed character and/or word reporting in consoles, or work in trusted environments and prefer password announcement.

##### Use enhanced typed character support in legacy Windows Console when available {#AdvancedSettingsKeyboardSupportInLegacy}

This option enables an alternative method for detecting typed characters in legacy Windows consoles.
While it improves performance and prevents some console output from being spelled out, it may be incompatible with some terminal programs.
This feature is available and enabled by default on Windows 10 versions 1607 and later when UI Automation is unavailable or disabled.
Warning: with this option enabled, typed characters that do not appear onscreen, such as passwords, will not be suppressed.
In untrusted environments, you may temporarily disable [speak typed characters](#KeyboardSettingsSpeakTypedCharacters) and [speak typed words](#KeyboardSettingsSpeakTypedWords) when entering passwords.

##### Diff algorithm {#DiffAlgo}

This setting controls how NVDA determines the new text to speak in terminals.
The diff algorithm combo box has three options:

* Automatic: This option causes NVDA to prefer Diff Match Patch in most situations, but fall back to Difflib in problematic applications, such as older versions of the Windows Console and Mintty.
* Diff Match Patch: This option causes NVDA to calculate changes to terminal text by character, even in situations where it is not recommended.
It may improve performance when large volumes of text are written to the console and allow more accurate reporting of changes made in the middle of lines.
However, in some applications, reading of new text may be choppy or inconsistent.
* Difflib: this option causes NVDA to calculate changes to terminal text by line, even in situations where it is not recommended.
It is identical to NVDA's behaviour in versions 2020.4 and earlier.
This setting may stabilize reading of incoming text in some applications.
However, in terminals, when inserting or deleting a character in the middle of a line, the text after the caret will be read out.

##### Speak new text in Windows Terminal via {#WtStrategy}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Default (Diffing), Diffing, UIA notifications|
|Default |Diffing|

This option selects how NVDA determines what text is "new" (and thus what to speak when "report dynamic content changes" is enabled) in Windows Terminal and the WPF Windows Terminal control used in Visual Studio 2022.
It does not affect the Windows Console (`conhost.exe`).
The Speak new text in Windows Terminal combo box has three options:

* Default: This option is currently equivalent to "diffing", but it is anticipated to change once support for UIA notifications is further developed.
* Diffing: This option uses the selected diff algorithm to calculate changes each time the terminal renders new text.
This is identical to NVDA's behaviour in versions 2022.4 and earlier.
* UIA notifications: This option defers the responsibility of determining what text to speak to Windows Terminal itself, meanning that NVDA no longer has to determine what text currently on-screen is "new".
This should markedly improve performance and stability of Windows Terminal, but this feature is not yet complete.
In particular, typed characters that are not displayed on-screen, such as passwords, are reported when this option is selected.
Additionally, contiguous spans of output of over 1,000 characters may not be reported accurately.

##### Attempt to cancel speech for expired focus events {#CancelExpiredFocusSpeech}

This option enables behaviour which attempts to cancel speech for expired focus events.
In particular moving quickly through messages in Gmail with Chrome can cause NVDA to speak outdated information.
This functionality is enabled by default as of NVDA 2021.1.

##### Caret move timeout (in MS) {#AdvancedSettingsCaretMoveTimeout}

This option allows you to configure the number of milliseconds NVDA will wait for the caret (insertion point) to move in editable text controls.
If you find that NVDA seems to be incorrectly tracking the caret E.g. it seems to be always one character behind or is repeating lines, then you may wish to try increasing this value.

##### Report transparency for colors {#ReportTransparentColors}

This option enables reporting when colors are transparent, useful for addon/appModule developers gathering information to improve user experience with a 3rd party application.
Some GDI applications will highlight text with a background color, NVDA (via display model) attempts to report this color.
In some situations, the text background may be entirely transparent, with the text layered on some other GUI element.
With several historically popular GUI APIs, the text may be rendered with a transparent background, but visually the background color is accurate.

##### Use WASAPI for audio output {#WASAPI}

| . {.hideHeaderRow} |.|
|---|---|
|Options |Default (Enabled), Disabled, Enabled|
|Default |Enabled|

This option enables audio output via the Windows Audio Session API (WASAPI).
WASAPI is a more modern audio framework which may improve the responsiveness, performance and stability of NVDA audio output, including both speech and sounds.
After changing this option, you will need to restart NVDA for the change to take effect.
Disabling WASAPI will disable the following options:

* [Volume of NVDA sounds follows voice volume](#SoundVolumeFollowsVoice)
* [Volume of NVDA sounds](#SoundVolume)

##### Debug logging categories {#AdvancedSettingsDebugLoggingCategories}

The checkboxes in this list allow you to enable specific categories of debug messages in NVDA's log.
Logging these messages can result in decreased performance and large log files.
Only turn one of these on if specifically instructed to by an NVDA developer e.g. when debugging why a braille display driver is not functioning correctly.

##### Play a sound for logged errors {#PlayErrorSound}

This option allows you to specify if NVDA will play an error sound in case an error is logged.
Choosing Only in test versions (default) makes NVDA play error sounds only if the current NVDA version is a test version (alpha, beta or run from source).
Choosing Yes allows to enable error sounds whatever your current NVDA version is.

##### Regular expression for text paragraph quick navigation commands {#TextParagraphRegexEdit}

This field allows users to customize regular expression for detecting text paragraphs in browse mode.
The [text paragraph navigation command](#TextNavigationCommand) searches for paragraphs matched by this regular expression.

### miscellaneous Settings {#MiscSettings}

Besides the [NVDA Settings](#NVDASettings) dialog, The Preferences sub-menu of the NVDA Menu contains several other items which are outlined below.

#### Speech dictionaries {#SpeechDictionaries}

The speech dictionaries menu (found in the Preferences menu) contains dialogs that allow you to manage the way NVDA pronounces particular words or phrases.
There are currently three different types of speech dictionaries.
They are:

* Default: rules in this dictionary affect all speech in NVDA.
* Voice: rules in this dictionary affect speech for the synthesizer voice currently being used.
* Temporary: rules in this dictionary affect all speech in NVDA, but only for the current session. These rules are temporary and will be lost if NVDA is restarted.

You need to assign custom gestures using the [Input Gestures dialog](#InputGestures) if you wish to open any of these dictionary dialogs from anywhere.

All dictionary dialogs contain a list of rules which will be used for processing the speech.
The dialog also contains Add, Edit, Remove and Remove all buttons.

To add a new rule to the dictionary, press the Add button, and fill in the fields in the dialog box that appears and then press Ok.
You will then see your new rule in the list of rules.
However, to make sure your rule is actually saved, make sure to press Ok to exit the dictionary dialog completely once you have finished adding/editing rules.

The rules for NVDA's speech dictionaries allow you to change one string of characters into another.
For example, you could create a rule which causes NVDA to say the word "frog" instead of "bird" whenever the word "bird" is encountered.
In the Add rule dialog, the easiest way to do this is to type the word bird in the Pattern field, and the word frog in the Replacement field.
You may also want to type a description of the rule in the Comment field (something like: changes bird to frog).

NVDA's speech dictionaries however are much more powerful than simple word replacement.
The Add rule dialog also contains a checkbox to say whether or not you want the rule to be case sensitive (meaning that NVDA should care whether the characters are uppercase or lowercase.
NVDA ignores case by default).

Finally, a set of radio buttons allows you to tell NVDA whether your pattern should match anywhere, should only match if it is a complete word or should be treated as a "Regular expression".
Setting the pattern to match as a whole word means that the replacement will only be made if the pattern does not occur as part of a larger word.
This condition is met if the characters immediately before and after the word are anything other than a letter, a number, or an underscore, or if there are no characters at all.
Thus, using the earlier example of replacing the word "bird" with "frog", if you were to make this a whole word replacement, it would not match "birds" or "bluebird".

A regular expression is a pattern containing special symbols that allow you to match on more than one character at a time, or match on just numbers, or just letters, as a few examples.
Regular expressions are not covered in this user guide.
For an introductory tutorial, please refer to [Python's Regular Expression Guide](https://docs.python.org/3.11/howto/regex.html).

#### Punctuation/symbol pronunciation {#SymbolPronunciation}

This dialog allows you to change the way punctuation and other symbols are pronounced, as well as the symbol level at which they are spoken.

The language for which symbol pronunciation is being edited will be shown in the dialog's title.
Note that this dialog respects the "Trust voice's language for processing symbols and characters" option found in the [Speech category](#SpeechSettings) of the [NVDA Settings](#NVDASettings) dialog; i.e. it uses the voice language rather than the NVDA global language setting when this option is enabled.

To change a symbol, first select it in the Symbols list.
You can filter the symbols by entering the symbol or a part of the symbol's replacement into the Filter by edit box.

* The Replacement field allows you to change the text that should be spoken in place of this symbol.
* Using the Level field, you can adjust the lowest symbol level at which this symbol should be spoken (none, some, most or all).
You can also set the level to character; in this case the symbol will not be spoken regardless of the symbol level in use, with the following two exceptions:
  * When navigating character by character.
  * When NVDA is spelling any text containing that symbol.
* The Send actual symbol to synthesizer field specifies when the symbol itself (in contrast to its replacement) should be sent to the synthesizer.
This is useful if the symbol causes the synthesizer to pause or change the inflection of the voice.
For example, a comma causes the synthesizer to pause.
There are three options:
  * never: Never send the actual symbol to the synthesizer.
  * always: Always send the actual symbol to the synthesizer.
  * only below symbols' level: Send the actual symbol only if the configured speech symbol level is lower than the level set for this symbol.
  For example, you might use this so that a symbol will have its replacement spoken at higher levels without pausing, while still being indicated with a pause at lower levels.

You can add new symbols by pressing the Add button.
In the dialog that appears, enter the symbol and press the OK button.
Then, change the fields for the new symbol as you would for other symbols.

You can remove a symbol you previously added by pressing the Remove button.

When you are finished, press the OK button to save your changes or the Cancel button to discard them.

In the case of complex symbols, the Replacement field may have to include some group references of the matched text. For instance, for a pattern matching a whole date, \1, \2, and \3 would need to appear in the field, to be replaced by the corresponding parts of the date.
Normal backslashes in the Replacement field should thus be doubled, e.g. "a\\b" should be typed in order to get the "a\b" replacement.

#### Input Gestures {#InputGestures}

In this dialog, you can customize the input gestures (keys on the keyboard, buttons on a braille display, etc.) for NVDA commands.

Only commands that are applicable immediately before the dialog is opened are shown.
For example, if you want to customize commands related to browse mode, you should open the Input Gestures dialog while you are in browse mode.

The tree in this dialog lists all of the applicable NVDA commands grouped by category.
You can filter them by entering one or more words from the command's name into the Filter by edit box in any order.
Any gestures associated with a command are listed beneath the command.

To add an input gesture to a command, select the command and press the Add button.
Then, perform the input gesture you wish to associate; e.g. press a key on the keyboard or a button on a braille display.
Often, a gesture can be interpreted in more than one way.
For example, if you pressed a key on the keyboard, you may wish it to be specific to the current keyboard layout (e.g. desktop or laptop) or you may wish it to apply for all layouts.
In this case, a menu will appear allowing you to select the desired option.

To remove a gesture from a command, select the gesture and press the Remove button.

The Emulated system keyboard keys category contains NVDA commands that emulate keys on the system keyboard.
These emulated system keyboard keys can be used to control a system keyboard right from your braille display.
To add an emulated input gesture, select the Emulated system keyboard keys category and press the Add button.
Then, press the key on the keyboard you wish to emulate.
After that, the key will be available from the Emulated system keyboard keys category and you will be able to assign an input gesture to it as described above.

Note:

* Emulated keys must have gestures assigned in order to persist when saving / closing the dialog.
* An input gesture with modifier keys may not be able to be mapped to an emulated gesture without modifier keys.
For instance, setting the emulated input `a` and configuring an input gesture of `ctrl+m`, may result in the application receiving `ctrl+a`.

When you are finished making changes, press the OK button to save them or the Cancel button to discard them.

### Saving and Reloading the configuration {#SavingAndReloading}

By default NVDA will automatically save your settings on exit.
Note, however, that this option can be changed under the general options in the preferences menu.
To save the settings manually at any time, choose the Save configuration item in the NVDA menu.

If you ever make a mistake with your settings and need to revert back to the saved settings, choose the "revert to saved configuration" item in the NVDA menu.
You can also reset your settings to their original factory defaults by choosing Reset Configuration To Factory Defaults, which is also found in the NVDA menu.

The following NVDA key commands are also useful:
<!-- KC:beginInclude -->

| Name |Desktop key |Laptop key |Description|
|---|---|---|---|
|Save configuration |NVDA+control+c |NVDA+control+c |Saves your current configuration so that it is not lost when you exit NVDA|
|Revert  configuration |NVDA+control+r |NVDA+control+r |Pressing once resets your configuration to when you last saved it. Pressing three times will reset it back to factory defaults.|

<!-- KC:endInclude -->

### Configuration Profiles {#ConfigurationProfiles}

Sometimes, you may wish to have different settings for different situations.
For example, you may wish to have reporting of indentation enabled while you are editing or reporting of font attributes enabled while you are proofreading.
NVDA allows you to do this using configuration profiles.

A configuration profile contains only those settings which are changed while the profile is being edited.
Most settings can be changed in configuration profiles except for those in the General category of the [NVDA Settings](#NVDASettings) dialog, which apply to the entirety of NVDA.

Configuration profiles can be manually activated either from a dialog or using custom added gestures.
They can also be activated automatically due to triggers such as switching to a particular application.

#### Basic Management {#ProfilesBasicManagement}

You manage configuration profiles by selecting "Configuration profiles" in the NVDA menu.
You can also do this using a key command:
<!-- KC:beginInclude -->

* NVDA+control+p: Show the Configuration Profiles dialog.

<!-- KC:endInclude -->

The first control in this dialog is the profile list from which you can select one of the available profiles.
When you open the dialog, the profile you are currently editing is selected.
Additional information is also shown for active profiles, indicating whether they are manually activated, triggered and/or being edited.

To rename or delete a profile, press the Rename or Delete buttons, respectively.

Press the Close button to close the dialog.

#### Creating a Profile {#ProfilesCreating}

To create a profile, press the New button.

In the New Profile dialog, you can enter a name for the profile.
You can also select how this profile should be used.
If you only want to use this profile manually, select Manual activation, which is the default.
Otherwise, select a trigger which should automatically activate this profile.
For convenience, if you haven't entered a name for the profile, selecting a trigger will fill in the name accordingly.
See [below](#ConfigProfileTriggers) for more information about triggers.

Pressing OK will create the profile and close the Configuration Profiles dialog so you can edit it.

#### Manual Activation {#ConfigProfileManual}

You can manually activate a profile by selecting a profile and pressing the Manual activate button.
Once activated, other profiles can still be activated due to triggers, but any settings in the manually activated profile will override them.
For example, if a profile is triggered for the current application and reporting of links is enabled in that profile but disabled it in the manually activated profile, links will not be reported.
However, if you have changed the voice in the triggered profile but have never changed it in the manually activated profile, the voice from the triggered profile will be used.
Any settings you change will be saved in the manually activated profile.
To deactivate a manually activated profile, select it in the Configuration Profiles dialog and press the Manual deactivate button.

#### Triggers {#ConfigProfileTriggers}

Pressing the Triggers button in the Configuration Profiles dialog allows you to change the profiles which should be automatically activated for various triggers.

The Triggers list shows the available triggers, which are as follows:

* Current application: Triggered when you switch to the current application.
* Say all: Triggered while reading with the say all command.

To change the profile which should be automatically activated for a trigger, select the trigger and then select the desired profile from the Profile list.
You can select "(normal configuration)" if you don't want a profile to be used.

Press the Close button to return to the Configuration Profiles dialog.

#### Editing a Profile {#ConfigProfileEditing}

If you have manually activated a profile, any settings you change will be saved to that profile.
Otherwise, any settings you change will be saved to the most recently triggered profile.
For example, if you have associated a profile with the Notepad application and you switch to Notepad, any changed settings will be saved to that profile.
Finally, if there is neither a manually activated nor a triggered profile, any settings you change will be saved to your normal configuration.

To edit the profile associated with say all, you must [manually activate](#ConfigProfileManual) that profile.

#### Temporarily Disabling Triggers {#ConfigProfileDisablingTriggers}

Sometimes, it is useful to temporarily disable all triggers.
For example, you might wish to edit a manually activated profile or your normal configuration without triggered profiles interfering.
You can do this by checking the Temporarily disable all triggers checkbox in the Configuration Profiles dialog.

To toggle disabling triggers from anywhere, please assign a custom gesture using the [Input Gestures dialog](#InputGestures).

#### Activating a profile using input gestures {#ConfigProfileGestures}

For every profile you add, you are able to assign one or more input gestures to activate it.
By default, configuration profiles do not have input gestures assigned.
You can add gestures to activate a profile using the [Input Gestures dialog](#InputGestures).
Every profile has its own entry under the configuration profiles category.
When you rename a profile, any gesture you added previously will still be available.
Removing a profile will automatically delete the gestures associated with it.

### Location of Configuration files {#LocationOfConfigurationFiles}

Portable versions of NVDA store all settings and add-ons in a directory called userConfig, found in the NVDA directory.

Installed versions of NVDA store all settings and add-ons in a special NVDA directory located in your Windows user profile.
This means that each user on the system can have their own NVDA settings.
To open your settings directory from anywhere you can use [Input Gestures dialog](#InputGestures) to add a custom gesture.
In addition for an installed version of NVDA, on the start menu you can go to programs -> NVDA -> explore user configuration directory.

Settings for NVDA when running during sign-in or on UAC screens are stored in the systemConfig directory in NVDA's installation directory.
Usually, this configuration should not be touched.
To change NVDA's configuration during sign-in or on UAC screens, configure NVDA as you wish while signed into Windows, save the configuration, and then press the "use currently saved settings during sign-in and on secure screens" button in the General category of the [NVDA Settings](#NVDASettings) dialog.

## Add-ons and the Add-on Store {#AddonsManager}

Add-ons are software packages which provide new or altered functionality for NVDA.
They are developed by the NVDA community, and external organisations such as commercial vendors.
Add-ons may do any of the following:

* Add or enhance support for certain applications.
* Provide support for extra Braille displays or speech synthesizers.
* Add or change features in NVDA.

NVDA's Add-on Store allows you to browse and manage add-on packages.
All add-ons that are available in the Add-on Store can be downloaded for free.
However, some of them may require users to pay for a license or additional software before they can be used.
Commercial speech synthesizers are an example of this type of add-on.
If you install an add-on with paid components and change your mind about using it, the add-on can be easily removed.

The Add-on Store is accessed from the Tools submenu of the NVDA menu.
To access the Add-on Store from anywhere, assign a custom gesture using the [Input Gestures dialog](#InputGestures).

### Browsing add-ons {#AddonStoreBrowsing}

When opened, the Add-on Store displays a list of add-ons.
If you have not installed an add-on before, the Add-on Store will open to a list of add-ons available to install.
If you have installed add-ons, the list will display currently installed add-ons.

Selecting an add-on, by moving to it with the up and down arrow keys, will display the details for the add-on.
Add-ons have associated actions that you can access through an [actions menu](#AddonStoreActions), such as install, help, disable, and remove.
Available actions will change based on whether the add-on is installed or not, and whether it is enabled or disabled.

#### Add-on list views {#AddonStoreFilterStatus}

There are different views for installed, updatable, available and incompatible add-ons.
To change the view of add-ons, change the active tab of the add-ons list using `ctrl+tab`.
You can also `tab` to the list of views, and move through them with the `leftArrow` and `rightArrow` keys.

#### Filtering for enabled or disabled add-ons {#AddonStoreFilterEnabled}

Normally, an installed add-on is "enabled", meaning that it is running and available within NVDA.
However, some of your installed add-ons may be set to the "disabled" state.
This means that they will not be used, and their functions won't be available during your current NVDA session.
You may have disabled an add-on because it conflicted with another add-on, or with a certain application.
NVDA may also disable certain add-ons, if they are found to be incompatible during an NVDA upgrade; though you will be warned if this is going to happen.
Add-ons can also be disabled if you simply don't need them for a prolonged period, but don't want to uninstall them because you expect to want them again in the future.

The lists of installed and incompatible add-ons can be filtered by their enabled or disabled state.
The default shows both enabled and disabled add-ons.

#### Include incompatible add-ons {#AddonStoreFilterIncompatible}

Available and updatable add-ons can be filtered to include [incompatible add-ons](#incompatibleAddonsManager) that are available to install.

#### Filter add-ons by channel {#AddonStoreFilterChannel}

Add-ons can be distributed through up to four channels:

* Stable: The developer has released this as a tested add-on with a released version of NVDA.
* Beta: This add-on may need further testing, but is released for user feedback.
Suggested for early adopters.
* Dev: This channel is suggested to be used by add-on developers to test unreleased API changes.
NVDA alpha testers may need to use a "Dev" version of their add-ons.
* External: Add-ons installed from external sources, outside of the Add-on Store.

To list add-ons only for specific channels, change the "Channel" filter selection.

#### Searching for add-ons {#AddonStoreFilterSearch}

To search add-ons, use the "Search" text box.
You can reach it by pressing `shift+tab` from the list of add-ons.
Type a keyword or two for the kind of add-on you're looking for, then `tab` to the list of add-ons.
Add-ons will be listed if the search text can be found in the add-on ID, display name, publisher, author or description.

### Add-on actions {#AddonStoreActions}

Add-ons have associated actions, such as install, help, disable, and remove.
For an add-on in the add-on list, these actions can be accessed through a menu opened by pressing the `applications` key, `enter`, right clicking or double clicking the add-on.
This menu can also be accessed through an Actions button in the selected add-on's details.

#### Installing add-ons {#AddonStoreInstalling}

Just because an add-on is available in the NVDA Add-on Store, does not mean that it has been approved or vetted by NV Access or anyone else.
It is very important to only install add-ons from sources you trust.
The functionality of add-ons is unrestricted inside NVDA.
This could include accessing your personal data or even the entire system.

You can install and update add-ons by [browsing Available add-ons](#AddonStoreBrowsing).
Select an add-on from the "Available add-ons" or "Updatable add-ons" tab.
Then use the update, install, or replace action to start the installation.

You can also install multiple add-ons at once.
This can be done by selecting multiple add-ons in the available add-ons tab, then activating the context menu on the selection and choosing the "Install selected add-ons" action.

To install an add-on you have obtained outside of the Add-on Store, press the "Install from external source" button.
This will allow you to browse for an add-on package (`.nvda-addon` file) somewhere on your computer or on a network.
Once you open the add-on package, the installation process will begin.

If NVDA is installed and running on your system, you can also open an add-on file directly from the browser or file system to begin the installation process.

When an add-on is being installed from an external source, NVDA will ask you to confirm the installation.
Once the add-on is installed, NVDA must be restarted for the add-on to start running, although you may postpone restarting NVDA if you have other add-ons to install or update.

#### Removing Add-ons {#AddonStoreRemoving}

To remove an add-on, select the add-on from the list and use the Remove action.
NVDA will ask you to confirm removal.
As with installing, NVDA must be restarted for the add-on to be fully removed.
Until you do, a status of "Pending removal" will be shown for that add-on in the list.
As with installing, you can also remove multiple add-ons at once.

#### Disabling and Enabling Add-ons {#AddonStoreDisablingEnabling}

To disable an add-on, use the "disable" action.
To enable a previously disabled add-on, use the "enable" action.
You can disable an add-on if the add-on status indicates it is  "enabled", or enable it if the add-on is "disabled".
For each use of the enable/disable action, add-on status changes to indicate what will happen when NVDA restarts.
If the add-on was previously "disabled", the status will show "enabled after restart".
If the add-on was previously "enabled", the status will show "disabled after restart".
Just like when you install or remove add-ons, you need to restart NVDA in order for changes to take effect.
You can also enable or disable multiple add-ons at once by selecting multiple add-ons in the available add-ons tab, then activating the context menu on the selection and choosing the appropriate action.

#### Reviewing add-ons and reading reviews {#AddonStoreReviews}

You may want to read reviews by other users who have experienced an add-on, for example before you install it, or as you are learning to use it.
Also, it is helpful to other users to provide feedback about add-ons you have tried.
To read reviews for an add-on, select it, and use the "Community reviews" action.
This links to a GitHub Discussion webpage, where you will be able to read and write reviews for the add-on.
Please be aware that this doesn't replace direct communication with add-on developers.
Instead, the purpose of this feature is to share feedback to help users decide if an add-on may be useful for them.

### Incompatible Add-ons {#incompatibleAddonsManager}

Some older add-ons may no longer be compatible with the version of NVDA that you have.
If you are using an older version of NVDA, some newer add-ons may not be compatible either.
Attempting to install an incompatible add-on will result in an error explaining why the add-on is considered incompatible.

For older add-ons, you can override the incompatibility at your own risk.
Incompatible add-ons may not work with your version of NVDA, and can cause unstable or unexpected behaviour including crashing.
You can override compatibility when enabling or installing an add-on.
If the incompatible add-on causes issues later, you can disable or remove it.

If you are having trouble running NVDA, and you have recently updated or installed an add-on, especially if it is an incompatible add-on, you may want to try running NVDA temporarily with all add-ons disabled.
To restart NVDA with all add-ons disabled, choose the appropriate option when quitting NVDA.
Alternatively, use the [command line option](#CommandLineOptions) `--disable-addons`.

You can browse available incompatible add-ons using the [available and updatable add-ons tabs](#AddonStoreFilterStatus).
You can browse installed incompatible add-ons using the [incompatible add-ons tab](#AddonStoreFilterStatus).

## Extra Tools {#ExtraTools}
### Log Viewer {#LogViewer}

The log viewer, found under Tools in the NVDA menu, allows you to view the logging output that has occurred since the latest session of NVDA was started.

Apart from reading the content, you can also Save a copy of the log file, or refresh the viewer so that it loads new log output generated after the Log viewer was opened.
These actions are available under the Log menu in the log viewer.

The file which is displayed when you open the log viewer is saved on your computer at the file location `%temp%\nvda.log`.
A new log file is created each time NVDA is started.
When this happens, the previous NVDA session's log file is moved to `%temp%\nvda-old.log`.

You can also copy a fragment of the current log file to the clipboard without opening the log viewer.
<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Open log viewer |`NVDA+f1` |Opens the log viewer and displays developer information about the current navigator object.|
|Copy a fragment of the log to the clipboard |`NVDA+control+shift+f1` |When this command is pressed once, it sets a starting point for the log content that should be captured. When pressed a second time, it copies the log content since the start point to your clipboard.|

<!-- KC:endInclude -->

### Speech Viewer {#SpeechViewer}

For sighted software developers or people demoing NVDA to sighted audiences, a floating window is available that allows you to view all the text that NVDA is currently speaking.

To enable the speech viewer, check the "Speech Viewer" menu item under Tools in the NVDA menu.
Uncheck the menu item to disable it.

The speech viewer window contains a check box labelled "Show speech viewer on startup".
If this is checked, the speech viewer will open when NVDA is started.
The speech viewer window will always attempt to re-open with the same dimensions and location as when it was closed.

While the speech viewer is enabled, it constantly updates to show you the most current text being spoken.
However, if you hover your mouse over or focus inside the viewer, NVDA will temporarily stop updating the text, so that you are able to easily select or copy the existing content.

To toggle the speech viewer from anywhere, please assign a custom gesture using the [Input Gestures dialog](#InputGestures).

### Braille Viewer {#BrailleViewer}

For sighted software developers or people demoing NVDA to sighted audiences, a floating window is available that allows you to view braille output, and the text equivalent for each braille character.
The braille viewer can be used at the same time as a physical braille display, it will match the number of cells on the physical device.
While the braille viewer is enabled, it constantly updates to show you the braille that would be displayed on a physical braille display.

To enable the braille viewer, check the "Braille Viewer" menu item under Tools in the NVDA menu.
Uncheck the menu item to disable it.

Physical braille displays typically have buttons to scroll forwards or backwards, to enable scrolling with the braille viewer tool use the [Input Gestures dialog](#InputGestures) to assign keyboard shortcuts which "Scrolls the braille display back" and "Scrolls the braille display forward"

The braille viewer window contains a check box labelled "Show braille viewer on startup".
If this is checked, the braille viewer will open when NVDA is started.
The braille viewer window will always attempt to re-open with the same dimensions and location as when it was closed.

The braille viewer window contains a check box labeled "Hover for cell routing", the default is unchecked.
If checked, hovering the mouse over a braille cell will enable trigger the "route to braille cell" command for that cell.
This is often used to move the caret or trigger the action for a control.
This can be useful for testing NVDA is able to correctly reverse map a from braille cell.
To prevent unintentionally routing to cells, the command is delayed.
The mouse must hover until the cell turns green.
The cell will start as a light yellow colour, transition to orange, then suddenly become green.

To toggle the braille viewer from anywhere, please assign a custom gesture using the [Input Gestures dialog](#InputGestures).

### Python Console {#PythonConsole}

The NVDA Python console, found under Tools in the NVDA menu, is a development tool which is useful for debugging, general inspection of NVDA internals or inspection of the accessibility hierarchy of an application.
For more information, please see the [NVDA Developer Guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html).

### Add-on Store {#AddonStoreMenuItem}

This will open the [NVDA Add-on Store](#AddonsManager).
For more information, read the in-depth section: [Add-ons and the Add-on Store](#AddonsManager).

### Create portable copy {#CreatePortableCopy}

This will open a dialog which allows you to create a portable copy of NVDA out of the installed version.
Either way, when running a portable copy of NVDA, in the extra tool sub menu the menu item will be called "install NVDA on this PC" instead of "create portable copy).

The dialog to create a portable copy of NVDA or to install NVDA on this PC will prompt you to choose a folder path in which NVDA should create the portable copy or in which NVDA should be installed.

In this dialog you can enable or disable the following:

* Copy current user configuration (this includes the files in %appdata%\roaming\NVDA or in the user configuration of your portable copy and also includes add-ons and other modules)
* Start the new portable copy after creation or start NVDA after installation (starts NVDA automatically after the portable copy creation or the installation)

### Run COM registration fixing tool... {#RunCOMRegistrationFixingTool}

Installing and uninstalling programs on a computer can, in certain cases, cause COM DLL files to get unregistered.
As COM Interfaces such as IAccessible depend on correct COM DLL registrations, issues can appear in case the correct registration is missing.

This can happen i.e. after installing and uninstalling Adobe Reader, Math Player and other programs.

The missing registration can cause issues in browsers, desktop apps, task bar and other interfaces.

Specifically, following issues can be solved by running this tool:

* NVDA reports "unknown" when navigating in browsers such as Firefox, Thunderbird etc.
* NVDA fails to switch between focus mode and browse mode
* NVDA is very slow when navigating in browsers while using browse mode
* And possibly other issues.

### Reload plugins {#ReloadPlugins}

This item, once activated, reloads app modules and global plugins without restarting NVDA, which can be useful for developers.
App modules manage how NVDA interacts with specific applications.
Global plugins manage how NVDA interacts with all applications.

The following NVDA key commands may also be useful:
<!-- KC:beginInclude -->

| Name |Key |Description|
|---|---|---|
|Reload plugins |`NVDA+control+f3` |Reloads NVDA's global plugins and app modules.|
|Report loaded app module and executable |`NVDA+control+f1` |Report the name of the app module, if any, and the name of the executable associated with the application which has the keyboard focus.|

<!-- KC:endInclude -->

## Supported Speech Synthesizers {#SupportedSpeechSynths}

This section contains information about the speech synthesizers supported by NVDA.
For an even more extensive list of  free and commercial synthesizers that you can purchase and download for use with NVDA, please see the [extra voices page](https://github.com/nvaccess/nvda/wiki/ExtraVoices).

### eSpeak NG {#eSpeakNG}

The [eSpeak NG](https://github.com/espeak-ng/espeak-ng) synthesizer is built directly into NVDA and does not require any other special drivers or components to be installed.
On Windows 8.1 NVDA uses eSpeak NG by default ([Windows OneCore](#OneCore) is used in Windows 10 and later by default).
As this synthesizer is built into NVDA, this is a great choice for when running NVDA off a USB thumb drive on other systems.

Each voice that comes with eSpeak NG speaks a different language.
There are over 43 different languages supported by eSpeak NG.

There are also many variants which can be chosen to alter the sound of the voice.

### Microsoft Speech API version 4 (SAPI 4) {#SAPI4}

SAPI 4 is an older Microsoft standard for software speech synthesizers.
NVDA still supports this for users who already have SAPI 4 synthesizers installed.
However, Microsoft no longer support this and needed components are no longer available from Microsoft.

When using this synthesizer with NVDA, the available voices (accessed from the [Speech category](#SpeechSettings) of the [NVDA Settings](#NVDASettings) dialog or by the [Synth Settings Ring](#SynthSettingsRing)) will contain all the voices from all the installed SAPI 4 engines found on your system.

### Microsoft Speech API version 5 (SAPI 5) {#SAPI5}

SAPI 5 is a Microsoft standard for software speech synthesizers.
Many speech synthesizers that comply with this standard may be purchased or downloaded for free from various companies and websites, though your system will probably already come with at least one SAPI 5 voice preinstalled.
When using this synthesizer with NVDA, the available voices (accessed from the [Speech category](#SpeechSettings) of the [NVDA Settings](#NVDASettings) dialog or by the [Synth Settings Ring](#SynthSettingsRing)) will contain all the voices from all the installed SAPI 5 engines found on your system.

### Microsoft Speech Platform {#MicrosoftSpeechPlatform}

The Microsoft Speech Platform provides voices for many languages which are normally used in the development of server-based speech applications.
These voices can also be used with NVDA.

To use these voices, you will need to install two components:

* [Microsoft Speech Platform - Runtime (Version 11), x86](https://www.microsoft.com/download/en/details.aspx?id=27225)
* [Microsoft Speech Platform - Runtime Languages (Version 11)](https://www.microsoft.com/download/en/details.aspx?id=27224)
  * This page includes many files for both speech recognition and text-to-speech.
 Choose the files containing the TTS data for the desired languages/voices.
 For example, the file MSSpeech_TTS_en-US_ZiraPro.msi is a U.S. English voice.

### Windows OneCore Voices {#OneCore}

Windows 10 and later includes voices known as "OneCore" or "mobile" voices.
Voices are provided for many languages, and they are more responsive than the Microsoft voices available using Microsoft Speech API version 5.
On Windows 10 and later, NVDA uses Windows OneCore voices by default ([eSpeak NG](#eSpeakNG) is used in other releases).

To add new Windows OneCore voices, go to "Speech Settings", within Windows system settings.
Use the "Add voices" option and search for the desired language.
Many languages include multiple variants.
"United Kingdom" and "Australia" are two of the English variants.
"France", "Canada" and "Switzerland" are French variants available.
Search for the broader language (such as English or French), then locate the variant in the list.
Select any languages desired and use the "add" button to add them.
Once added, restart NVDA.

Please see [Supported languages and voices](https://support.microsoft.com/en-us/windows/appendix-a-supported-languages-and-voices-4486e345-7730-53da-fcfe-55cc64300f01) for a list of available voices.

## Supported Braille Displays {#SupportedBrailleDisplays}

This section contains information about the Braille displays supported by NVDA.

### Displays supporting automatic detection in the background {#AutomaticDetection}

NVDA has the ability to detect many braille displays in the background automatically, either via USB or bluetooth.
This behaviour is achieved by selecting the Automatic option as the preferred braille display from NVDA's [Braille Settings dialog](#BrailleSettings).
This option is selected by default.

The following displays support this automatic detection functionality.

* Handy Tech displays
* Baum/Humanware/APH/Orbit braille displays
* HumanWare Brailliant BI/B series
* HumanWare BrailleNote
* SuperBraille
* Optelec ALVA 6 series
* HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille Series
* Eurobraille Esys/Esytime/Iris displays
* Nattiq nBraille displays
* Seika Notetaker: MiniSeika (16, 24 cells), V6, and V6Pro (40 cells)
* Tivomatic Caiku Albatross 46/80 displays
* Any Display that supports the Standard HID Braille protocol

### Freedom Scientific Focus/PAC Mate Series {#FreedomScientificFocus}

All Focus and PAC Mate displays from [Freedom Scientific](https://www.freedomscientific.com/) are supported when connected via USB or bluetooth.
You will need the Freedom Scientific braille display drivers installed on your system.
If you do not have them already, you can obtain them from the [Focus Blue Braille Display Driver page](https://support.freedomscientific.com/Downloads/Focus/FocusBlueBrailleDisplayDriver).
Although this page only mentions the Focus Blue display, the drivers support all Freedom Scientific Focus and Pacmate displays.

By default, NVDA can automatically detect and connect to these displays either via USB or bluetooth.
However, when configuring the display, you can explicitly select "USB" or "Bluetooth" ports to restrict the connection type to be used.
This might be useful if you want to connect the focus display to NVDA using bluetooth, but still be able to charge it using USB power from your computer.
NVDA's automatic braille display detection will also recognize the display on USB or Bluetooth.

Following are the key assignments for this display with NVDA.
Please see the display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |topRouting1 (first cell on display)|
|Scroll braille display forward |topRouting20/40/80 (last cell on display)|
|Scroll braille display back |leftAdvanceBar|
|Scroll braille display forward |rightAdvanceBar|
|Toggle braille tethered to |leftGDFButton+rightGDFButton|
|Toggle left wiz wheel action |leftWizWheelPress|
|Move back using left wiz wheel action |leftWizWheelUp|
|Move forward using left wiz wheel action |leftWizWheelDown|
|Toggle right wiz wheel action |rightWizWheelPress|
|Move back using right wiz wheel action |rightWizWheelUp|
|Move forward using right wiz wheel action |rightWizWheelDown|
|Route to braille cell |routing|
|shift+tab key |brailleSpaceBar+dot1+dot2|
|tab key |brailleSpaceBar+dot4+dot5|
|upArrow key |brailleSpaceBar+dot1|
|downArrow key |brailleSpaceBar+dot4|
|control+leftArrow key |brailleSpaceBar+dot2|
|control+rightArrow key |brailleSpaceBar+dot5|
|leftArrow |brailleSpaceBar+dot3|
|rightArrow key |brailleSpaceBar+dot6|
|home key |brailleSpaceBar+dot1+dot3|
|end key |brailleSpaceBar+dot4+dot6|
|control+home key |brailleSpaceBar+dot1+dot2+dot3|
|control+end key |brailleSpaceBar+dot4+dot5+dot6|
|alt key |brailleSpaceBar+dot1+dot3+dot4|
|alt+tab key |brailleSpaceBar+dot2+dot3+dot4+dot5|
|alt+shift+tab key |brailleSpaceBar+dot1+dot2+dot5+dot6|
|windows+tab key |brailleSpaceBar+dot2+dot3+dot4|
|escape key |brailleSpaceBar+dot1+dot5|
|windows key |brailleSpaceBar+dot2+dot4+dot5+dot6|
|space key |brailleSpaceBar|
|Toggle control key |brailleSpaceBar+dot3+dot8|
|Toggle alt key |brailleSpaceBar+dot6+dot8|
|Toggle windows key |brailleSpaceBar+dot4+dot8|
|Toggle NVDA key |brailleSpaceBar+dot5+dot8|
|Toggle shift key |brailleSpaceBar+dot7+dot8|
|Toggle control and shift keys |brailleSpaceBar+dot3+dot7+dot8|
|Toggle alt and shift keys |brailleSpaceBar+dot6+dot7+dot8|
|Toggle windows and shift keys |brailleSpaceBar+dot4+dot7+dot8|
|Toggle NVDA and shift keys |brailleSpaceBar+dot5+dot7+dot8|
|Toggle control and alt keys |brailleSpaceBar+dot3+dot6+dot8|
|Toggle control, alt, and shift keys |brailleSpaceBar+dot3+dot6+dot7+dot8|
|windows+d key (minimize all applications) |brailleSpaceBar+dot1+dot2+dot3+dot4+dot5+dot6|
|Report Current Line |brailleSpaceBar+dot1+dot4|
|NVDA menu |brailleSpaceBar+dot1+dot3+dot4+dot5|

For newer Focus models that contain rocker bar keys (focus 40, focus 80 and focus blue):

| Name |Key|
|---|---|
|Move braille display to previous line |leftRockerBarUp, rightRockerBarUp|
|Move braille display to next line |leftRockerBarDown, rightRockerBarDown|

For Focus 80 only:

| Name |Key|
|---|---|
|Scroll braille display back |leftBumperBarUp, rightBumperBarUp|
|Scroll braille display forward |leftBumperBarDown, rightBumperBarDown|

<!-- KC:endInclude -->

### Optelec ALVA 6 series/protocol converter {#OptelecALVA}

Both the ALVA BC640 and BC680 displays from [Optelec](https://www.optelec.com/) are supported when connected via USB or bluetooth.
Alternatively, you can connect an older Optelec display, such as a Braille Voyager, using a protocol converter supplied by Optelec.
You do not need any specific drivers to be installed to use these displays.
Just plug in the display and configure NVDA to use it.

Note: NVDA might be unable to use an ALVA BC6 display over Bluetooth when it is paired using the ALVA Bluetooth utility.
When you have paired your device using this utility and NVDA is unable to detect your device, we recommend you to pair your ALVA display the regular way using the Windows Bluetooth settings.

Note: while some of these displays do have a braille keyboard, they handle translation from braille to text themselves by default.
This means that NVDA's braille input system is not in use in the default situation (i.e. the input braille table setting has no effect).
For ALVA displays with recent firmware, it is possible to disable this HID keyboard simulation using an input gesture.

Following are key assignments for this display with NVDA.
Please see the display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |t1, etouch1|
|Move braille display to previous line |t2|
|Move to current focus |t3|
|Move braille display to next line |t4|
|Scroll braille display forward |t5, etouch3|
|Route to braille cell |routing|
|Report text formatting under braille cell |secondary routing|
|Toggle HID keyboard simulation |t1+spEnter|
|Move to top line in review |t1+t2|
|Move to bottom line in review |t4+t5|
|Toggle braille tethered to |t1+t3|
|Report title |etouch2|
|Report status bar |etouch4|
|shift+tab key |sp1|
|alt key |sp2, alt|
|escape key |sp3|
|tab key |sp4|
|upArrow key |spUp|
|downArrow key |spDown|
|leftArrow key |spLeft|
|rightArrow key |spRight|
|enter key |spEnter, enter|
|Report date/time |sp2+sp3|
|NVDA Menu |sp1+sp3|
|windows+d key (minimize all applications) |sp1+sp4|
|windows+b key (focus system tray) |sp3+sp4|
|windows key |sp1+sp2, windows|
|alt+tab key |sp2+sp4|
|control+home key |t3+spUp|
|control+end key |t3+spDown|
|home key |t3+spLeft|
|end key |t3+spRight|
|control key |control|

<!-- KC:endInclude -->

### Handy Tech Displays {#HandyTech}

NVDA supports most displays from [Handy Tech](https://www.handytech.de/) when connected via USB, serial port or bluetooth.
For older USB displays, you will need to install the USB drivers from Handy Tech on your system.

The following displays are not supported out of the box, but can be used via [Handy Tech's universal driver](https://handytech.de/en/service/downloads-and-manuals/handy-tech-software/braille-display-drivers) and NVDA add-on:

* Braillino
* Bookworm
* Modular displays with firmware version 1.13 or lower. Please note that the firmware of this displays can be updated.

Following are the key assignments for Handy Tech displays with NVDA.
Please see the display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |left, up, b3|
|Scroll braille display forward |right, down, b6|
|Move braille display to previous line |b4|
|Move braille display to next line |b5|
|Route to braille cell |routing|
|shift+tab key |esc, left triple action key up+down|
|alt key |b2+b4+b5|
|escape key |b4+b6|
|tab key |enter, right triple action key up+down|
|enter key |esc+enter, left+right triple action key up+down, joystickAction|
|upArrow key |joystickUp|
|downArrow key |joystickDown|
|leftArrow key |joystickLeft|
|rightArrow key |joystickRight|
|NVDA Menu |b2+b4+b5+b6|
|Toggle braille tethered to |b2|
|Toggle the braille cursor |b1|
|Toggle focus context presentation |b7|
|Toggle braille input |space+b1+b3+b4 (space+capital B)|

<!-- KC:endInclude -->

### MDV Lilli {#MDVLilli}

The Lilli braille display available from [MDV](https://www.mdvbologna.it/) is supported.
You do not need any specific drivers to be installed to use this display.
Just plug in the display and configure NVDA to use it.

This display does not support NVDA's automatic background braille display detection functionality.

Following are the key assignments for this display with NVDA.
Please see the display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display backward |LF|
|Scroll braille display forward |RG|
|Move braille display to previous line |UP|
|Move braille display to next line |DN|
|Route to braille cell |route|
|shift+tab key |SLF|
|tab key |SRG|
|alt+tab key |SDN|
|alt+shift+tab key |SUP|

<!-- KC:endInclude -->

### Baum/Humanware/APH/Orbit Braille Displays {#Baum}

Several [Baum](https://www.visiobraille.de/index.php?article_id=1&clang=2), [HumanWare](https://www.humanware.com/), [APH](https://www.aph.org/) and [Orbit](https://www.orbitresearch.com/) displays are supported when connected via USB, bluetooth or serial.
These include:

* Baum: SuperVario, PocketVario, VarioUltra, Pronto!, SuperVario2, Vario 340
* HumanWare: Brailliant, BrailleConnect, Brailliant2
* APH: Refreshabraille
* Orbit: Orbit Reader 20

Some other displays manufactured by Baum may also work, though this has not been tested.

If connecting via USB to displays which do not use HID, you must first install the USB drivers provided by the manufacturer.
The VarioUltra and Pronto! use HID.
The Refreshabraille and Orbit Reader 20 can use HID if configured appropriately.

The USB serial mode of the Orbit Reader 20 is currently only supported in Windows 10 and later.
USB HID should generally be used instead.

Following are the key assignments for these displays with NVDA.
Please see your display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |`d2`|
|Scroll braille display forward |`d5`|
|Move braille display to previous line |`d1`|
|Move braille display to next line |`d3`|
|Route to braille cell |`routing`|
|`shift+tab` key |`space+dot1+dot3`|
|`tab` key |`space+dot4+dot6`|
|`alt` key |`space+dot1+dot3+dot4` (`space+m`)|
|`escape` key |`space+dot1+dot5` (`space+e`)|
|`windows` key |`space+dot3+dot4`|
|`alt+tab` key |`space+dot2+dot3+dot4+dot5` (`space+t`)|
|NVDA Menu |`space+dot1+dot3+dot4+dot5` (`space+n`)|
|`windows+d` key (minimize all applications) |`space+dot1+dot4+dot5` (`space+d`)|
|Say all |`space+dot1+dot2+dot3+dot4+dot5+dot6`|

For displays which have a joystick:

| Name |Key|
|---|---|
|upArrow key |up|
|downArrow key |down|
|leftArrow key |left|
|rightArrow key |right|
|enter key |select|

<!-- KC:endInclude -->

### hedo ProfiLine USB {#HedoProfiLine}

The hedo ProfiLine USB from [hedo Reha-Technik](https://www.hedo.de/) is supported.
You must first install the USB drivers provided by the manufacturer.

This display does not yet support NVDA's automatic background braille display detection functionality.

Following are the key assignments for this display with NVDA.
Please see the display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |K1|
|Scroll braille display forward |K3|
|Move braille display to previous line |B2|
|Move braille display to next line |B5|
|Route to braille cell |routing|
|Toggle braille tethered to |K2|
|Say all |B6|

<!-- KC:endInclude -->

### hedo MobilLine USB {#HedoMobilLine}

The hedo MobilLine USB from [hedo Reha-Technik](https://www.hedo.de/) is supported.
You must first install the USB drivers provided by the manufacturer.

This display does not yet support NVDA's automatic background braille display detection functionality.

Following are the key assignments for this display with NVDA.
Please see the display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |K1|
|Scroll braille display forward |K3|
|Move braille display to previous line |B2|
|Move braille display to next line |B5|
|Route to braille cell |routing|
|Toggle braille tethered to |K2|
|Say all |B6|

<!-- KC:endInclude -->

### HumanWare Brailliant BI/B Series / BrailleNote Touch {#HumanWareBrailliant}

The Brailliant BI and B series of displays  from [HumanWare](https://www.humanware.com/), including the BI 14, BI 32, BI 20X, BI 40, BI 40X and B 80, are supported when connected via USB or bluetooth.
If connecting via USB with the protocol set to HumanWare, you must first install the USB drivers provided by the manufacturer.
USB drivers are not required if the protocol is set to OpenBraille.

The following extra devices are also supported (and do not require any special drivers to be installed):

* APH Mantis Q40
* APH Chameleon 20
* Humanware BrailleOne
* NLS eReader

Following are the key assignments for  the Brailliant BI/B and BrailleNote touch displays with NVDA.
Please see the display's documentation for descriptions of where these keys can be found.

#### Key assignments for All models {#HumanWareBrailliantKeyAssignmentForAllModels}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Move braille display to previous line |up|
|Move braille display to next line |down|
|Route to braille cell |routing|
|Toggle braille tethered to |up+down|
|upArrow key |space+dot1|
|downArrow key |space+dot4|
|leftArrow key |space+dot3|
|rightArrow key |space+dot6|
|shift+tab key |space+dot1+dot3|
|tab key |space+dot4+dot6|
|alt key |space+dot1+dot3+dot4 (space+m)|
|escape key |space+dot1+dot5 (space+e)|
|enter key |dot8|
|windows key |space+dot3+dot4|
|alt+tab key |space+dot2+dot3+dot4+dot5 (space+t)|
|NVDA Menu |space+dot1+dot3+dot4+dot5 (space+n)|
|windows+d key (minimize all applications) |space+dot1+dot4+dot5 (space+d)|
|Say all |space+dot1+dot2+dot3+dot4+dot5+dot6|

<!-- KC:endInclude -->

#### Key assignments for Brailliant BI 32, BI 40 and B 80 {#HumanWareBrailliantKeyAssignmentForBI32BI40AndB80}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|NVDA Menu |c1+c3+c4+c5 (command n)|
|windows+d key (minimize all applications) |c1+c4+c5 (command d)|
|Say all |c1+c2+c3+c4+c5+c6|

<!-- KC:endInclude -->

#### Key assignments for Brailliant BI 14 {#HumanWareBrailliantKeyAssignmentForBI14}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|up arrow key |joystick up|
|down arrow key |joystick down|
|left arrow key |joystick left|
|right arrow key |joystick right|
|enter key |joystick action|

<!-- KC:endInclude -->

### HIMS Braille Sense/Braille EDGE/Smart Beetle/Sync Braille Series {#Hims}

NVDA supports Braille Sense, Braille EDGE, Smart Beetle and Sync Braille displays from [Hims](https://www.hims-inc.com/) when connected via USB or bluetooth.
If connecting via USB, you will need to install the [USB drivers from HIMS](http://www.himsintl.com/upload/HIMS_USB_Driver_v25.zip) on your system.

Following are the key assignments for these displays with NVDA.
Please see the display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Route to braille cell |routing|
|Scroll braille display back |leftSideScrollUp, rightSideScrollUp, leftSideScroll|
|Scroll braille display forward |leftSideScrollDown, rightSideScrollDown, rightSideScroll|
|Move braille display to previous line |leftSideScrollUp+rightSideScrollUp|
|Move braille display to next line |leftSideScrollDown+rightSideScrollDown|
|Move to previous line in review |rightSideUpArrow|
|Move to next line in review |rightSideDownArrow|
|Move to previous character in review |rightSideLeftArrow|
|Move to next character in review |rightSideRightArrow|
|Move to current focus |leftSideScrollUp+leftSideScrollDown, rightSideScrollUp+rightSideScrollDown, leftSideScroll+rightSideScroll|
|control key |smartbeetle:f1, brailleedge:f3|
|windows key |f7, smartbeetle:f2|
|alt key |dot1+dot3+dot4+space, f2, smartbeetle:f3, brailleedge:f4|
|shift key |f5|
|insert key |dot2+dot4+space, f6|
|applications key |dot1+dot2+dot3+dot4+space, f8|
|Caps Lock key |dot1+dot3+dot6+space|
|tab key |dot4+dot5+space, f3, brailleedge:f2|
|shift+alt+tab key |f2+f3+f1|
|alt+tab key |f2+f3|
|shift+tab key |dot1+dot2+space|
|end key |dot4+dot6+space|
|control+end key |dot4+dot5+dot6+space|
|home key |dot1+dot3+space, smartbeetle:f4|
|control+home key |dot1+dot2+dot3+space|
|alt+f4 key |dot1+dot3+dot5+dot6+space|
|leftArrow key |dot3+space, leftSideLeftArrow|
|control+shift+leftArrow key |dot2+dot8+space+f1|
|control+leftArrow key |dot2+space|
|shift+alt+leftArrow key |dot2+dot7+f1|
|`alt+leftArrow` |`dot2+dot7+space`|
|rightArrow key |dot6+space, leftSideRightArrow|
|control+shift+rightArrow key |dot5+dot8+space+f1|
|control+rightArrow key |dot5+space|
|shift+alt+rightArrow key |dot5+dot7+f1|
|`alt+rightArrow` |`dot5+dot7+space`|
|pageUp key |dot1+dot2+dot6+space|
|control+pageUp key |dot1+dot2+dot6+dot8+space|
|upArrow key |dot1+space, leftSideUpArrow|
|control+shift+upArrow key |dot2+dot3+dot8+space+f1|
|control+upArrow key |dot2+dot3+space|
|shift+alt+upArrow key |dot2+dot3+dot7+f1|
|`alt+upArrow` |`dot2+dot3+dot7+space`|
|shift+upArrow key |leftSideScrollDown+space|
|pageDown key |dot3+dot4+dot5+space|
|control+pageDown key |dot3+dot4+dot5+dot8+space|
|downArrow key |dot4+space, leftSideDownArrow|
|control+shift+downArrow key |dot5+dot6+dot8+space+f1|
|control+downArrow key |dot5+dot6+space|
|shift+alt+downArrow key |dot5+dot6+dot7+f1|
|`alt+downArrow` |`dot5+dot6+dot7+space`|
|shift+downArrow key |space+rightSideScrollDown|
|escape key |dot1+dot5+space, f4, brailleedge:f1|
|delete key |dot1+dot3+dot5+space, dot1+dot4+dot5+space|
|f1 key |dot1+dot2+dot5+space|
|f3 key |dot1+dot4+dot8+space|
|f4 key |dot7+f3|
|windows+b key |dot1+dot2+f1|
|windows+d key |dot1+dot4+dot5+f1|
|control+insert key |smartbeetle:f1+rightSideScroll|
|alt+insert key |smartbeetle:f3+rightSideScroll|

<!-- KC:endInclude -->

### Seika Braille Displays {#Seika}

The following Seika Braille displays from Nippon Telesoft are supported in two groups with different functionality:

* [Seika Version 3, 4, and 5 (40 cells), Seika80 (80 cells)](#SeikaBrailleDisplays)
* [MiniSeika (16, 24 cells), V6, and V6Pro (40 cells)](#SeikaNotetaker)

You can find more information about the displays on their [Demo and Driver Download page](https://en.seika-braille.com/down/index.html).

#### Seika Version 3, 4, and 5 (40 cells), Seika80 (80 cells) {#SeikaBrailleDisplays}

* These displays do not yet support NVDA's automatic background braille display detection functionality.
* Select "Seika Braille Displays" to manually configure
* A device drivers must be installed before using Seika v3/4/5/80.
The drivers are [provided by the manufacturer](https://en.seika-braille.com/down/index.html).

The Seika Braille Display key assignments follow.
Please see the display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Move braille display to previous line |b3|
|Move braille display to next line |b4|
|Toggle braille tethered to |b5|
|Say all |b6|
|tab |b1|
|shift+tab |b2|
|alt+tab |b1+b2|
|NVDA Menu |left+right|
|Route to braille cell |routing|

<!-- KC:endInclude -->

#### MiniSeika (16, 24 cells), V6, and V6Pro (40 cells) {#SeikaNotetaker}

* NVDA's automatic background braille display detection functionality is supported via USB and Bluetooth.
* Select "Seika Notetaker" or "auto" to configure.
* No extra drivers are required when using a Seika Notetaker braille display.

The Seika Notetaker key assignments follow.
Please see the display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Say all |space+Backspace|
|NVDA Menu |Left+Right|
|Move braille display to previous line |LJ up|
|Move braille display to next line |LJ down|
|Toggle braille tethered to |LJ center|
|tab |LJ right|
|shift+tab |LJ left|
|upArrow key |RJ up|
|downArrow key |RJ down|
|leftArrow key |RJ left|
|rightArrow key |RJ right|
|Route to braille cell |routing|
|shift+upArrow key |Space+RJ up, Backspace+RJ up|
|shift+downArrow key |Space+RJ down, Backspace+RJ down|
|shift+leftArrow key |Space+RJ left, Backspace+RJ left|
|shift+rightArrow key |Space+RJ right, Backspace+RJ right|
|enter key |RJ center, dot8|
|escape key |Space+RJ center|
|windows key |Backspace+RJ center|
|space key |Space, Backspace|
|backspace key |dot7|
|pageup key |space+LJ right|
|pagedown key |space+LJ left|
|home key |space+LJ up|
|end key |space+LJ down|
|control+home key |backspace+LJ up|
|control+end key |backspace+LJ down|

### Papenmeier BRAILLEX Newer Models {#Papenmeier}

The following Braille displays are supported:

* BRAILLEX EL 40c, EL 80c, EL 20c, EL 60c (USB)
* BRAILLEX EL 40s, EL 80s, EL 2d80s, EL 70s, EL 66s (USB)
* BRAILLEX Trio (USB and bluetooth)
* BRAILLEX Live 20, BRAILLEX Live and BRAILLEX Live Plus (USB and bluetooth)

These displays do not support NVDA's automatic background braille display detection functionality.
There is an option in the display's USB driver which can cause an issue with loading the display.
Please try the following:

1. Please make sure that you have installed the [latest driver](https://www.papenmeier-rehatechnik.de/en/service/downloadcenter/software/articles/software-braille-devices.html).
1. Open the Windows Device Manager.
1. Scroll down the list to "USB Controllers" or "USB Devices".
1. Select "Papenmeier Braillex USB Device".
1. Open the properties and switch to the "Advanced" tab.
Sometimes the "Advanced" tab doesn't appear.
If this is the case, disconnect the braille display from the computer, exit NVDA, wait a moment and reconnect the braille display.
Repeat this 4 to 5 times if necessary.
If the "Advanced" tab is still not displayed, please restart the computer.
1. Disable the "Load VCP" option.

Most devices have an Easy Access Bar (EAB) that allows intuitive and fast operation.
The EAB can be moved in four directions where generally each direction has two switches.
The C and Live series are the only exceptions to this rule.

The c-series and some other displays have two routing rows whereby the upper row is used to report formatting information.
Holding one of the upper routing keys and pressing the EAB on c-series devices emulates the second switch state.
The live series displays have one routing row only and the EAB has one step per direction.
The second step may be emulated by pressing one of the routing keys and pressing the EAB in the corresponding direction.
Pressing and holding the up, down, right and left keys (or EAB) causes the corresponding action to be repeated.

Generally, the following keys are available on these braille displays:

| Name |Key|
|---|---|
|l1 |Left front key|
|l2 |Left rear key|
|r1 |Right front key|
|r2 |Right rear key|
|up |1 Step up|
|up2 |2 Steps up|
|left |1 Step left|
|left2 |2 Steps left|
|right |1 Step right|
|right2 |2 Steps right|
|dn |1 Step down|
|dn2 |2 Steps down|

Following are the Papenmeier command assignments for NVDA:
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Move braille display to previous line |up|
|Move braille display to next line |dn|
|Route to braille cell |routing|
|Report current character in review |l1|
|Activate current navigator object |l2|
|Toggle braille tethered to |r2|
|Report title |l1+up|
|Report Status Bar |l2+down|
|Move to containing object |up2|
|Move to first contained object |dn2|
|Move to previous object |left2|
|Move to next object |right2|
|Report text formatting under braille cell |upper routing row|

<!-- KC:endInclude -->

The Trio model has four additional keys which are in front of the braille keyboard.
These are (ordered from left to right):

* left thumb key (lt)
* space
* space
* right thumb key (rt)

Currently, the right thumb key is not in use.
The inner keys are both mapped to space.

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|escape key |space with dot 7|
|upArrow key |space with dot 2|
|leftArrow key |space with dot 1|
|rightArrow key |space with dot 4|
|downArrow |space with dot 5|
|control key |lt+dot2|
|alt key |lt+dot3|
|control+escape key |space with dot 1 2 3 4 5 6|
|tab key |space with dot 3 7|

<!-- KC:endInclude -->

### Papenmeier Braille BRAILLEX Older Models {#PapenmeierOld}

The following Braille displays are supported:

* BRAILLEX EL 80, EL 2D-80, EL 40 P
* BRAILLEX Tiny, 2D Screen

Note that these displays can only be connected via a serial port.
Due to this, these displays do not support NVDA's automatic background braille display detection functionality.
You should select the port to which the display is connected after you have chosen this driver in the [Select Braille Display](#SelectBrailleDisplay) dialog.

Some of these devices have an Easy Access Bar (EAB) that allows intuitive and fast operation.
The EAB can be moved in four directions where generally each direction has two switches.
Pressing and holding the up, down, right and left keys (or EAB) causes the corresponding action to be repeated.
Older devices do not have an EAB; front keys are used instead.

Generally, the following keys are available on braille displays:

| Name |Key|
|---|---|
|l1 |Left front key|
|l2 |Left rear key|
|r1 |Right front key|
|r2 |Right rear key|
|up |1 Step up|
|up2 |2 Steps up|
|left |1 Step left|
|left2 |2 Steps left|
|right |1 Step right|
|right2 |2 Steps right|
|dn |1 Step down|
|dn2 |2 Steps down|

Following are the Papenmeier command assignments for NVDA:

<!-- KC:beginInclude -->
Devices with EAB:

| Name |Key|
|---|---|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Move braille display to previous line |up|
|Move braille display to next line |dn|
|Route to braille cell |routing|
|Report current character in review |l1|
|Activate current navigator object |l2|
|Report title |l1up|
|Report Status Bar |l2down|
|Move to containing object |up2|
|Move to first contained object |dn2|
|Move to next object |right2|
|Move to previous object |left2|
|Report text formatting under braille cell |upper routing strip|

BRAILLEX Tiny:

| Name |Key|
|---|---|
|Report current character in review |l1|
|Activate current navigator object |l2|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Move braille display to previous line |up|
|Move braille display to next line |dn|
|Toggle braille tethered to |r2|
|Move to containing object |r1+up|
|Move to first contained object |r1+dn|
|Move to previous object |r1+left|
|Move to next object |r1+right|
|Report text formatting under braille cell |upper routing strip|
|Report title |l1+up|
|Report status bar |l2+down|

BRAILLEX 2D Screen:

| Name |Key|
|---|---|
|Report current character in review |l1|
|Activate current navigator object |l2|
|Toggle braille tethered to |r2|
|Report text formatting under braille cell |upper routing strip|
|Move braille display to previous line |up|
|Scroll braille display back |left|
|Scroll braille display forward |right|
|Move braille display to next line |dn|
|Move to next object |left2|
|Move to containing object |up2|
|Move to first contained object |dn2|
|Move to previous object |right2|

<!-- KC:endInclude -->

### HumanWare BrailleNote {#HumanWareBrailleNote}

NVDA supports the BrailleNote notetakers from [Humanware](https://www.humanware.com) when acting as a display terminal for a screen reader.
The following models are supported:

* BrailleNote Classic (serial connection only)
* BrailleNote PK (Serial and bluetooth connections)
* BrailleNote MPower (Serial and bluetooth connections)
* BrailleNote Apex (USB and Bluetooth connections)

For BrailleNote Touch, please refer to  the [Brailliant BI Series / BrailleNote Touch](#HumanWareBrailliant) section.

Except for BrailleNote PK, both braille (BT) and QWERTY (QT) keyboards are supported.
For BrailleNote QT, PC keyboard emulation isn't supported.
You can also enter braille dots using the QT keyboard.
Please check the braille terminal section of the BrailleNote manual guide for details.

If your device supports more than one type of connection, when connecting your BrailleNote to NVDA, you must set the braille terminal port in braille terminal options.
Please check the BrailleNote manual for details.
In NVDA, you may also need to set the port in the [Select Braille Display](#SelectBrailleDisplay) dialog.
If you are connecting via USB or bluetooth, you can set the port to "Automatic", "USB" or "Bluetooth", depending on the available choices.
If connecting using a legacy serial port (or a USB to serial converter) or if none of the previous options appear, you must explicitly choose the communication port to be used from the list of hardware ports.

Before connecting your BrailleNote Apex using its USB client interface, you must install the drivers provided by HumanWare.

On the BrailleNote Apex BT, you can use the scroll wheel located between dots 1 and 4 for various NVDA commands.
The wheel consists of four directional dots, a centre click button, and a wheel that spins clockwise or counterclockwise.

Following are the BrailleNote command assignments for NVDA.
Please check your BrailleNote's documentation to find where these keys are located.

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |back|
|Scroll braille display forward |advance|
|Move braille display to previous line |previous|
|Move braille display to next line |next|
|Route to braille cell |routing|
|NVDA menu |space+dot1+dot3+dot4+dot5 (space+n)|
|Toggle braille tethered to |previous+next|
|Up arrow key |space+dot1|
|Down arrow key |space+dot4|
|Left Arrow key |space+dot3|
|Right arrow key |space+dot6|
|Page up key |space+dot1+dot3|
|Page down key |space+dot4+dot6|
|Home key |space+dot1+dot2|
|End key |space+dot4+dot5|
|Control+home keys |space+dot1+dot2+dot3|
|Control+end keys |space+dot4+dot5+dot6|
|Space key |space|
|Enter |space+dot8|
|Backspace |space+dot7|
|Tab key |space+dot2+dot3+dot4+dot5 (space+t)|
|Shift+tab keys |space+dot1+dot2+dot5+dot6|
|Windows key |space+dot2+dot4+dot5+dot6 (space+w)|
|Alt key |space+dot1+dot3+dot4 (space+m)|
|Toggle input help |space+dot2+dot3+dot6 (space+lower h)|

Following are commands assigned to BrailleNote QT when it is not in braille input mode.

| Name |Key|
|---|---|
|NVDA menu |read+n|
|Up arrow key |upArrow|
|Down arrow key |downArrow|
|Left Arrow key |leftArrow|
|Right arrow key |rightArrow|
|Page up key |function+upArrow|
|Page down key |function+downArrow|
|Home key |function+leftArrow|
|End key |function+rightArrow|
|Control+home keys |read+t|
|Control+end keys |read+b|
|Enter key |enter|
|Backspace key |backspace|
|Tab key |tab|
|Shift+tab keys |shift+tab|
|Windows key |read+w|
|Alt key |read+m|
|Toggle input help |read+1|

Following are commands assigned to the scroll wheel:

| Name |Key|
|---|---|
|Up arrow key |upArrow|
|Down arrow key |downArrow|
|Left Arrow key |leftArrow|
|Right arrow key |rightArrow|
|Enter key |centre button|
|Tab key |scroll wheel clockwise|
|Shift+tab keys |scroll wheel counterclockwise|

<!-- KC:endInclude -->

### EcoBraille {#EcoBraille}

NVDA supports EcoBraille displays from [ONCE](https://www.once.es/).
The following models are supported:

* EcoBraille 20
* EcoBraille 40
* EcoBraille 80
* EcoBraille Plus

In NVDA, you can set the serial port to which the display is connected in the [Select Braille Display](#SelectBrailleDisplay) dialog.
These displays do not support NVDA's automatic background braille display detection functionality.

Following are the key assignments for EcoBraille displays.
Please see the [EcoBraille documentation](ftp://ftp.once.es/pub/utt/bibliotecnia/Lineas_Braille/ECO/) for descriptions of where these keys can be found.

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |T2|
|Scroll braille display forward |T4|
|Move braille display to previous line |T1|
|Move braille display to next line |T5|
|Route to braille cell |Routing|
|Activate current navigator object |T3|
|Switch to next review mode |F1|
|Move to containing object |F2|
|Switch to previous review mode |F3|
|Move to previous object |F4|
|Report current object |F5|
|Move to next object |F6|
|Move to focus object |F7|
|Move to first contained object |F8|
|Move System focus or caret to current review position |F9|
|Report review cursor location |F0|
|Toggle braille tethered to |A|

<!-- KC:endInclude -->

### SuperBraille {#SuperBraille}

The SuperBraille device, mostly available in Taiwan, can be connected to by either USB or serial.
As the SuperBraille does not have any physical typing keys or scrolling buttons, all input must be performed via a standard computer keyboard.
Due to this, and to maintain compatibility with other screen readers in Taiwan, two key bindings for scrolling the braille display have been provided:
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |numpadMinus|
|Scroll braille display forward |numpadPlus|

<!-- KC:endInclude -->

### Eurobraille displays {#Eurobraille}

The b.book, b.note, Esys, Esytime and Iris displays from Eurobraille are supported by NVDA.
These devices have a braille keyboard with 10 keys.
Please refer to the display's documentation for descriptions of these keys.
Of the two keys placed like a space bar, the left key is corresponding to the backspace key and the right key to the space key.

These devices are connected via USB and have one stand-alone USB keyboard.
It is possible to enable/disable this keyboard by toggling "HID Keyboard simulation" using an input gesture.
The braille keyboard functions described directly below is when "HID Keyboard simulation" is disabled.

#### Braille keyboard functions {#EurobrailleBraille}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Erase the last entered braille cell or character |`backspace`|
|Translate any braille input and press the enter key |`backspace+space`|
|Toggle `NVDA` key |`dot3+dot5+space`|
|`insert` key |`dot1+dot3+dot5+space`, `dot3+dot4+dot5+space`|
|`delete` key |`dot3+dot6+space`|
|`home` key |`dot1+dot2+dot3+space`|
|`end` key |`dot4+dot5+dot6+space`|
|`leftArrow` key |`dot2+space`|
|`rightArrow` key |`dot5+space`|
|`upArrow` key |`dot1+space`|
|`downArrow` key |`dot6+space`|
|`pageUp` key |`dot1+dot3+space`|
|`pageDown` key |`dot4+dot6+space`|
|`numpad1` key |`dot1+dot6+backspace`|
|`numpad2` key |`dot1+dot2+dot6+backspace`|
|`numpad3` key |`dot1+dot4+dot6+backspace`|
|`numpad4` key |`dot1+dot4+dot5+dot6+backspace`|
|`numpad5` key |`dot1+dot5+dot6+backspace`|
|`numpad6` key |`dot1+dot2+dot4+dot6+backspace`|
|`numpad7` key |`dot1+dot2+dot4+dot5+dot6+backspace`|
|`numpad8` key |`dot1+dot2+dot5+dot6+backspace`|
|`numpad9` key |`dot2+dot4+dot6+backspace`|
|`numpadInsert` key |`dot3+dot4+dot5+dot6+backspace`|
|`numpadDecimal` key |`dot2+backspace`|
|`numpadDivide` key |`dot3+dot4+backspace`|
|`numpadMultiply` key |`dot3+dot5+backspace`|
|`numpadMinus` key |`dot3+dot6+backspace`|
|`numpadPlus` key |`dot2+dot3+dot5+backspace`|
|`numpadEnter` key |`dot3+dot4+dot5+backspace`|
|`escape` key |`dot1+dot2+dot4+dot5+space`, `l2`|
|`tab` key |`dot2+dot5+dot6+space`, `l3`|
|`shift+tab` keys |`dot2+dot3+dot5+space`|
|`printScreen` key |`dot1+dot3+dot4+dot6+space`|
|`pause` key |`dot1+dot4+space`|
|`applications` key |`dot5+dot6+backspace`|
|`f1` key |`dot1+backspace`|
|`f2` key |`dot1+dot2+backspace`|
|`f3` key |`dot1+dot4+backspace`|
|`f4` key |`dot1+dot4+dot5+backspace`|
|`f5` key |`dot1+dot5+backspace`|
|`f6` key |`dot1+dot2+dot4+backspace`|
|`f7` key |`dot1+dot2+dot4+dot5+backspace`|
|`f8` key |`dot1+dot2+dot5+backspace`|
|`f9` key |`dot2+dot4+backspace`|
|`f10` key |`dot2+dot4+dot5+backspace`|
|`f11` key |`dot1+dot3+backspace`|
|`f12` key |`dot1+dot2+dot3+backspace`|
|`windows` key |`dot1+dot2+dot4+dot5+dot6+space`|
|Toggle `windows` key |`dot1+dot2+dot3+dot4+backspace`, `dot2+dot4+dot5+dot6+space`|
|`capsLock` key |`dot7+backspace`, `dot8+backspace`|
|`numLock` key |`dot3+backspace`, `dot6+backspace`|
|`shift` key |`dot7+space`|
|Toggle `shift` key |`dot1+dot7+space`, `dot4+dot7+space`|
|`control` key |`dot7+dot8+space`|
|Toggle `control` key |`dot1+dot7+dot8+space`, `dot4+dot7+dot8+space`|
|`alt` key |`dot8+space`|
|Toggle `alt` key |`dot1+dot8+space`, `dot4+dot8+space`|
|Toggle HID Keyboard simulation |`switch1Left+joystick1Down`, `switch1Right+joystick1Down`|

<!-- KC:endInclude -->

#### b.book keyboard commands {#Eurobraillebbook}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |`backward`|
|Scroll braille display forward |`forward`|
|Move to current focus |`backward+forward`|
|Route to braille cell |`routing`|
|`leftArrow` key |`joystick2Left`|
|`rightArrow` key |`joystick2Right`|
|`upArrow` key |`joystick2Up`|
|`downArrow` key |`joystick2Down`|
|`enter` key |`joystick2Center`|
|`escape` key |`c1`|
|`tab` key |`c2`|
|Toggle `shift` key |`c3`|
|Toggle `control` key |`c4`|
|Toggle `alt` key |`c5`|
|Toggle `NVDA` key |`c6`|
|`control+Home` key |`c1+c2+c3`|
|`control+End` key |`c4+c5+c6`|

<!-- KC:endInclude -->

#### b.note keyboard commands {#Eurobraillebnote}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |`leftKeypadLeft`|
|Scroll braille display forward |`leftKeypadRight`|
|Route to braille cell |`routing`|
|Report text formatting under braille cell |`doubleRouting`|
|Move to next line in review |`leftKeypadDown`|
|Switch to previous review mode |`leftKeypadLeft+leftKeypadUp`|
|Switch to next review mode |`leftKeypadRight+leftKeypadDown`|
|`leftArrow` key |`rightKeypadLeft`|
|`rightArrow` key |`rightKeypadRight`|
|`upArrow` key |`rightKeypadUp`|
|`downArrow` key |`rightKeypadDown`|
|`control+home` key |`rightKeypadLeft+rightKeypadUp`|
|`control+end` key |`rightKeypadLeft+rightKeypadUp`|

<!-- KC:endInclude -->

#### Esys keyboard commands {#Eurobrailleesys}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |`switch1Left`|
|Scroll braille display forward |`switch1Right`|
|Move to current focus |`switch1Center`|
|Route to braille cell |`routing`|
|Report text formatting under braille cell |`doubleRouting`|
|Move to previous line in review |`joystick1Up`|
|Move to next line in review |`joystick1Down`|
|Move to previous character in review |`joystick1Left`|
|Move to next character in review |`joystick1Right`|
|`leftArrow` key |`joystick2Left`|
|`rightArrow` key |`joystick2Right`|
|`upArrow` key |`joystick2Up`|
|`downArrow` key |`joystick2Down`|
|`enter` key |`joystick2Center`|

<!-- KC:endInclude -->

#### Esytime keyboard commands {#EurobrailleEsytime}

<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |`l1`|
|Scroll braille display forward |`l8`|
|Move to current focus |`l1+l8`|
|Route to braille cell |`routing`|
|Report text formatting under braille cell |`doubleRouting`|
|Move to previous line in review |`joystick1Up`|
|Move to next line in review |`joystick1Down`|
|Move to previous character in review |`joystick1Left`|
|Move to next character in review |`joystick1Right`|
|`leftArrow` key |`joystick2Left`|
|`rightArrow` key |`joystick2Right`|
|`upArrow` key |`joystick2Up`|
|`downArrow` key |`joystick2Down`|
|`enter` key |`joystick2Center`|
|`escape` key |`l2`|
|`tab` key |`l3`|
|Toggle `shift` key |`l4`|
|Toggle `control` key |`l5`|
|Toggle `alt` key |`l6`|
|Toggle `NVDA` key |`l7`|
|`control+home` key |`l1+l2+l3`, `l2+l3+l4`|
|`control+end` key |`l6+l7+l8`, `l5+l6+l7`|
|Toggle HID Keyboard simulation |`l1+joystick1Down`, `l8+joystick1Down`|

<!-- KC:endInclude -->

### Nattiq nBraille Displays {#NattiqTechnologies}

NVDA supports displays from [Nattiq Technologies](https://www.nattiq.com/) when connected via USB.
Windows 10 and later detects the Braille Displays once connected, you may need to install USB drivers if using older versions of Windows (below Win10).
You can get them from the manufacturer's website.

Following are the key assignments for Nattiq Technologies displays with NVDA.
Please see the display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |up|
|Scroll braille display forward |down|
|Move braille display to previous line |left|
|Move braille display to next line |right|
|Route to braille cell |routing|

<!-- KC:endInclude -->

### BRLTTY {#BRLTTY}

[BRLTTY](https://www.brltty.app/) is a separate program which can be used to support many more braille displays.
In order to use this, you need to install [BRLTTY for Windows](https://www.brltty.app/download.html).
You should download and install the latest installer package, which will be named, for example, brltty-win-4.2-2.exe.
When configuring the display and port to use, be sure to pay close attention to the instructions, especially if you are using a USB display and already have the manufacturer's drivers installed.

For displays which have a braille keyboard, BRLTTY currently handles braille input itself.
Therefore, NVDA's braille input table setting is not relevant.

BRLTTY is not involved in NVDA's automatic background braille display detection functionality.

Following are the BRLTTY command assignments for NVDA.
Please see the [BRLTTY key binding lists](https://brltty.app/doc/KeyBindings/) for information about how BRLTTY commands are mapped to controls on braille displays.
<!-- KC:beginInclude -->

| Name |BRLTTY command|
|---|---|
|Scroll braille display back |`fwinlt` (go left one window)|
|Scroll braille display forward |`fwinrt` (go right one window)|
|Move braille display to previous line |`lnup` (go up one line)|
|Move braille display to next line |`lndn` (go down one line)|
|Route to braille cell |`route` (bring cursor to character)|
|Toggle input help |`learn` (enter/leave command learn mode)|
|Open the NVDA menu |`prefmenu` (enter/leave preferences menu)|
|Revert configuration |`prefload` (restore preferences from disk)|
|Save configuration |`prefsave` (save preferences to disk)|
|Report time |`time` (show current date and time)|
|Speak the line where the review cursor is located |`say_line` (speak current line)|
|Say all using review cursor |`say_below` (speak from current line through bottom of screen)|

<!-- KC:endInclude -->

### Tivomatic Caiku Albatross 46/80 {#Albatross}

The Caiku Albatross devices, which were manufactured by Tivomatic and available in Finland, can be connected to by either USB or serial.
You do not need any specific drivers to be installed to use these displays.
Just plug in the display and configure NVDA to use it.

Note: Baud rate 19200 is strongly recommended.
If required, switch Baud rate setting value to 19200 from the braille device's menu.
Although the driver supports 9600 baud rate, it has no way to control what baud rate the display uses.
Because 19200 is the display default baud rate, the driver tries it at first.
If baud rates are not the same, the driver may behave unexpectedly.

Following are key assignments for these displays with NVDA.
Please see the display's documentation for descriptions of where these keys can be found.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Move to top line in review |`home1`, `home2`|
|Move to bottom line in review |`end1`, `end2`|
|Sets the navigator object to the current focus |`eCursor1`, `eCursor2`|
|Move to current focus |`cursor1`, `cursor2`|
|Moves the mouse pointer to the current navigator object |`home1+home2`|
|Sets the navigator object to the current object under the mouse pointer and speaks it |`end1+end2`|
|Moves focus to current navigator object |`eCursor1+eCursor2`|
|Toggle braille tethered to |`cursor1+cursor2`|
|Move braille display to previous line |`up1`, `up2`, `up3`|
|Move braille display to next line |`down1`, `down2`, `down3`|
|Scroll braille display back |`left`, `lWheelLeft`, `rWheelLeft`|
|Scroll braille display forward |`right`, `lWheelRight`, `rWheelRight`|
|Route to braille cell |`routing`|
|Report text formatting under braille cell |`secondary routing`|
|Toggle the way context information is presented in braille |`attribute1+attribute3`|
|Cycles between speech modes |`attribute2+attribute4`|
|Switches to the previous review mode (e.g. object, document or screen) |`f1`|
|Switches to the next review mode (e.g. object, document or screen) |`f2`|
|Moves the navigator object to the object containing it |`f3`|
|Moves the navigator object to the first object inside it |`f4`|
|Moves the navigator object to the previous object |`f5`|
|Moves the navigator object to the next object |`f6`|
|Reports the current navigator object |`f7`|
|Reports information about the location of the text or object at the review cursor |`f8`|
|Shows braille settings |`f1+home1`, `f9+home2`|
|Reads status bar and moves navigator object into it |`f1+end1`, `f9+end2`|
|Cycle the braille cursor shape |`f1+eCursor1`, `f9+eCursor2`|
|Toggle the braille cursor |`f1+cursor1`, `f9+cursor2`|
|Cycle the braille show messages mode |`f1+f2`, `f9+f10`|
|Cycle the braille show selection state |`f1+f5`, `f9+f14`|
|Cycle the "braille move system caret when routing review cursor" states |`f1+f3`, `f9+f11`|
|Performs the default action on the current navigator object |`f7+f8`|
|Reports date/time |`f9`|
|Reports battery status and time remaining if AC is not plugged in |`f10`|
|Reports title |`f11`|
|Reports status bar |`f12`|
|Reports the current line under the application cursor |`f13`|
|Say all |`f14`|
|Reports current character under review cursor |`f15`|
|Reports the line of the current navigator object where the review cursor is situated |`f16`|
|Speaks the word of the current navigator object where the review cursor is situated |`f15+f16`|
|Moves the review cursor to the previous line of the current navigator object and speaks it |`lWheelUp`, `rWheelUp`|
|Moves the review cursor to the next line of the current navigator object and speaks it |`lWheelDown`, `rWheelDown`|
|`Windows+d` key (minimize all applications) |`attribute1`|
|`Windows+e` key (this computer) |`attribute2`|
|`Windows+b` key (focus system tray) |`attribute3`|
|`Windows+i` key (Windows settings) |`attribute4`|

<!-- KC:endInclude -->

### Standard HID Braille displays {#HIDBraille}

This is an experimental driver for the new Standard HID Braille Specification, agreed upon in 2018 by Microsoft, Google, Apple and several assistive technology companies including NV Access.
The hope is that all future Braille Display models created by any manufacturer, will use this standard protocol which will remove the need for manufacturer-specific Braille drivers.

NVDA's automatic braille display detection will also recognize any display that supports this protocol.

Following are the current key assignments for these displays.
<!-- KC:beginInclude -->

| Name |Key|
|---|---|
|Scroll braille display back |pan left or rocker up|
|Scroll braille display forward |pan right or rocker down|
|Route to braille cell |routing set 1|
|Toggle braille tethered to |up+down|
|upArrow key |joystick up, dpad up or space+dot1|
|downArrow key |joystick down, dpad down or space+dot4|
|leftArrow key |space+dot3, joystick left  or dpad left|
|rightArrow key |space+dot6, joystick right or dpad right|
|shift+tab key |space+dot1+dot3|
|tab key |space+dot4+dot6|
|alt key |space+dot1+dot3+dot4 (space+m)|
|escape key |space+dot1+dot5 (space+e)|
|enter key |dot8, joystick center or dpad center|
|windows key |space+dot3+dot4|
|alt+tab key |space+dot2+dot3+dot4+dot5 (space+t)|
|NVDA Menu |space+dot1+dot3+dot4+dot5 (space+n)|
|windows+d key (minimize all applications) |space+dot1+dot4+dot5 (space+d)|
|Say all |space+dot1+dot2+dot3+dot4+dot5+dot6|

<!-- KC:endInclude -->

## Advanced Topics {#AdvancedTopics}
### Secure Mode {#SecureMode}

System administrators may wish to configure NVDA to restrict unauthorized system access.
NVDA allows the installation of custom add-ons, which can execute arbitrary code, including when NVDA is elevated to administrator privileges.
NVDA also allows users to execute arbitrary code through the NVDA Python Console.
NVDA secure mode prevents users from modifying their NVDA configuration, and otherwise limits unauthorized system access.

NVDA runs in secure mode when executed on [secure screens](#SecureScreens), unless the `serviceDebug` [system wide parameter](#SystemWideParameters) is enabled.
To force NVDA to always start in secure mode, set the `forceSecureMode` [system wide parameter](#SystemWideParameters).
NVDA can also be started in secure mode with the `-s` [command line option](#CommandLineOptions).

Secure mode disables:

* Saving configuration and other settings to disk
* Saving the gesture map to disk
* [Configuration Profile](#ConfigurationProfiles) features such as creation, deletion, renaming profiles etc.
* Loading custom configuration folders using [the `-c` command line option](#CommandLineOptions)
* Updating NVDA and creating portable copies
* The [Add-on Store](#AddonsManager)
* The [NVDA Python console](#PythonConsole)
* The [Log Viewer](#LogViewer) and logging
* The [Braille Viewer](#BrailleViewer) and [Speech Viewer](#SpeechViewer)
* Opening external documents from the NVDA menu, such as the user guide or contributors file.

Installed copies of NVDA store their configuration including add-ons in `%APPDATA%\nvda`.
To prevent NVDA users from modifying their configuration or add-ons directly, user access to this folder must also be restricted.

Secure mode is ineffective for portable copies of NVDA.
This limitation also applies to the temporary copy of NVDA which runs when launching the installer.
In secure environments, a user being able to run a portable executable is the same security risk regardless of secure mode.
It is expected that system administrators restrict unauthorized software from running on their systems, including portable copies of NVDA.

NVDA users often rely on configuring their NVDA profile to suit their needs.
This may include installing and configuring custom add-ons, which should be vetted independently to NVDA.
Secure mode freezes changes to NVDA configuration, so please ensure that NVDA is configured appropriately before forcing secure mode.

### Secure Screens {#SecureScreens}

NVDA runs in [secure mode](#SecureMode) when executed on secure screens unless the `serviceDebug` [system wide parameter](#SystemWideParameters) is enabled.

When running from a secure screen, NVDA uses a system profile for preferences.
NVDA user preferences can be copied [for use in secure screens](#GeneralSettingsCopySettings).

Secure screens include:

* The Windows sign-in screen
* The User Access Control dialog, active when performing an action as an administrator
  * This includes installing programs

### Command Line Options {#CommandLineOptions}

NVDA can accept one or more additional options when it starts which alter its behaviour.
You can pass as many options as you need.
These options can be passed when starting from a shortcut (in the shortcut properties), from the Run dialog (Start Menu -> Run or Windows+r) or from a Windows command console.
Options should be separated from the name of NVDA's executable file and from other options by spaces.
For example, a useful option is `--disable-addons`, which tells NVDA to suspend all running add-ons.
This allows you to determine whether a problem is caused by an add-on and to recover from serious problems caused by add-ons.

As an example, you can exit the currently running copy of NVDA by entering the following in the Run dialog:

    nvda -q

Some of the command line options have a short and a long version, while some of them have only a long version.
For those which have a short version, you can combine them like this:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -mc CONFIGPATH` |This will start NVDA with startup sounds and message disabled, and the specified configuration|
|`nvda -mc CONFIGPATH --disable-addons` |Same as above, but with add-ons disabled|

Some of the command line options accept additional parameters; e.g. how detailed the logging should be or the path to the user configuration directory.
Those parameters should be placed after the option, separated from the option by a space when using the short version or an equals sign (`=`) when using the long version; e.g.:

| . {.hideHeaderRow} |.|
|---|---|
|`nvda -l 10` |Tells NVDA to start with log level set to debug|
|`nvda --log-file=c:\nvda.log` |Tells NVDA to write its log to `c:\nvda.log`|
|`nvda --log-level=20 -f c:\nvda.log` |Tells NVDA to start with log level set to info and to write its log to `c:\nvda.log`|

Following are the command line options for NVDA:

| Short |Long |Description|
|---|---|---|
|`-h` |`--help` |show command line help and exit|
|`-q` |`--quit` |Quit already running copy of NVDA|
|`-k` |`--check-running` |Report whether NVDA is running via the exit code; 0 if running, 1 if not running|
|`-f LOGFILENAME` |`--log-file=LOGFILENAME` |The file where log messages should be written to. Logging is always disabled if secure mode is enabled.|
|`-l LOGLEVEL` |`--log-level=LOGLEVEL` |The lowest level of message logged (debug 10, input/output 12, debug warning 15, info 20, disabled 100). Logging is always disabled if secure mode is enabled.|
|`-c CONFIGPATH` |`--config-path=CONFIGPATH` |The path where all settings for NVDA are stored. The default value is forced if secure mode is enabled.|
|None |`--lang=LANGUAGE` |Override the configured NVDA language. Set to "Windows" for current user default, "en" for English, etc.|
|`-m` |`--minimal` |No sounds, no interface, no start message, etc.|
|`-s` |`--secure` |Starts NVDA in [Secure Mode](#SecureMode)|
|None |`--disable-addons` |Add-ons will have no effect|
|None |`--debug-logging` |Enable debug level logging just for this run. This setting will override any other log level ( `--loglevel`, `-l`) argument given, including no logging option.|
|None |`--no-logging` |Disable logging altogether while using NVDA. This setting can be overridden if a log level (`--loglevel`, `-l`) is specified from command line or if debug logging is turned on.|
|None |`--no-sr-flag` |Don't change the global system screen reader flag|
|None |`--install` |Installs NVDA (starting the newly installed copy)|
|None |`--install-silent` |Silently installs NVDA (does not start the newly installed copy)|
|None |`--enable-start-on-logon=True|False` |When installing, enable NVDA's [Use NVDA during Windows sign-in](#StartAtWindowsLogon)|
|None |`--copy-portable-config` |When installing, copy the portable configuration from the provided path (`--config-path`, `-c`) to the current user account|
|None |`--create-portable` |Creates a portable copy of NVDA (starting the newly created copy). Requires `--portable-path` to be specified|
|None |`--create-portable-silent` |Creates a portable copy of NVDA (does not start the newly installed copy). Requires `--portable-path` to be specified|
|None |`--portable-path=PORTABLEPATH` |The path where a portable copy will be created|

### System Wide Parameters {#SystemWideParameters}

NVDA allows some values to be set in the system registry which alter the system wide behaviour of NVDA.
These values are stored in the registry under one of the following keys:

* 32-bit system: `HKEY_LOCAL_MACHINE\SOFTWARE\nvda`
* 64-bit system: `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\nvda`

The following values can be set under this registry key:

| Name |Type |Possible values |Description|
|---|---|---|---|
|`configInLocalAppData` |DWORD |0 (default) to disable, 1 to enable |If enabled, stores the NVDA user configuration in the local application data instead of the roaming application data|
|`serviceDebug` |DWORD |0 (default) to disable, 1 to enable |If enabled, disables [Secure Mode](#SecureMode) on [secure screens](#SecureScreens). Due to several major security implications, the use of this option is strongly discouraged|
|`forceSecureMode` |DWORD |0 (default) to disable, 1 to enable |If enabled, forces [Secure Mode](#SecureMode) to be enabled when running NVDA.|

## Further Information {#FurtherInformation}

If you require further information or assistance regarding NVDA, please visit the [NVDA web site](NVDA_URL).
Here, you can find additional documentation, as well as technical support and community resources.
This site also provides information and resources concerning NVDA development.
