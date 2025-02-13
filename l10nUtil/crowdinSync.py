# A part of NonVisual Desktop Access (NVDA)
# based on file from https://github.com/jcsteh/osara
# Copyright (C) 2023-2024 NV Access Limited, James Teh
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import os

import requests


crowdinFileIDs = {
	"nvda.po": 2,
	# alias for nvda.po
	"nvda.pot": 2,
	"userGuide.xliff": 18,
	# lowercase alias for userGuide.xliff
	"userguide.xliff": 18,
	"changes.xliff": 20,
}


def normalizeLanguage(lang: str) -> str:
	""" Normalize a language code to Crowdin's format. """
	lang = lang.replace("_", "-")
	return lang


PROJECT_ID = "598017"


def fetchAuthToken():
	token = os.getenv("crowdinAuthToken", "").strip()
	if token:
		print("Using auth token from environment variable")
		return token
	token_path = os.path.expanduser("~/.nvda_crowdin")
	if os.path.exists(token_path):
		with open(token_path, 'r') as f:
			token = f.read().strip()
			print("Using auth token from ~/.nvda_crowdin")
			return token
	token = input("Enter Crowdin auth token: ").strip()
	with open(token_path, 'w') as f:
		f.write(token)
	return token


def request(
	path: str,
	method=requests.get,
	headers: dict[str, str] | None = None,
	**kwargs,
) -> requests.Response:
	if headers is None:
		headers = {}
	AUTH_TOKEN = fetchAuthToken()
	headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
	r = method(
		f"https://api.crowdin.com/api/v2/{path}",
		headers=headers,
		**kwargs,
	)
	# Convert errors to exceptions, but print the response before raising.
	try:
		r.raise_for_status()
	except requests.exceptions.HTTPError:
		print(r.json())
		raise
	return r


def projectRequest(path: str, **kwargs) -> requests.Response:
	return request(f"projects/{PROJECT_ID}/{path}", **kwargs)


def uploadSourceFile(crowdinFilePath: str, localFilePath: str) -> None:
	crowdinFileID = crowdinFileIDs[crowdinFilePath]
	fn = os.path.basename(localFilePath)
	print(f"Uploading {localFilePath} to Crowdin temporary storage as {fn}")
	with open(localFilePath, "rb") as f:
		r = request(
			"storages",
			method=requests.post,
			headers={"Crowdin-API-FileName": fn},
			data=f,
		)
	storageID = r.json()["data"]["id"]
	print(f"Updating file {crowdinFileID} ({crowdinFilePath})  on Crowdin with storage ID {storageID}")
	r = projectRequest(
		f"files/{crowdinFileID}",
		method=requests.put,
		json={"storageId": storageID},
	)
	revisionId = r.json()["data"]["revisionId"]
	print(f"Updated to revision {revisionId}")

def downloadTranslationFile(crowdinFilePath: str, localFilePath: str, language: str) -> None:
	crowdinFileID = crowdinFileIDs[crowdinFilePath]
	language = normalizeLanguage(language)
	print(f"Requesting {crowdinFilePath} (file ID {crowdinFileID}) for {language} from Crowdin")
	r = projectRequest(f"translations/exports", method=requests.post, json={"fileIds": [crowdinFileID], "targetLanguageId": language})
	r.raise_for_status()
	json = r.json()
	download_url = json["data"]["url"]
	print(f"Downloading {crowdinFilePath} for {language} from {download_url}")
	r2 = requests.get(download_url)
	r2.raise_for_status()
	with open(localFilePath, "wb") as f:
		f.write(r2.content)
	print(f"Downloaded {crowdinFilePath} for {language} to {localFilePath}")

def uploadTranslationFile(crowdinFilePath: str, localFilePath: str, language: str) -> None:
	crowdinFileID = crowdinFileIDs[crowdinFilePath]
	language = normalizeLanguage(language)
	fn = os.path.basename(localFilePath)
	print(f"Uploading {localFilePath} to Crowdin temporary storage as {fn}")
	with open(localFilePath, "rb") as f:
		r = request(
			"storages",
			method=requests.post,
			headers={"Crowdin-API-FileName": fn},
			data=f,
		)
	storageID = r.json()["data"]["id"]
	print(f"Updating file {crowdinFileID} ({crowdinFilePath})  on Crowdin with storage ID {storageID}")
	r = projectRequest(
		f"translations/{language}",
		method=requests.post,
		json={"storageId": storageID, "fileId": crowdinFileID,},
	)
	print("Done")
