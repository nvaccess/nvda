CFLAGS=/nologo
LINKERFLAGS=/nologo
MIDLFLAGS=/nologo /win32

!if defined(DEBUG)
CFLAGS=$(CFLAGS) /MTd /Gm /Zi /DDEBUG /Od
LINKERFLAGS=$(LINKERFLAGS) /DEBUG
!else
CFLAGS=$(CFLAGS) /MT /O2 /DNDEBUG 
LINKERFLAGS=$(LINKERFLAGS) /release
MTLFLAGS=$(MTLFLAGS) /DNDEBUG
!endif

all: NVDAControlServer.dll NVDAControlClient.dll

NVDAControler.h NVDAControler_s.c NVDAControler_c.c: NVDAControler.idl
	midl $(MIDLFLAGS) /prefix all NVDAControler_ $**

NVDAControlServer.dll: server.obj NVDAControler_s.obj
 	link $(LINKERFLAGS) /dll $** rpcrt4.lib /out:NVDAControlServer.dll

NVDAControlClient.dll: NVDAControlClient.obj NVDAControler_c.obj
 	link $(LINKERFLAGS) /dll $** rpcrt4.lib /out:NVDAControlClient.dll

clean:
	-@del *.obj 2>NUL
	-@del NVDAControler_s.c 2>NUL
	-@del NVDAControler_c.c 2>NUL
	-@del NVDAControler.h 2>NUL

distclean: clean
	-@del *.dll 2>NUL
	-@del *.lib 2>NUL
	-@del *.exp 2>NUL

