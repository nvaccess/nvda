#MSRPC tool
#Provides the MSRPCStubs builder which can use MIDL to generate header, client stub, and server stub files from an IDL.

from SCons import Util
from SCons.Builder import Builder

#This build emitter tells the builder that a header file, a client stub c file, and a server stub c file will be generated 
def MSRPCStubs_buildEmitter(target,source,env):
	base,ext=Util.splitext(str(target[0] if len(target)>0 else source[0]))
	targets=[base+'.h',base+'_c.c',base+'_s.c']
	return (targets,source)

def MSRPCStubs_builder_actionGenerator(target,source,env,for_signature):
	#As we support .acf files as sources, we must insert the /acf switch before each one
	sourcesString=" ".join([('/acf %s'%src if str(src).endswith('.acf') else str(src)) for src in source])
	return "${MIDL} ${MIDLFLAGS} /header ${TARGETS[0]} /cstub ${TARGETS[1]} /sstub ${TARGETS[2]} %s"%sourcesString

MSRPCStubs_builder=Builder(
	generator=MSRPCStubs_builder_actionGenerator,
	src_suffix=['.idl','.acf'],
	emitter=MSRPCStubs_buildEmitter,
)

def exists(env):
	from SCons.Tool import midl
	return midl.exists(env)

def generate(env):
	if not 'MIDL' in env:
		from SCons.Tool import midl
		midl.generate(env)
	env['BUILDERS']['MSRPCStubs']=MSRPCStubs_builder
