#MSRPC tool
#Provides the MSRPCStubs builder which can use MIDL to generate header, client stub, and server stub files from an IDL.

from SCons import Util
from SCons.Builder import Builder

def MSRPCStubs_buildEmitter(target,source,env):
	base,ext=Util.splitext(str(source[0]))
	targets=[base+'.h',base+'_c.c',base+'_s.c']
	return (targets,source)

def exists(env):
	from SCons.Tool import midl
	return midl.exists(env)

def generate(env):
	if not 'MIDL' in env:
		from SCons.Tool import midl
		midl.generate(env)
	env['BUILDERS']['MSRPCStubs']=Builder(action="${MIDL} ${MIDLFLAGS} /header ${TARGETS[0]} /cstub ${TARGETS[1]} /sstub ${TARGETS[2]} $SOURCE",suffix='.h',src_suffix=['.idl'],emitter=MSRPCStubs_buildEmitter)
