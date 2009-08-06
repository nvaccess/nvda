###
# base/Makefile
# Part of the NV  Virtual Buffer Library
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=..
!include $(TOPDIR)\make.opts

all: $(OUTDIR)\VBufBase_static.lib

$(OUTDIR)\VBufBase_static.lib: storage.obj utils.obj lock.obj backend.obj debug.obj
	lib /nologo $** $(OUTDIR)\nvdaHelperRemote.lib /out:$@

clean:
	-del *.obj 2>NUL
	-del *.pdb 2>NUL
