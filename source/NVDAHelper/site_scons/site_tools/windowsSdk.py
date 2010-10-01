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
msvc.msvc_setup_env_once=lambda env: False
msvc.msvc_exists=lambda: True

scriptSwitchByTargetArch={
	'x86':'/x86',
	'x86_64':'/x64',
	'ia64':'/ia64',
}

def fetchSDKVars(targetArch='x86',wantedVersion=None):
	archSwitch=scriptSwitchByTargetArch.get(targetArch)
	if not archSwitch:
		common.debug("windowsSdk.py, fetchSDKVars: Unsupported target arch: %s"%targetArch)
	try:
		versionsKey=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\Microsoft\Microsoft SDKs\Windows')
	except Exception as e:
		common.debug("windowsSdk.py, fetchSDKVars: Windows SDK tool: no SDKs installed: root registry key not found, %s"%e)
		return None
	versionsKeyLen=_winreg.QueryInfoKey(versionsKey)[0]
	if versionsKeyLen<1:
		common.debug("windowsSdk.py, fetchSDKVars: No SDK versions found: root registry key empty")
		return None
	if wantedVersion:
		versionStrings=[wantedVersion]
	else:
		versionStrings=[x for x in (_winreg.EnumKey(versionsKey,index) for index in xrange(versionsKeyLen)) if x.startswith('v')]
	for v in reversed(versionStrings):
		try:
			versionKey=_winreg.OpenKey(versionsKey,v)
		except Exception as e:
			common.debug("windowsSdk.py, fetchSDKVars: failed to open registry key for version %s: %s"%(v,e))
			continue
		try:
			installDir=_winreg.QueryValueEx(versionKey,"InstallationFolder")[0]
		except Exception as e:
			common.debug("windowsSdk.py, fetchSDKVars: no InstallationFolder value in registry key: %s: %s"%(v,e))
			continue
		scriptPath=os.path.join(installDir,os.path.join('bin','setenv.cmd'))
		if not os.path.isfile(scriptPath):
			common.debug("windowsSdk.py, fetchSDKVars: Script %s does not exist"%scriptPath)
			continue
		p=subprocess.Popen(['cmd','/V','/c',scriptPath,archSwitch,'&&','set'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		stdout,stderr=p.communicate()
		try:
			return common.parse_output(stdout)
		except Exception as e:
			common.debug("windowsSdk.py, fetchSDKVars: Error parsing script output: %s"%e)
			continue
	common.debug("windowsSdk.py, fetchSDKVars: No suitable SDK could be used")
	return None

def exists(env):
	return True

def generate(env):
	targetArch=env.get('TARGET_ARCH','x86')
	d=fetchSDKVars(targetArch=targetArch)
	if not d:
		return False
	for k, v in d.iteritems():
		env.PrependENVPath(k,v,delete_existing=True)
	env['MSVC_USE_SCRIPT']=False
	return msvc.generate(env)
