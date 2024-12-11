# A part of NonVisual Desktop Access (NVDA)
# based on file from https://github.com/jcsteh/osara
# Copyright (C) 2023-2024 NV Access Limited, James Teh
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import argparse
import os

import requests

crowdinFileIDs = {
	"nvda.po": 2,
	# alias for nvda.po
	"nvda.pot": 2,
	"userGuide.xliff": 18,
	"changes.xliff": 20,
}


AUTH_TOKEN = os.getenv("crowdinAuthToken", "").strip()
AUTH_TOKEN = "e74a03dccb6ee4f7bef20bb3f2635af032c600046b4622f948a1cb5a3a876060e6b491c413f6dd1d"
if not AUTH_TOKEN:
	raise ValueError("crowdinAuthToken environment variable not set")
PROJECT_ID = os.getenv("crowdinProjectID", "").strip()
PROJECT_ID = "598017"
if not PROJECT_ID:
	raise ValueError("crowdinProjectID environment variable not set")


def request(
	path: str,
	method=requests.get,
	headers: dict[str, str] | None = None,
	**kwargs,
) -> requests.Response:
	if headers is None:
		headers = {}
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
	print(f"Requesting {crowdinFilePath} for {language} from Crowdin")
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


def main():
	parser = argparse.ArgumentParser(
		description="Syncs translations with Crowdin.",
	)
	commands = parser.add_subparsers(dest="command", required=True)
	uploadSourceFileCommand = commands.add_parser(
		"uploadSourceFile",
		help="Upload a source file to Crowdin.",
	)
	uploadSourceFileCommand.add_argument(
		"crowdinFilePath",
		choices=crowdinFileIDs.keys(),
		help="The Crowdin file path"
	)
	uploadSourceFileCommand.add_argument("localFilePath", help="The path to the local file.")
	downloadTranslationFileCommand = commands.add_parser(
		"downloadTranslationFile",
		help="Download a translation file from Crowdin.",
	)
	downloadTranslationFileCommand.add_argument(
		"crowdinFilePath",
		choices=crowdinFileIDs.keys(),
		help="The Crowdin file path"
	)
	downloadTranslationFileCommand.add_argument("localFilePath", help="The path to save the local file.")
	downloadTranslationFileCommand.add_argument(
		"language",
		help="The language code to download the translation for."
	)
	uploadTranslationFileCommand = commands.add_parser(
		"uploadTranslationFile",
		help="Upload a translation file to Crowdin.",
	)
	uploadTranslationFileCommand.add_argument(
		"crowdinFilePath",
		choices=crowdinFileIDs.keys(),
		help="The Crowdin file path"
	)
	uploadTranslationFileCommand.add_argument("localFilePath", help="The path to the local file.")
	uploadTranslationFileCommand.add_argument(
		"language",
		help="The language code to upload the translation for."
	)
	args = parser.parse_args()
	match args.command:
		case "uploadSourceFile":
			uploadSourceFile(args.crowdinFilePath, args.localFilePath)
		case "downloadTranslationFile":
			downloadTranslationFile(args.crowdinFilePath, args.localFilePath, args.language)
		case "uploadTranslationFile":
			uploadTranslationFile(args.crowdinFilePath, args.localFilePath, args.language)
		case _:
			raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
	main()
