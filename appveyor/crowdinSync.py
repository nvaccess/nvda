# A part of NonVisual Desktop Access (NVDA)
# based on file from https://github.com/jcsteh/osara
# Copyright (C) 2023-2024 NV Access Limited, James Teh
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


import argparse
import os

import requests


AUTH_TOKEN = os.getenv("crowdinAuthToken", "").strip()
if not AUTH_TOKEN:
	raise ValueError("crowdinAuthToken environment variable not set")
PROJECT_ID = os.getenv("crowdinProjectID", "").strip()
if not PROJECT_ID:
	raise ValueError("crowdinProjectID environment variable not set")


def request(
		path: str,
		method=requests.get,
		headers: dict[str, str] | None = None,
		**kwargs
) -> requests.Response:
	if headers is None:
		headers = {}
	headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
	r = method(
		f"https://api.crowdin.com/api/v2/{path}",
		headers=headers,
		**kwargs
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


def uploadSourceFile(crowdinFileID: int, localFilePath: str) -> None:
	fn = os.path.basename(localFilePath)
	print(f"Uploading {localFilePath} to Crowdin temporary storage as {fn}")
	with open(localFilePath, "rb") as f:
		r = request(
			"storages",
			method=requests.post,
			headers={"Crowdin-API-FileName": fn},
			data=f
		)
	storageID = r.json()["data"]["id"]
	print(f"Updating file {crowdinFileID} on Crowdin with storage ID {storageID}")
	r = projectRequest(
		f"files/{crowdinFileID}",
		method=requests.put,
		json={"storageId": storageID}
	)
	revisionId = r.json()["data"]["revisionId"]
	print(f"Updated to revision {revisionId}")


def main():
	parser = argparse.ArgumentParser(
		description="Syncs translations with Crowdin."
	)
	commands = parser.add_subparsers(dest="command", required=True)
	uploadCommand = commands.add_parser(
		"uploadSourceFile",
		help="Upload a source file to Crowdin."
	)
	uploadCommand.add_argument("crowdinFileID", type=int, help="The Crowdin file ID.")
	uploadCommand.add_argument("localFilePath", help="The path to the local file.")
	args = parser.parse_args()
	if args.command == "uploadSourceFile":
		uploadSourceFile(args.crowdinFileID, args.localFilePath)
	else:
		raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
	main()
