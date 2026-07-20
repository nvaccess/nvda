# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Ryan McCleary
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Map MathCAT NavNode ids to source MathML rectangles."""

import xml.etree.ElementTree as ElementTree
from collections.abc import Generator
from typing import TYPE_CHECKING

import mathPres
from mathPres.mathMlNode import (
	MathMlNodeInfo,
	MathMlNodePath,
	SyntheticMathMlNodeId,
)
from logHandler import log

if TYPE_CHECKING:
	from locationHelper import RectLTRB
	from NVDAObjects import NVDAObject


MATHML_NAMESPACE = "http://www.w3.org/1998/Math/MathML"
NAV_NODE_ID_PREFIX = "nvda-math-node-"
_NAV_NODE_ID_ADDED_ATTR = "data-nvda-math-id-added"
_NAV_NODE_ORIGINAL_ID_ATTR = "data-nvda-math-original-id"
_MATHCAT_ID_ADDED_ATTR = "data-id-added"


def _stripMathMlNamespace(tag: str) -> str:
	return tag.rsplit("}", 1)[-1]


def _getSyntheticNodeId(nodePath: MathMlNodePath) -> str:
	if not nodePath:
		return f"{NAV_NODE_ID_PREFIX}root"
	return f"{NAV_NODE_ID_PREFIX}{'-'.join(str(index) for index in nodePath)}"


def _iterMathMlElements(
	element: ElementTree.Element,
	nodePath: MathMlNodePath,
) -> Generator[tuple[ElementTree.Element, MathMlNodePath], None, None]:
	stack = [(element, nodePath)]
	while stack:
		currentElement, currentNodePath = stack.pop()
		yield currentElement, currentNodePath
		mathElementChildren = tuple(child for child in currentElement if isinstance(child.tag, str))
		stack.extend(
			(child, currentNodePath + (index,))
			for index, child in reversed(tuple(enumerate(mathElementChildren)))
		)


def _addSyntheticIdsToMathMl(
	mathml: str,
) -> tuple[str, dict[SyntheticMathMlNodeId, MathMlNodeInfo]]:
	ElementTree.register_namespace("", MATHML_NAMESPACE)
	try:
		root = ElementTree.fromstring(mathPres.stripExtraneousXml(mathml))
	except ElementTree.ParseError:
		log.debugWarning("Math highlight could not parse MathML for synthetic node ids", exc_info=True)
		return mathml, {}
	if _stripMathMlNamespace(root.tag) != "math":
		log.debug("Math highlight did not add synthetic ids because MathML root is not <math>")
		return mathml, {}
	nodeInfoById: dict[SyntheticMathMlNodeId, MathMlNodeInfo] = {}
	for element, nodePath in _iterMathMlElements(root, ()):
		# MathCAT exposes the current NavNode by MathML id, so add stable ids to this copy only.
		nodeId = _getSyntheticNodeId(nodePath)
		if originalId := element.get("id"):
			element.set(_NAV_NODE_ORIGINAL_ID_ATTR, originalId)
		element.set("id", nodeId)
		element.set(_NAV_NODE_ID_ADDED_ATTR, "true")
		nodeInfoById[nodeId] = MathMlNodeInfo(
			path=nodePath,
			tag=_stripMathMlNamespace(element.tag),
		)
	return ElementTree.tostring(root, encoding="unicode"), nodeInfoById


def removeSyntheticIdsFromMathMl(mathml: str) -> str:
	try:
		root = ElementTree.fromstring(mathml)
	except ElementTree.ParseError:
		return mathml
	for element, _nodePath in _iterMathMlElements(root, ()):
		if element.get(_MATHCAT_ID_ADDED_ATTR) == "true":
			element.attrib.pop("id", None)
			element.attrib.pop(_MATHCAT_ID_ADDED_ATTR, None)
			continue
		if element.get(_NAV_NODE_ID_ADDED_ATTR) != "true":
			continue
		originalId = element.attrib.pop(_NAV_NODE_ORIGINAL_ID_ATTR, None)
		if originalId is not None:
			element.set("id", originalId)
		else:
			element.attrib.pop("id", None)
		element.attrib.pop(_NAV_NODE_ID_ADDED_ATTR, None)
	return ElementTree.tostring(root, encoding="unicode")


def prepareMathMlForNavigation(
	mathml: str,
	sourceObj: "NVDAObject | None",
) -> tuple[str, dict[SyntheticMathMlNodeId, "RectLTRB"]]:
	"""Add synthetic ids to MathML and map those ids to IA2 rectangles."""
	if not sourceObj:
		return mathml, {}
	# Avoid importing ia2Web at startup.
	from NVDAObjects.IAccessible.ia2Web import Math as Ia2WebMath

	if not isinstance(sourceObj, Ia2WebMath):
		return mathml, {}
	mathmlWithIds, mathMlNodeInfoById = _addSyntheticIdsToMathMl(mathml)
	if not mathMlNodeInfoById:
		return mathml, {}
	try:
		ia2NodeInfoByPath = sourceObj.getMathNodeInfoByPath()
	except Exception:
		log.debugWarning("Math highlight could not build IA2 rectangle map", exc_info=True)
		return mathml, {}
	nodeRectsById: dict[SyntheticMathMlNodeId, "RectLTRB"] = {}
	missingPathCount = 0
	tagMismatchCount = 0
	for nodeId, mathMlNodeInfo in mathMlNodeInfoById.items():
		try:
			ia2NodeInfo = ia2NodeInfoByPath[mathMlNodeInfo.path]
		except KeyError:
			missingPathCount += 1
			continue
		if ia2NodeInfo.tag != mathMlNodeInfo.tag:
			tagMismatchCount += 1
			continue
		nodeRectsById[nodeId] = ia2NodeInfo.rect
	log.debug(
		f"Math highlight added synthetic ids to {len(mathMlNodeInfoById)} MathML nodes; "
		f"mapped {len(nodeRectsById)} ids to IA2 rectangles; "
		f"missing IA2 paths: {missingPathCount}; tag mismatches: {tagMismatchCount}",
	)
	if not nodeRectsById:
		return mathml, {}
	return mathmlWithIds, nodeRectsById
