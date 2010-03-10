#MSRPC tool
#Provides the MSRPCStubs builder which can use MIDL to generate header, client stub, and server stub files from an IDL.

from SCons import Util
from SCons.Builder import Builder

#This build emitter tells the builder that a header file, a client stub c file, and a server stub c file will be generated 
def MSRPCStubs_buildEmitter(target,source,env):
	base,ext=Util.splitext(str(target[0] if len(target)>0 else source[0]))
	newTargets=['%s.h'%base]
	if not env['MSRPCStubs_noServer']:
		newTargets.append('%s_S.c'%base)
	if not env['MSRPCStubs_noClient']:
		newTargets.append('%s_C.c'%base)
	return (newTargets,source)

def MSRPCStubs_builder_actionGenerator(target,source,env,for_signature):
	sources=[]
	for src in source:
		src=str(src)
		if src.endswith('.acf'):
			sources.append('/acf %s'%src)
		else:
			sources.append(src)
	sources=" ".join(sources)
	targets=[]
	for tg in target:
		tg=str(tg)
		if tg.endswith('.h'):
			targets.append('/header %s'%tg)
		elif tg.endswith('_S.c'):
			targets.append('/sstub %s'%tg)
		elif tg.endswith('_C.c'):
			targets.append('/cstub %s'%tg)
		else:
			raise ValueError("Don't know what to do with %s"%tg)
	targets=" ".join(targets)
	noServer="/server none" if env.get('MSRPCStubs_noServer',False) else ""
	noClient="/client none" if env.get('MSRPCStubs_noClient',False) else ""

	prefix=env.get('MSRPCStubs_prefix',"")
	if prefix:
		prefix="/prefix all %s"%prefix
	serverPrefix=env.get('MSRPCStubs_serverPrefix',"")
	if serverPrefix:
		serverPrefix="/prefix server %s"%serverPrefix
	clientPrefix=env.get('MSRPCStubs_clientPrefix',"")
	if clientPrefix:
		clientPrefix="/prefix client %s"%clientPrefix

	return " ".join(['${MIDL}','${MIDLFLAGS}',noServer,noClient,prefix,serverPrefix,clientPrefix,targets,sources])

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
	env['MSRPCStubs_noServer']=False
	env['MSRPCStubs_noClient']=False
