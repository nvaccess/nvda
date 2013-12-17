#winVersion.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2013 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import sys
import winUser

def canRunVc2010Builds():
	OSVersion=sys.getwindowsversion()
	if (OSVersion.major, OSVersion.minor) < (5, 1):
		# Earlier than Windows XP.
		return False
	if OSVersion.major == 5:
		if OSVersion.minor == 1:
			# Windows XP for x86.
			return OSVersion.service_pack_major >= 2
		if OSVersion.minor == 2 and OSVersion.product_type!=1: 
			# Windows Server 2003.
			# (5.2 x64 is Windows XP x64. Its RTM is based on Server 2003 sp1,
			# so all versions should be fine.)
			return OSVersion.service_pack_major >= 1
	return True
