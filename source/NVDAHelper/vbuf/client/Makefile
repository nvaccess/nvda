###
# client/Makefile
# Part of the NV  Virtual Buffer Library
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=..
!include $(TOPDIR)\make.opts
CPPFLAGS=$(CPPFLAGS) /DVBUFLIBENTRYTYPE=2

all: $(OUTDIR)\VBufClient.dll

$(OUTDIR)\VBufClient.dll: client.cpp $(TOPDIR)\remoteApi\remoteApi_c.c
	cl $(CPPFLAGS) $** /link rpcrt4.lib /dll /out:$@ $(LINKERFLAGS)

clean:
	-del *.obj 2>NUL
	-del *.pdb 2>NUL
