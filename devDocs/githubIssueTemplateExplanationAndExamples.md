# Creating new issues on the NVDA project

This page is meant to serve as an explanation for how to fill out our
[Github issue templates](https://github.com/nvaccess/nvda/blob/master/.github/ISSUE_TEMPLATE/).

The template uses github markdown, to provide formatting for headings, lists, quotes etc.
If you are not familiar, please take some time to learn about 
[Github markdown](https://guides.github.com/features/mastering-markdown/)

**Warning**: In all but exceptional circumstances we require this template to be completed.
Your issue will likely be closed if this template has not been followed.

We currently have two templates, both are described on this page:
- for bug reports
- for feature requests.

## General information
The following information applies to all issues (bug reports, new features, even pull requests).
At the start of the template there is an HTML comment block which points to this wiki page, it can
be left in place and will not appear once the issue is saved.
Feel free to delete it.

### Attachments / Images

It's important to include any files that are required to reproduce an issue.
This might be a required file for an office suite, or a link to a code playground such as CodePen or
JSFiddle, or perhaps a standalone HTML file.
Github does not allow all
[file types to be attached](https://help.github.com/articles/file-attachments-on-issues-and-pull-requests/),
however, zip files are allowed, so you can always zip your file and attach that instead.

#### Logs
In most cases an NVDA log file is incredibly helpful when trying to understand/fix an issue, please
remember to attach one.
More [instructions are available on the wiki](https://github.com/nvaccess/nvda/wiki/LogFilesAndCrashDumps). If you are getting a crash dump file (nvda_crash.dmp) please also include it.

#### Screenshots
While we welcome **images/screenshots** to help explain a problem, be aware that many of the 
developers of NVDA are blind and will greatly appreciate this image being described in text.
Most tools allow you to copy text out of them.

### Tips
* Consider swapping to the preview tab in order to read through your issue at any stage to confirm
  the issue reads as expected.
* If you have trouble following this template, or with the initial investigation that is required,
  please politely ask for assistance from the fantastic community of people on the
  [NVDA users mailing list](https://github.com/nvaccess/nvda-community/wiki/Connect#international-users-mailing-list-english)


## Feature Request template

After the HTML comment ([discussed earlier](#General_information)), you may provide a brief overview
of the issue.
Then fill in each of the following headings which match those that are found in the template, with a
short description of how to fill in each section.

### Is your feature request related to a problem? Please describe.
This section should provide a clear and concise description of what the problem is.
Ex. I'm always frustrated when [...]

### Describe the solution you'd like
A clear and concise description of what you want to happen.
If you can provide technical details about how to address the problem, please do so.
Feel free to add a subheading.

### Describe alternatives you've considered
A clear and concise description of any alternative solutions or features you've considered.

### Additional context
Add any other context for the feature request here.
This might list the application name and version number that the feature is expected to work with
(EG Firefox or Microsoft Word).
Also consider whether you can upload an attachment document to be used to demonstrate the missing
feature.

## Bug report template

After the HTML comment ([discussed earlier](#general-information)), you may provide a brief overview
of the issue.
Then fill in each of the following headings which match those that are found in the template, with a
short description of how to fill in each section.

### Steps to reproduce:

This section is very important, please be clear and concise.
This section should contain a list of the steps you take to demonstrate the problem.
While you are working out the steps required, please make a copy of your
[NVDA log to attach to the issue](https://github.com/nvaccess/nvda/wiki/LogFilesAndCrashDumps).

*Example:*
> 1. Open Chrome
> 1. Browse to www.google.com
> 1. Type "Hello"
> 1. Press Enter

### Actual behavior:
This section should tell us what actually happens when these steps are taken.
Please describe verbatim what NVDA does, ideally use speech viewer to copy the speech from NVDA.
This helps developers to be sure they are reproducing the same issue as you.

*Example:*
> An NVDA error sound is heard.

> NVDA Speech:
> "button enable sound"

### Expected behavior:
This section should tell us what you expect to happen when these steps are taken.

*Example:*
> There should be no error sound, and the page should change to show the search results.

> NVDA Speech:
> "checkbox enable sound"

### System configuration:

This section has several sub-sections.
These are all about the system you are using when encountering the issue.
If you are encountering the issue with multiple different configurations, please list them.
This helps us to be able to reproduce the issue, or help us to investigate why this issue occurs
for some users and not others.

#### NVDA installed/portable/running from source:
This tells us how you are using NVDA.

*Example:*
> Installed

#### NVDA version:
The version of NVDA that you are using when demonstrating the issue.
This can be copied from the about option, in the NVDA help menu.

*Example:*
> alpha-15370,21fd217a

> release 2020.4

#### Windows version:
The version of Windows that you are using.
You can copy this from the "System Information" application:
1. Press `Windows+r` to open the run dialog
1. Type `msinfo32` and press enter
1. From the "System summary" treeview item, press tab to get to the right pane.
1. Press down arrow twice to get to "Version"
1. Press `Control+C` to copy the version information.

*Example:*
> Windows 10 Version 1607 Build 14393.1066

#### Name and version of other software in use when reproducing the issue:
Typically, you can get this information from the "About" dialog of the software.

*Example:*
> Chrome version: 67.0.3396.87

#### Other information about your system:
This is other information about your setup that you think might be relevant to us.

*Example:*
> Running Windows 10 in a VM

### Other questions:
This section has sub-sections, asking about the basic investigation steps you may have completed.
Please feel free to add more information here to tell us about what you have tried.

#### Does the issue still occur after restarting your Computer?

Restarting your computer will help to ensure that software is in a fresh state.

#### Have you tried any other versions of NVDA? If so, please report their behaviors.

Knowing whether this issue occurs in previous releases helps us to understand if this is a newly
introduced issue.
It can help us determine if changes in NVDA or other software introduced the problem.

*Example:*
> * NVDA 2018.1 - no error sound
> * NVDA 2018.2 - has error sound

#### If NVDA add-ons are disabled, is your problem still occurring?

In many cases issues could be caused by an add-on not working correctly or conflicting with other
features already integrated in NVDA itself.
Therefore, it is recommended to reproduce issues with all add-ons disabled.
In case the issue is caused by an add-on, it is recommended to contact the author of the add-on first.

#### Does the issue still occur after you run the COM Registration Fixing Tool in NVDA's tools menu?

COM DLL files, which i.e. the IAccessible COM interface depends on, can get unregistered after
installing and uninstalling different programs on a computer.
The consequence is that NVDA in certain cases does not work properly.
Specifically, it reports "unknown" when trying to navigate websites or fails to switch between focus
and browse mode, it causes performance issues, focus instability and other odd problems.
The COM registry fixing tool has been introduced in order to re-register those DLL files.
In any case, re-registering those DLL files does not have any negative impact on computers'
functionality.
Thus, it is recommended to run the fixing tool whenever focus problems, performance problems on
websites or navigation problems in focus or browse mode on different interfaces are encountered.
