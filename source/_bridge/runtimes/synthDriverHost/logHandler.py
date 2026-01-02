# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import inspect
import logging


# old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
	record = old_factory(*args, **kwargs)
	frame = inspect.currentframe()
	count = 5
	while count > 0:
		if not frame.f_back:
			break
		frame = frame.f_back
		count -= 1
	record.qualname = frame.f_code.co_qualname.removesuffix(".__init__")
	mod = os.path.splitext(os.path.basename(frame.f_code.co_filename))[0]
	record.module = mod
	return record


# logging.setLogRecordFactory(record_factory)


log = logging.getLogger()
log.debugWarning = log.debug
