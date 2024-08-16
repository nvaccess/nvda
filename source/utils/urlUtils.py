# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited, Noelia Ruiz Martínez, Leonard de Ruijter

from urllib.parse import ParseResult, urlparse


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

	if (
		urlOnPageParsed.scheme == rootUrlParsed.scheme
		and urlOnPageParsed.netloc == rootUrlParsed.netloc
		and urlOnPageParsed.path == rootUrlParsed.path
		and urlOnPageParsed.query == rootUrlParsed.query
		and urlOnPageParsed.fragment
		and urlOnPageParsed.fragment.isalnum()
	):
		return True

	return False
