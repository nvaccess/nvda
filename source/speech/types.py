# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 NV Access Limited

"""Types used by speech package.
Kept here so they can be re-used without having to worry about circular imports.
"""
from typing import Union, List
from .commands import SpeechCommand

SpeechSequence = List[Union[SpeechCommand, str]]
