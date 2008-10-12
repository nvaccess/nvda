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
NEEDEDLIBS=kernel32.lib

all: $(OUTDIR)\VBufBase.dll

$(OUTDIR)\VBufBase.dll: storage.obj utils.obj lock.obj backend.obj container.obj debug.obj
	if not EXIST $(OUTDIR) mkdir $(OUTDIR)
	$(LINKER) -dll $** $(NEEDEDLIBS) /out:$@ $(LINKERFLAGS) /VERSION:$(VERSION) 

clean:
	-del *.obj 2>NUL
	-del *.pdb 2>NUL
