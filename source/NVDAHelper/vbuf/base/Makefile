###
# base/Makefile
# Part of the NV  Virtual Buffer Library
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=..
!include $(TOPDIR)\make.opts
CPPFLAGS=$(CPPFLAGS) /DVBUFLIBENTRYTYPE=1

VERSION=2.0

all: $(OUTDIR)\VBufBase.dll

$(TOPDIR)\remoteApi\remoteApi_s.c: $(TOPDIR)\remoteApi\remoteApi.idl $(TOPDIR)\remoteApi\remoteApi.acf
	cd $(TOPDIR)\remoteApi && $(MAKE) DEBUG=$(DEBUG)

$(OUTDIR)\VBufBase.dll: storage.cpp $(TOPDIR)\common\utils.cpp lock.cpp backend.cpp container.cpp remoteApi.cpp rpcSrv.cpp $(TOPDIR)\remoteApi\remoteApi_s.c debug.cpp
	if not EXIST $(OUTDIR) mkdir $(OUTDIR)
	cl $(CPPFLAGS)  $** /link rpcrt4.lib kernel32.lib /dll /out:$@ /version:$(VERSION)

clean:
	-del *.obj 2>NUL
	-del *.pdb 2>NUL
