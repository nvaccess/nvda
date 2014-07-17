###
#This file is a part of the NVDA project.
#URL: http://www.nvda-project.org/
#Copyright 2006-2010 NVDA contributers.
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License version 2.0, as published by
#the Free Software Foundation.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#This license can be found at:
#http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
###

import subprocess
import _winreg
import os
from SCons.Tool.MSCommon import common
from SCons.Tool import msvc

#Forecefully disable MSVC detection and path setup
#msvc.msvc_setup_env_once=lambda env: False
#msvc.msvc_exists=lambda: True

scriptSwitchByTargetArch={
	'x86':'/x86',
	'x86_64':'/x64',
	'amd64':'/x64',
	'ia64':'/ia64',
}

def fetchSDKVars(targetArch,versionString):
	common.debug("windowsSdk.py, fetchSDKVars: Searching for SDK %s"%versionString)
	archSwitch=scriptSwitchByTargetArch.get(targetArch)
	if not archSwitch:
		common.debug("windowsSdk.py, fetchSDKVars: Unsupported target arch: %s"%targetArch)
	try:
		versionKey=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Microsoft SDKs\Windows\%s'%versionString)
	except Exception as e:
		common.debug("windowsSdk.py, fetchSDKVars: failed to open registry key for version %s: %s"%(versionString,e))
		return
	try:
		installDir=_winreg.QueryValueEx(versionKey,"InstallationFolder")[0]
	except Exception as e:
		common.debug("windowsSdk.py, fetchSDKVars: no InstallationFolder value in registry key: %s: %s"%(v,e))
		return
	if versionString=='v7.1A':
		#V7.1A (comes with vc2012) does not come with a batch file 
		d=dict(PATH=os.path.join(installDir,'bin'),INCLUDE=os.path.join(installDir,'include'),LIB=os.path.join(installDir,'lib'))
		if targetArch in ('x86_64','amd64'):
			d['PATH']=os.path.join(d['PATH'],'x64')
			d['LIB']=os.path.join(d['LIB'],'x64')
		return d
	scriptPath=os.path.join(installDir,os.path.join('bin','setenv.cmd'))
	if not os.path.isfile(scriptPath):
		common.debug("windowsSdk.py, fetchSDKVars: Script %s does not exist"%scriptPath)
		return
	p=subprocess.Popen(['cmd','/V','/c',scriptPath,archSwitch,'&&','set'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr=p.communicate()
	try:
		return common.parse_output(stdout)
	except Exception as e:
		common.debug("windowsSdk.py, fetchSDKVars: Error parsing script output: %s"%e)
		return
	common.debug("windowsSdk.py, fetchSDKVars: No suitable SDK could be used")

def exists(env):
	return True

def generate(env):
	targetArch=env.get('TARGET_ARCH','x86')
	d=fetchSDKVars(targetArch,'v7.1A')
	if d:
		env.Append(CPPDEFINES='_USING_V110_SDK71_')
		if targetArch.endswith('64'):
			env.Append(LINKFLAGS=[env['LINKFLAGS'],'/SUBSYSTEM:WINDOWS,5.02'])
		else:
			# #3730: VC2012 uses SSE2 by default, but NVDA is still run on some older processers (AMD Athlon etc) which don't support this.
			env.Append(CCFLAGS='/arch:IA32')
			env.Append(LINKFLAGS=[env['LINKFLAGS'],'/SUBSYSTEM:WINDOWS,5.01'])
	if not d:
		d=fetchSDKVars(targetArch,'v7.1')
	if not d:
		d=fetchSDKVars(targetArch,'v7.0')
	if not d:
		common.debug("windowsSdk.py, Generate: No suitable SDK could be used")
		raise RuntimeError("No usable Windows SDK found")
	#msvc.generate(env)
	for k, v in d.iteritems():
		env.PrependENVPath(k,v,delete_existing=True)

