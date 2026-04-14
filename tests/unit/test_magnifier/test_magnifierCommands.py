# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import unittest
from unittest.mock import MagicMock, patch

class TestZoomCommand(unittest.TestCase):
    """Tests zoom command behavior when magnifier is active or inactive."""

    def _makeMockMagnifier(self, isActive: bool) -> MagicMock:
        magnifier = MagicMock()
        magnifier.configure_mock(**{"_isActive": isActive})
        magnifier.zoomLevel = 2.0
        return magnifier

    @patch("_magnifier.commands.ui.message")
    @patch("_magnifier.commands.getMagnifier")
    @patch("_magnifier.commands.toggleMagnifier")
    def testInactiveZoomIn(
        self,
        mockToggle: MagicMock,
        mockGetMagnifier: MagicMock,
        mockMessage: MagicMock, 
    ) -> None:
        """Attempting to zoom in with an inactive magnifier should start the magnifier."""
        from _magnifier.commands import zoom
        from _magnifier.utils.types import Direction

        mockGetMagnifier.return_value = self._makeMockMagnifier(isActive=False)
        zoom(Direction.IN)
        mockToggle.assert_called_once()
        mockGetMagnifier.return_value._zoom.assert_not_called()

    @patch("_magnifier.commands.ui.message")
    @patch("_magnifier.commands.getMagnifier")
    @patch("_magnifier.commands.toggleMagnifier")
    @patch("_magnifier.commands.magnifierIsActiveVerify")
    def testInactiveZoomOut(
        self,
        mockVerify: MagicMock,
        mockToggle: MagicMock,
        mockGetMagnifier: MagicMock,
        mockMessage: MagicMock, 
    ) -> None:
        """Attempting to zoom out with an inactive magnifier should result in a warning."""
        from _magnifier.commands import zoom
        from _magnifier.utils.types import Direction

        mockGetMagnifier.return_value = self._makeMockMagnifier(isActive=False)
        zoom(Direction.OUT)
        mockToggle.assert_not_called()
        mockVerify.assert_called_once()

    @patch("_magnifier.commands.ui.message")
    @patch("_magnifier.commands.getMagnifier")
    @patch("_magnifier.commands.toggleMagnifier")
    def testActiveZoomIn(
        self,
        mockToggle: MagicMock,
        mockGetMagnifier: MagicMock,
        mockMessage: MagicMock, 
    ) -> None:
        """Attempting to zoom in with an active magnifier should zoom in."""
        from _magnifier.commands import zoom
        from _magnifier.utils.types import Direction

        magnifier = self._makeMockMagnifier(isActive=True)
        mockGetMagnifier.return_value = magnifier
        zoom(Direction.IN)
        mockToggle.assert_not_called()
        magnifier._zoom.assert_called_once_with(Direction.IN)

    @patch("_magnifier.commands.ui.message")
    @patch("_magnifier.commands.getMagnifier")
    @patch("_magnifier.commands.toggleMagnifier")
    def testActiveZoomOut(
        self,
        mockToggle: MagicMock,
        mockGetMagnifier: MagicMock,
        mockMessage: MagicMock, 
    ) -> None:
        """Attempting to zoom out with an active magnifier should zoom out."""
        from _magnifier.commands import zoom
        from _magnifier.utils.types import Direction

        magnifier = self._makeMockMagnifier(isActive=True)
        mockGetMagnifier.return_value = magnifier
        zoom(Direction.OUT)
        mockToggle.assert_not_called()
        magnifier._zoom.assert_called_once_with(Direction.OUT)

if __name__ == "__main__":
    unittest.main()
    