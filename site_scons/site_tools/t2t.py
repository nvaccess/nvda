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

def txt2tags_actionFunc(target,source,env):
	import txt2tags
	txt2tags.exec_command_line([str(source[0])])

def exists(env):
	try:
		import txt2tags
		return True
	except ImportError:
		return False

def generate(env):
	env['BUILDERS']['txt2tags']=env.Builder(
		action=env.Action(txt2tags_actionFunc,lambda t,s,e: 'Converting %s to html'%s[0].path),
		suffix='.html',
		src_suffix='.t2t'
	)
