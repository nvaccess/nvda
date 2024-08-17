# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited, Noelia Ruiz Martínez, Leonard de Ruijter

import controlTypes
from urllib.parse import ParseResult, urlparse, urlunparse
from logHandler import log


def getLinkType(url: str, rootUrl: str) -> controlTypes.State | None:
	"""Returns the link type corresponding to a given URL.

	:param url: The URL of the link destination
	:param rootUrl: The root URL of the page
	:return: A controlTypes.State corresponding to the link type, or C{None} if the state cannot be determined
	"""
	if not url or not rootUrl:
		log.debug("getLinkType: Either url or rootUrl is empty.")
		return None
	if isSamePageUrl(url, rootUrl):
		log.debug(f"getLinkType: {url} is an internal link.")
		return controlTypes.State.INTERNAL_LINK
	log.debug(f"getLinkType: {url} type is unknown.")
	return None


def isSamePageUrl(urlOnPage: str, rootUrl: str) -> bool:
	"""Returns whether a given URL belongs to the same page as another URL.

	:param urlOnPage: The URL that should be on the same page as `rootUrl`
	:param rootUrl: The root URL of the page
	:return: Whether `urlOnPage` belongs to the same page as `rootUrl`
	"""
	if not urlOnPage or not rootUrl:
		return False

	# Parse the URLs
	urlOnPageParsed: ParseResult = urlparse(urlOnPage)
	rootUrlParsed: ParseResult = urlparse(rootUrl)

	# Reconstruct URLs without fragments for comparison
	urlOnPageWithoutFragment = urlunparse(urlOnPageParsed._replace(fragment=""))
	rootUrlWithoutFragment = urlunparse(rootUrlParsed._replace(fragment=""))
	fragmentInvalidChars: str = "%/"  # Characters not considered valid in fragments
	return (
		urlOnPageWithoutFragment == rootUrlWithoutFragment
		and urlOnPageParsed.fragment
		and not any(char in urlOnPageParsed.fragment for char in fragmentInvalidChars)
	)
