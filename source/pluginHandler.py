#pluginHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010 James Teh <jamie@jantrid.net>

import pkgutil
import config
import baseObject
from logHandler import log
import plugins

#: All currently running plugins.
runningPlugins = set()

def listPlugins():
	for loader, name, isPkg in pkgutil.iter_modules(plugins.__path__):
		if name.startswith("_"):
			continue
		try:
			plugin = __import__("plugins.%s" % name, globals(), locals(), ("plugins",)).Plugin
		except:
			log.error("Error importing plugin %s" % name, exc_info=True)
		yield plugin

def initialize():
	config.addConfigDirsToPythonPackagePath(plugins)
	for plugin in listPlugins():
		try:
			runningPlugins.add(plugin())
		except:
			log.error("Error initializing plugin %r" % plugin)

def terminate():
	for plugin in list(runningPlugins):
		runningPlugins.discard(plugin)
		try:
			plugin.terminate()
		except:
			log.exception("Error terminating plugin %r" % plugin)

class Plugin(baseObject.ScriptableObject):
	"""Base plugin.
	Each plugin should be a separate Python module in the plugins package containing a C{Plugin} class which inherits from this base class.
	"""

	def terminate(self):
		"""Terminate this plugin.
		This will be called when NVDA is finished with this plugin.
		"""
