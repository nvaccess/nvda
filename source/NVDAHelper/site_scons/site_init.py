#Hack in better support for vc9 that comes with the Microsoft Windows SDK
from SCons.Tool.MSCommon.vc import VisualC
VisualC.batch_file_map[('x86_64','x86')].append(r'bin\vcvarsx86_amd64.bat')
VisualC.batch_file_map[('x86_64','x86_64')].append(r'bin\vcvars64.bat')
