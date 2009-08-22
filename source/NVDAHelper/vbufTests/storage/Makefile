###
# tests/storage/Makefile
# Part of the NV  Virtual Buffer Library
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=../..
!include $(TOPDIR)\make.opts

all: $(OUTDIR)\test_storage_createDestroy.exe
	cd $(OUTDIR) && .\test_storage_createDestroy.exe

$(OUTDIR)\test_storage_createDestroy.exe: createDestroy.cpp $(TOPDIR)\base\storage.cpp $(TOPDIR)\base\lock.cpp $(TOPDIR)\base\utils.cpp $(TOPDIR)\base\debug.cpp
	cl $(CPPFLAGS) $** /link $(LINKERFLAGS) /out:$@

clean:
	-del *.obj 2>NUL
	-del *.pdb 2>NUL
