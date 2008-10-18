###
# remoteApi/Makefile
# Part of the NV  Virtual Buffer Library
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=..
!include $(TOPDIR)\make.opts

all: remoteApi.h

remoteApi.h remoteApi_c.c remoteApi_s.c: remoteApi.idl
	$(MIDL) $(MIDLFLAGS) /prefix all VBufRemote_ $**

clean:
	-del remoteApi_s.c 2>NUL
	-del remoteApi_c.c 2>NUL
	-del remoteApi.h 2>NUL
