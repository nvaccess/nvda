#globalPluginHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010 James Teh <jamie@jantrid.net>

import sys
import pkgutil
import importlib
import config
import baseObject
from logHandler import log
import globalPlugins

#: All currently running global plugins.
runningPlugins = set()

def listPlugins():
	for loader, name, isPkg in pkgutil.iter_modules(globalPlugins.__path__):
		if name.startswith("_"):
			continue
		try:
			plugin = importlib.import_module("globalPlugins.%s" % name, package="globalPlugins").GlobalPlugin
		except:
			log.error("Error importing global plugin %s" % name, exc_info=True)
			continue
		yield plugin

def initialize():
	config.addConfigDirsToPythonPackagePath(globalPlugins)
	for plugin in listPlugins():
		try:
			runningPlugins.add(plugin())
		except:
			log.error("Error initializing global plugin %r" % plugin, exc_info=True)

def terminate():
	for plugin in list(runningPlugins):
		runningPlugins.discard(plugin)
		try:
			plugin.terminate()
		except:
			log.exception("Error terminating global plugin %r" % plugin)

def reloadGlobalPlugins():
	"""Reloads running global plugins.
	"""
	global globalPlugins
	terminate()
	del globalPlugins
	mods=[k for k,v in sys.modules.items() if k.startswith("globalPlugins") and v is not None]
	for mod in mods:
		del sys.modules[mod]
	import globalPlugins
	initialize()

class GlobalPlugin(baseObject.ScriptableObject):
	"""Base global plugin.
	Global plugins facilitate the implementation of new global commands,
	support for objects which may be found across many applications, etc.
	Each global plugin should be a separate Python module in the globalPlugins package containing a C{GlobalPlugin} class which inherits from this base class.
	Global plugins can implement and bind gestures to scripts which will take effect at all times.
	See L{ScriptableObject} for details.
	Global plugins can also receive NVDAObject events for all NVDAObjects.
	This is done by implementing methods called C{event_eventName},
	where C{eventName} is the name of the event; e.g. C{event_gainFocus}.
	These event methods take two arguments: the NVDAObject on which the event was fired
	and a callable taking no arguments which calls the next event handler.
	"""

	def terminate(self):
		"""Terminate this global plugin.
		This will be called when NVDA is finished with this global plugin.
		"""

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		"""Choose NVDAObject overlay classes for a given NVDAObject.
		This is called when an NVDAObject is being instantiated after L{NVDAObjects.NVDAObject.findOverlayClasses} has been called on the API-level class.
		This allows a global plugin to add or remove overlay classes.
		See L{NVDAObjects.NVDAObject.findOverlayClasses} for details about overlay classes.
		@param obj: The object being created.
		@type obj: L{NVDAObjects.NVDAObject}
		@param clsList: The list of classes, which will be modified by this method if appropriate.
		@type clsList: list of L{NVDAObjects.NVDAObject}
		"""
