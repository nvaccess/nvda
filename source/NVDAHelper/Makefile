MIDL=midl
MIDLFLAGS=/nologo /notlb
LINKER=link
LINKERFLAGS=/NOLOGO
CFLAGS=/nologo
CPPFLAGS=/nologo
!if defined(DEBUG)
CFLAGS=$(CFLAGS) /DDEBUG /Zi
CPPFLAGS=$(CPPFLAGS) /DDEBUG /Zi
LINKERFLAGS=$(LINKERFLAGS) /DEBUG
!else
CFLAGS=$(CFLAGS) /O2
CPPFLAGS=$(CPPFLAGS) /O2
LINKERFLAGS=$(LINKERFLAGS) /RELEASE
!endif

NEEDEDLIBS=user32.lib ole32.lib  

all: NVDAHelper.dll

ia2_i.obj: ia2.h ia2_i.c

ia2.h ia2_i.c: ..\include\ia2_api_all.idl
	$(MIDL) $(MIDLFLAGS) $** /h ia2.h /iid ia2_i.c

NVDAHelper.dll: hookManager.obj inputLangChange.obj typedCharacter.obj IA2Support.obj ia2_i.obj
	$(LINKER) -dll $** $(NEEDEDLIBS) /out:$@ $(LINKERFLAGS)

clean:
	-del *.obj 2>NUL
	-del ia2.h ia2.tlb ia2_i.c ia2_p.c dlldata.c 2>NUL
