import urllib.parse

from .protocol import SERVER_PORT


def addressToHostPort(addr):
	"""Converts an address such as google.com:80 into a tuple of (address, port).
	If no port is given, use SERVER_PORT."""
	addr = urllib.parse.urlparse("//" + addr)
	port = addr.port or SERVER_PORT
	return (addr.hostname, port)


def hostPortToAddress(hostPort):
	host, port = hostPort
	if ":" in host:
		host = "[" + host + "]"
	if port != SERVER_PORT:
		return host + ":" + str(port)
	return host
