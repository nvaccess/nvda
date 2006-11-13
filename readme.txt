Nonvisual Desktop Access (NVDA)
Access to Windows through free, open source, and nonvisual means.

Created by Michael Curran and James Teh.

Introduction

NVDA was started because of a lack of affordable, or free, Windows access solutions for blind and vision impaired users. Currently people can be paying up to $2000 to use a Windows screen reader, yet on other platforms such as Linux, screen readers are already existing that are free.

NVDA is so far written entirely in the Python programming language, which is itself a free language, and is very quick to learn. Because Python can be also looked at as a scripting language, this also allows NVDA to be added to, and changed to suit user specific needs very easily.

All source code is included with NVDA, and anyone is free to change it to suit their own needs.

NVDA works pretty much like any screen reader you would be used to.  Its main features are:
*Uses MSAA to find out a control's name, role, state, value, description, help and index.
*Uses the windows API to be able to read characters, selection and full text, of windows such as edit fields.
*Uses OLE/com to access documents 
*Responds to many MSAA events such as focus change, active item change, object creation, object destruction etc, and also when ever any of a control's MSAA attributes change.
*Can access html pages through internet Explorer_server windows.
*Responds to key press events.
*Is modular-based (synth drivers and support for specific applications can be written as modules).
*Has the ability to navigate the MSAA object tree with out moving the focus.
*Can read dos console windows.

Running NVDA

If you have the standallone version, you can just run nvda.exe and off you go.

For the python source version: As long as you have installed all dependency packages (python, pyAA, pyTTS, pyHook etc) you should be able to simply press enter on nvda.pyw in the source directory.
Or in a cmd prompt, move to the source directory and execute nvda.pyw.

NVDA is covered by the GNU General Public Licence. More details can be found in the file COPYING in this directory.

Please send bugs and suggestions to:
mick@kulgan.net

NVDA website:
http://www.kulgan.net/nvda/

We are always looking for testers, and we are always needing people who are interested in writing support for various applications.

If interested, please email
Michael Curran <mick@kulgan.net>
