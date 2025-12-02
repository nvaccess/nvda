from enum import Enum
import ctypes


class filter(Enum):
	NORMAL = "normal"
	GREYSCALE = "greyscale"
	INVERTED = "inverted"


class filterMatrix(Enum):
	NORMAL = (ctypes.c_float * 25)(
		1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
	)

	GREYSCALE = (ctypes.c_float * 25)(
		0.33,
		0.33,
		0.33,
		0.0,
		0.0,
		0.59,
		0.59,
		0.59,
		0.0,
		0.0,
		0.11,
		0.11,
		0.11,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
	)

	INVERTED = (ctypes.c_float * 25)(
		-1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		-1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		-1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
		0.0,
		1.0,
		1.0,
		1.0,
		0.0,
		1.0,
	)
