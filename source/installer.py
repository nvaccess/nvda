from ctypes import *
from ctypes.wintypes import *
import threading
import time
import os
import tempfile
import shellapi
import globalVars
import versionInfo

autorunTemplate="""[AutoRun]
open={exe}
action={name} {version}
icon={icon}
"""

class CreatePortableCopy(threading.Thread):

	def __init__(self,destPath,copyUserConfig=True,createAutorun=False):
		super(CreatePortableCopy,self).__init__()
		self.destPath=destPath
		self.copyUserConfig=copyUserConfig
		self.createAutorun=createAutorun
		self.threadExc=None
		self.start()
		time.sleep(0.1)
		threadHandle=c_int()
		threadHandle.value=windll.kernel32.OpenThread(0x100000,False,self.ident)
		msg=MSG()
		while windll.user32.MsgWaitForMultipleObjects(1,byref(threadHandle),False,-1,255)==1:
			while windll.user32.PeekMessageW(byref(msg),None,0,0,1):
				windll.user32.TranslateMessage(byref(msg))
				windll.user32.DispatchMessageW(byref(msg))
		if self.threadExc:
			raise self.threadExc

	def run(self,*args,**kwargs):
		try:
			destPath=os.path.abspath(self.destPath)
			opStruct=shellapi.SHFILEOPSTRUCT(wFunc=shellapi.FO_COPY,pFrom=os.path.join(os.getcwd(),'*')+u"\x00",pTo=destPath+u"\x00",lpszProgressTitle=_("Copying NVDA program files"),fFlags=shellapi.FOF_NOCONFIRMMKDIR)
			if windll.shell32.SHFileOperationW(byref(opStruct))!=0 or opStruct.fAnyOperationsAborted:
				raise OSError("Error copying program files")
			if self.copyUserConfig:
				opStruct=shellapi.SHFILEOPSTRUCT(wFunc=shellapi.FO_COPY,pFrom=os.path.join(globalVars.appArgs.configPath,'*')+u"\x00",pTo=os.path.join(destPath,u"userConfig")+u"\x00",lpszProgressTitle=_("Copying NVDA user config"),fFlags=shellapi.FOF_NOCONFIRMMKDIR)
				if windll.shell32.SHFileOperationW(byref(opStruct))!=0 or opStruct.fAnyOperationsAborted:
					raise OSError("Error copying user config")
			if self.createAutorun:
				drive,relDestPath=os.path.splitdrive(destPath)
				with tempfile.NamedTemporaryFile(mode="wt") as arFile:
					autorunString=autorunTemplate.format(exe=os.path.join(relDestPath,'nvda.exe'),name=versionInfo.name,version=versionInfo.version,icon=os.path.join(relDestPath,'images/nvda.ico'))
					arFile.write(autorunString)
					arFile.flush()
					opStruct=shellapi.SHFILEOPSTRUCT(wFunc=shellapi.FO_COPY,pFrom=arFile.name+u"\x00",pTo=os.path.join(drive+'\\','autorun.inf')+u"\x00")
					if windll.shell32.SHFileOperationW(byref(opStruct))!=0:
						raise OSError("Error copying autorun file")
		except Exception as e:
			self.threadExc=e
