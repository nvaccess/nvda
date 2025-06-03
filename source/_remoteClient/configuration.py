# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import config

from .connectionInfo import ConnectionInfo


def getRemoteConfig():
	return config.conf["remote"]


def writeConnectionToConfig(connectionInfo: ConnectionInfo):
	"""
	Writes a connection to the last connected section of the config.
	If the connection is already in the config, move it to the end.

		:param connectionInfo: The :class:`ConnectionInfo` object containing connection details
	"""
	conf = getRemoteConfig()
	lastConnections = conf["connections"]["lastConnected"]
	address = connectionInfo.getAddress()
	if address in lastConnections:
		if lastConnections[-1] == address:
			# This address is already the last connected address, so no action is needed.
			return
		# Remove the address from the list, so appending it won't result in a duplicate.
		lastConnections.remove(address)
	lastConnections.append(address)
	# Configobj recognises items as changed based on calls to __setitem__,
	# so will not know that the underlying list has been mutated.
	# Set the list to itself to force configobj to realise the key is dirty.
	conf["connections"]["lastConnected"] = lastConnections


def _isDebugForRemoteClient() -> bool:
	return config.conf["debugLog"]["remoteClient"]
