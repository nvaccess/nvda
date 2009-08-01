###
# interfaces/vbuf/Makefile
# Part of NVDA Helper
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=..\..
!include $(TOPDIR)\make.opts

all: vbuf.h

vbuf.h vbuf_c.c vbuf_s.c: vbuf.idl
	$(MIDL) $(MIDLFLAGS) /prefix client VBuf_ /prefix server VBufRemote_ $**

clean:
	-del vbuf_s.c 2>NUL
	-del vbuf_c.c 2>NUL
	-del vbuf.h 2>NUL
