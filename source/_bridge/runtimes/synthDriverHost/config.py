# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import types

# fixme: This is a minimal config.conf dict to allow synth drivers to initialize.
# This should be converted to a proper proxy.
class FakeConfDict(dict):
	getConfigValidation = staticmethod(lambda path: types.SimpleNamespace(default='default') if path[0] == 'audio' and path[1] == 'outputDevice' else None)

conf = FakeConfDict()
conf.update({
	'audio': {
		'outputDevice': 'default',
	},
	'speech': {
		'useWASAPIForSAPI4': True,
	},
	'debugLog': {
		'synthDriver': False,
	},
})
