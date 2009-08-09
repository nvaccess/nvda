from SCons import *

def buildEmitter(target,source,env):
	base,ext=Util.splitext(str(source[0]))
	targets=[base+'.h',base+'_c.c',base+'_s.c']
	return (targets,source)

MSRPCStubs=Builder.Builder(action="${MIDL} ${MIDLFLAGS} /header ${TARGETS[0]} /cstub ${TARGETS[1]} /sstub ${TARGETS[2]} $SOURCE",suffix='.h',src_suffix=['.idl'],emitter=buildEmitter)
