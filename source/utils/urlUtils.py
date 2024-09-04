# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited, Noelia Ruiz Martínez, Leonard de Ruijter

import controlTypes
from urllib.parse import ParseResult, urlparse, urlunparse
from logHandler import log


def getLinkType(targetUrl: str, rootUrl: str) -> controlTypes.State | None:
	"""Returns the link type corresponding to a given URL.

	:param targetUrl: The URL of the link destination
	:param rootUrl: The root URL of the page
	:return: A controlTypes.State corresponding to the link type, or C{None} if the state cannot be determined
	"""
	if not targetUrl or not rootUrl:
		log.debug(f"getLinkType: Either targetUrl {targetUrl} or rootUrl {rootUrl} is empty.")
		return None
	if isSamePageUrl(targetUrl, rootUrl):
		log.debug(f"getLinkType: {targetUrl} is an internal link.")
		return controlTypes.State.INTERNAL_LINK
	log.debug(f"getLinkType: {targetUrl} type is unknown.")
	return None


def isSamePageUrl(targetUrlOnPage: str, rootUrl: str) -> bool:
	"""Returns whether a given URL belongs to the same page as another URL.

	:param targetUrlOnPage: The URL that should be on the same page as `rootUrl`
	:param rootUrl: The root URL of the page
	:return: Whether `targetUrlOnPage` belongs to the same page as `rootUrl`
	"""
	if not targetUrlOnPage or not rootUrl:
		return False

	validSchemes = ("http", "https")
	# Parse the URLs
	targetUrlOnPageParsed: ParseResult = urlparse(targetUrlOnPage)
	if targetUrlOnPageParsed.scheme not in validSchemes:
		return False
	rootUrlParsed: ParseResult = urlparse(rootUrl)
	if rootUrlParsed.scheme not in validSchemes:
		return False

	# Reconstruct URLs without schemes and without fragments for comparison
	targetUrlOnPageWithoutFragments = urlunparse(targetUrlOnPageParsed._replace(scheme="", fragment=""))
	rootUrlWithoutFragments = urlunparse(rootUrlParsed._replace(scheme="", fragment=""))

	fragmentInvalidChars: str = "/"  # Characters not considered valid in fragments
	return targetUrlOnPageWithoutFragments == rootUrlWithoutFragments and not any(
		char in targetUrlOnPageParsed.fragment for char in fragmentInvalidChars
	)
