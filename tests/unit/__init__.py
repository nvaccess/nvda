#tests/unit/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""NVDA unit testing.
All unit tests should reside within this package and should be
divided into modules and packages similar to the code they are testing.
Test modules must have a C{test_} prefix
and should contain one or more classes with a C{Test} prefix which subclass C{unittest.TestCase}.
Methods in test classes should have a C{test_} prefix.
"""

### Ugly bootstrapping code.

import os
import sys

import locale
import gettext
#Localization settings
locale.setlocale(locale.LC_ALL,'')
gettext.install('nvda',unicode=True)

# The path to the unit tests.
UNIT_DIR = os.path.dirname(os.path.abspath(__file__))
# The path to the top of the repo.
TOP_DIR = os.path.dirname(os.path.dirname(UNIT_DIR))
# The path to the NVDA "source" directory.
SOURCE_DIR = os.path.join(TOP_DIR, "source")
# Let us import modules from the NVDA source.
sys.path.insert(1, SOURCE_DIR)
import sourceEnv

# Set options normally taken from the command line.
import globalVars
class AppArgs:
	# The path from which to load a configuration file.
	# Ideally, this would be an in-memory, default configuration.
	# However, config currently requires a path.
	# We use the unit test directory, since we want a clean config.
	configPath = UNIT_DIR.decode("mbcs")
	secure = False
	disableAddons = True
	launcher = False
globalVars.appArgs = AppArgs()

# We depend on the current directory to load some files;
# e.g. braille imports louis which loads liblouis.dll using a relative path.
os.chdir(SOURCE_DIR)
# The path to this package might be relative, so make it absolute,
# since we just changed directory.
__path__[0] = UNIT_DIR
# We don't want logging for now,
# though we may optionally want this in future; see #7045.
import logging
from logHandler import log
log.addHandler(logging.NullHandler())
# There's no point in logging anything at all, since it'll go nowhere.
log.setLevel(100)

# Much of this should eventually be replaced by stuff which gets reset before each test
# so the tests are isolated.
import config
config.initialize()
# Initialize languageHandler so that translatable strings work.
import languageHandler
languageHandler.setLanguage("en")
# NVDAObjects need appModuleHandler to be initialized.
import appModuleHandler
appModuleHandler.initialize()
# Anything which notifies of cursor updates requires braille to be initialized.
import braille
# Disable auto detection of braille displays when unit testing.
config.conf['braille']['display'] = "noBraille"
braille.initialize()
# For braille unit tests, we need to construct a fake braille display as well as enable the braille handler
# Give the display 40 cells
braille.handler.displaySize=40
braille.handler.enabled = True
# The focus and navigator objects need to be initialized to something.
from objectProvider import PlaceholderNVDAObject,NVDAObjectWithRole
phObj = PlaceholderNVDAObject()
import api
api.setFocusObject(phObj)
api.setNavigatorObject(phObj)
api.setDesktopObject(phObj)

# Stub speech functions to make them no-ops.
# Eventually, these should keep track of calls so we can make assertions.
import speech
speech.speak = lambda speechSequence, symbolLevel=None: None
speech.speakSpelling = lambda text, locale=None, useCharacterDescriptions=False: None
