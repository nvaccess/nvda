#httpRequest.py
#A part of NonVisual Desktop Access (NVDA)
#See the file COPYING for more details.
#Copyright (C) 2017 Matt Shaw, NV Access Limited

"""Provides HTTP request functionality not supported by urllib2 such as uploading files and JSON post data.
Ideally, the requests module would be used,
but requests can't currently be included in NVDA due to licensing issues.
"""

import mimetypes
import urllib2
import json

# Based on code from http://mattshaw.org/news/multi-part-form-post-with-files-in-python/
BOUNDARY = 'b8c09f07e6e54ff703f8845626a4cb64'
def encodeMultipartFormData(fields, files):
	"""
	fields is a sequence of (name, value) elements for regular form fields.
	files is a sequence of (name, filename, value) elements for data to be uploaded as files,
	where value may be a file-like object to be read.
	Note that all data is read into memory at once.
	Return (headers, body) ready for HTTP request
	"""
	CRLF = '\r\n'
	L = []
	for (key, value) in fields:
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name="%s"' % key)
		L.append('')
		L.append(value)
	for (key, filename, value) in files:
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
		L.append('Content-Type: %s' % getContentType(filename))
		L.append('')
		if not isinstance(value, str):
			value = value.read()
		L.append(value)
	L.append('--' + BOUNDARY + '--')
	L.append('')
	body = CRLF.join(L)
	headers = {'Content-Type': 'multipart/form-data; boundary=%s' % BOUNDARY}
	return headers, body

def getContentType(filename):
	return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def urlopenWithFiles(url, files, headers=None, **kwargs):
	"""Extends urllib2.urlopen to support file upload.
	url and any additional keyword arguments are passed to urllib2.urlopen as is.
	@param files: A sequence of (name, filename, value) elements for data to be uploaded as files,
		where value may be a file-like object to be read.
	@type files: sequence
	@param headers: HTTP headers.
	@type: dict of {str: str}
	"""
	if not headers:
		headers = {}
	multiHeaders, data = encodeMultipartFormData((), files)
	headers.update(multiHeaders)
	req = urllib2.Request(url, data=data, headers=headers)
	return urllib2.urlopen(req, **kwargs)

def urlopenWithJson(url, jsonData, headers=None, **kwargs):
	"""Extends urllib2.urlopen to support JSON post data.
	url and any additional keyword arguments are passed to urllib2.urlopen as is.
	@param jsonData: Object to be serialized to JSON and passed as data.
	@param headers: HTTP headers.
	@type: dict of {str: str}
	"""
	if not headers:
		headers = {}
	headers["Content-Type"] = "application/json"
	data = json.dumps(jsonData)
	req = urllib2.Request(url, data=data, headers=headers)
	return urllib2.urlopen(req, **kwargs)

def getJsonFromResponse(response):
	"""Get the JSON object from the response to an HTTP request.
	@param response: The object returned from urlopen.
	"""
	return json.loads(response.read())
