import sys

def ding():
	raise ValueError("ding")

def dong():
	try:
		ding()
	except ValueError as e:
		return e

def dang():
	e=dong()
	raise e


dang()

