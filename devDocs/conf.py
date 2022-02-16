# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019-2020 NV Access Limited, Leonard de Ruijter, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('../source'))
import sourceEnv  # noqa: F401, E402

# Initialize languageHandler so that sphinx is able to deal with translatable strings.
import languageHandler  # noqa: E402
languageHandler.setLanguage("en")

# Initialize globalVars.appArgs to something sensible.
import globalVars  # noqa: E402


# Set an empty config path
# This is never used as we don't initialize config, but some modules expect this to be set.
globalVars.appArgs.configPath = ""
globalVars.appArgs.disableAddons = True


# #11971: NVDA is not running, therefore app dir is undefined.
# Therefore tell NVDA that apt source directory is app dir.
appDir = os.path.join("..", "source")
globalVars.appDir = os.path.abspath(appDir)


# Import NVDA's versionInfo module.
import versionInfo  # noqa: E402
# Set a suitable updateVersionType for the updateCheck module to be imported
versionInfo.updateVersionType = "stable"

# -- Project information -----------------------------------------------------

project = versionInfo.name
copyright = versionInfo.copyright
author = versionInfo.publisher

# The major project version
version = versionInfo.formatVersionForGUI(
	versionInfo.version_year,
	versionInfo.version_major,
	versionInfo.version_minor
)

# The full version, including alpha/beta/rc tags
release = versionInfo.version

# -- General configuration ---------------------------------------------------

default_role = 'py:obj'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	'sphinx.ext.autodoc',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
	"_build"
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.

html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

# sphinx.ext.autodoc configuration

# Both the class’ and the __init__ method’s docstring are concatenated and inserted.
autoclass_content = "both"
autodoc_member_order = 'bysource'
autodoc_mock_imports = [
	"louis",  # Not our project
]

# Perform some manual mocking of specific objects.
# autodoc can only mock modules, not objects.
from sphinx.ext.autodoc.mock import _make_subclass  # noqa: E402

import config  # noqa: E402
# Mock an instance of the configuration manager.
config.conf = _make_subclass("conf", "config")()
