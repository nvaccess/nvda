# based on file from https://github.com/jcsteh/osara

import time
import os
import glob
import sys
import zipfile
import shutil
import subprocess
import requests

AUTH_TOKEN = os.getenv("crowdinAuthToken")
if not AUTH_TOKEN:
	raise ValueError("crowdinAuthToken environment variable not set")
PROJECT_ID = int(os.getenv("crowdinProjectID"))
if not PROJECT_ID:
	raise ValueError("crowdinProjectID environment variable not set")


def request(path, method=requests.get, headers={}, **kwargs):
	headers["Authorization"] = "Bearer %s" % AUTH_TOKEN
	r = method("https://api.crowdin.com/api/v2/%s" % path, headers=headers,
		**kwargs)
	# Convert errors to exceptions, but print the response before raising.
	try:
		r.raise_for_status()
	except requests.exceptions.HTTPError:
		print(r.json())
		raise
	return r

def projectRequest(path, **kwargs):
	return request("projects/%d/%s" % (PROJECT_ID, path), **kwargs)

def uploadSourceFile(crowdinFileID, crowdinFileName, localFilePath):
	fn = os.path.basename(localFilePath)
	f = open(localFilePath, "rb")
	print(f"Uploading {localFilePath}  to Crowdin temporary storage as {crowdinFileName}")
	r = request("storages", method=requests.post,
		headers={"Crowdin-API-FileName": crowdinFileName}, data=f)
	storageID = r.json()["data"]["id"]
	print(f"Updating file {crowdinFileID} on Crowdin with storage ID {storageID}")
	r = projectRequest("files/%d" % crowdinFileID, method=requests.put,
		json={"storageId": storageID})
	return r

if __name__ == "__main__":
	command = sys.argv[1]
	if command == "uploadSourceFile":
		crowdinFileID = int(sys.argv[2])
		crowdinFileName = sys.argv[3]
		localFilePath = sys.argv[4]
		uploadSourceFile(crowdinFileID, crowdinFileName, localFilePath)
	else:
		raise ValueError("Unknown command")
