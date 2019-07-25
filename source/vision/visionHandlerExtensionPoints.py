# vision/visionHandlerExtensionPoints.py
# A  part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Module containing extension points for vision enhancement providers.

Consult the documentation of L{EventExtensionPoints} for more details.
"""

from extensionPoints import Action
from dataclasses import dataclass, field


@dataclass(repr=False, frozen=True)
class EventExtensionPoints:
	"""Data class containing extension points that will be used to notify
	vision enhancement providers about occuring events, particularly for NVDA Objects.
	Though an instance of this class is created when initializing the vision handler,
	it should never be accessed from the vision handler directly.
	Instead, vision enhancement providers should implement a "registerEventExtensionPoints" method,
	taking an instance of this class as the only argument,
	performing registration to the extension points it is interested in.
	For an example, see the L{visionEnhancementProviders.NVDAHighlighter} module.
	"""
	#: Notifies a vision enhancement provider when an object property has changed.
	#: This allows a vision enhancement provider to take an action
	#: when one of the properties of an object has changed.
	#: For example, a magnifier can track the magnified area of the screen to this object,
	#: when the name of the object has changed.
	#: Handlers are called with two  arguments.
	#: @param obj: The object that received a property change.
	#: @type obj: L{NVDAObjects.NVDAObject}
	#: @param property: The object's property that changed, e.g. "name" or "description".
	#: @type property: str
	post_objectUpdate: Action = field(default_factory=Action, init=False)
	#: Notifies a vision enhancement provider when the focused NVDAObject has changed.
	#: This allows a vision enhancement provider to take an action when the focus changed.
	#: For example, a magnifier can track the magnified area of the screen to this object.
	#: Handlers are called with one argument.
	#: @param obj: The object that received focus.
	#: @type obj: L{NVDAObjects.NVDAObject}
	post_focusChange: Action = field(default_factory=Action, init=False)
	#: Notifies a vision enhancement provider when the foreground NVDAObject has changed.
	#: This allows a vision enhancement provider to take an action
	#: when another window takes the foreground.
	#: For example, a magnifier can track the magnified area of the screen to this object.
	#: Handlers are called with one argument.
	#: @param obj: The object that became the foreground object.
	#: @type obj: L{NVDAObjects.NVDAObject}
	post_foregroundChange: Action = field(default_factory=Action, init=False)
	#: Notifies a vision enhancement provider when a physical caret has moved.
	#: This allows a vision enhancement provider to take an action
	#: when the caret moves in a window.
	#: For example, a magnifier can track the magnified area of the screen to the new caret position.
	#: Handlers are strongly encouraged to cache the new caret position,
	#: and handle the pending caret update at the end of every core cycle using L{post_coreCycle},
	#: unless they delegate caret change handling to a separate thread.
	#: Handlers are called with one argument.
	#: @param obj: The object in which the caret position changed.
	#: @type obj: L{NVDAObjects.NVDAObject}
	post_caretMove: Action = field(default_factory=Action, init=False)
	#: Notifies a vision enhancement provider when a virtual caret has moved.
	#: This allows a vision enhancement provider to take an action
	#: when the virtual caret moves in a browse mode document.
	#: For example, a magnifier can track the magnified area of the screen to the new virtual caret position.
	#: Handlers are strongly encouraged to cache the new virtual caret position,
	#: and handle the pending update at the end of every core cycle using L{post_coreCycle},
	#: unless they delegate virtual caret change handling to a separate thread.
	#: Handlers are called with one argument.
	#: @param obj: The cursor manager that changed it virtual caret position.
	#: @type obj: L{cursorManager.CursorManager}
	post_browseModeMove: Action = field(default_factory=Action, init=False)
	#: Notifies a vision enhancement provider when the position of the review cursor has changed.
	#: This allows a vision enhancement provider to take an action
	#: when the review position has changed.
	#: For example, a magnifier can track the magnified area of the screen to the new navigator object,
	#: or the exact location of the review cursor within the object.
	#: Handlers are strongly encouraged to cache the last context that triggered the change,
	#: and handle the pending review position change at the end of every core cycle using L{post_coreCycle},
	#: unless they delegate review position change handling to a separate thread.
	#: Handlers are called with one argument.
	#: @param context: The context that triggered the review position change.
	#: @type context: L{vision.constants.Context}
	post_reviewMove: Action = field(default_factory=Action, init=False)
	#: Notifies a vision enhancement provider when the mouse has moved.
	#: This allows a vision enhancement provider to take an action for mouse moves.
	#: For example, a magnifier can track the magnified area of the screen to the position of the mouse.
	#: Note that, by the nature of NVDA's mouse tracking implementation,
	#: This extension point is only called once per core cycle.
	#: Handlers are called with one argument.
	#: @param obj: The object that received focus.
	#: @type obj: L{NVDAObjects.NVDAObject}
	post_mouseMove: Action = field(default_factory=Action, init=False)
	#: Notifies a vision enhancement provider at the end of every core cycle.
	#: This allows a vision enhancement provider to rate limit certain actions.
	#: For example, many caret updates could take place during one core cycle.
	#: Especially if handling a caret update takes some time,
	#: handling only one of them is enough.
	#: Handlers are called without arguments.
	post_coreCycle: Action = field(default_factory=Action, init=False)
