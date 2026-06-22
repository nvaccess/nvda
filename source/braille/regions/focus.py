# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

from typing import (
	TYPE_CHECKING,
	Generator,
	List,
	Optional,
)

import api
import config
from utils.security import objectBelowLockScreenAndWindowsIsLocked

if TYPE_CHECKING:
	from NVDAObjects import NVDAObject


from .base import Region
from ..constants import CONTEXTPRES_CHANGEDCONTEXT, TEXT_SEPARATOR
from .NVDAObject import NVDAObjectRegion, NVDAObjectHasUsefulText, ReviewNVDAObjectRegion
from .textInfo import (
	CursorManagerRegion,
	ReviewCursorManagerRegion,
	ReviewTextInfoRegion,
	TextInfoRegion,
)


_cachedFocusAncestorsEnd = 0


def invalidateCachedFocusAncestors(index):
	"""Invalidate cached focus ancestors from a given index.
	This will cause regions to be generated for the focus ancestors >= index next time L{getFocusContextRegions} is called,
	rather than using cached regions for those ancestors.
	@param index: The index from which cached focus ancestors should be invalidated.
	@type index: int
	"""
	global _cachedFocusAncestorsEnd
	# There could be multiple calls to this function before getFocusContextRegions() is called.
	_cachedFocusAncestorsEnd = min(_cachedFocusAncestorsEnd, index)


def getFocusContextRegions(
	obj: "NVDAObject",
	oldFocusRegions: Optional[List[Region]] = None,
) -> Generator[Region, None, None]:
	if objectBelowLockScreenAndWindowsIsLocked(obj):
		return
	global _cachedFocusAncestorsEnd
	# Late import to avoid circular import.
	from treeInterceptorHandler import TreeInterceptor

	ancestors = api.getFocusAncestors()

	ancestorsEnd = len(ancestors)
	if isinstance(obj, TreeInterceptor):
		obj = obj.rootNVDAObject
		# We only want the ancestors of the buffer's root NVDAObject.
		if obj != api.getFocusObject():
			# Search backwards through the focus ancestors to find the index of obj.
			for index, ancestor in zip(range(len(ancestors) - 1, 0, -1), reversed(ancestors)):
				if obj == ancestor:
					ancestorsEnd = index
					break

	if oldFocusRegions:
		# We have the regions from the previous focus, so use them as a cache to avoid rebuilding regions which are the same.
		# We need to generate new regions from _cachedFocusAncestorsEnd onwards.
		# However, we must ensure that it is not beyond the last ancestor we wish to consider.
		# Also, we don't ever want to fetch ancestor 0 (the desktop).
		newAncestorsStart = max(min(_cachedFocusAncestorsEnd, ancestorsEnd), 1)
		# Search backwards through the old regions to find the last common region.
		for index, region in zip(range(len(oldFocusRegions) - 1, -1, -1), reversed(oldFocusRegions)):
			ancestorIndex = getattr(region, "_focusAncestorIndex", None)
			if ancestorIndex is None:
				continue
			if ancestorIndex < newAncestorsStart:
				# This is the last common region.
				# An ancestor may have been skipped and not have a region, which means that we need to grab new ancestors from this point.
				newAncestorsStart = ancestorIndex + 1
				commonRegionsEnd = index + 1
				break
		else:
			# No common regions were found.
			commonRegionsEnd = 0
			newAncestorsStart = 1
		# Yield the common regions.
		for region in oldFocusRegions[0:commonRegionsEnd]:
			# We are setting focusToHardLeft to False for every cached region.
			# This is necessary as BrailleHandler._doNewObject checks focusToHardLeft on every region
			# and sets it to True for the first focus region if the context didn't change.
			# If we don't do this, BrailleHandler._doNewObject can't set focusToHardLeft properly.
			region.focusToHardLeft = False
			yield region
	else:
		# Fetch all ancestors.
		newAncestorsStart = 1

	focusToHardLeftSet = False
	for index, parent in enumerate(ancestors[newAncestorsStart:ancestorsEnd], newAncestorsStart):
		if not parent.isPresentableFocusAncestor:
			continue
		region = NVDAObjectRegion(parent, appendText=TEXT_SEPARATOR)
		region._focusAncestorIndex = index
		if (
			config.conf["braille"]["focusContextPresentation"] == CONTEXTPRES_CHANGEDCONTEXT
			and not focusToHardLeftSet
		):
			# We are presenting context changes to the user
			# Thus, only scroll back as far as the start of the first new focus ancestor
			# focusToHardLeftSet is used since the first new ancestor isn't always represented by a region
			region.focusToHardLeft = True
			focusToHardLeftSet = True
		region.update()
		yield region

	_cachedFocusAncestorsEnd = ancestorsEnd


def getFocusRegions(
	obj: "NVDAObject",
	review: bool = False,
) -> Generator[Region, None, None]:
	if objectBelowLockScreenAndWindowsIsLocked(obj):
		return
	# Allow objects to override normal behaviour.
	try:
		regions = obj.getBrailleRegions(review=review)
	except (AttributeError, NotImplementedError):
		pass
	else:
		for region in regions:
			region.update()
			yield region
		return

	# Late import to avoid circular import.
	from cursorManager import CursorManager
	from NVDAObjects import NVDAObject
	from treeInterceptorHandler import DocumentTreeInterceptor, TreeInterceptor

	if isinstance(obj, CursorManager):
		region2 = (ReviewCursorManagerRegion if review else CursorManagerRegion)(obj)
	elif isinstance(obj, DocumentTreeInterceptor) or (
		isinstance(obj, NVDAObject) and NVDAObjectHasUsefulText(obj)
	):
		region2 = (ReviewTextInfoRegion if review else TextInfoRegion)(obj)
	else:
		region2 = None
	if isinstance(obj, TreeInterceptor):
		obj = obj.rootNVDAObject
	region = (ReviewNVDAObjectRegion if review else NVDAObjectRegion)(
		obj,
		appendText=TEXT_SEPARATOR if region2 else "",
	)
	region.update()
	yield region
	if region2:
		region2.update()
		yield region2
