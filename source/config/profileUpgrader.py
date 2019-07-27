# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from logHandler import log
from .configSpec import latestSchemaVersion, confspec
from configobj import flatten_errors
from copy import deepcopy
from . import profileUpgradeSteps

SCHEMA_VERSION_KEY = "schemaVersion"

def upgrade(profile, validator, writeProfileToFileFunc):
	""" Upgrade a profile in memory and validate it
	If it is safe to do so, as defined by shouldWriteProfileToFile, the profile is written out.
	"""
	# when profile is none or empty we can still validate. It should at least have a version set.
	_ensureVersionProperty(profile)
	startSchemaVersion = int(profile[SCHEMA_VERSION_KEY])
	log.debug("Current config schema version: {0}, latest: {1}".format(startSchemaVersion, latestSchemaVersion))
	for fromVersion in range(startSchemaVersion, latestSchemaVersion):
		_doConfigUpgrade(profile, fromVersion)
	_doValidation(deepcopy(profile), validator) # copy the profile, since validating mutates the object
	try:
		# write out the configuration once the upgrade has been validated. This means that if NVDA crashes for some
		# other reason the file does not need to be upgraded again.
		if writeProfileToFileFunc:
			writeProfileToFileFunc(profile.filename, profile)
	except Exception as e:
		log.warning("Error saving configuration; probably read only file system")
		log.debugWarning("", exc_info=True)
		pass

def _doConfigUpgrade(profile, fromVersion):
	toVersion = fromVersion+1
	upgradeStepName = "upgradeConfigFrom_{0}_to_{1}".format(fromVersion, toVersion)
	upgradeStepFunc = getattr(profileUpgradeSteps, upgradeStepName)
	log.debug("Upgrading from schema version {0} to {1}".format(fromVersion, toVersion))
	upgradeStepFunc(profile)
	profile[SCHEMA_VERSION_KEY] = toVersion

def _doValidation(profile, validator):
	oldConfSpec = profile.configspec
	profile.configspec = confspec
	result = profile.validate(validator, preserve_errors=True)
	profile.configspec = oldConfSpec

	if isinstance(result, bool) and not result:
		# empty file?
		raise ValueError("Unable to validate config file after upgrade.")

	flatResult = flatten_errors(profile, result)
	for section_list, key, value in flatResult :
		 # bool values don't matter
		 #	True and the value is fine.
		 #	False and the value is missing (which is typically fine)
		 # dict values should be recursively checked 
		if not isinstance(value, bool):
			errorString=(
				u"Unable to validate config file after upgrade: Key {0} : {1}\n" +
				"Full result: (value of false means the key was not present)\n" +
				"{2}"
				).format(key, value, flatResult)
			raise ValueError(errorString)

def _ensureVersionProperty(profile):
	isEmptyProfile = 1 > len(profile)
	if isEmptyProfile:
		log.debug("Empty profile, triggering default schema version")
		profile[SCHEMA_VERSION_KEY] = latestSchemaVersion
	elif not SCHEMA_VERSION_KEY in profile:
		# this must be a "before schema versions" config file.
		log.debug("No schema version found, setting to zero.")
		profile[SCHEMA_VERSION_KEY] = 0
