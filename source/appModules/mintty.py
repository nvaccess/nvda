"""App module for mintty"""

from . import putty


class AppModule(putty.AppModule):
	TERMINAL_WINDOW_CLASS = "mintty"
