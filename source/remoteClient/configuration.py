import os
from io import StringIO

import configobj
import globalVars
from configobj import validate

from .connection_info import ConnectionInfo

CONFIG_FILE_NAME = "remote.ini"

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
		_config = configobj.ConfigObj(infile=path, configspec=configspec, create_empty=True)
		val = validate.Validator()
		_config.validate(val, copy=True)
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
	conf.write()
