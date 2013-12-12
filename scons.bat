@echo off
rem We need this script because .py probably isn't in pathext.
rem We can't just call python -c because it may not be in the path.
rem Python registers itself with the .py extension, so call scons.py.
%~dp0\scons.py %*
