###
#This file is a part of the NVDA project.
#URL: http://www.nvda-project.org/
#Copyright 2010 James Teh <jamie@jantrid.net>.
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License version 2.0, as published by
#the Free Software Foundation.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#This license can be found at:
#http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
###

import os
import sys

__path__=[os.path.join(sys.exec_prefix,'tools','i18n')]
import msgfmt
del __path__

def gettextMoFile_actionFunc(target,source,env):
	msgfmt.make(source[0].path,target[0].path)
	msgfmt.MESSAGES={}

def exists(env):
	return True

def generate(env):
	env['BUILDERS']['gettextMoFile']=env.Builder(
		action=env.Action(gettextMoFile_actionFunc,lambda t,s,e: 'Compiling gettext template %s'%s[0].path),
		suffix='.mo',
		src_suffix='.po'
	)
