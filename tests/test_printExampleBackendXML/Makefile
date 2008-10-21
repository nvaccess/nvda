###
# tests/test_printExampleBackendXML/Makefile
# Part of the NV  Virtual Buffer Library
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=../..
!include $(TOPDIR)\make.opts

BASEDIR=$(TOPDIR)\base

all: $(OUTDIR)\test_printExampleBackendXML.exe
	cd $(OUTDIR) && .\test_printExampleBackendXML.exe

$(OUTDIR)\test_printExampleBackendXML.exe: test_printExampleBackendXML.cpp $(TOPDIR)\backends\example\example.cpp $(BASEDIR)\storage.cpp $(BASEDIR)\lock.cpp $(BASEDIR)\utils.cpp $(BASEDIR)\backend.cpp $(BASEDIR)\debug.cpp
	cl $(CPPFLAGS)  $** /link kernel32.lib $(LINKERFLAGS) /out:$@

clean:
	-del *.obj 2>NUL
	-del *.pdb 2>NUL
