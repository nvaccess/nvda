# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from abc import ABC, abstractmethod


class ImageCaptioner(ABC):
	"""Abstract interface for image caption generation.

	Supports generate caption for image
	"""

	@abstractmethod
	def generateCaption(self, image: str | bytes, maxLength: int | None = None) -> str:
		"""
		Generate a caption for the given image.

		:param image: Image file path or binary data.
		:param maxLength: Optional maximum length for the generated caption.
		:return: The generated image caption as a string.
		"""
		pass
