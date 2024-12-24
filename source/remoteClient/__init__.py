from .client import RemoteClient


def initialize():
	"""Initialise the remote client."""
	import globalVars
	import globalCommands

	globalVars.remoteClient = RemoteClient()
	globalVars.remoteClient.registerLocalScript(globalCommands.commands.script_sendKeys)


def terminate():
	"""Terminate the remote client."""
	import globalVars

	globalVars.remoteClient.terminate()
	globalVars.remoteClient = None
