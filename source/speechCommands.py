#speechCommands.py
#part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2011 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

class SpeechCommand(object):
	"""
	The base class for objects that can be inserted between string of text for parituclar speech functions that convey  things such as indexing or voice parameter changes.
	"""

class IndexCommand(SpeechCommand):
	"""Represents an index within some speech."""

	def __init__(self,index):
		"""
		@param index: the value of this index
		@type index: integer
		"""
		if not isinstance(index,int): raise ValueError("index must be int, not %s"%type(index))
		self.index=index

class CharacterMode(object):
	"""Turns character mode on and off for speech synths."""

	def __init__(self,state):
		"""
		@param state: if true character mode is on, if false its turned off.
		@type state: boolean
		"""
		if not isinstance(state,bool): raise ValueError("state must be boolean, not %s"%type(state))
		self.state=state
