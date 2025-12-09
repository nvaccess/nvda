import types
import os
import sys

appDir = os.path.dirname(sys.executable)
appArgs = types.SimpleNamespace()
appArgs.launcher = False
appArgs.secure = False
appArgs.configPath = '.'
