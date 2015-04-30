#winVersion.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2013 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import sys
import winUser

winVersion=sys.getwindowsversion()
winVersionText="{v.major}.{v.minor}.{v.build}".format(v=winVersion)
if winVersion.service_pack_major!=0:
	winVersionText+=" service pack %d"%winVersion.service_pack_major
	if winVersion.service_pack_minor!=0:
		winVersionText+=".%d"%winVersion.service_pack_minor
winVersionText+=" %s" % ("workstation","domain controller","server")[winVersion.product_type-1]

def canRunVc2010Builds():
	if (winVersion.major, winVersion.minor) < (5, 1):
		# Earlier than Windows XP.
		return False
	if winVersion.major == 5:
		if winVersion.minor == 1:
			# Windows XP for x86.
			return winVersion.service_pack_major >= 2
		if winVersion.minor == 2 and winVersion.product_type!=1: 
			# Windows Server 2003.
			# (5.2 x64 is Windows XP x64. Its RTM is based on Server 2003 sp1,
			# so all versions should be fine.)
			return winVersion.service_pack_major >= 1
	return True
