# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from functools import reduce
from itertools import product
from typing import Any, NamedTuple
import unittest
from unittest import mock
import winreg
from _remoteClient.localMachine import LocalMachine, SoftwareSASGeneration


class CanSendSASFactors(NamedTuple):
	"""Possible external factors that could influence whether NVDA can call SendSAS."""

	hasUIAccess: bool
	openKeyRaises: Exception | None
	queryValueRaises: Exception | None
	valueData: Any
	valueType: int
	isRunningOnSecureDesktop: bool


FACTOR_VALUES = {
	"hasUIAccess": (True, False),
	"openKeyRaises": (None, FileNotFoundError, OSError),
	"queryValueRaises": (None, FileNotFoundError),
	"valueData": (*SoftwareSASGeneration, 999, "nonsense"),
	"valueType": (winreg.REG_DWORD, 999),
	"isRunningOnSecureDesktop": (True, False),
}
"""Possible values for each of the factors in :class:`CanSendSASFactors`."""

EXPECTED_SUCCESS_CASES = (
	CanSendSASFactors(
		hasUIAccess=True,
		openKeyRaises=None,
		queryValueRaises=None,
		valueData=SoftwareSASGeneration.UIACCESS,
		valueType=winreg.REG_DWORD,
		isRunningOnSecureDesktop=False,
	),
	CanSendSASFactors(
		hasUIAccess=True,
		openKeyRaises=None,
		queryValueRaises=None,
		valueData=SoftwareSASGeneration.UIACCESS,
		valueType=winreg.REG_DWORD,
		isRunningOnSecureDesktop=True,
	),
	CanSendSASFactors(
		hasUIAccess=True,
		openKeyRaises=None,
		queryValueRaises=None,
		valueData=SoftwareSASGeneration.BOTH,
		valueType=winreg.REG_DWORD,
		isRunningOnSecureDesktop=False,
	),
	CanSendSASFactors(
		hasUIAccess=True,
		openKeyRaises=None,
		queryValueRaises=None,
		valueData=SoftwareSASGeneration.BOTH,
		valueType=winreg.REG_DWORD,
		isRunningOnSecureDesktop=True,
	),
	CanSendSASFactors(
		hasUIAccess=True,
		openKeyRaises=FileNotFoundError,
		queryValueRaises=None,
		valueData=None,
		valueType=None,
		isRunningOnSecureDesktop=True,
	),
	CanSendSASFactors(
		hasUIAccess=True,
		openKeyRaises=None,
		queryValueRaises=FileNotFoundError,
		valueData=None,
		valueType=None,
		isRunningOnSecureDesktop=True,
	),
	# This case should not happen in practice
	CanSendSASFactors(
		hasUIAccess=True,
		openKeyRaises=FileNotFoundError,
		queryValueRaises=FileNotFoundError,
		valueData=None,
		valueType=None,
		isRunningOnSecureDesktop=True,
	),
)
"""Combinations of external factors under which we expect to be able to call SendSAS."""


class TestCanSendSAS(unittest.TestCase):
	"""Tests for :meth:`LocalMachine._canSendSAS`."""

	def _generate_parameters(self):
		"""Generate a list of factors sets, removing extraneous values and duplicates."""
		yield from reduce(
			# Only keep first instance of a given parameter set
			lambda acc, val: acc if val in acc else [*acc, val],
			map(
				# Keep return values
				lambda params: params
				#  if OpenKeyEx and QueryValueEx don't raise
				if params.openKeyRaises is params.queryValueRaises is None
				# Otherwise, discard the return values as they don't matter
				else params._replace(valueData=None, valueType=None),
				# Make Params instances out of the product of all of the possible parameter values
				map(CanSendSASFactors._make, product(*FACTOR_VALUES.values())),
			),
			# Start with an empty list of parameter sets
			[],
		)

	def test_canSendSAS(self):
		for params in self._generate_parameters():
			with self.subTest(**params._asdict()):
				with (
					mock.patch("_remoteClient.localMachine.hasUiAccess", return_value=params.hasUIAccess),
					mock.patch("winreg.OpenKeyEx", side_effect=params.openKeyRaises),
					mock.patch(
						"winreg.QueryValueEx",
						return_value=(params.valueData, params.valueType),
						side_effect=params.queryValueRaises,
					),
					mock.patch(
						"_remoteClient.localMachine.isRunningOnSecureDesktop",
						return_value=params.isRunningOnSecureDesktop,
					),
				):
					# Most combinations of factors will cause SendSAS to fail
					# so assume _canSendSAS should fail, unless a limited confluence of factors is achieved.
					self.assertEqual(LocalMachine._canSendSAS(), params in EXPECTED_SUCCESS_CASES)
