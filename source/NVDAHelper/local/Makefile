###
# local/Makefile
# Part of NVDA Helper
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=..
!include $(TOPDIR)\make.opts

all: $(OUTDIR)\nvdaHelperLocal.dll

$(TOPDIR)\interfaces\vbuf\vbuf_c.c: $(TOPDIR)\interfaces\vbuf\vbuf.acf $(TOPDIR)\interfaces\vbuf\vbuf.idl
	cd $(TOPDIR)\interfaces\vbuf && $(MAKE) /nologo DEBUG=$(DEBUG) DEBUGLOG=$(DEBUGLOG)

$(OUTDIR)\nvdaHelperLocal.dll: nvdaHelperLocal.cpp $(TOPDIR)\interfaces\vbuf\vbuf_c.c
	$(CPP) $(CPPFLAGS) $** /link rpcrt4.lib /dll /out:$@ $(LINKERFLAGS)

clean:
	cd $(TOPDIR)\interfaces\vbuf && $(MAKE) /nologo clean
	-del *.obj 2>NUL
	-del *.pdb 2>NUL
