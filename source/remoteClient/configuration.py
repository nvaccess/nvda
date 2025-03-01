# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import config

from .connectionInfo import ConnectionInfo


def getRemoteConfig():
	return config.conf["remote"]


def write_connection_to_config(connection_info: ConnectionInfo):
	"""Writes a connection to the last connected section of the config.
	If the connection is already in the config, move it to the end.

	Args:
		connection_info: The ConnectionInfo object containing connection details
	"""
	conf = getRemoteConfig()
	last_cons = conf["connections"]["last_connected"]
	address = connection_info.getAddress()
	if address in last_cons:
		conf["connections"]["last_connected"].remove(address)
	conf["connections"]["last_connected"].append(address)
