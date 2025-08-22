# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019-2023 NV Access Limited, Leonard de Ruijter, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

import os

_appDir = os.path.abspath(os.path.join("..", "..", "..", "source"))

# Apply several monkey patches to comtypes.
# Add our `comInterfaces` to the `comtypes.gen` search path to replicate the behavior at runtime
# without this patch many modules aren't importable, since they depend on `comInterfaces` being present.
# When a virtual environment has been created under a different version of Windows than the one
# used for developer documentation build, "ImportError: Typelib different than module" is raised
# by comTypes.
# This patch causes the error to be ignored, which matches the behavior at runtime.
import monkeyPatches.comtypesMonkeyPatches  # noqa: E402

monkeyPatches.comtypesMonkeyPatches.replace_check_version()
monkeyPatches.comtypesMonkeyPatches.appendComInterfacesToGenSearchPath()

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
globalVars.appDir = _appDir


# Import NVDA's versionInfo module.
import buildVersion  # noqa: E402
import versionInfo  # noqa: E402

# Set a suitable updateVersionType for the updateCheck module to be imported
buildVersion.updateVersionType = "stable"

# -- Project information -----------------------------------------------------

project = buildVersion.name
copyright = versionInfo.copyright
author = buildVersion.publisher

# The major project version
version = buildVersion.formatVersionForGUI(
	buildVersion.version_year,
	buildVersion.version_major,
	buildVersion.version_minor,
)

# The full version, including alpha/beta/rc tags
release = buildVersion.version

# -- General configuration ---------------------------------------------------

default_role = "py:obj"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	"sphinx.ext.autodoc",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
	"_build",
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.

html_theme = "sphinx_rtd_theme"

# -- Extension configuration -------------------------------------------------

# sphinx.ext.autodoc configuration

# Both the class’ and the __init__ method’s docstring are concatenated and inserted.
autoclass_content = "both"
autodoc_member_order = "bysource"
autodoc_mock_imports = [
	"louis",  # Not our project
]

# Perform some manual mocking of specific objects.
# autodoc can only mock modules, not objects.
from sphinx.ext.autodoc.mock import _make_subclass  # noqa: E402

import config  # noqa: E402

# Mock an instance of the configuration manager.
config.conf = _make_subclass("conf", "config")()
