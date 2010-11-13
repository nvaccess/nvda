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

msgfmtPath=os.path.join(sys.exec_prefix, "Tools", "i18n", "msgfmt.py")

def exists(env):
	return os.path.isfile(msgfmtPath)

def generate(env):
	env['BUILDERS']['gettextMoFile']=env.Builder(
		action=env.Action([[sys.executable,msgfmtPath,'$SOURCE']],lambda t,s,e: 'Compiling gettext template %s'%s[0].path),
		suffix='.mo',
		src_suffix='.po'
	)
