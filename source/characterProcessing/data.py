# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2010-2024 NV Access Limited, World Light Information Limited,
# Hong Kong Blind Union, Babbage B.V., Julien Cochuyt, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


from typing import Callable, Generic, TypeVar


_LocaleDataT = TypeVar("_LocaleDataT")


class LocaleDataMap(Generic[_LocaleDataT], object):
	"""Allows access to locale-specific data objects, dynamically loading them if needed on request"""

	def __init__(self, localeDataFactory: Callable[[str], _LocaleDataT]):
		"""
		:param localeDataFactory: the factory to create data objects for the requested locale.
		"""
		self._localeDataFactory: Callable[[str], _LocaleDataT] = localeDataFactory
		self._dataMap: dict[str, _LocaleDataT] = {}

	def fetchLocaleData(self, locale: str, fallback: bool = True) -> _LocaleDataT:
		"""
		Fetches a data object for the given locale.
		This may mean that the data object is first created and stored if it does not yet exist in the map.
		The locale is also simplified (country is dropped) if the fallback argument is True and the full locale can not be used to create a data object.
		:param locale: the locale of the data object requested
		:param fallback: if true and there is no data for the locale, then the country (if it exists) is stripped and just the language is tried.
		:return: the data object for the given locale
		"""
		localeList = [locale]
		if fallback and "_" in locale:
			localeList.append(locale.split("_")[0])
		for loc in localeList:
			data = self._dataMap.get(loc)
			if data:
				return data
			try:
				data = self._localeDataFactory(loc)
			except LookupError:
				data = None
			if not data:
				continue
			self._dataMap[loc] = data
			return data
		raise LookupError(locale)

	def invalidateLocaleData(self, locale: str) -> None:
		"""Invalidate the data object (if any) for the given locale.
		This will cause a new data object to be created when this locale is next requested.
		:param locale: The locale for which the data object should be invalidated.
		"""
		try:
			del self._dataMap[locale]
		except KeyError:
			pass

	def invalidateAllData(self):
		"""Invalidate all data within this locale map.
		This will cause a new data object to be created for every locale that is next requested.
		"""
		self._dataMap.clear()
