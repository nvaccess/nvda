# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 Pavol Kecskemety <pavol.kecskemety@eset.sk>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import appModuleHandler


class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self, obj):
		obj.description = None
		obj.shouldAllowIAccessibleFocusEvent = True

		if obj.name == obj.value:
			obj.value = None
