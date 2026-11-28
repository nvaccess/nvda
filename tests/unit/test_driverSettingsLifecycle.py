# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Cary-rowen
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Settings persistence across profile changes, without hardware."""

import unittest
from copy import deepcopy
from unittest.mock import Mock, patch

import braille
import config
import extensionPoints
import synthDriverHandler
from autoSettingsUtils import autoSettings
from autoSettingsUtils.driverSetting import NumericDriverSetting
from configobj import ConfigObj
from driverHandler import Driver
from speech.manager import SpeechManager
from synthDrivers.silence import SynthDriver as SilenceSynthDriver


class SettingsDriver(Driver):
	name = "memory"
	_configSection = "speech"
	supportedSettings = (NumericDriverSetting("rate", "Rate", defaultVal=50),)
	rate = 50


class SettingsSynth(SilenceSynthDriver):
	name = "memory"
	supportedSettings = (synthDriverHandler.SynthDriver.RateSetting(),)
	rate = 50


class TestDriverSettingsLifecycle(unittest.TestCase):
	def setUp(self) -> None:
		for name in ("pre_configProfileSwitch", "post_configProfileSwitch", "pre_configSave"):
			self.enterContext(patch.object(config, name, extensionPoints.Action()))
		self.enterContext(patch.object(config, "confspec", deepcopy(config.confspec)))
		with patch.object(config.NVDAState, "shouldWriteToDisk", return_value=False):
			self.conf = config.ConfigManager()
		self.enterContext(patch.object(config, "conf", self.conf))
		self.base = self.conf.profiles[0]
		self.conf["speech"]["synth"] = "memory"
		self.conf["speech"]["memory"] = {"rate": 85}
		self.first = self.addProfile("first", 55)
		self.second = self.addProfile("second", 35)

	def addProfile(self, name: str, rate: int) -> ConfigObj:
		profile = ConfigObj({"speech": {"memory": {"rate": rate}}})
		profile.name = name
		profile.manual = False
		profile.triggered = False
		self.conf._profileCache[name] = profile
		return profile

	def trigger(self, name: str, notify: bool = True) -> config.ProfileTrigger:
		trigger = config.ProfileTrigger()
		trigger.spec = name
		trigger._shouldNotifyProfileSwitch = notify
		self.conf.triggersToProfiles[name] = name
		return trigger

	def makeDriver(self) -> SettingsDriver:
		driver = SettingsDriver()
		driver.initSettings()
		self.addCleanup(driver.terminate)
		return driver

	def installSynth(self) -> SettingsSynth:
		self.enterContext(patch.object(synthDriverHandler, "changeVoice"))
		synth = SettingsSynth()
		synth.initSettings()
		self.enterContext(patch.object(synthDriverHandler, "_curSynth", synth))
		self.enterContext(
			patch.object(synthDriverHandler, "_audioOutputDevice", self.conf["audio"]["outputDevice"]),
		)
		self.addCleanup(synthDriverHandler.setSynth, None)
		synthDriverHandler.initialize()
		return synth

	def test_preSwitchWritesOutgoingProfile(self) -> None:
		self.conf.manualActivateProfile("first")
		cachedSpeech = self.conf["speech"]
		seen = []

		def before() -> None:
			self.assertIs(self.conf.profiles[-1], self.first)
			cachedSpeech["memory"]["rate"] = 60
			self.conf["braille"]["cursorBlinkRate"] = 800
			seen.append("pre")

		def after(prevConf: dict) -> None:
			self.assertEqual(prevConf["speech"]["memory"]["rate"], 60)
			self.assertEqual(self.conf["speech"]["memory"]["rate"], 35)
			seen.append("post")

		config.pre_configProfileSwitch.register(before)
		config.post_configProfileSwitch.register(after)
		self.conf.manualActivateProfile("second")
		self.assertEqual(seen, ["pre", "post"])
		self.assertEqual(self.first["braille"]["cursorBlinkRate"], 800)
		self.assertEqual(self.conf._dirtyProfiles, {"first"})
		self.assertNotIn("braille", self.second)

	def test_nestedAtomicSwitchAppliesOnlyFinalStack(self) -> None:
		synth = self.installSynth()
		synth.rate = 90
		before = Mock()
		config.pre_configProfileSwitch.register(before)
		with self.conf.atomicProfileSwitch():
			self.trigger("first", notify=False).enter()
			with self.conf.atomicProfileSwitch():
				self.conf.manualActivateProfile("second")
			self.assertIs(self.conf.profiles[-1], self.base)
			before.assert_not_called()
		before.assert_called_once_with()
		self.assertEqual(self.base["speech"]["memory"]["rate"], 90)
		self.assertEqual(self.first["speech"]["memory"]["rate"], 55)
		self.assertEqual(synth.rate, 35)

	def test_atomicNoOpDoesNotNotify(self) -> None:
		notified = Mock()
		config.pre_configProfileSwitch.register(notified)
		config.post_configProfileSwitch.register(notified)
		with self.conf.atomicProfileSwitch():
			self.conf.manualActivateProfile("first")
			self.conf.manualActivateProfile(None)
		notified.assert_not_called()

	def test_failedActivationKeepsOldProfile(self) -> None:
		self.conf.manualActivateProfile("first")
		with (
			patch.object(self.conf, "_getProfile", side_effect=OSError("unreadable")),
			self.assertRaises(OSError),
		):
			self.conf.manualActivateProfile("missing")
		self.assertIs(self.conf.profiles[-1], self.first)
		self.assertTrue(self.first.manual)

	def test_deleteDuringAtomicSwitchDoesNotLeaveDirtyProfile(self) -> None:
		self.installSynth()
		self.conf.manualActivateProfile("first")
		synthDriverHandler.getSynth().rate = 60
		with (
			patch("config.os.path.isfile", return_value=True),
			patch("config.os.remove"),
			patch("globalCommands.ConfigProfileActivationCommands.removeScriptForProfile"),
			self.conf.atomicProfileSwitch(),
		):
			self.conf.deleteProfile("first")
		self.assertNotIn("first", self.conf._dirtyProfiles)
		self.assertNotIn("first", self.conf._profileCache)
		self.assertEqual(synthDriverHandler.getSynth().rate, 85)

	def test_resetAndTerminationDiscardUnsavedSettings(self) -> None:
		driver = self.makeDriver()
		driver.rate = 99
		driver.terminate()
		config.pre_configSave.notify()
		self.assertEqual(self.base["speech"]["memory"]["rate"], 85)
		before = Mock()
		config.pre_configProfileSwitch.register(before)
		self.conf.reset(factoryDefaults=True)
		before.assert_not_called()
		self.assertNotIn("memory", self.conf.profiles[0].get("speech", {}))

	def test_hostDriverCleanupDoesNotRequireProfileManager(self) -> None:
		from _bridge.runtimes.synthDriverHost import config as hostConfig

		with patch.object(autoSettings, "config", hostConfig):
			driver = SettingsDriver()
			driver.terminate()

	def test_userReplacementSavesBeforeInitializing(self) -> None:
		synth = self.installSynth()
		synth.rate = 90
		with patch.object(synthDriverHandler, "_getSynthDriver", return_value=SettingsSynth):
			synthDriverHandler.setSynth("memory")
		self.assertEqual(synthDriverHandler.getSynth().rate, 90)

	def test_audioDeviceReloadResolvesAutoWithoutRepeatedReplacement(self) -> None:
		self.installSynth().rate = 90
		self.first["speech"]["synth"] = "auto"
		self.first["audio"] = {"outputDevice": "otherDevice"}
		with (
			patch.object(synthDriverHandler, "defaultSynthPriorityList", ["memory"]),
			patch.object(synthDriverHandler, "_getSynthDriver", return_value=SettingsSynth) as factory,
			patch("speech.cancelSpeech") as cancelSpeech,
		):
			self.conf.manualActivateProfile("first")
			self.trigger("second").enter()
		factory.assert_called_once()
		cancelSpeech.assert_called_once()
		self.assertEqual(self.base["speech"]["memory"]["rate"], 90)
		self.assertEqual(synthDriverHandler.getSynth().rate, 55)
		self.assertEqual(self.first["speech"]["synth"], "memory")

	def test_cancellationDoesNotSaveOldSpeechIntoIncomingProfile(self) -> None:
		self.installSynth()
		manager = SpeechManager()
		trigger = self.trigger("first", notify=False)
		manager._restoreProfileTriggers([trigger])
		self.second["audio"] = {"outputDevice": "otherDevice"}
		with (
			patch.object(synthDriverHandler, "_getSynthDriver", return_value=SettingsSynth),
			patch("speech.cancelSpeech", side_effect=lambda: manager._exitProfileTriggers([trigger])),
		):
			self.conf.manualActivateProfile("second")
		self.assertEqual(self.second["speech"]["memory"]["rate"], 35)
		self.assertEqual(synthDriverHandler.getSynth().rate, 35)

	def test_speechBatchesDoNotSaveIntermediateProfiles(self) -> None:
		synth = self.installSynth()
		synth.rate = 90
		unrelated = Mock()
		config.pre_configProfileSwitch.register(unrelated)
		config.post_configProfileSwitch.register(unrelated)
		manager = SpeechManager()
		triggers = [self.trigger("first", notify=False), self.trigger("second", notify=False)]
		manager._restoreProfileTriggers(triggers)
		self.assertEqual(synth.rate, 35)
		synth.rate = 40
		manager._exitProfileTriggers(triggers)
		self.assertEqual(synth.rate, 90)
		self.assertEqual(self.second["speech"]["memory"]["rate"], 40)
		self.assertEqual(self.first["speech"]["memory"]["rate"], 55)
		unrelated.assert_not_called()

	def test_saveDuringSuppressedSwitchUsesLastLoadedProfile(self) -> None:
		self.first["speech"] = {}
		firstTrigger = self.trigger("first")
		firstTrigger.enter()
		driver = self.makeDriver()
		self.trigger("second", notify=False).enter()
		driver.rate = 60
		with patch.object(config.NVDAState, "shouldWriteToDisk", return_value=False):
			self.conf.save()
		self.assertEqual(self.first["speech"]["memory"]["rate"], 60)
		self.assertEqual(self.second["speech"]["memory"]["rate"], 35)
		self.assertEqual(self.conf._dirtyProfiles, {"first"})
		driver.loadSettings()
		self.assertEqual(driver.rate, 35)
		driver.rate = 40
		firstTrigger.exit()
		driver.saveSettings()
		self.assertEqual(self.second["speech"]["memory"]["rate"], 40)

	def test_saveDoesNotChangeActiveStackOrUndoAnotherSwitch(self) -> None:
		driver = self.makeDriver()
		self.trigger("first", notify=False).enter()
		driver.rate = 90
		save = driver._saveSpecificSettings

		def switchDuringSave(*args, **kwargs):
			self.assertIs(self.conf.profiles[-1], self.first)
			self.conf.manualActivateProfile("second")
			save(*args, **kwargs)

		with patch.object(driver, "_saveSpecificSettings", side_effect=switchDuringSave):
			driver.saveSettings()
		self.assertIs(self.conf.profiles[-1], self.second)
		self.assertEqual(self.base["speech"]["memory"]["rate"], 90)
		self.assertEqual(self.conf["speech"]["memory"]["rate"], 35)

	def test_saveRefreshesInheritedValuesAndLeavesConfigOnFailure(self) -> None:
		driver = self.makeDriver()
		self.first["speech"] = {}
		self.trigger("first", notify=False).enter()
		self.assertEqual(self.conf["speech"]["memory"]["rate"], 85)
		driver.rate = 90
		driver.saveSettings()
		self.assertEqual(self.conf["speech"]["memory"]["rate"], 90)
		self.assertNotIn("memory", self.first["speech"])
		with (
			patch.object(driver, "_saveSpecificSettings", side_effect=RuntimeError("disconnected")),
			self.assertRaises(RuntimeError),
		):
			driver.saveSettings()
		self.assertIs(self.conf.profiles[-1], self.first)
		self.assertEqual(self.conf["speech"]["memory"]["rate"], 90)

	def test_displaySettingsFailureStillAppliesBrailleConfig(self) -> None:
		self.conf["braille"]["display"] = "noBraille"
		self.conf["braille"]["tetherTo"] = "review"
		with (
			patch.object(braille.handler, "_tether", "focus"),
			patch.object(braille.handler, "_table", braille.handler._table),
			patch.object(braille.handler.display, "loadSettings", side_effect=OSError("disconnected")),
		):
			braille.handler.handlePostConfigProfileSwitch()
			self.assertEqual(braille.handler._tether, "review")
