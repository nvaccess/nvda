/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2010 NVDA contributers.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <list>
#include <set>
#include <sstream>
#include <regex>
#include <vector>
#include <sstream>
#include <algorithm>
#include <common/xml.h>
#include <common/log.h>
#include "utils.h"
#include "storage.h"

using namespace std;

//controlFieldNodeIdentifier implementation

VBufStorage_controlFieldNodeIdentifier_t::VBufStorage_controlFieldNodeIdentifier_t(int docHandleArg, int IDArg) : docHandle(docHandleArg), ID(IDArg) {
}

bool VBufStorage_controlFieldNodeIdentifier_t::operator<(const VBufStorage_controlFieldNodeIdentifier_t &other) const {
	int docHandleCmp=this->docHandle-other.docHandle;
	if(docHandleCmp==0) {
		return (this->ID-other.ID)<0;
	}
	return docHandleCmp<0;
}

bool VBufStorage_controlFieldNodeIdentifier_t::operator!=(const VBufStorage_controlFieldNodeIdentifier_t &other) const {
	return (this->docHandle!=other.docHandle)||(this->ID!=other.ID);
}

bool VBufStorage_controlFieldNodeIdentifier_t::operator==(const VBufStorage_controlFieldNodeIdentifier_t &other) const {
	return (this->docHandle==other.docHandle)&&(this->ID==other.ID);
}

//field  node implementation

VBufStorage_fieldNode_t* VBufStorage_fieldNode_t::nextNodeInTree(int direction, VBufStorage_fieldNode_t* limitNode, int *relativeStartOffset) {
	int relativeOffset=0;
	VBufStorage_fieldNode_t* tempNode=this;
	if(direction==TREEDIRECTION_FORWARD) {
		LOG_DEBUG(L"moving forward");
		if(tempNode->firstChild!=NULL) {
			LOG_DEBUG(L"Moving to first child");
			tempNode=tempNode->firstChild;
		} else {
			while(tempNode!=NULL&&tempNode->next==NULL) {
				LOG_DEBUG(L"moving past parent");
				tempNode=tempNode->parent;
				if(tempNode==limitNode) tempNode=NULL;
			}
			if(tempNode==NULL||tempNode->next==NULL) {
				LOG_DEBUG(L"cannot move any further, returning NULL");
				return NULL;
			}
			LOG_DEBUG(L"Moving to next");
			relativeOffset=this->length;
			tempNode=tempNode->next;
		}
	} else if(direction==TREEDIRECTION_BACK) {
		LOG_DEBUG(L"Moving backwards");
		if(tempNode->previous!=NULL) {
			if(tempNode->previous==limitNode) return NULL;
			LOG_DEBUG(L"Using previous node");
			tempNode=tempNode->previous;
			while(tempNode->lastChild!=NULL&&tempNode->lastChild!=limitNode) {
				LOG_DEBUG(L"Using lastChild");
				tempNode=tempNode->lastChild;
			}
			relativeOffset-=tempNode->length;
		} else if(tempNode->parent!=NULL) {
			LOG_DEBUG(L"Using parent");
			tempNode=tempNode->parent;
		} else {
			LOG_DEBUG(L"No parent or previous, returning NULL");
			return NULL;
		}
	} else if(direction==TREEDIRECTION_SYMMETRICAL_BACK) {
		LOG_DEBUG(L"Moving symmetrical backwards");
		if(tempNode->lastChild!=NULL) {
			LOG_DEBUG(L"Moving to last child");
			tempNode=tempNode->lastChild;
			relativeOffset=this->length-tempNode->length;
		} else {
			while(tempNode!=NULL&&tempNode->previous==NULL) {
				LOG_DEBUG(L"moving past parent");
				tempNode=tempNode->parent;
				if(tempNode==limitNode) tempNode=NULL;
			}
			if(tempNode==NULL||tempNode->previous==NULL) {
				LOG_DEBUG(L"cannot move any further, returning NULL");
				return NULL;
			}
			tempNode=tempNode->previous;
			relativeOffset-=tempNode->length;
		}
	}
	if(tempNode==limitNode) {
		LOG_DEBUG(L"passed limit node at "<<limitNode<<L", returning NULL");
		return NULL;
	}
	*relativeStartOffset=relativeOffset;
	LOG_DEBUG(L"reached node at "<<tempNode<<L", with a relative start offset of "<<relativeOffset);
	return tempNode;
}

// @param out the stream to which the escaped attribute string should be written
// @param text The attribute string to be escaped
// @param maxLength the maximum length of the attribute string that should be copied. If maxLength is 0 or not specified, the entire string is copied.
// @return the number of characters written to the output stream (before expansion / filtering). This number can be used to see if the string was truncated at all.
inline size_t outputEscapedAttribute(wostringstream& out, const wstring& text, size_t maxLength=0) {
	size_t count=0;
	for (wstring::const_iterator it = text.begin(); it != text.end(); ++it) {
		switch (*it) {
			case L':':
			case L';':
			case L'\\':
			out << L"\\";
			default:
			out << *it;
		}
		count++;
		if(maxLength>0) {
			if(count==maxLength) {
				break;
			}
		}
	}
	return count;
}

bool VBufStorage_fieldNode_t::matchAttributes(const std::vector<std::wstring>& attribs, const std::wregex& regexp) {
	// The max length for a node attribute value when used in a regular expression for matching.
	// regex_match throws regex_error (error_stack) In Firefox when a value is very large.
	// Most values will be way under this limit, but for large ones such as name for example, as we only are checking whether it is not empty, then truncating is fine.
	const size_t regexAttribValueLimit=100;
	wostringstream regexpInput;
	wstring parentPrefix=L"parent::";
	for (vector<wstring>::const_iterator attribName = attribs.begin(); attribName != attribs.end(); ++attribName) {
		outputEscapedAttribute(regexpInput, *attribName);
		regexpInput << L":";
		// A given attribute can start with a parent prefix, which means the parent node will be checked for that attribute instead of this one. 
		// E.g. "parent::IAccessible2::role".
		// Although we will only redirect  the attribute to the parent if the parent prefix is found at the very beginning of the string (I.e. index 0),
		// an attribute like "blah_grandparent::color" is not an error and will be processed literally like any other attribute.
		if(this->parent&&attribName->find(parentPrefix)==0) {
			VBufStorage_attributeMap_t::const_iterator foundAttrib = this->parent->attributes.find(attribName->substr(parentPrefix.length()));
			if (foundAttrib != this->parent->attributes.end()) {
				auto outLen=outputEscapedAttribute(regexpInput, foundAttrib->second,regexAttribValueLimit);
				if(outLen<foundAttrib->second.length()) {
					LOG_DEBUGWARNING(L"Truncated attribute "<<(*attribName));
				}
			}
			regexpInput << L";";
		} else { // not a parent attribute
			VBufStorage_attributeMap_t::const_iterator foundAttrib = attributes.find(*attribName);
			if (foundAttrib != attributes.end()) {
				auto outLen=outputEscapedAttribute(regexpInput, foundAttrib->second,regexAttribValueLimit);
				if(outLen<foundAttrib->second.length()) {
					LOG_DEBUGWARNING(L"Truncated attribute "<<(*attribName));
				}
			}
			regexpInput << L";";
		}
	}
	try {
		return regex_match(regexpInput.str(), regexp);
	} catch(const std::regex_error& e) {
		LOG_DEBUGWARNING(L"regex_match threw "<<(e.what()));
	}
	return false;
}

int VBufStorage_fieldNode_t::calculateOffsetInTree() const {
	int startOffset=0;
	for(VBufStorage_fieldNode_t* previous=this->previous;previous!=NULL;previous=previous->previous) {
		startOffset+=previous->length;
	}
	LOG_DEBUG(L"node has local offset of "<<startOffset);
	if(this->parent) {
		startOffset+=this->parent->calculateOffsetInTree();
	LOG_DEBUG(L"With parents offset is now "<<startOffset);
	}
	LOG_DEBUG(L"Returning node start offset of "<<startOffset);
	return startOffset;
}

VBufStorage_textFieldNode_t* VBufStorage_fieldNode_t::locateTextFieldNodeAtOffset(int offset, int *relativeOffset) {
	LOG_DEBUG(L"Searching through children to reach offset "<<offset);
	int tempOffset=0;
	nhAssert(this->firstChild!=NULL||this->length==0); //Length of a node with out children can not be greater than 0
	for(VBufStorage_fieldNode_t* child=this->firstChild;child!=NULL;child=child->next) {
		if(offset<tempOffset+child->length) {
			LOG_DEBUG(L"found child at offset "<<tempOffset);
			VBufStorage_textFieldNode_t* textFieldNode=child->locateTextFieldNodeAtOffset(offset-tempOffset, relativeOffset);
			nhAssert(textFieldNode); //textFieldNode can't be NULL
			return textFieldNode;
		} else {
			tempOffset+=child->length;
		}
	}
	LOG_DEBUG(L"No textFieldNode found, returning NULL");
	return NULL;
}

void VBufStorage_fieldNode_t::generateAttributesForMarkupOpeningTag(std::wstring& text, int startOffset, int endOffset) {
	wostringstream s;
	s<<L"_startOfNode=\""<<(startOffset==0?1:0)<<L"\" ";
	s<<L"_endOfNode=\""<<(endOffset>=this->length?1:0)<<L"\" ";
	s<<L"isBlock=\""<<this->isBlock<<L"\" ";
	s<<L"isHidden=\""<<this->isHidden<<L"\" ";
	int childCount=0;
	int childControlCount=0;
	for(VBufStorage_fieldNode_t* child=this->firstChild;child!=NULL;child=child->next) {
		++childCount;
		if((child->length)>0&&child->firstChild) ++childControlCount;
	}
	int parentChildCount=1;
	int indexInParent=0;
	for(VBufStorage_fieldNode_t* prev=this->previous;prev!=NULL;prev=prev->previous) {
		++indexInParent;
		++parentChildCount;
	}
	for(VBufStorage_fieldNode_t* next=this->next;next!=NULL;next=next->next) {
		++parentChildCount;
	}
	s<<L"_childcount=\""<<childCount<<L"\" _childcontrolcount=\""<<childControlCount<<L"\" _indexInParent=\""<<indexInParent<<L"\" _parentChildCount=\""<<parentChildCount<<L"\" ";
	text+=s.str();
	for(VBufStorage_attributeMap_t::iterator i=this->attributes.begin();i!=this->attributes.end();++i) {
		text+=sanitizeXMLAttribName(i->first);
		text+=L"=\"";
		for(std::wstring::iterator j=i->second.begin();j!=i->second.end();++j) {
			appendCharToXML(*j,text,true);
		}
		text+=L"\" ";
	}
}

void VBufStorage_fieldNode_t::generateMarkupOpeningTag(std::wstring& text, int startOffset, int endOffset) {
	text+=L"<";
	this->generateMarkupTagName(text);
	text+=L" ";
	this->generateAttributesForMarkupOpeningTag(text,startOffset,endOffset);
	text+=L">";
}

void VBufStorage_fieldNode_t::generateMarkupClosingTag(std::wstring& text) {
	text+=L"</";
	this->generateMarkupTagName(text);
	text+=L">";
}

void VBufStorage_fieldNode_t::getTextInRange(int startOffset, int endOffset, std::wstring& text, bool useMarkup, bool(*filter)(VBufStorage_fieldNode_t*)) {
	if(this->length==0) {
		LOG_DEBUG(L"node has 0 length, not collecting text");
		return;
	}
	LOG_DEBUG(L"getting text between offsets "<<startOffset<<L" and "<<endOffset);
	nhAssert(startOffset>=0); //startOffset can't be negative
	nhAssert(startOffset<endOffset); //startOffset must be before endOffset
	nhAssert(endOffset<=this->length); //endOffset can't be bigger than node length
	if(useMarkup) {
		this->generateMarkupOpeningTag(text,startOffset,endOffset);
	}
	nhAssert(this->firstChild!=NULL||this->length==0); //Length of a node with out children can not be greater than 0
	int childStart=0;
	int childEnd=0;
	int childLength=0;
	for(VBufStorage_fieldNode_t* child=this->firstChild;child!=NULL;child=child->next) {
		childLength=child->length;
		nhAssert(childLength>=0); //length can't be negative
		childEnd+=childLength;
		LOG_DEBUG(L"child with offsets of "<<childStart<<L" and "<<childEnd); 
		if(childEnd>startOffset&&endOffset>childStart&&(!filter||filter(child))) {
			LOG_DEBUG(L"child offsets overlap requested offsets");
			child->getTextInRange(max(startOffset,childStart)-childStart,min(endOffset-childStart,childLength),text,useMarkup,filter);
		}
		childStart+=childLength;
		LOG_DEBUG(L"childStart is now "<<childStart);
	}
	if(useMarkup) {
		this->generateMarkupClosingTag(text);
	}
	LOG_DEBUG(L"Generated, text string is now "<<text.length());
}

void VBufStorage_fieldNode_t::disassociateFromBuffer(VBufStorage_buffer_t* buffer) {
	nhAssert(buffer); //Buffer can't be NULL
	LOG_DEBUG(L"Disassociating fieldNode from buffer");
}

VBufStorage_fieldNode_t::VBufStorage_fieldNode_t(int lengthArg, bool isBlockArg): parent(NULL), previous(NULL), next(NULL), firstChild(NULL), lastChild(NULL), length(lengthArg), isBlock(isBlockArg), isHidden(false), attributes() {
	LOG_DEBUG(L"field node initialization at "<<this<<L"length is "<<length);
}

VBufStorage_fieldNode_t::~VBufStorage_fieldNode_t() {
	LOG_DEBUG(L"fieldNode being destroied");
}

bool VBufStorage_fieldNode_t::addAttribute(const std::wstring& name, const std::wstring& value) {
	LOG_DEBUG(L"Adding attribute "<<name<<L" with value "<<value);
	this->attributes[name]=value;
	return true;
}

std::wstring VBufStorage_fieldNode_t::getAttributesString() const {
	std::wstring attributesString;
	for(std::map<std::wstring,std::wstring>::const_iterator i=attributes.begin();i!=attributes.end();++i) {
		attributesString+=i->first;
		attributesString+=L':';
		attributesString+=i->second;
		attributesString+=L';';
	}
	return attributesString;
}

std::wstring VBufStorage_fieldNode_t::getDebugInfo() const {
	std::wostringstream s;
	s<<L"field node at "<<this<<L", parent at "<<parent<<L", previous at "<<previous<<L", next at "<<next<<L", firstChild at "<<firstChild<<L", lastChild at "<<lastChild<<L", length is "<<length<<L", attributes are "<<getAttributesString();
	return s.str();
}

//controlFieldNode implementation

void VBufStorage_controlFieldNode_t::generateMarkupTagName(std::wstring& text) {
	text+=L"control";
}

void VBufStorage_controlFieldNode_t::generateAttributesForMarkupOpeningTag(std::wstring& text, int startOffset, int endOffset) {
	std::wostringstream s;
	s<<L"controlIdentifier_docHandle=\""<<identifier.docHandle<<L"\" controlIdentifier_ID=\""<<identifier.ID<<L"\" ";
	text+=s.str();
	this->VBufStorage_fieldNode_t::generateAttributesForMarkupOpeningTag(text,startOffset,endOffset);
}

void VBufStorage_controlFieldNode_t::disassociateFromBuffer(VBufStorage_buffer_t* buffer) {
	nhAssert(buffer); //Must be associated with a buffer
	LOG_DEBUG(L"Disassociating controlFieldNode from buffer");
	buffer->forgetControlFieldNode(this);
	this->VBufStorage_fieldNode_t::disassociateFromBuffer(buffer);
}

VBufStorage_controlFieldNode_t::VBufStorage_controlFieldNode_t(int docHandle, int ID, bool isBlockArg): VBufStorage_fieldNode_t(0,isBlockArg), identifier(docHandle,ID) {  
	LOG_DEBUG(L"controlFieldNode initialization at "<<this<<L", with docHandle of "<<identifier.docHandle<<L" and ID of "<<identifier.ID); 
}

bool VBufStorage_controlFieldNode_t::getIdentifier(int* docHandle, int* ID) {
	*docHandle=this->identifier.docHandle;
	*ID=this->identifier.ID;
	return true;
}

std::wstring VBufStorage_controlFieldNode_t::getDebugInfo() const {
	std::wostringstream s;
	s<<L"control "<<this->VBufStorage_fieldNode_t::getDebugInfo()<<L", docHandle "<<identifier.docHandle<<L", ID is "<<identifier.ID<<L", requiresParentUpdate "<<requiresParentUpdate<<L", allowReuseInAncestorUpdate "<<allowReuseInAncestorUpdate<<L", denyReuseIfPreviousSiblingsChanged "<<denyReuseIfPreviousSiblingsChanged<<L", alwaysRerenderChildren "<<alwaysRerenderChildren;  
	return s.str();
}

//textFieldNode implementation

VBufStorage_textFieldNode_t* VBufStorage_textFieldNode_t::locateTextFieldNodeAtOffset(int offset, int *relativeOffset) {
	nhAssert(offset<length); //Offset must be in this node
	LOG_DEBUG(L"Node is a textField");
	*relativeOffset=offset;
	return this;
}

void VBufStorage_textFieldNode_t::generateMarkupTagName(std::wstring& text) {
	text+=L"text";
}

void VBufStorage_textFieldNode_t::getTextInRange(int startOffset, int endOffset, std::wstring& text, bool useMarkup, bool(*filter)(VBufStorage_fieldNode_t*)) {
	LOG_DEBUG(L"getting text between offsets "<<startOffset<<L" and "<<endOffset);
	if(useMarkup) {
		this->generateMarkupOpeningTag(text,startOffset,endOffset);
	}
	nhAssert(startOffset>=0); //StartOffset must be not negative
	nhAssert(startOffset<endOffset); //StartOffset must be less than endOffset
	nhAssert(endOffset<=this->length); //endOffset can't be greater than node length
	if(useMarkup) {
		wchar_t c;
		for(int offset=startOffset;offset<endOffset;++offset) {
			c=this->text[offset];
			appendCharToXML(c,text);
		}
	} else {
		text.append(this->text,startOffset,endOffset-startOffset);
	}
	if(useMarkup) {
		this->generateMarkupClosingTag(text);
	}
	LOG_DEBUG(L"generated, text string is now of length "<<text.length());
}

VBufStorage_textFieldNode_t::VBufStorage_textFieldNode_t(const std::wstring& textArg): VBufStorage_fieldNode_t(static_cast<int>(textArg.length()),false), text(textArg) {
	LOG_DEBUG(L"textFieldNode initialization, with text of length "<<length);
}

std::wstring VBufStorage_textFieldNode_t::getDebugInfo() const {
	std::wostringstream s;
	s<<L"text "<<this->VBufStorage_fieldNode_t::getDebugInfo();
	return s.str();
}

//buffer implementation

void VBufStorage_buffer_t::forgetControlFieldNode(VBufStorage_controlFieldNode_t* node) {
	nhAssert(node); //Node can't be NULL
	map<VBufStorage_controlFieldNodeIdentifier_t,VBufStorage_controlFieldNode_t*>::iterator i=controlFieldNodesByIdentifier.find(node->identifier);
	nhAssert(i!=controlFieldNodesByIdentifier.end());
	nhAssert(i->second==node);
	controlFieldNodesByIdentifier.erase(i);
}

bool VBufStorage_buffer_t::insertNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_fieldNode_t* node) {
	if(!node) {
		LOG_DEBUGWARNING(L"Cannot insert a NULL node. Returning false");
		return false;
	}
	if(!parent&&previous) {
		LOG_DEBUGWARNING(L"Previous cannot be specified with no parent. Returning false");
		return false;
	}
	if(parent&&!isNodeInBuffer(parent)) {
		LOG_DEBUGWARNING(L"Bad parent: node at "<<parent<<L" not in this buffer at "<<this<<L". Returning false");
		return false;
	}
	if(previous&&!isNodeInBuffer(previous)) {
		LOG_DEBUGWARNING(L"Bad previous: node at "<<previous<<L" not in this buffer at "<<this<<L". Returning false");
		return false;
	}
	if(parent&&previous&&parent!=previous->parent) {
		LOG_DEBUGWARNING(L"Bad relation: parent at "<<parent<<L" is not a parent of previous at "<<previous<<L". Returning false");
		return false;
	}
	if(!parent&&this->rootNode) {
		LOG_DEBUGWARNING(L"No parent specified but the root node already exists at "<<this->rootNode<<L". returning false");
		return false;
	}
	VBufStorage_fieldNode_t* next=NULL;
	//make sure we have a good parent, previous and next
	if(previous!=NULL) parent=previous->parent;
	next=(previous?previous->next:(parent?parent->firstChild:NULL));
	LOG_DEBUG(L"using parent: "<<(parent?parent->getDebugInfo():L"NULL"));
	LOG_DEBUG(L"Using previous: "<<(previous?previous->getDebugInfo():L"NULL"));
	LOG_DEBUG(L"Using next: "<<(next?next->getDebugInfo():L"NULL"));
	if(parent==NULL) {
		LOG_DEBUG(L"making node root node of buffer");
		this->rootNode=node;
	} else { 
		if(previous==NULL) {
			LOG_DEBUG(L"Making node first child of parent");
			parent->firstChild=node;
		}
		if(next==NULL) {
			LOG_DEBUG(L"Making node last child of parent");
			parent->lastChild=node;
		}
	}
	if(previous) {
		LOG_DEBUG(L"Making node previous's next");
		previous->next=node;
	}
	if(next) {
		LOG_DEBUG(L"Making node next's previous");
		next->previous=node;
	}
	LOG_DEBUG(L"setting node's parent, previous and next");
	node->parent=parent;
	node->previous=previous;
	node->next=next;
	if(node->length>0) {
		LOG_DEBUG(L"Widening ancestors by "<<node->length);
		for(VBufStorage_fieldNode_t* ancestor=node->parent;ancestor!=NULL;ancestor=ancestor->parent) {
			LOG_DEBUG(L"Ancestor: "<<ancestor->getDebugInfo());
			ancestor->length+=node->length;
			nhAssert(ancestor->length>=0); //length must never be negative
			LOG_DEBUG(L"Ancestor length now"<<ancestor->length);
		}
	}
	LOG_DEBUG(L"Inserted subtree");
	nhAssert(this->nodes.count(node)==0);
	this->nodes.insert(node);
	return true;
}

void VBufStorage_buffer_t::deleteNode(VBufStorage_fieldNode_t* node) {
	nhAssert(node);
	node->disassociateFromBuffer(this);
	nhAssert(this->nodes.count(node)==1);
	this->nodes.erase(node);
	LOG_DEBUG(L"deleting node at "<<node);
	delete node;
}

void VBufStorage_buffer_t::deleteSubtree(VBufStorage_fieldNode_t* node) {
	nhAssert(node); //node can't be null
	LOG_DEBUG(L"deleting subtree starting at "<<node->getDebugInfo());
	//Save off next before deleting the subtree 
	for(VBufStorage_fieldNode_t* child=node->firstChild;child!=NULL;) {
		VBufStorage_fieldNode_t* next=child->next;
		deleteSubtree(child);
		child=next;
	}
	deleteNode(node);
	LOG_DEBUG(L"Deleted subtree");
}

VBufStorage_buffer_t::VBufStorage_buffer_t(): rootNode(NULL), nodes(), controlFieldNodesByIdentifier(), selectionStart(0), selectionLength(0) {
	LOG_DEBUG(L"buffer initializing");
}

VBufStorage_buffer_t::~VBufStorage_buffer_t() {
	LOG_DEBUG(L"buffer being destroied");
	this->clearBuffer();
}

VBufStorage_controlFieldNode_t*  VBufStorage_buffer_t::addControlFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, int docHandle, int ID, bool isBlock) {
	LOG_DEBUG(L"Adding control field node to buffer with parent at "<<parent<<L", previous at "<<previous<<L", docHandle "<<docHandle<<L", ID "<<ID);
	VBufStorage_controlFieldNode_t* controlFieldNode=new VBufStorage_controlFieldNode_t(docHandle,ID,isBlock);
	nhAssert(controlFieldNode); //controlFieldNode must have been allocated
	LOG_DEBUG(L"Created controlFieldNode: "<<controlFieldNode->getDebugInfo());
	if(addControlFieldNode(parent,previous,controlFieldNode)!=controlFieldNode) {
		LOG_DEBUGWARNING(L"Error adding control field node to buffer");
		delete controlFieldNode;
		return NULL;
	}
	return controlFieldNode;
}

VBufStorage_controlFieldNode_t*  VBufStorage_buffer_t::addControlFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_controlFieldNode_t* controlFieldNode) {
	if(!controlFieldNode) {
		LOG_DEBUGWARNING(L"Node is NULL. Returnning NULL");
		return NULL;
	}
	LOG_DEBUG(L"Add controlFieldNode using parent at "<<parent<<L", previous at "<<previous<<L", node at "<<controlFieldNode);
	if(controlFieldNodesByIdentifier.count(controlFieldNode->identifier)>0) {
		LOG_DEBUGWARNING(L"Buffer at "<<this<<L" already has a node with the same identifier as node "<<controlFieldNode->getDebugInfo()<<L". Returning NULL"); 
		return NULL;
	}
	LOG_DEBUG(L"Inserting controlFieldNode in to buffer");
	if(!insertNode(parent, previous, controlFieldNode)) {
		LOG_DEBUGWARNING(L"Error inserting node at "<<controlFieldNode<<L". Returning NULL");
		return NULL;
	}
	controlFieldNodesByIdentifier[controlFieldNode->identifier]=controlFieldNode;
	// If the node's new parent requires descendants to always be rerendered, copy this etting to the node as well.
	if(parent&&parent->alwaysRerenderDescendants) {
		controlFieldNode->alwaysRerenderDescendants=true;
	}
	LOG_DEBUG(L"Added new controlFieldNode, returning node");
	return controlFieldNode;
}

VBufStorage_textFieldNode_t*  VBufStorage_buffer_t::addTextFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, const std::wstring& text) {
	LOG_DEBUG(L"Add textFieldNode using parent at "<<parent<<L", previous at "<<previous);
	// #2963: Strip any private area unicode or 0-with spaces from the start and end of the string
	size_t textLength=text.length();
	bool needsStrip=false;
	size_t i;
	for(i=0;i<textLength;++i) {
		if(!isPrivateCharacter(text[i])) { 
			break;
		}
		needsStrip=true;
	}
	size_t subStart=i;
	for(i=0;i<textLength;++i) {
		if(!isPrivateCharacter(text[(textLength-1)-i])) { 
			break;
		}
		needsStrip=true;
	}
	size_t subLength=max(textLength-i,subStart)-subStart;
	VBufStorage_textFieldNode_t* textFieldNode=new VBufStorage_textFieldNode_t(needsStrip?text.substr(subStart,subLength):text);
	nhAssert(textFieldNode); //controlFieldNode must have been allocated
	LOG_DEBUG(L"Created textFieldNode: "<<textFieldNode->getDebugInfo());
	if(addTextFieldNode(parent,previous,textFieldNode)!=textFieldNode) {
		LOG_DEBUGWARNING(L"Error adding textFieldNode to buffer");
		delete textFieldNode;
		return NULL;
	}
	if (needsStrip && subStart>0) {
		// There are characters stripped from the start of the text.
		// We save the number of these characters in an attribute, required for calculating offsets in IA2Text.
		wostringstream s;
		s << subStart;
		textFieldNode->addAttribute(L"strippedCharsFromStart", s.str());
	}
	return textFieldNode;
}

VBufStorage_textFieldNode_t*  VBufStorage_buffer_t::addTextFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_textFieldNode_t* textFieldNode) {
	if(!textFieldNode) {
		LOG_DEBUGWARNING(L"Node is NULL. Returnning NULL");
		return NULL;
	}
	LOG_DEBUG(L"Add textFieldNode using parent at "<<parent<<L", previous at "<<previous<<L", node at "<<textFieldNode);
	if(parent==NULL) {
		LOG_DEBUGWARNING(L"Can not add a text field node at the root of the buffer. Returnning NULL");
		return NULL;
	}
	LOG_DEBUG(L"Inserting textFieldNode in to buffer");
	if(!insertNode(parent, previous, textFieldNode)) {
		LOG_DEBUGWARNING(L"Error inserting node at "<<textFieldNode<<L". Returning NULL");
		return NULL;
	}
	LOG_DEBUG(L"Added new textFieldNode, returning node");
	return textFieldNode;
}

bool VBufStorage_buffer_t::replaceSubtrees(map<VBufStorage_fieldNode_t*,VBufStorage_buffer_t*>& m) {
	VBufStorage_controlFieldNode_t* parent=NULL;
	VBufStorage_fieldNode_t* previous=NULL;
	//Using the current selection start, record a list of ancestor fields by their identifier, 
	//and a relative offset of the selection start to those fields, so that the selection can be corrected after the replacement.
	VBufStorage_relativeSelection_t identifierList;
	if(this->getTextLength()>0) {
		int controlDocHandle, controlID, controlNodeStart, controlNodeEnd;
		parent=this->locateControlFieldNodeAtOffset(this->selectionStart,&controlNodeStart,&controlNodeEnd,&controlDocHandle,&controlID);
		int relativeSelectionStart=this->selectionStart-controlNodeStart;
		for(;parent!=NULL;parent=parent->parent) {
			identifierList.push_front(pair<VBufStorage_controlFieldNodeIdentifier_t,int>(parent->identifier,relativeSelectionStart));
			for(previous=parent->previous;previous!=NULL;relativeSelectionStart+=previous->length,previous=previous->previous);
		}
	}
	// For each buffer in the map,
	// Reverse iterate over all reference nodes, replacing them with the existing nodes in the original buffer they point to.
	// We must iterate in reverse as new nodes are always inserted using parent and previous as the location,
	// iterating forward would cause a future reference node's previous to be come invalid as it had been replaced. 
	for(auto subtreeEntryIter=m.cbegin();subtreeEntryIter!=m.cend();++subtreeEntryIter) {
		auto node=subtreeEntryIter->first;
		auto buffer=subtreeEntryIter->second;
		for(auto referenceNodeIter=buffer->referenceNodes.rbegin();referenceNodeIter!=buffer->referenceNodes.rend();++referenceNodeIter) {
			auto parent=(*referenceNodeIter)->parent;
			auto previous=(*referenceNodeIter)->previous;
			auto referenced=(*referenceNodeIter)->referenceNode;
			buffer->removeFieldNode(*referenceNodeIter);
			this->unlinkFieldNode(referenced);
			buffer->insertNode(parent,previous,referenced);
		}
	}
	//For each node in the map,
	//Replace the node on this buffer, with the content of the buffer in the map for that node
	//Note that controlField info will automatically be removed, but not added again.
	bool failedBuffers=false;
	for(map<VBufStorage_fieldNode_t*,VBufStorage_buffer_t*>::iterator i=m.begin();i!=m.end();) {
		VBufStorage_fieldNode_t* node=i->first;
		VBufStorage_buffer_t* buffer=i->second;
		if(buffer==this) {
			LOG_DEBUGWARNING(L"Cannot replace a subtree on a buffer with the same buffer. Skipping");
			failedBuffers=true;
			m.erase(i++);
			continue;
		}
		parent=node->parent;
		previous=node->previous;
		if(!this->removeFieldNode(node)) {
			LOG_DEBUGWARNING(L"Error removing node. Skipping");
			failedBuffers=true;
			buffer->clearBuffer();
			delete buffer;
			m.erase(i++);
			continue;
		}
		if(!buffer->rootNode) {
			LOG_DEBUGWARNING(L"Empty temp buffer");
			delete buffer;
			m.erase(i++);
			continue;
		}
		if(!this->insertNode(parent,previous,buffer->rootNode)) {
			LOG_DEBUGWARNING(L"Error inserting node. Skipping");
			failedBuffers=true;
			buffer->clearBuffer();
			delete buffer;
			m.erase(i++);
			continue;
		}
		buffer->nodes.erase(buffer->rootNode);
		this->nodes.insert(buffer->nodes.begin(),buffer->nodes.end());
		buffer->nodes.clear();
		buffer->rootNode=NULL;
		++i;
	}
	//Update the controlField info on this buffer using all the buffers in the map
	//We do this all in one go instead of for each replacement in case there are issues with ordering
	//e.g. an identifier appears in one place before its removed in another
	for(auto i=m.begin();i!=m.end();++i) {
		VBufStorage_buffer_t* buffer=i->second;
		int failedIDs=0;
		for(map<VBufStorage_controlFieldNodeIdentifier_t,VBufStorage_controlFieldNode_t*>::iterator j=buffer->controlFieldNodesByIdentifier.begin();j!=buffer->controlFieldNodesByIdentifier.end();++j) {
			map<VBufStorage_controlFieldNodeIdentifier_t,VBufStorage_controlFieldNode_t*>::iterator existing=this->controlFieldNodesByIdentifier.find(j->first);
			if(existing!=this->controlFieldNodesByIdentifier.end()) {
				++failedIDs;
				if(!removeFieldNode(existing->second,false)) {
					LOG_DEBUGWARNING(L"Error removing old node to make when handling ID clash");
					continue;
				}
				nhAssert(this->controlFieldNodesByIdentifier.count(j->first)==0);
			}
			this->controlFieldNodesByIdentifier.insert(make_pair(j->first,j->second));
		}
		buffer->controlFieldNodesByIdentifier.clear();
		delete buffer;
		if(failedIDs>0) {
			LOG_DEBUGWARNING(L"Duplicate IDs when replacing subtree. Duplicate count "<<failedIDs);
			failedBuffers=true;
		}
	}
	m.clear();
	//Find the deepest field the selection started in that still exists, 
	//and correct the selection so its still positioned accurately relative to that field. 
	if(!identifierList.empty()) {
		VBufStorage_controlFieldNode_t* lastAncestorNode=NULL;
		int lastRelativeSelectionStart=0;
		for(list<pair<VBufStorage_controlFieldNodeIdentifier_t,int> >::iterator i=identifierList.begin();i!=identifierList.end();++i) {
			VBufStorage_controlFieldNode_t* currentAncestorNode=this->getControlFieldNodeWithIdentifier(i->first.docHandle,i->first.ID);
			if(currentAncestorNode==NULL) break;
			if(currentAncestorNode->parent!=lastAncestorNode) break;
			lastAncestorNode=currentAncestorNode;
			lastRelativeSelectionStart=i->second;
		}
		if(lastAncestorNode!=NULL) {
			int lastAncestorStartOffset, lastAncestorEndOffset;
			if(!this->getFieldNodeOffsets(lastAncestorNode,&lastAncestorStartOffset,&lastAncestorEndOffset)) {
				LOG_DEBUGWARNING(L"Error getting offsets for last ancestor node. Returnning false");
				return false;
			}
			this->selectionStart=lastAncestorStartOffset+min(lastRelativeSelectionStart,max(lastAncestorNode->length-1,0));
		}
	}
	return !failedBuffers;
}

bool VBufStorage_buffer_t::unlinkFieldNode(VBufStorage_fieldNode_t* node, bool removeDescendants) {
	if(!isNodeInBuffer(node)) {
		LOG_DEBUGWARNING(L"Node at "<<node<<L" is not in buffer at "<<this<<L". Returnning false");
		return false;
	}
	if(node==this->rootNode&&!removeDescendants) {
		LOG_DEBUGWARNING(L"Cannot remove the rootNode without removing its descendants. Returnning false");
		return false;
	}
	if((removeDescendants||!node->firstChild)&&node->length>0) {
		LOG_DEBUG(L"collapsing length of ancestors by "<<node->length);
		for(VBufStorage_fieldNode_t* ancestor=node->parent;ancestor!=NULL;ancestor=ancestor->parent) {
			LOG_DEBUG(L"Ancestor: "<<ancestor->getDebugInfo());
			ancestor->length-=node->length;
			nhAssert(ancestor->length>=0); //ancestor length can't be negative
			LOG_DEBUG(L"Ancestor length now"<<ancestor->length);
		}
	}
	LOG_DEBUG(L"Disconnecting node from its siblings and or parent");
	if(node->next!=NULL) {
		node->next->previous=(!removeDescendants&&node->lastChild)?node->lastChild:node->previous;
	} else if(node->parent) {
		node->parent->lastChild=(!removeDescendants&&node->lastChild)?node->lastChild:node->previous;
	}
	if(node->previous!=NULL) {
		node->previous->next=(!removeDescendants&&node->firstChild)?node->firstChild:node->next;
	} else if(node->parent) {
		node->parent->firstChild=(!removeDescendants&&node->firstChild)?node->firstChild:node->next;
	}
	if(!removeDescendants) {
		for(VBufStorage_fieldNode_t* child=node->firstChild;child!=NULL;child=child->next) child->parent=node->parent;
		if(node->firstChild) node->firstChild->previous=node->previous;
		if(node->lastChild) node->lastChild->next=node->next;
	}
	if(node==this->rootNode) {
		LOG_DEBUG(L"Removing root node from buffer ");
		this->rootNode=NULL;
	}
	LOG_DEBUG(L"Removed fieldNode and descendants, returning true");
	return true;
}

bool VBufStorage_buffer_t::removeFieldNode(VBufStorage_fieldNode_t* node,bool removeDescendants) {
	if(!unlinkFieldNode(node,removeDescendants)) {
		LOG_DEBUGWARNING(L"Could not unlink field node");
		return false;
	}
	if(removeDescendants) {
		deleteSubtree(node);
	} else {
		deleteNode(node);
	}
	return true;
}

void VBufStorage_buffer_t::clearBuffer() {
	for(set<VBufStorage_fieldNode_t*>::iterator i=nodes.begin();i!=nodes.end();++i) {
		nhAssert(*i);
		delete *i;
	}
	nodes.clear();
	controlFieldNodesByIdentifier.clear();
	selectionStart=selectionLength=0;
	this->rootNode=NULL;
}

bool VBufStorage_buffer_t::getFieldNodeOffsets(VBufStorage_fieldNode_t* node, int *startOffset, int *endOffset) {
	if(!isNodeInBuffer(node)) {
		LOG_DEBUGWARNING(L"Node at "<<node<<L" is not in buffer at "<<this<<L". Returnning false");
		return false;
	}
	*startOffset=node->calculateOffsetInTree();
	*endOffset=(*startOffset)+node->length;
	LOG_DEBUG(L"node has offsets "<<*startOffset<<L" and "<<*endOffset<<L", returning true");
	return true;
}

bool VBufStorage_buffer_t::isFieldNodeAtOffset(VBufStorage_fieldNode_t* node, int offset) {
	if(!isNodeInBuffer(node)) {
		LOG_DEBUGWARNING(L"Node at "<<node<<L" is not in buffer at "<<this<<L". Returnning false");
		return false;
	}
	if(offset<0||offset>=this->getTextLength()) {
		LOG_DEBUGWARNING(L"Offset "<<offset<<L" out of range. Returnning false");
		return false;
	}
	int startOffset, endOffset;
	if(!getFieldNodeOffsets(node,&startOffset,&endOffset)) {
		LOG_DEBUGWARNING(L"Could not get offsets for node at "<<node<<L", returning false");
		return false;
	}
	if(offset<startOffset||offset>=endOffset) {
		LOG_DEBUG(L"node is not at offset, returning false");
		return false;
	}
	LOG_DEBUG(L"Node is at offset "<<offset<<L", returning true");
	return true;
}

VBufStorage_textFieldNode_t* VBufStorage_buffer_t::locateTextFieldNodeAtOffset(int offset, int *nodeStartOffset, int *nodeEndOffset) {
	if(this->rootNode==NULL) {
		LOG_DEBUGWARNING(L"Buffer is empty, returning NULL");
		return NULL;
	}
	if(offset<0||offset>=this->getTextLength()) {
		LOG_DEBUGWARNING(L"Offset "<<offset<<L" out of range. Returnning NULL");
		return NULL;
	}
	int relativeOffset=0;
	VBufStorage_textFieldNode_t* node=this->rootNode->locateTextFieldNodeAtOffset(offset,&relativeOffset);
	if(node==NULL) {
		LOG_DEBUGWARNING(L"Could not locate node, returning NULL");
		return NULL;
	}
	int startOffset=offset-relativeOffset;
	if(nodeStartOffset) *nodeStartOffset=startOffset;
	if(nodeEndOffset) *nodeEndOffset=startOffset+node->length;
	LOG_DEBUG(L"Located node, returning node at "<<node);
	return node;
}

VBufStorage_controlFieldNode_t* VBufStorage_buffer_t::locateControlFieldNodeAtOffset(int offset, int *nodeStartOffset, int * nodeEndOffset, int *docHandle, int *ID) {
	int startOffset, endOffset;
	VBufStorage_textFieldNode_t* node=this->locateTextFieldNodeAtOffset(offset,&startOffset,&endOffset);
	if(node==NULL) {
		LOG_DEBUGWARNING(L"Could not locate node at offset, returning NULL");
		return NULL;
	}
	nhAssert(node->parent);
	for(VBufStorage_fieldNode_t* previous=node->previous;previous!=NULL;previous=previous->previous) {
		startOffset-=previous->length;
	}
	endOffset=startOffset+node->parent->length;
	nhAssert(startOffset>=0&&endOffset>=startOffset); //Offsets must not be negative
	VBufStorage_controlFieldNode_t* controlFieldNode = node->parent;
	if(nodeStartOffset) *nodeStartOffset=startOffset;
	if(nodeEndOffset) *nodeEndOffset=endOffset;
	if(docHandle) *docHandle=controlFieldNode->identifier.docHandle;
	if(ID) *ID=controlFieldNode->identifier.ID;
	LOG_DEBUG(L"Found node, returning "<<controlFieldNode->getDebugInfo()); 
	return controlFieldNode;
	}

VBufStorage_controlFieldNode_t* VBufStorage_buffer_t::getControlFieldNodeWithIdentifier(int docHandle, int ID) {
	VBufStorage_controlFieldNodeIdentifier_t identifier(docHandle, ID);
	std::map<VBufStorage_controlFieldNodeIdentifier_t,VBufStorage_controlFieldNode_t*>::iterator i=this->controlFieldNodesByIdentifier.find(identifier);
	if(i==this->controlFieldNodesByIdentifier.end()) {
		LOG_DEBUG(L"No controlFieldNode with identifier, returning NULL");
		return NULL;
	}
	VBufStorage_controlFieldNode_t* node=i->second;
	nhAssert(node); //Node can not be NULL
	LOG_DEBUG(L"returning node at "<<node);
	return node;
}

bool VBufStorage_buffer_t::getIdentifierFromControlFieldNode(VBufStorage_controlFieldNode_t* node, int* docHandle, int* ID) {
	if(!isNodeInBuffer(node)) {
		LOG_DEBUGWARNING(L"Node at "<<node<<L" is not in buffer at "<<this<<L". Returnning false");
		return false;
	}
	if(docHandle) *docHandle=node->identifier.docHandle;
	if(ID) *ID=node->identifier.ID;
	return true;
}

bool VBufStorage_buffer_t::getSelectionOffsets(int *startOffset, int *endOffset) const {
	nhAssert(this->selectionStart>=0&&this->selectionLength>=0); //Selection can't be negative
	int minStartOffset=0;
	int maxEndOffset=(this->rootNode)?this->rootNode->length:0;
	if(startOffset) *startOffset=max(minStartOffset,this->selectionStart);
	if(endOffset) *endOffset=min(this->selectionStart+this->selectionLength,maxEndOffset);
	LOG_DEBUG(L"Selection is "<<*startOffset<<L" and "<<*endOffset<<L", returning true");
	return true;
}

bool VBufStorage_buffer_t::setSelectionOffsets(int startOffset, int endOffset) {
	if(startOffset<0||endOffset<0||endOffset<startOffset) {
		LOG_DEBUGWARNING(L"invalid offsets of "<<startOffset<<L" and "<<endOffset<<L", returning false");
		return false;
	}
	this->selectionStart=startOffset;
	this->selectionLength=endOffset-startOffset;
	LOG_DEBUG(L"Selection set to "<<startOffset<<L" and "<<endOffset<<L", returning true");
	return true;
}

int VBufStorage_buffer_t::getTextLength() const {
	int length=(this->rootNode)?this->rootNode->length:0;
	LOG_DEBUG(L"Returning length of "<<length);
	return length;
}

bool VBufStorage_buffer_t::getTextInRange(int startOffset, int endOffset, wstring& text, bool useMarkup) {
	if(this->rootNode==NULL) {
		LOG_DEBUGWARNING(L"buffer is empty, returning NULL");
		return false;
	}
	if(startOffset<0||startOffset>=endOffset||endOffset>this->rootNode->length) {
		LOG_DEBUGWARNING(L"Bad offsets of "<<startOffset<<L" and "<<endOffset<<L", returning NULL");
		return false;
	}
	this->rootNode->getTextInRange(startOffset,endOffset,text,useMarkup);
	LOG_DEBUG(L"Got text between offsets "<<startOffset<<L" and "<<endOffset<<L", returning true");
	return true;
}

VBufStorage_fieldNode_t* VBufStorage_buffer_t::findNodeByAttributes(int offset, VBufStorage_findDirection_t direction, const std::wstring& attribs, const std::wstring &regexp, int *startOffset, int *endOffset) {
	if(this->rootNode==NULL) {
		LOG_DEBUGWARNING(L"buffer empty, returning NULL");
		return NULL;
	}
	if(offset>=this->rootNode->length) {
		LOG_DEBUGWARNING(L" offset "<<offset<<L" is past end of buffer, returning NULL");
		return NULL;
	}
	LOG_DEBUG(L"find node starting at offset "<<offset<<L", with attribute regexp: "<<regexp);
	int bufferStart, bufferEnd, tempRelativeStart=0;
	VBufStorage_fieldNode_t* node=NULL;
	if(offset==-1) {
		node=this->rootNode;
		bufferStart=0;
		bufferEnd=node->length;
	} else if(offset>=0) {
		node=this->locateTextFieldNodeAtOffset(offset,&bufferStart,&bufferEnd);
	} else {
		LOG_DEBUGWARNING(L"Invalid offset: "<<offset);
		return NULL;
	}
	if(node==NULL) {
		LOG_DEBUGWARNING(L"Could not find node at offset "<<offset<<L", returning NULL");
		return NULL;
	}
	// Split attribs at spaces.
	vector<wstring> attribsList;
	copy(istream_iterator<wstring, wchar_t, std::char_traits<wchar_t>>(wistringstream(attribs)),
		istream_iterator<wstring, wchar_t, std::char_traits<wchar_t>>(),
		back_inserter<vector<wstring> >(attribsList));
	wregex regexObj;
	try {
		regexObj=wregex(regexp);
	} catch (...) {
		LOG_ERROR(L"Error in regular expression");
		return NULL;
	}
	LOG_DEBUG(L"starting from node "<<node->getDebugInfo());
	LOG_DEBUG(L"initial start is "<<bufferStart<<L" and initial end is "<<bufferEnd);
	if(direction==VBufStorage_findDirection_forward) {
		LOG_DEBUG(L"searching forward");
		for(node=node->nextNodeInTree(TREEDIRECTION_FORWARD,NULL,&tempRelativeStart);node!=NULL;node=node->nextNodeInTree(TREEDIRECTION_FORWARD,NULL,&tempRelativeStart)) {
			bufferStart+=tempRelativeStart;
			bufferEnd=bufferStart+node->length;
			LOG_DEBUG(L"start is now "<<bufferStart<<L" and end is now "<<bufferEnd);
			LOG_DEBUG(L"Checking node "<<node->getDebugInfo());
			if(node->length>0&&!(node->isHidden)&&node->matchAttributes(attribsList,regexObj)) {
				LOG_DEBUG(L"found a match");
				break;
			}
		}
	} else if(direction==VBufStorage_findDirection_back) {
		LOG_DEBUG(L"searching back");
		bool skippedFirstMatch=false;
		for(node=node->nextNodeInTree(TREEDIRECTION_BACK,NULL,&tempRelativeStart);node!=NULL;node=node->nextNodeInTree(TREEDIRECTION_BACK,NULL,&tempRelativeStart)) {
			bufferStart+=tempRelativeStart;
			bufferEnd=bufferStart+node->length;
			LOG_DEBUG(L"start is now "<<bufferStart<<L" and end is now "<<bufferEnd);
			if(node->length>0&&!(node->isHidden)&&node->matchAttributes(attribsList,regexObj)) {
				//Skip first containing parent match or parent match where offset hasn't changed 
				if((bufferStart==offset)||(!skippedFirstMatch&&bufferStart<offset&&bufferEnd>offset)) {
					LOG_DEBUG(L"skipping initial parent");
					skippedFirstMatch=true;
					continue;
				}
				LOG_DEBUG(L"found match");
				break;
			}
		}
	} else if(direction==VBufStorage_findDirection_up) {
		LOG_DEBUG(L"searching up");
		do {
			for(;node->previous!=NULL;node=node->previous,bufferStart-=node->length);
			LOG_DEBUG(L"start is now "<<bufferStart);
			node=node->parent;
			if(node) {
				bufferEnd=bufferStart+node->length;
			}
		} while(node!=NULL&&(node->isHidden||!node->matchAttributes(attribsList,regexObj)));
		LOG_DEBUG(L"end is now "<<bufferEnd);
	}
	if(node==NULL) {
		LOG_DEBUG(L"Could not find node, returning NULL");
		return NULL;
	}
	if(startOffset) *startOffset=bufferStart;
	if(endOffset) *endOffset=bufferEnd;
	LOG_DEBUG(L"returning node at "<<node<<L" with offsets of "<<*startOffset<<L" and "<<*endOffset);
	return node;
}

bool VBufStorage_buffer_t::getLineOffsets(int offset, int maxLineLength, bool useScreenLayout, int *startOffset, int *endOffset) {
	if(this->rootNode==NULL||offset>=this->rootNode->length) {
		LOG_DEBUGWARNING(L"Offset of "<<offset<<L" too big for buffer, returning false");
		return false;
	}
	LOG_DEBUG(L"Calculating line offsets, using offset "<<offset<<L", with max line length of "<<maxLineLength<<L", useing screen layout "<<useScreenLayout);
	int initBufferStart, initBufferEnd;
	VBufStorage_fieldNode_t* initNode=locateTextFieldNodeAtOffset(offset,&initBufferStart,&initBufferEnd);
	LOG_DEBUG(L"Starting at node "<<initNode->getDebugInfo());
	std::set<int> possibleBreaks;
	//Find the node at which to limit the search for line endings.
	VBufStorage_fieldNode_t* limitBlockNode=NULL;
	for(limitBlockNode=initNode->parent;limitBlockNode!=NULL&&!limitBlockNode->isBlock;limitBlockNode=limitBlockNode->parent);
	//Some needed variables for searching back and forward
	VBufStorage_fieldNode_t* node=NULL;
	int relative, bufferStart, bufferEnd, tempRelativeStart;
	bool foundHardBreak=false;
	//Search forward for the next line ending.
	node = initNode;
	relative = offset - initBufferStart;
	bufferStart = initBufferStart;
	bufferEnd = initBufferEnd;
	int lineEnd;
	do {
	possibleBreaks.insert(bufferStart);
	possibleBreaks.insert(bufferEnd);
		if(node->length>0&&node->firstChild==NULL) {
			std::wstring text;
			lineEnd = bufferEnd;
			node->getTextInRange(0,node->length,text,false);
			bool lastWasSpace = false;
			for (int i = relative; i < node->length; ++i) {
				if ((text[i] == L'\r' && (i + 1 >= node->length || text[i + 1] != L'\n'))
					|| text[i] == L'\n'
				) {
					lineEnd = bufferStart + i + 1;
					foundHardBreak=true;
					break;
				}
				if(iswspace(text[i])) {
					lastWasSpace = true;
				} else {
					if(lastWasSpace) {
						possibleBreaks.insert(bufferStart + i);
					}
					lastWasSpace = false;
				}
			}
			if (foundHardBreak) {
				//A hard line break was found.
				break;
			}
		}
		//Move on to the next node.
		node = node->nextNodeInTree(TREEDIRECTION_FORWARD,limitBlockNode,&tempRelativeStart);
		//If not using screen layout, make sure not to pass in to another control field node
		if(node&&((!useScreenLayout&&node->firstChild)||node->isBlock)) {
			node=NULL;
		}
		if(node) {
			bufferStart+=tempRelativeStart;
			bufferEnd=bufferStart+node->length;
			relative = 0;
		}
	} while (node);
	//Search backward for the previous line ending.
	node = initNode;
	relative = offset - initBufferStart;
	bufferStart = initBufferStart;
	bufferEnd = initBufferEnd;
	int lineStart;
	foundHardBreak=false;
	do {
		possibleBreaks.insert(bufferStart);
		possibleBreaks.insert(bufferEnd);
		if(node->length>0&&node->firstChild==NULL) {
			std::wstring text;
			lineStart = bufferStart;
			node->getTextInRange(0,node->length,text,false);
			bool lastWasSpace = false;
			for (int i = relative - 1; i >= 0; i--) {
				if ((text[i] == L'\r' && (i + 1 >= node->length || text[i + 1] != L'\n'))
					|| text[i] == L'\n'
				) {
					lineStart = bufferStart + i + 1;
					foundHardBreak=true;
					break;
				}
				if (iswspace(text[i])) {
					if (!lastWasSpace) {
						possibleBreaks.insert(bufferStart + i + 1);
					}
					lastWasSpace = true;
				} else {
					lastWasSpace = false;
				}
			}
			if (foundHardBreak) {
				//A hard line break was found.
				break;
			}
		}
		//Move on to the previous node.
		node = node->nextNodeInTree(TREEDIRECTION_SYMMETRICAL_BACK,useScreenLayout?limitBlockNode:node->parent,&tempRelativeStart);
		//If not using screen layout, make sure not to pass in to another control field node
		if(node&&node->isBlock) {
			node=NULL;
		}
		if(node) {
			bufferStart+=tempRelativeStart;
			bufferEnd=bufferStart+node->length;
			relative = node->length;
		}
	} while (node);
	LOG_DEBUG(L"line offsets after searching back and forth for line feeds and block edges is "<<lineStart<<L" and "<<lineEnd);
	//Finally take maxLineLength in to account
	if(maxLineLength>0) {
		set<int> realBreaks;
		realBreaks.insert(lineStart);
		realBreaks.insert(lineEnd);
		for(int i=lineStart,lineCharCounter=0;i<lineEnd;++i,++lineCharCounter) {
			if(lineCharCounter==maxLineLength) {
				if(possibleBreaks.size()>0) {
					set<int>::iterator possible=possibleBreaks.upper_bound(i);
					if((possible!=possibleBreaks.begin())&&(*(--possible)>(i-maxLineLength))) {
												i=*possible;
					}
				}
				realBreaks.insert(i);
				lineCharCounter=0;
			}
		}
		set<int>::iterator real=realBreaks.upper_bound(offset);
		lineEnd=*real;
		lineStart=*(--real);
		LOG_DEBUG(L"limits after fixing for maxLineLength %: start "<<lineStart<<L" end "<<lineEnd);
	}
	*startOffset=lineStart;
	*endOffset=lineEnd;
	LOG_DEBUG(L"Successfully calculated Line offsets of "<<lineStart<<L", "<<lineEnd<<L", returning true");
	return true;
}

bool VBufStorage_buffer_t::hasContent() {
	return (this->rootNode)?true:false;
}

bool VBufStorage_buffer_t::isDescendantNode(VBufStorage_fieldNode_t* parent, VBufStorage_fieldNode_t* descendant) {
	nhAssert(parent);
	nhAssert(descendant);
	LOG_DEBUG(L"is node at "<<descendant<<L" a descendant of node at "<<parent);
	for(VBufStorage_fieldNode_t* tempNode=descendant->parent;tempNode!=NULL;tempNode=tempNode->parent) {
		if(tempNode==parent) {
			LOG_DEBUG(L"Node is a descendant");
			return true;
		}
	}
	LOG_DEBUG(L"Not a descendant");
	return false;
}

bool VBufStorage_buffer_t::isNodeInBuffer(VBufStorage_fieldNode_t* node) {
	return this->nodes.count(node)?true:false;
}

VBufStorage_referenceNode_t*  VBufStorage_buffer_t::addReferenceNodeToBuffer(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_controlFieldNode_t* node) {
	if(!node) return nullptr;
	auto referenceNode=new VBufStorage_referenceNode_t(node->identifier.docHandle,node->identifier.ID,node);
	if(!addControlFieldNode(parent,previous,referenceNode)) {
		delete referenceNode;
		return nullptr;
	}
	referenceNodes.push_back(referenceNode);
	return referenceNode;
}

std::wstring VBufStorage_buffer_t::getDebugInfo() const {
	std::wostringstream s;
	s<<L"buffer at "<<this<<L", selectionStart is "<<selectionStart<<L", selectionEnd is "<<selectionLength+selectionStart;
	return s.str();
}
