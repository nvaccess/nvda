###
#This file is a part of the NVDA project.
#URL: http://www.nvda-project.org/
#Copyright 2010-2012 NV Access Limited
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

# Get the path to msgfmt.
MSGFMT = os.path.abspath(os.path.join("miscDeps", "tools", "msgfmt.exe"))

def exists(env):
	return True

def generate(env):
	env['BUILDERS']['gettextMoFile']=env.Builder(
		action=env.Action([[MSGFMT,"-o","$TARGET","$SOURCE"]],
			lambda t,s,e: 'Compiling gettext template %s'%s[0].path),
		suffix='.mo',
		src_suffix='.po'
	)
