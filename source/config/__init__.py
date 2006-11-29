# NVDA Configuration Support

configFileName = "nvda.ini"

import os
from StringIO import StringIO
from configobj import ConfigObj
from validate import Validator
val = Validator()

### The configuration specification
confspec = StringIO("""# NVDA Configuration File

#Language settings
[language]
	language = string(default="enu")

# Speech settings
[speech]
	# The synthesiser to use
	synth = string(default=auto)

	[[__many__]]
		rate = integer(default=60)
		pitch = integer(default=50)
		volume = integer(default=100)
		voice = integer(default=1)
		speakPunctuation = boolean(default=False)
		relativeUppercasePitch = integer(default=20)

# Presentation settings
[presentation]
		reportClassOfClientObjects = boolean(default=true)
		reportClassOfAllObjects = boolean(default=false)
		reportKeyboardShortcuts = boolean(default=true)
		reportTooltips = boolean(default=true)
		reportHelpBalloons = boolean(default=true)

[mouse]
	reportObjectUnderMouse = boolean(default=true)
	reportMouseShapeChanges = boolean(default=false)

#Keyboard settings
[keyboard]
	speakTypedCharacters = boolean(default=true)
	speakTypedWords = boolean(default=false)
	speakCommandKeys = boolean(default=false)


#Settings for document reading (such as MS Word and wordpad)
[documentFormatting]
	#These settings affect what information is reported when you navigate to text where the formatting  or placement has changed
	reportFontName = boolean(default=false)
	reportFontSize = boolean(default=false)
	reportFontAttributes = boolean(default=false)
	reportStyle = boolean(default=true)
	reportPage = boolean(default=true)
	reportTables = boolean(default=true)
	reportAlignment = boolean(default=false)

""".replace("\n", "\r\n"))

### Globals
conf = None
mtime = 0

def load():
	global conf, mtime
	# If the config file exists, store its mtime.
	if os.path.isfile(configFileName):
		mtime = os.path.getmtime(configFileName)
	conf = ConfigObj(configFileName, configspec = confspec, indent_type = "\t")
	# Python converts \r\n to \n when reading files in Windows, so ConfigObj can't determine the true line ending.
	conf.newlines = "\r\n"
	conf.validate(val)

def checkSynth(name):
	"Validate the configuration for the selected synth."
	speech = conf["speech"]
	# If there are no settings for this synth, make sure there are defaults.
	if not speech.has_key(name):
		speech[name] = {}
		conf.validate(val, copy = True, section = speech)

def save(force = False):
	global conf, mtime
	# If the file has changed since it was read, don't save over the top of it.
	if not force and os.path.isfile(configFileName) and os.path.getmtime(configFileName) != mtime:
		return
	# Copy default settings and formatting.
	conf.validate(val, copy = True)
	conf.write()

def getSynthConfig():
	"A convenience function to return the config for the current speech synth."
	return conf["speech"][conf["speech"]["synth"]]

### Main
load()
