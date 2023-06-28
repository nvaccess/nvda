# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023, NV Access Limited, Luke Davis
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

# To add/edit URL entries in this module, search for "###".

"""
Centralized URL provider.
The purpose of this module is to provide a centralized location for all
URLs used as part of the NVDA source, and a singleton to manage them.
This will make it unnecessary to search code when URLs need to be
updated, and will provide a central mechanism for URLs to be changed
at runtime by add-ons.

Usage:

It is intended that all URLs be managed by a single object.

```
from utils.urls import URLs

# Add the URL for NV Access:
URLs.add("nvAccess", "https://nvaccess.org")

# Read access:
ui.browseableMessage(URLs.nvAccess, title="A link to NV Access")

# Divert the NV Access URL to somewhere else, such as an add-on might do:
URLs.divert(
	"nvAccess",
	reason="Our country does not allow this URL to be reached directly",
	URL="https://fake.proxy.site/target=nvaccess.org"
)
```

The info level log will contain notices as URLs are requested, and will
note the reason if they have been diverted.
"""


import sys
from dataclasses import dataclass, field
from typing import Dict, Any

from logHandler import log


# Gives us singleton behavior
class _Singleton(type):
	_instances: dict = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super().__call__(*args, **kwargs)
		return cls._instances[cls]


#: Contains a single URL used somewhere in NVDA.
#: Does its best to make that an immutable string.
@dataclass(frozen=True, repr=False)
class _URL(str):
	__slots__ = ("_URL")
	_URL: str


@dataclass(frozen=True, repr=False, init=True)
class URLManager(metaclass=_Singleton):
	"""Singleton class to manage a collection of URLs. Handles
	adding/returning them, and replacing them when they are
	overridden (diverted) by an add-on.
	"""
	_originalURLs: Dict[str, str] = field(default_factory=dict)
	"""
	URLs setup by the add method.
	E.g.: URLs added at NVDA compile time.
	"""
	_divertedURLs: Dict[str, str] = field(default_factory=dict)
	"""
	URLs wherein the original URL has been replaced by another.
	E.g.: an add-on patching a URL to reach an alternate address.
	"""
	_blames: Dict[str, str] = field(default_factory=dict)
	"""Loggable info about methods which diverted original URLs."""

	def __post_init__(self):
		log.debug("Initializing URLManager")

	def add(self, handle: str, URL: str, requireSecure: bool = True) -> None:
		"""Adds a new URL to the URLs collection.

		@param handle: a name by which this URL will be known.
		@param URL: A URL which should start with "https".
		@param requireSecure: Set to False if an "http" URL must
		be used. Avoid if possible.
		"""
		# Check URL security
		if (
			not URL.lower().startswith("https://")
			and requireSecure
		):
			raise ValueError("URL is not secure (does not start with 'https').")
		# If we don't know about this URL, add it to the collection
		if handle not in self._originalURLs:
			self._originalURLs[handle] = _URL(URL)
		else:
			log.error(
				f"Attempted to set a URL for handle {handle}, which is already set in URLs collection."
				f" The URL was: {URL}.",
				exc_info=True
			)
			raise NameError(f"Handle {handle} already in use in URLs collection.") from None

	def divert(self, handle: str, reason: str, URL: str, requireSecure: bool = True) -> None:
		"""Replaces a URL in the URLs collection.

		@param handle: The handle of the URL being diverted.
		@param reason: Brief loggable purpose for diversion.
		@param URL: A URL which should start with "https".
		@param requireSecure: Set to False if an "http" URL must
		be used. Avoid if possible.
		"""
		# Check URL security
		if (
			not URL.lower().startswith("https://")
			and requireSecure
		):
			raise ValueError("URL is not secure (does not start with 'https').")
		# If we don't know about this URL, add it to the collection
		if handle not in self._originalURLs:
			log.warn(
				f"Attempted to divert the {handle} URL, which wasn't set. "
				f"Adding it instead.\nDiscarding reason, which was: '{reason}'."
			)
			self._originalURLs[handle] = _URL(URL)
		else:
			self._divertedURLs[handle] = _URL(URL)
			stackInfo = sys._getframe().f_back.f_code
			self._blames[handle] = (
				stackInfo.co_name,
				stackInfo.co_filename,
				reason
			)
			log.debug(
				f"Set diversion of the {handle} URL by {stackInfo.co_name} in "
			 	f"{stackInfo.co_filename}, because {reason}"
			 )

	def __getattr__(self, handle) -> Any:
		"""Delivers the requested URL.

		@returns the URL for the handle if set.
		@raises AttributeError if the URL doesn't exist.
		"""
		if handle in self._divertedURLs:
			log.info(
				f"Using diverted URL for {handle}: <{self._divertedURLs[handle]}>. "
				f"{self._blames[handle][0]} diverted this URL because {self._blames[handle][2]}."
			)
			return self._divertedURLs[handle]
		elif handle in self._originalURLs:
			log.info(f"Using URL for {handle}: <{self._originalURLs[handle]}>.")
			return self._originalURLs[handle]
		else:
			raise AttributeError(f"{handle} does not refer to a recognized URL.")


# Create the URLs singleton.
URLs = URLManager()


### The rest of this file contains URL entries ###

URLs.add("nvAccess", "https://nvaccess.org")
URLs.add("NVDAUpdateChecks", "https://www.nvaccess.org/nvdaUpdateCheck")
URLs.add("donate", "https://www.nvaccess.org/donate/")
URLs.add("gpl2", "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html")
URLs.add("communityAddonsSite", "https://addons.nvda-project.org")

# speechXml.py
URLs.add("speechXMLNS", "https://www.w3.org/2001/10/synthesis")
