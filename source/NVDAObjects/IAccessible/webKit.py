#NVDAObjects/IAccessible/webKit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2011 NV Access Inc
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from . import IAccessible

"""NVDAObjects for WebKit.
"""

class Document(IAccessible):

	def _get_treeInterceptorClass(self):
		from virtualBuffers.webKit import WebKit
		return WebKit
