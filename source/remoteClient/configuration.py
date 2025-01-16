# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
from io import StringIO

import config
import configobj
import globalVars
from configobj import validate

from .connectionInfo import ConnectionInfo

CONFIG_FILE_NAME = "remote.ini"
configRoot = "Remote"

_config = None
configspec = StringIO("""
[connections]
	last_connected = list(default=list())
[controlserver]
	autoconnect = boolean(default=False)
	self_hosted = boolean(default=False)
	connection_type = integer(default=0)
	host = string(default="")
	port = integer(default=6837)
	key = string(default="")

[seen_motds]
	__many__ = string(default="")

[trusted_certs]
	__many__ = string(default="")

[ui]
	play_sounds = boolean(default=True)
""")


def get_config():
	global _config
	if not _config:
		path = os.path.abspath(os.path.join(globalVars.appArgs.configPath, CONFIG_FILE_NAME))
		if os.path.isfile(path):
			_config = configobj.ConfigObj(infile=path, configspec=configspec)
			validator = validate.Validator()
			_config.validate(validator)
			config.conf[configRoot] = _config.dict()
			config.post_configSave.register(onSave)
			config.post_configReset.register(onReset)
		else:
			_config = configobj.ConfigObj(configspec=configspec)
			config.conf.spec[configRoot] = _config.configspec.dict()
	_config = config.conf[configRoot]
	return _config


def write_connection_to_config(connection_info: ConnectionInfo):
	"""Writes a connection to the last connected section of the config.
	If the connection is already in the config, move it to the end.

	Args:
		connection_info: The ConnectionInfo object containing connection details
	"""
	conf = get_config()
	last_cons = conf["connections"]["last_connected"]
	address = connection_info.getAddress()
	if address in last_cons:
		conf["connections"]["last_connected"].remove(address)
	conf["connections"]["last_connected"].append(address)


def onSave():
	path = os.path.abspath(os.path.join(globalVars.appArgs.configPath, CONFIG_FILE_NAME))
	if os.path.isfile(path):  # We have already merged the config, so we can just delete the file
		os.remove(path)
	config.post_configSave.unregister(onSave)
	config.post_configReset.unregister(onReset)


def onReset():
	config.post_configSave.unregister(
		onSave,
	)  # We don't want to delete the file if we reset the config after merging
	config.post_configReset.unregister(onReset)
