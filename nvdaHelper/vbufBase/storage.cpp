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
#include <windows.h>
#include <remote/log.h>
#include "utils.h"
#include "storage.h"

using namespace std;

inline void appendCharToXML(const wchar_t c, wstring& xml) {
	switch(c) {
		case L'"':
		xml+=L"&quot;";
		break;
		case L'<':
		xml+=L"&lt;";
		break;
		case L'>':
		xml+=L"&gt;";
		break;
		case L'&':
		xml+=L"&amp;";
		break;
		default:
		if (c == 0x9 || c == 0xA || c == 0xD
			|| (c >= 0x20 && c <= 0xD7FF) || (c >= 0xE000 && c <= 0xFFFD)
		) {
			// Valid XML character.
			xml+=c;
		} else {
			// Invalid XML character.
			xml += 0xfffd; // Unicode replacement character
		}
	}
}

VBufStorage_textContainer_t::VBufStorage_textContainer_t(wstring str): wstring(str) {}

VBufStorage_textContainer_t::~VBufStorage_textContainer_t() {}

const wstring& VBufStorage_textContainer_t::getString() {
	return *this;
}

void VBufStorage_textContainer_t::destroy() {
	delete this;
}

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

bool VBufStorage_fieldNode_t::matchAttributes(const std::wstring& attribsString) {
	LOG_DEBUG(L"using attributes of "<<attribsString);
	multiValueAttribsMap attribsMap;
	multiValueAttribsStringToMap(attribsString,attribsMap);
	bool outerMatch=true;
	for(multiValueAttribsMap::iterator i=attribsMap.begin();i!=attribsMap.end();++i) {
		LOG_DEBUG(L"Checking for attrib "<<i->first);
		VBufStorage_attributeMap_t::iterator foundIterator=attributes.find(i->first);
		const std::wstring& foundValue=(foundIterator!=attributes.end())?foundIterator->second:L"";
		wstring foundValueTrailingSpaces=L" "+foundValue+L" ";
		LOG_DEBUG(L"node's value for this attribute is "<<foundValue);
		multiValueAttribsMap::iterator upperBound=attribsMap.upper_bound(i->first);
		bool innerMatch=false;
		for(multiValueAttribsMap::iterator j=i;j!=upperBound;++j) { 
			i=j;
			if(innerMatch)
				continue;
			LOG_DEBUG(L"Checking value "<<j->second);
			if(
				// Word match.
				(j->second.compare(0, 2, L"~w")==0&&foundValueTrailingSpaces.find(L" "+j->second.substr(2)+L" ")!=wstring::npos)
				// Full match.
				||(j->second==foundValue)
			) {
				LOG_DEBUG(L"values match");
				innerMatch=true;
			}
		}
		outerMatch=innerMatch;
		if(!outerMatch) { 
			LOG_DEBUG(L"given attributes do not match node's attributes, returning false");
			return false;
		}
	}
	LOG_DEBUG(L"Given attributes match node's attributes, returning true");
	return true;
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

void VBufStorage_fieldNode_t::generateAttributesForMarkupOpeningTag(std::wstring& text) {
	wostringstream s;
	int childCount=0;
	for(VBufStorage_fieldNode_t* child=this->firstChild;child!=NULL;child=child->next) {
		++childCount;
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
	s<<L"_childcount=\""<<childCount<<L"\" _indexInParent=\""<<indexInParent<<L"\" _parentChildCount=\""<<parentChildCount<<L"\" ";
	text+=s.str();
	for(VBufStorage_attributeMap_t::iterator i=this->attributes.begin();i!=this->attributes.end();++i) {
		text+=i->first;
		text+=L"=\"";
		for(std::wstring::iterator j=i->second.begin();j!=i->second.end();++j) {
			appendCharToXML(*j,text);
		}
		text+=L"\" ";
	}
}

void VBufStorage_fieldNode_t::generateMarkupOpeningTag(std::wstring& text) {
	text+=L"<";
	this->generateMarkupTagName(text);
	text+=L" ";
	this->generateAttributesForMarkupOpeningTag(text);
	text+=L">";
}

void VBufStorage_fieldNode_t::generateMarkupClosingTag(std::wstring& text) {
	text+=L"</";
	this->generateMarkupTagName(text);
	text+=L">";
}

void VBufStorage_fieldNode_t::getTextInRange(int startOffset, int endOffset, std::wstring& text, bool useMarkup) {
	if(this->length==0) {
		LOG_DEBUG(L"node has 0 length, not collecting text");
		return;
	}
	LOG_DEBUG(L"getting text between offsets "<<startOffset<<L" and "<<endOffset);
	nhAssert(startOffset>=0); //startOffset can't be negative
	nhAssert(startOffset<endOffset); //startOffset must be before endOffset
	nhAssert(endOffset<=this->length); //endOffset can't be bigger than node length
	if(useMarkup) {
		this->generateMarkupOpeningTag(text);
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
		if(childEnd>startOffset&&endOffset>childStart) {
			LOG_DEBUG(L"child offsets overlap requested offsets");
			child->getTextInRange(max(startOffset,childStart)-childStart,min(endOffset-childStart,childLength),text,useMarkup);
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

VBufStorage_fieldNode_t::VBufStorage_fieldNode_t(int lengthArg, bool isBlockArg): parent(NULL), previous(NULL), next(NULL), firstChild(NULL), lastChild(NULL), length(lengthArg), isBlock(isBlockArg), attributes() {
	LOG_DEBUG(L"field node initialization at "<<this<<L"length is "<<length);
}

VBufStorage_fieldNode_t::~VBufStorage_fieldNode_t() {
	LOG_DEBUG(L"fieldNode being destroied");
}

VBufStorage_controlFieldNode_t* VBufStorage_fieldNode_t::getParent() {
	LOG_DEBUG(L"parent at "<<parent);
	return parent;
}

VBufStorage_fieldNode_t* VBufStorage_fieldNode_t::getPrevious() {
	LOG_DEBUG(L"previous at "<<previous);
	return previous;
}

VBufStorage_fieldNode_t* VBufStorage_fieldNode_t::getNext() {
	LOG_DEBUG(L"next at "<<next);
	return next;
}

VBufStorage_fieldNode_t* VBufStorage_fieldNode_t::getFirstChild() {
	LOG_DEBUG(L"first child at "<<firstChild);
	return firstChild;
}

VBufStorage_fieldNode_t* VBufStorage_fieldNode_t::getLastChild() {
	LOG_DEBUG(L"last child at "<<lastChild);
	return lastChild;
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

void VBufStorage_fieldNode_t::setIsBlock(bool isBlock) {
	this->isBlock=isBlock;
}

int VBufStorage_fieldNode_t::getLength() {
		return this->length;
	}

//controlFieldNode implementation

void VBufStorage_controlFieldNode_t::generateMarkupTagName(std::wstring& text) {
	text+=L"control";
}

void VBufStorage_controlFieldNode_t::generateAttributesForMarkupOpeningTag(std::wstring& text) {
	std::wostringstream s;
	s<<L"controlIdentifier_docHandle=\""<<identifier.docHandle<<L"\" controlIdentifier_ID=\""<<identifier.ID<<L"\" ";
	text+=s.str();
	this->VBufStorage_fieldNode_t::generateAttributesForMarkupOpeningTag(text);
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
	s<<L"control "<<this->VBufStorage_fieldNode_t::getDebugInfo()<<L", docHandle "<<identifier.docHandle<<L", ID is "<<identifier.ID;  
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

void VBufStorage_textFieldNode_t::getTextInRange(int startOffset, int endOffset, std::wstring& text, bool useMarkup) {
	LOG_DEBUG(L"getting text between offsets "<<startOffset<<L" and "<<endOffset);
	if(useMarkup) {
		this->generateMarkupOpeningTag(text);
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

VBufStorage_textFieldNode_t::VBufStorage_textFieldNode_t(const std::wstring& textArg): VBufStorage_fieldNode_t(textArg.length(),false), text(textArg) {
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
	nhAssert(this->controlFieldNodesByIdentifier.count(node->identifier)==1); //Node must exist in the set
	nhAssert(this->controlFieldNodesByIdentifier[node->identifier]->identifier==node->identifier);
	nhAssert(this->controlFieldNodesByIdentifier[node->identifier]==node); //Remembered node and this node must be equal
	this->controlFieldNodesByIdentifier.erase(node->identifier);
	LOG_DEBUG(L"Forgot controlFieldNode with docHandle "<<node->identifier.docHandle<<L" and ID "<<node->identifier.ID);
}

void VBufStorage_buffer_t::insertNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_fieldNode_t* node) {
	VBufStorage_fieldNode_t* next=NULL;
	nhAssert(node); //node can't be NULL
	nhAssert(previous==NULL||previous!=this->rootNode); //a root node can not have nodes after it on the same level
	//make sure we have a good parent, previous and next
	if(previous!=NULL) parent=previous->parent;
	next=(previous?previous->next:(parent?parent->firstChild:NULL));
	LOG_DEBUG(L"using parent: "<<(parent?parent->getDebugInfo():L"NULL"));
	LOG_DEBUG(L"Using previous: "<<(previous?previous->getDebugInfo():L"NULL"));
	LOG_DEBUG(L"Using next: "<<(next?next->getDebugInfo():L"NULL"));
	if(parent==NULL) {
		nhAssert(this->rootNode==NULL); //A buffer can only have one root node.
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
	node->disassociateFromBuffer(this);
	LOG_DEBUG(L"deleting node at "<<node);
	delete node;
	LOG_DEBUG(L"Deleted subtree");
}

VBufStorage_buffer_t::VBufStorage_buffer_t(): rootNode(NULL), controlFieldNodesByIdentifier(), selectionStart(0), selectionLength(0) {
	LOG_DEBUG(L"buffer initializing");
}

VBufStorage_buffer_t::~VBufStorage_buffer_t() {
	LOG_DEBUG(L"buffer being destroied");
	if(this->rootNode) {
		this->removeFieldNode(this->rootNode);
	}
}

VBufStorage_controlFieldNode_t*  VBufStorage_buffer_t::addControlFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, int docHandle, int ID, bool isBlock) {
	LOG_DEBUG(L"Adding control field node to buffer with parent at "<<parent<<L", previous at "<<previous<<L", docHandle "<<docHandle<<L", ID "<<ID);
	VBufStorage_controlFieldNode_t* controlFieldNode=new VBufStorage_controlFieldNode_t(docHandle,ID,isBlock);
	nhAssert(controlFieldNode); //controlFieldNode must have been allocated
	LOG_DEBUG(L"Created controlFieldNode: "<<controlFieldNode->getDebugInfo());
	if(addControlFieldNode(parent,previous,controlFieldNode)!=controlFieldNode) {
		LOG_DEBUG(L"Error adding control field node to buffer");
		delete controlFieldNode;
		return NULL;
	}
	return controlFieldNode;
}

VBufStorage_controlFieldNode_t*  VBufStorage_buffer_t::addControlFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_controlFieldNode_t* controlFieldNode) {
	nhAssert(!parent||this->isNodeInBuffer(parent));
	nhAssert(!previous||this->isNodeInBuffer(previous));
	LOG_DEBUG(L"Add controlFieldNode using parent at "<<parent<<L", previous at "<<previous<<L", node at "<<controlFieldNode);
	if(previous!=NULL&&previous->parent!=parent) {
		LOG_DEBUG(L"previous is not a child of parent, returning NULL");
		return NULL;
	}
	if(parent==NULL&&previous!=NULL) {
		LOG_DEBUG(L"Can not add more than one node at root level");
		return NULL;
	}
	LOG_DEBUG(L"Inserting controlFieldNode in to buffer");
	insertNode(parent, previous, controlFieldNode);
	nhAssert(controlFieldNodesByIdentifier.count(controlFieldNode->identifier)==0); //node can't be previously remembered
	controlFieldNodesByIdentifier[controlFieldNode->identifier]=controlFieldNode;
	LOG_DEBUG(L"Added new controlFieldNode, returning node");
	return controlFieldNode;
}

VBufStorage_textFieldNode_t*  VBufStorage_buffer_t::addTextFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, const std::wstring& text) {
	LOG_DEBUG(L"Add textFieldNode using parent at "<<parent<<L", previous at "<<previous);
	VBufStorage_textFieldNode_t* textFieldNode=new VBufStorage_textFieldNode_t(text);
	nhAssert(textFieldNode); //controlFieldNode must have been allocated
	LOG_DEBUG(L"Created textFieldNode: "<<textFieldNode->getDebugInfo());
	if(addTextFieldNode(parent,previous,textFieldNode)!=textFieldNode) {
		LOG_DEBUG(L"Error adding textFieldNode to buffer");
		delete textFieldNode;
		return NULL;
	}
	return textFieldNode;
}

VBufStorage_textFieldNode_t*  VBufStorage_buffer_t::addTextFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_textFieldNode_t* textFieldNode) {
	nhAssert(!parent||this->isNodeInBuffer(parent));
	nhAssert(!previous||this->isNodeInBuffer(previous));
	LOG_DEBUG(L"Add textFieldNode using parent at "<<parent<<L", previous at "<<previous<<L", node at "<<textFieldNode);
	if(previous!=NULL&&previous->parent!=parent) {
		LOG_DEBUG(L"previous is not a child of parent, returning NULL");
		return NULL;
	}
	if(parent==NULL) {
		LOG_DEBUG(L"Can not add a text field node at the root of the buffer");
		return NULL;
	}
	LOG_DEBUG(L"Inserting textFieldNode in to buffer");
	insertNode(parent, previous, textFieldNode);
	LOG_DEBUG(L"Added new textFieldNode, returning node");
	return textFieldNode;
}

bool VBufStorage_buffer_t::replaceSubtrees(const map<VBufStorage_fieldNode_t*,VBufStorage_buffer_t*>& m) {
	VBufStorage_controlFieldNode_t* parent=NULL;
	VBufStorage_fieldNode_t* previous=NULL;
	//Using the current selection start, record a list of ancestor fields by their identifier, 
	//and a relative offset of the selection start to those fields, so that the selection can be corrected after the replacement.
	list<pair<VBufStorage_controlFieldNodeIdentifier_t,int>> identifierList;
	if(this->getTextLength()>0) {
		int controlDocHandle, controlID, controlNodeStart, controlNodeEnd;
		parent=this->locateControlFieldNodeAtOffset(this->selectionStart,&controlNodeStart,&controlNodeEnd,&controlDocHandle,&controlID);
		int relativeSelectionStart=this->selectionStart-controlNodeStart;
		for(;parent!=NULL;parent=parent->parent) {
			identifierList.push_front(pair<VBufStorage_controlFieldNodeIdentifier_t,int>(parent->identifier,relativeSelectionStart));
			for(previous=parent->previous;previous!=NULL;relativeSelectionStart+=previous->length,previous=previous->previous);
		}
	}
	//For each node in the map,
		//Replace the node on this buffer, with the content of the buffer in the map for that node
		//Note that controlField info will automatically be removed, but not added again
	for(map<VBufStorage_fieldNode_t*,VBufStorage_buffer_t*>::const_iterator i=m.begin();i!=m.end();++i) {
		VBufStorage_fieldNode_t* node=i->first;
		VBufStorage_buffer_t* buffer=i->second;
		parent=node->parent;
		previous=node->previous;
		if(!this->removeFieldNode(node)) {
			LOG_DEBUG(L"Error removing node");
			return false;
		}
		this->insertNode(parent,previous,buffer->rootNode);
		buffer->rootNode=NULL;
	}
	//Update the controlField info on this buffer using all the buffers in the map
	//We do this all in one go instead of for each replacement in case there are issues with ordering
	//e.g. an identifier appears in one place before its removed in another
	for(map<VBufStorage_fieldNode_t*,VBufStorage_buffer_t*>::const_iterator i=m.begin();i!=m.end();++i) {
		VBufStorage_buffer_t* buffer=i->second;
		for(map<VBufStorage_controlFieldNodeIdentifier_t,VBufStorage_controlFieldNode_t*>::iterator j=buffer->controlFieldNodesByIdentifier.begin();j!=buffer->controlFieldNodesByIdentifier.end();++j) {
			nhAssert(this->controlFieldNodesByIdentifier.count(j->first)==0);
			this->controlFieldNodesByIdentifier.erase(j->first);
			this->controlFieldNodesByIdentifier.insert(make_pair(j->first,j->second));
		}
	}
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
				LOG_DEBUG(L"Error getting offsets for last ancestor node");
				return false;
			}
			this->selectionStart=lastAncestorStartOffset+min(lastRelativeSelectionStart,max(lastAncestorNode->length-1,0));
		}
	}
	return TRUE;
}

bool VBufStorage_buffer_t::removeFieldNode(VBufStorage_fieldNode_t* node) {
	nhAssert(this->isNodeInBuffer(node));
	LOG_DEBUG(L"Removing subtree starting at "<<node->getDebugInfo());
	if(node->length>0) {
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
		node->next->previous=node->previous;
	} else if(node->parent) {
		node->parent->lastChild=node->previous;
	}
	if(node->previous!=NULL) {
		node->previous->next=node->next;
	} else if(node->parent) {
		node->parent->firstChild=node->next;
	}
	LOG_DEBUG(L"Deleting subtree");
	deleteSubtree(node);
	if(node==this->rootNode) {
		LOG_DEBUG(L"Removing root node from buffer ");
		this->rootNode=NULL;
	}
	LOG_DEBUG(L"Removed fieldNode and descendants, returning true");
	return true;
}

bool VBufStorage_buffer_t::clearBuffer() {
	if(this->rootNode) {
		if(!this->removeFieldNode(this->rootNode)) {
			LOG_DEBUG(L"Error removing root node");
			return false;
		}
	} else {
		LOG_DEBUG(L"Buffer already empty");
	}
	return true;
}

bool VBufStorage_buffer_t::getFieldNodeOffsets(VBufStorage_fieldNode_t* node, int *startOffset, int *endOffset) {
	nhAssert(this->isNodeInBuffer(node));
	*startOffset=node->calculateOffsetInTree();
	*endOffset=(*startOffset)+node->length;
	LOG_DEBUG(L"node has offsets "<<*startOffset<<L" and "<<*endOffset<<L", returning true");
	return true;
}

bool VBufStorage_buffer_t::isFieldNodeAtOffset(VBufStorage_fieldNode_t* node, int offset) {
	nhAssert(this->isNodeInBuffer(node));
	int startOffset, endOffset;
	if(!getFieldNodeOffsets(node,&startOffset,&endOffset)) {
		LOG_DEBUG(L"Could not get offsets for node at "<<node<<L", returning false");
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
		LOG_DEBUG(L"Buffer is empty, returning NULL");
		return NULL;
	}
	int relativeOffset=0;
	VBufStorage_textFieldNode_t* node=this->rootNode->locateTextFieldNodeAtOffset(offset,&relativeOffset);
	if(node==NULL) {
		LOG_DEBUG(L"Could not locate node, returning NULL");
		return NULL;
	}
	*nodeStartOffset=offset-relativeOffset;
	*nodeEndOffset=*nodeStartOffset+node->length;
	LOG_DEBUG(L"Located node, returning node at "<<node);
	return node;
}

VBufStorage_controlFieldNode_t* VBufStorage_buffer_t::locateControlFieldNodeAtOffset(int offset, int *nodeStartOffset, int * nodeEndOffset, int *docHandle, int *ID) {
	int startOffset, endOffset;
	VBufStorage_textFieldNode_t* node=this->locateTextFieldNodeAtOffset(offset,&startOffset,&endOffset);
	if(node==NULL) {
		LOG_DEBUG(L"Could not locate node at offset, returning NULL");
		return NULL;
	}
	if(node->parent==NULL) {
		LOG_DEBUG(L"text field node has no parents, returning NULL");
		return NULL;
	}
	for(VBufStorage_fieldNode_t* previous=node->previous;previous!=NULL;previous=previous->previous) {
		startOffset-=previous->length;
	}
	endOffset=startOffset+node->parent->length;
	nhAssert(startOffset>=0&&endOffset>=startOffset); //Offsets must not be negative
	VBufStorage_controlFieldNode_t* controlFieldNode = node->parent;
	*nodeStartOffset=startOffset;
	*nodeEndOffset=endOffset;
	*docHandle=controlFieldNode->identifier.docHandle;
	*ID=controlFieldNode->identifier.ID;
	LOG_DEBUG(L"Found node, returning "<<controlFieldNode->getDebugInfo()); 
	return controlFieldNode;
	}

VBufStorage_controlFieldNode_t* VBufStorage_buffer_t::getControlFieldNodeWithIdentifier(int docHandle, int ID) {
	VBufStorage_controlFieldNodeIdentifier_t identifier(docHandle, ID);
	std::map<VBufStorage_controlFieldNodeIdentifier_t,VBufStorage_controlFieldNode_t*>::iterator i=this->controlFieldNodesByIdentifier.find(identifier);
	if(i==this->controlFieldNodesByIdentifier.end()) {
		LOG_DEBUG(L"No controlFieldNode with identifier, returning NULL");
		return false;
	}
	VBufStorage_controlFieldNode_t* node=i->second;
	nhAssert(node); //Node can not be NULL
	LOG_DEBUG(L"returning node at "<<node);
	return node;
}

bool VBufStorage_buffer_t::getIdentifierFromControlFieldNode(VBufStorage_controlFieldNode_t* node, int* docHandle, int* ID) {
	nhAssert(node);
	nhAssert(isNodeInBuffer(node));
	*docHandle=node->identifier.docHandle;
	*ID=node->identifier.ID;
	return true;
}


bool VBufStorage_buffer_t::getSelectionOffsets(int *startOffset, int *endOffset) const {
	nhAssert(this->selectionStart>=0&&this->selectionLength>=0); //Selection can't be negative
	int minStartOffset=0;
	int maxEndOffset=(this->rootNode)?this->rootNode->length:0;
	*startOffset=max(minStartOffset,this->selectionStart);
	*endOffset=min(this->selectionStart+this->selectionLength,maxEndOffset);
	LOG_DEBUG(L"Selection is "<<*startOffset<<L" and "<<*endOffset<<L", returning true");
	return true;
}

bool VBufStorage_buffer_t::setSelectionOffsets(int startOffset, int endOffset) {
	if(startOffset<0||endOffset<0||endOffset<startOffset) {
		LOG_DEBUG(L"invalid offsets of "<<startOffset<<L" and "<<endOffset<<L", returning false");
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

VBufStorage_textContainer_t*  VBufStorage_buffer_t::getTextInRange(int startOffset, int endOffset, bool useMarkup) {
	if(this->rootNode==NULL) {
		LOG_DEBUG(L"buffer is empty, returning false");
		return false;
	}
	if(startOffset<0||startOffset>=endOffset||endOffset>this->rootNode->length) {
		LOG_DEBUG(L"Bad offsets of "<<startOffset<<L" and "<<endOffset<<L", returning false");
		return false;
	}
	wstring text;
	this->rootNode->getTextInRange(startOffset,endOffset,text,useMarkup);
	LOG_DEBUG(L"Got text between offsets "<<startOffset<<L" and "<<endOffset<<L", returning true");
	return new VBufStorage_textContainer_t(text);
}

VBufStorage_fieldNode_t* VBufStorage_buffer_t::findNodeByAttributes(int offset, VBufStorage_findDirection_t direction, const std::wstring& attribsString, int *startOffset, int *endOffset) {
	if(this->rootNode==NULL) {
		LOG_DEBUG(L"buffer empty, returning NULL");
		return NULL;
	}
	if(offset>=this->rootNode->length) {
		LOG_DEBUG(L" offset "<<offset<<L" is past end of buffer, returning NULL");
		return NULL;
	}
	LOG_DEBUG(L"find node starting at offset "<<offset<<L", with attributes: "<<attribsString);
	int bufferStart, bufferEnd, tempRelativeStart=0;
	VBufStorage_fieldNode_t* node=NULL;
	if(offset==-1) {
		node=this->rootNode;
		bufferStart=0;
		bufferEnd=node->length;
	} else if(offset>=0) {
		node=this->locateTextFieldNodeAtOffset(offset,&bufferStart,&bufferEnd);
	} else {
		LOG_DEBUG(L"Invalid offset: "<<offset);
		return NULL;
	}
	if(node==NULL) {
		LOG_DEBUG(L"Could not find node at offset "<<offset<<L", returning NULL");
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
			if(node->length>0&&node->matchAttributes(attribsString)) {
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
			if(node->length>0&&node->matchAttributes(attribsString)) {
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
		} while(node!=NULL&&!node->matchAttributes(attribsString));
		LOG_DEBUG(L"end is now "<<bufferEnd);
	}
	if(node==NULL) {
		LOG_DEBUG(L"Could not find node, returning NULL");
		return NULL;
	}
	*startOffset=bufferStart;
	*endOffset=bufferEnd;
	LOG_DEBUG(L"returning node at "<<node<<L" with offsets of "<<*startOffset<<L" and "<<*endOffset);
	return node;
}

bool VBufStorage_buffer_t::getLineOffsets(int offset, int maxLineLength, bool useScreenLayout, int *startOffset, int *endOffset) {
	if(this->rootNode==NULL||offset>=this->rootNode->length) {
		LOG_DEBUG(L"Offset of "<<offset<<L" too big for buffer, returning false");
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
	nhAssert(node);
	LOG_DEBUG(L"Walking parents to top from node "<<node);
	for(;node->parent!=NULL;node=node->parent);
	LOG_DEBUG(L"Comparing node "<<node<<L" with buffer's root node "<<node);
	if(node==this->rootNode) {
		LOG_DEBUG(L"Node is in buffer");
		return true;
	}
	LOG_DEBUG(L"Node is not in buffer");
	return false;
}

std::wstring VBufStorage_buffer_t::getDebugInfo() const {
	std::wostringstream s;
	s<<L"buffer at "<<this<<L", selectionStart is "<<selectionStart<<L", selectionEnd is "<<selectionLength+selectionStart;
	return s.str();
}
