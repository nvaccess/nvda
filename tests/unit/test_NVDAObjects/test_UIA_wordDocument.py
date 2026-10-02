# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for NVDAObjects.UIA.wordDocument."""

import unittest
from unittest.mock import Mock, patch

import braille
import browseMode
import NVDAState
import textInfos
import UIAHandler
from NVDAObjects.UIA import UIA, wordDocument
from NVDAObjects.UIA.wordDocument import (
	CommentReplyUIATextInfoQuickNavItem,
	CommentUIATextInfoQuickNavItem,
	RevisionUIATextInfoQuickNavItem,
	_CommentInfo,
)
from speech.commands import EndUtteranceCommand
from textInfos.offsets import Offsets

from ..textProvider import BasicTextProvider

_RESOLVED_COMMENT_ID = 12345


def _patchResolvedCommentId(resolvedCommentId: int = _RESOLVED_COMMENT_ID):
	"""Patches the runtime ID of Word's resolved comment annotation type."""
	return patch.object(
		UIA,
		"_UIACustomAnnotationTypes",
		Mock(**{"microsoftWord_resolvedComment.id": resolvedCommentId}),
	)


_textProvider = BasicTextProvider(text="a" * 40)


def _makeRange(start: int, end: int) -> textInfos.TextInfo:
	"""Creates a text range between the given offsets."""
	return _textProvider.makeTextInfo(Offsets(start, end))


def _makeCachedElement(properties: dict[int, object], **attributes) -> Mock:
	"""Creates a UIA element mock returning the given values for cached properties, by property ID."""
	element = Mock(**attributes)
	element.GetCachedPropertyValue.side_effect = properties.__getitem__
	return element


def _commentProperties(commentInfo: "_CommentInfo") -> dict[int, object]:
	"""The cached properties of a comment thread element holding the given comment."""
	return {
		UIAHandler.UIA_FullDescriptionPropertyId: commentInfo.comment,
		UIAHandler.UIA_AnnotationAuthorPropertyId: commentInfo.author,
		UIAHandler.UIA_AnnotationDateTimePropertyId: commentInfo.date,
	}


def _makeElementArray(*elements: Mock) -> Mock:
	"""Creates a UIA element array mock holding the given elements."""
	return Mock(length=len(elements), getElement=lambda index: elements[index])


_ROOT = _CommentInfo("Please rephrase this sentence.", "Alice", "1 January 2026 at 10:00")
_REPLY = _CommentInfo("Done.", "Bob", "2 January 2026 at 11:00", isReply=True)
_THREAD_RUNTIME_ID = (42, 7, 4, 1)
_OTHER_THREAD_RUNTIME_ID = (42, 7, 4, 2)


class TestCommentInfoPresentation(unittest.TestCase):
	"""Tests for the presentation of comment information."""

	def test_comment(self):
		"""A comment is presented with its text, author and date."""
		self.assertEqual(
			"Comment: Please rephrase this sentence. by Alice on 1 January 2026 at 10:00",
			_ROOT.getPresentation(),
		)

	def test_commentWithoutDate(self):
		"""A comment without a date is presented with its text and author."""
		self.assertEqual(
			"Comment: Please rephrase this sentence. by Alice",
			_CommentInfo("Please rephrase this sentence.", "Alice").getPresentation(),
		)

	def test_resolvedComment(self):
		"""A resolved comment is presented as resolved."""
		self.assertEqual(
			"Resolved comment: Please rephrase this sentence. by Alice on 1 January 2026 at 10:00",
			_CommentInfo(
				"Please rephrase this sentence.",
				"Alice",
				"1 January 2026 at 10:00",
				resolved=True,
			).getPresentation(),
		)

	def test_reply(self):
		"""A reply is presented as a reply."""
		self.assertEqual(
			"Reply: Done. by Bob on 2 January 2026 at 11:00",
			_REPLY.getPresentation(),
		)


class TestResolvedComment(unittest.TestCase):
	"""Tests for the detection of resolved comments."""

	def test_resolvedIdInAnnotationTypes(self):
		"""A comment is resolved when its annotation types contain the resolved comment ID."""
		with _patchResolvedCommentId():
			self.assertTrue(
				wordDocument._isResolvedComment((UIAHandler.AnnotationType_Comment, _RESOLVED_COMMENT_ID)),
			)

	def test_resolvedIdNotInAnnotationTypes(self):
		"""A comment is not resolved when its annotation types lack the resolved comment ID."""
		with _patchResolvedCommentId():
			self.assertFalse(wordDocument._isResolvedComment((UIAHandler.AnnotationType_Comment,)))

	def test_unregisteredResolvedIdNeverMatches(self):
		"""An unregistered resolved comment ID of 0 never marks a comment as resolved."""
		with _patchResolvedCommentId(0):
			self.assertFalse(wordDocument._isResolvedComment((0,)))

	def test_singleAnnotationTypeAtPosition(self):
		"""A single annotation type at a position, rather than a tuple, is checked as well."""
		position = Mock()
		position._rangeObj.getAttributeValue.return_value = _RESOLVED_COMMENT_ID
		with _patchResolvedCommentId():
			self.assertTrue(wordDocument._isResolvedCommentAtPosition(position))
		position._rangeObj.getAttributeValue.assert_called_once_with(
			UIAHandler.UIA_AnnotationTypesAttributeId,
		)


class TestCommentThreadElement(unittest.TestCase):
	"""Tests for finding the comment thread element of a comment annotation element."""

	def _getThreadElement(
		self,
		parent: Mock | None,
		controlType: int = UIAHandler.UIA_TreeItemControlTypeId,
	) -> Mock:
		element = Mock(CachedControlType=controlType)
		handler = Mock()
		handler.baseTreeWalker.GetParentElementBuildCache.return_value = parent
		with patch.object(UIAHandler, "handler", handler):
			return wordDocument._getCommentThreadElement(element), element

	def test_replyResolvesToThread(self):
		"""A reply element resolves to its parent comment thread element."""
		parent = _makeCachedElement(
			{UIAHandler.UIA_IsAnnotationPatternAvailablePropertyId: True},
			CachedControlType=UIAHandler.UIA_TreeItemControlTypeId,
		)
		threadElement, _element = self._getThreadElement(parent)
		self.assertIs(parent, threadElement)

	def test_classicReplyResolvesToThread(self):
		"""A reply element of a classic comment resolves to its parent comment element."""
		parent = _makeCachedElement(
			{UIAHandler.UIA_IsAnnotationPatternAvailablePropertyId: True},
			CachedControlType=UIAHandler.UIA_GroupControlTypeId,
		)
		threadElement, _element = self._getThreadElement(parent, UIAHandler.UIA_GroupControlTypeId)
		self.assertIs(parent, threadElement)

	def test_threadResolvesToItself(self):
		"""A comment thread element resolves to itself."""
		parent = Mock(CachedControlType=UIAHandler.UIA_GroupControlTypeId)
		threadElement, element = self._getThreadElement(parent)
		self.assertIs(element, threadElement)

	def test_elementWithoutParentResolvesToItself(self):
		"""An element without a parent resolves to itself."""
		threadElement, element = self._getThreadElement(None)
		self.assertIs(element, threadElement)


class TestCommentThreadInfo(unittest.TestCase):
	"""Tests for fetching a comment thread with its replies."""

	def _getThreadInfo(self, replyElements: Mock | None) -> _CommentInfo:
		cachedThread = _makeCachedElement(_commentProperties(_ROOT))
		cachedThread.getCachedChildren.return_value = replyElements
		cachedThread.getRuntimeId.return_value = _THREAD_RUNTIME_ID
		threadElement = Mock()
		threadElement.buildUpdatedCache.return_value = cachedThread
		with patch.object(UIAHandler, "handler", Mock()):
			return wordDocument._getCommentThreadInfo(threadElement, resolved=True)

	def test_threadWithReply(self):
		"""The root comment of a thread holds its replies and the runtime ID of the thread element."""
		threadInfo = self._getThreadInfo(_makeElementArray(_makeCachedElement(_commentProperties(_REPLY))))
		self.assertEqual(
			_CommentInfo(
				_ROOT.comment,
				_ROOT.author,
				_ROOT.date,
				resolved=True,
				replies=(_REPLY,),
				threadRuntimeId=_THREAD_RUNTIME_ID,
			),
			threadInfo,
		)

	def test_threadWithoutReplies(self):
		"""The root comment of a thread without replies holds no replies."""
		threadInfo = self._getThreadInfo(None)
		self.assertEqual(
			_CommentInfo(
				_ROOT.comment,
				_ROOT.author,
				_ROOT.date,
				resolved=True,
				threadRuntimeId=_THREAD_RUNTIME_ID,
			),
			threadInfo,
		)

	def test_classicCommentTextFromEditField(self):
		"""The text of a classic comment comes from the edit field in its element."""
		cachedThread = _makeCachedElement(
			{**_commentProperties(_ROOT), UIAHandler.UIA_FullDescriptionPropertyId: ""},
		)
		cachedThread.getCachedChildren.return_value = None
		editElement = Mock()
		textPattern = editElement.GetCachedPattern.return_value.QueryInterface.return_value
		textPattern.DocumentRange.GetText.return_value = f"{_ROOT.comment}\r"
		cachedThread.FindFirstBuildCache.return_value = editElement
		cachedThread.getRuntimeId.return_value = _THREAD_RUNTIME_ID
		threadElement = Mock()
		threadElement.buildUpdatedCache.return_value = cachedThread
		with patch.object(UIAHandler, "handler", Mock()):
			threadInfo = wordDocument._getCommentThreadInfo(threadElement, resolved=False)
		self.assertEqual(
			_CommentInfo(_ROOT.comment, _ROOT.author, _ROOT.date, threadRuntimeId=_THREAD_RUNTIME_ID),
			threadInfo,
		)


class TestCommentInfoFromPosition(unittest.TestCase):
	"""Tests for fetching comment information at a position in a document."""

	def _makePosition(self, element: Mock | None, annotationTypes: tuple[int, ...] = ()) -> Mock:
		annotationObjects = Mock()
		annotationObjects.QueryInterface.return_value = (
			_makeElementArray(element) if element else _makeElementArray()
		)
		values = {
			UIAHandler.UIA_AnnotationObjectsAttributeId: annotationObjects,
			UIAHandler.UIA_AnnotationTypesAttributeId: annotationTypes,
		}
		position = Mock()
		position._rangeObj.getAttributeValue.side_effect = values.__getitem__
		return position

	def _makeAnnotationElement(self, controlType: int) -> tuple[Mock, Mock]:
		cachedElement = _makeCachedElement(
			{
				UIAHandler.UIA_AnnotationAnnotationTypeIdPropertyId: UIAHandler.AnnotationType_Comment,
				UIAHandler.UIA_AnnotationAuthorPropertyId: "Alice",
				UIAHandler.UIA_AnnotationDateTimePropertyId: "Thursday",
			},
			CachedControlType=controlType,
			CachedName="Comment Hint Button",
		)
		element = Mock()
		element.buildUpdatedCache.return_value = cachedElement
		return element, cachedElement

	def test_noAnnotationObjects(self):
		"""There is no comment information without annotation objects at the position."""
		position = Mock()
		position._rangeObj.getAttributeValue.return_value = None
		self.assertIsNone(wordDocument._getCommentInfoFromPosition(position))

	def test_hintButton(self):
		"""A comment hint button provides its name, author and date."""
		element, _cachedElement = self._makeAnnotationElement(UIAHandler.UIA_ListItemControlTypeId)
		with patch.object(UIAHandler, "handler", Mock()):
			commentInfo = wordDocument._getCommentInfoFromPosition(self._makePosition(element))
		self.assertEqual(_CommentInfo("Comment Hint Button", "Alice", "Thursday"), commentInfo)

	def test_threadChecksResolvedAtPosition(self):
		"""A comment thread is checked for being resolved at the position when no resolved state is given."""
		element, cachedElement = self._makeAnnotationElement(UIAHandler.UIA_TreeItemControlTypeId)
		position = self._makePosition(element, (_RESOLVED_COMMENT_ID,))
		with (
			patch.object(UIAHandler, "handler", Mock()),
			_patchResolvedCommentId(),
			patch.object(wordDocument, "_getCommentThreadElement") as getThreadElement,
			patch.object(wordDocument, "_getCommentThreadInfo") as getThreadInfo,
		):
			commentInfo = wordDocument._getCommentInfoFromPosition(position)
		getThreadElement.assert_called_once_with(cachedElement)
		getThreadInfo.assert_called_once_with(getThreadElement.return_value, resolved=True)
		self.assertIs(getThreadInfo.return_value, commentInfo)

	def test_threadUsesGivenResolvedState(self):
		"""A comment thread uses the given resolved state without checking the position."""
		element, _cachedElement = self._makeAnnotationElement(UIAHandler.UIA_TreeItemControlTypeId)
		position = self._makePosition(element, (_RESOLVED_COMMENT_ID,))
		with (
			patch.object(UIAHandler, "handler", Mock()),
			_patchResolvedCommentId(),
			patch.object(wordDocument, "_getCommentThreadElement"),
			patch.object(wordDocument, "_getCommentThreadInfo") as getThreadInfo,
		):
			wordDocument._getCommentInfoFromPosition(position, resolved=False)
		self.assertFalse(getThreadInfo.call_args.kwargs["resolved"])
		self.assertNotIn(
			((UIAHandler.UIA_AnnotationTypesAttributeId,),),
			position._rangeObj.getAttributeValue.call_args_list,
		)

	def _makeEditElement(self, parent: Mock | None) -> tuple[Mock, Mock]:
		cachedEdit = _makeCachedElement({UIAHandler.UIA_AnnotationAnnotationTypeIdPropertyId: object()})
		edit = Mock()
		edit.buildUpdatedCache.return_value = cachedEdit
		handler = Mock()
		handler.baseTreeWalker.GetParentElementBuildCache.return_value = parent
		return edit, handler

	def test_classicCommentUsesCommentElement(self):
		"""The edit field of a classic comment resolves to the element of the comment."""
		_element, cachedGroup = self._makeAnnotationElement(UIAHandler.UIA_GroupControlTypeId)
		edit, handler = self._makeEditElement(cachedGroup)
		with (
			patch.object(UIAHandler, "handler", handler),
			_patchResolvedCommentId(),
			patch.object(wordDocument, "_getCommentThreadElement") as getThreadElement,
			patch.object(wordDocument, "_getCommentThreadInfo") as getThreadInfo,
		):
			commentInfo = wordDocument._getCommentInfoFromPosition(self._makePosition(edit))
		getThreadElement.assert_called_once_with(cachedGroup)
		getThreadInfo.assert_called_once_with(getThreadElement.return_value, resolved=False)
		self.assertIs(getThreadInfo.return_value, commentInfo)

	def test_otherAnnotationObject(self):
		"""There is no comment information for an annotation object that is not part of a comment."""
		edit, handler = self._makeEditElement(
			_makeCachedElement({UIAHandler.UIA_AnnotationAnnotationTypeIdPropertyId: object()}),
		)
		with patch.object(UIAHandler, "handler", handler):
			self.assertIsNone(wordDocument._getCommentInfoFromPosition(self._makePosition(edit)))


class TestCommentQuickNavItems(unittest.TestCase):
	"""Tests for the comment and reply items of quick navigation and the Elements List."""

	def setUp(self):
		self.document = Mock()
		self.comment = CommentUIATextInfoQuickNavItem(
			(UIAHandler.AnnotationType_Comment,),
			"annotation",
			self.document,
			_makeRange(10, 20),
		)
		self.comment.__dict__["commentInfo"] = _CommentInfo(
			_ROOT.comment,
			_ROOT.author,
			_ROOT.date,
			replies=(
				_REPLY,
				_CommentInfo("Thanks.", "Alice", "3 January 2026 at 12:00", isReply=True),
			),
		)

	def test_wantedAttribValuesIncludeResolvedComments(self):
		"""Comment items match resolved comments when the resolved comment ID is registered."""
		with _patchResolvedCommentId():
			self.assertEqual(
				{UIAHandler.AnnotationType_Comment, _RESOLVED_COMMENT_ID},
				CommentUIATextInfoQuickNavItem.wantedAttribValues,
			)

	def test_wantedAttribValuesWithoutResolvedCommentId(self):
		"""Comment items only match comments when the resolved comment ID isn't registered."""
		with _patchResolvedCommentId(0):
			self.assertEqual(
				{UIAHandler.AnnotationType_Comment},
				CommentUIATextInfoQuickNavItem.wantedAttribValues,
			)

	def test_labels(self):
		"""Comment and reply items are labelled with the presentation of their comment."""
		reply = CommentReplyUIATextInfoQuickNavItem(self.comment, _REPLY)
		self.assertEqual(_ROOT.getPresentation(), self.comment.label)
		self.assertEqual(_REPLY.getPresentation(), reply.label)

	def test_elementsListNesting(self):
		"""Replies nest under their comment, and so do other annotations within the comment."""
		items = list(
			wordDocument._iterWithCommentReplies(
				browseMode.mergeQuickNavItemIterators(
					[
						iter([self.comment]),
						iter(
							[
								RevisionUIATextInfoQuickNavItem(
									(UIAHandler.AnnotationType_InsertionChange,),
									"annotation",
									self.document,
									_makeRange(10, 12),
								),
							],
						),
					],
				),
			),
		)
		# Same parent lookup as browseMode.ElementsListDialog.initElementType.
		parentElements = []
		parents = []
		for item in items:
			for parent in reversed(parentElements):
				if item.isChild(parent):
					break
				else:
					parentElements.pop()
			else:
				parent = None
			parents.append(parent)
			parentElements.append(item)
		self.assertEqual(
			[
				CommentUIATextInfoQuickNavItem,
				CommentReplyUIATextInfoQuickNavItem,
				CommentReplyUIATextInfoQuickNavItem,
				RevisionUIATextInfoQuickNavItem,
			],
			[type(item) for item in items],
		)
		self.assertEqual([None, self.comment, self.comment, self.comment], parents)

	def test_repliesAreOnlyFetchedWhenIterated(self):
		"""The comment information of an item is only fetched when iterating past the item."""
		comment = CommentUIATextInfoQuickNavItem(
			(UIAHandler.AnnotationType_Comment,),
			"annotation",
			self.document,
			_makeRange(10, 20),
		)
		with patch.object(wordDocument, "_getCommentInfoFromPosition") as getCommentInfo:
			items = wordDocument._iterWithCommentReplies(iter([comment]))
			self.assertIs(comment, next(items))
			getCommentInfo.assert_not_called()

	def test_commentWithoutInfoHasNoReplies(self):
		"""A comment item without comment information yields no reply items."""
		self.comment.__dict__["commentInfo"] = None
		self.assertEqual([self.comment], list(wordDocument._iterWithCommentReplies(iter([self.comment]))))

	def _makeComment(
		self,
		start: int,
		end: int,
		threadRuntimeId: tuple[int, ...] | None,
	) -> CommentUIATextInfoQuickNavItem:
		comment = CommentUIATextInfoQuickNavItem(
			(UIAHandler.AnnotationType_Comment,),
			"annotation",
			self.document,
			_makeRange(start, end),
		)
		comment.__dict__["commentInfo"] = _CommentInfo(
			_ROOT.comment,
			_ROOT.author,
			_ROOT.date,
			replies=(_REPLY,),
			threadRuntimeId=threadRuntimeId,
		)
		return comment

	def test_threadRuntimeId(self):
		"""A comment item has the thread runtime ID of its comment information, if any."""
		self.assertEqual(_THREAD_RUNTIME_ID, self._makeComment(10, 20, _THREAD_RUNTIME_ID).threadRuntimeId)
		self.comment.__dict__["commentInfo"] = None
		self.assertIsNone(self.comment.threadRuntimeId)

	def test_commentOfSameThreadIsListedOnce(self):
		"""A comment item of the same thread as the previous comment item is skipped with its replies."""
		firstRun = self._makeComment(10, 15, _THREAD_RUNTIME_ID)
		secondRun = self._makeComment(15, 20, _THREAD_RUNTIME_ID)
		revision = RevisionUIATextInfoQuickNavItem(
			(UIAHandler.AnnotationType_InsertionChange,),
			"annotation",
			self.document,
			_makeRange(16, 18),
		)
		otherComment = self._makeComment(30, 35, _OTHER_THREAD_RUNTIME_ID)
		items = list(
			wordDocument._iterWithCommentReplies(
				browseMode.mergeQuickNavItemIterators(
					[iter([firstRun, secondRun, otherComment]), iter([revision])],
				),
			),
		)
		self.assertEqual(
			[
				CommentUIATextInfoQuickNavItem,
				CommentReplyUIATextInfoQuickNavItem,
				RevisionUIATextInfoQuickNavItem,
				CommentUIATextInfoQuickNavItem,
				CommentReplyUIATextInfoQuickNavItem,
			],
			[type(item) for item in items],
		)
		self.assertIs(firstRun, items[0])
		self.assertIs(revision, items[2])
		self.assertIs(otherComment, items[3])

	def test_commentsWithoutThreadAreNotSkipped(self):
		"""Comment items without a thread runtime ID are never skipped."""
		firstRun = self._makeComment(10, 15, None)
		secondRun = self._makeComment(15, 20, None)
		items = list(wordDocument._iterWithCommentReplies(iter([firstRun, secondRun])))
		self.assertEqual(
			[
				CommentUIATextInfoQuickNavItem,
				CommentReplyUIATextInfoQuickNavItem,
				CommentUIATextInfoQuickNavItem,
				CommentReplyUIATextInfoQuickNavItem,
			],
			[type(item) for item in items],
		)
		self.assertIs(firstRun, items[0])
		self.assertIs(secondRun, items[2])


class TestReportCurrentComment(unittest.TestCase):
	"""Tests for the script that reports the comment at the caret."""

	def _reportComment(self, repeatCount: int) -> dict[str, Mock]:
		document = object.__new__(wordDocument.WordDocument)
		document.makeTextInfo = Mock()
		mocks = {}
		with (
			patch.object(
				wordDocument,
				"_getCommentInfoFromPosition",
				return_value=_CommentInfo(_ROOT.comment, _ROOT.author, _ROOT.date, replies=(_REPLY,)),
			),
			patch.object(wordDocument.scriptHandler, "getLastScriptRepeatCount", return_value=repeatCount),
			patch.object(wordDocument.speech, "speak") as mocks["speak"],
			patch.object(braille, "handler") as mocks["braille"],
			patch.object(wordDocument.ui, "browseableMessage") as mocks["browseableMessage"],
		):
			wordDocument.WordDocument.script_reportCurrentComment(document, None)
		return mocks

	def test_speaksEachPostAsUtterance(self):
		"""The comment and each reply are spoken as separate utterances, and brailled as one message."""
		mocks = self._reportComment(0)
		(speechSequence,), _kwargs = mocks["speak"].call_args
		self.assertEqual(
			[_ROOT.getPresentation(), EndUtteranceCommand, _REPLY.getPresentation()],
			[item if isinstance(item, str) else type(item) for item in speechSequence],
		)
		mocks["braille"].message.assert_called_once_with(
			f"{_ROOT.getPresentation()}\n{_REPLY.getPresentation()}",
		)

	def test_browseableMessageOnSecondPress(self):
		"""Pressing the script twice shows the comment and its replies in a browseable message."""
		mocks = self._reportComment(1)
		mocks["speak"].assert_not_called()
		(text, _title), _kwargs = mocks["browseableMessage"].call_args
		self.assertEqual(f"{_ROOT.getPresentation()}\n{_REPLY.getPresentation()}", text)


class TestDeprecatedCommentInfo(unittest.TestCase):
	"""Tests for the deprecated comment information functions."""

	def setUp(self):
		allowDeprecatedAPI = patch.object(NVDAState, "_allowDeprecatedAPI", return_value=True)
		allowDeprecatedAPI.start()
		self.addCleanup(allowDeprecatedAPI.stop)

	def _getCommentInfo(self, commentInfo: _CommentInfo | None) -> dict[str, str] | None:
		with patch.object(wordDocument, "_getCommentInfoFromPosition", return_value=commentInfo):
			return wordDocument.getCommentInfoFromPosition(Mock())

	def test_getCommentInfoFromPosition(self):
		"""The deprecated function returns the comment, author and date as a dictionary."""
		self.assertEqual(
			{"comment": _ROOT.comment, "author": _ROOT.author, "date": _ROOT.date},
			self._getCommentInfo(_CommentInfo(_ROOT.comment, _ROOT.author, _ROOT.date, replies=(_REPLY,))),
		)

	def test_getCommentInfoFromPositionWithoutDate(self):
		"""The deprecated function omits the date when it isn't known."""
		self.assertEqual(
			{"comment": _ROOT.comment, "author": _ROOT.author},
			self._getCommentInfo(_CommentInfo(_ROOT.comment, _ROOT.author)),
		)

	def test_getCommentInfoFromPositionWithoutComment(self):
		"""The deprecated function returns ``None`` when there is no comment."""
		self.assertIsNone(self._getCommentInfo(None))

	def test_getPresentableCommentInfoFromPosition(self):
		"""The deprecated function presents a comment from its dictionary."""
		self.assertEqual(
			_ROOT.getPresentation(),
			wordDocument.getPresentableCommentInfoFromPosition(
				{"comment": _ROOT.comment, "author": _ROOT.author, "date": _ROOT.date},
			),
		)
		self.assertEqual(
			"Comment: Please rephrase this sentence. by Alice",
			wordDocument.getPresentableCommentInfoFromPosition(
				{"comment": _ROOT.comment, "author": _ROOT.author},
			),
		)
