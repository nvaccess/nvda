/**
 * base/storage.cpp
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#include <iostream>
#include <fstream>
#include <cassert>
#include <string>
#include <map>
#include <set>
#include <sstream>
#include "debug.h"
#include <common/utils.h>
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

VBufStorage_fieldNode_t* VBufStorage_fieldNode_t::nextNodeByDepthFirst(bool moveBackwards, VBufStorage_fieldNode_t* limitNode, int *relativeStartOffset) {
	int relativeOffset=0;
	VBufStorage_fieldNode_t* tempNode=this;
	if(!moveBackwards) {
		DEBUG_MSG(L"moving forward");
		if(tempNode->firstChild!=NULL) {
			DEBUG_MSG(L"Moving to first child");
			tempNode=tempNode->firstChild;
		} else {
			while(tempNode!=NULL&&tempNode->next==NULL) {
				DEBUG_MSG(L"moving past parent");
				tempNode=tempNode->parent;
				if(tempNode==limitNode) tempNode=NULL;
			}
			if(tempNode==NULL||tempNode->next==NULL) {
				DEBUG_MSG(L"cannot move any further, returning NULL");
				return NULL;
			}
			DEBUG_MSG(L"Moving to next");
			relativeOffset=this->length;
			tempNode=tempNode->next;
		}
	} else {
		DEBUG_MSG(L"Moving backwards");
		if(tempNode->lastChild!=NULL) {
			DEBUG_MSG(L"Moving to last child");
			tempNode=tempNode->lastChild;
			relativeOffset=this->length-tempNode->length;
		} else {
			while(tempNode!=NULL&&tempNode->previous==NULL) {
				DEBUG_MSG(L"moving past parent");
				tempNode=tempNode->parent;
				if(tempNode==limitNode) tempNode=NULL;
			}
			if(tempNode==NULL||tempNode->previous==NULL) {
				DEBUG_MSG(L"cannot move any further, returning NULL");
				return NULL;
			}
			tempNode=tempNode->previous;
			relativeOffset-=tempNode->length;
		}
	}
	if(tempNode==limitNode) {
		DEBUG_MSG(L"passed limit node at "<<limitNode<<L", returning NULL");
		return NULL;
	}
	*relativeStartOffset=relativeOffset;
	DEBUG_MSG(L"reached node at "<<tempNode<<L", with a relative start offset of "<<relativeOffset);
	return tempNode;
}

bool VBufStorage_fieldNode_t::matchAttributes(const std::wstring& attribsString) {
	DEBUG_MSG(L"using attributes of "<<attribsString);
	multiValueAttribsMap attribsMap;
	multiValueAttribsStringToMap(attribsString,attribsMap);
	bool outerMatch=true;
	for(multiValueAttribsMap::iterator i=attribsMap.begin();i!=attribsMap.end();i++) {
		DEBUG_MSG(L"Checking for attrib "<<i->first);
		VBufStorage_attributeMap_t::iterator foundIterator=attributes.find(i->first);
		const std::wstring& foundValue=(foundIterator!=attributes.end())?foundIterator->second:L"";
		DEBUG_MSG(L"node's value for this attribute is "<<foundValue);
		multiValueAttribsMap::iterator upperBound=attribsMap.upper_bound(i->first);
		bool innerMatch=false;
		for(multiValueAttribsMap::iterator j=i;j!=upperBound;j++) { 
			DEBUG_MSG(L"Checking value "<<j->second);
			if(!innerMatch&&(j->second==foundValue)) {
				DEBUG_MSG(L"values match");
				innerMatch=true;
			}
			i=j;
		}
		outerMatch=innerMatch;
		if(!outerMatch) { 
			DEBUG_MSG(L"given attributes do not match node's attributes, returning false");
			return false;
		}
	}
	DEBUG_MSG(L"Given attributes match node's attributes, returning true");
	return true;
}

int VBufStorage_fieldNode_t::calculateOffsetInTree() const {
	int startOffset=0;
	for(VBufStorage_fieldNode_t* previous=this->previous;previous!=NULL;previous=previous->previous) {
		startOffset+=previous->length;
	}
	DEBUG_MSG(L"node has local offset of "<<startOffset);
	if(this->parent) {
		startOffset+=this->parent->calculateOffsetInTree();
	DEBUG_MSG(L"With parents offset is now "<<startOffset);
	}
	DEBUG_MSG(L"Returning node start offset of "<<startOffset);
	return startOffset;
}

VBufStorage_textFieldNode_t* VBufStorage_fieldNode_t::locateTextFieldNodeAtOffset(int offset, int *relativeOffset) {
	DEBUG_MSG(L"Searching through children to reach offset "<<offset);
	int tempOffset=0;
	assert(this->firstChild!=NULL||this->length==0); //Length of a node with out children can not be greater than 0
	for(VBufStorage_fieldNode_t* child=this->firstChild;child!=NULL;child=child->next) {
		if(offset<tempOffset+child->length) {
			DEBUG_MSG(L"found child at offset "<<tempOffset);
			VBufStorage_textFieldNode_t* textFieldNode=child->locateTextFieldNodeAtOffset(offset-tempOffset, relativeOffset);
			assert(textFieldNode); //textFieldNode can't be NULL
			return textFieldNode;
		} else {
			tempOffset+=child->length;
		}
	}
	DEBUG_MSG(L"No textFieldNode found, returning NULL");
	return NULL;
}

void VBufStorage_fieldNode_t::generateAttributesForMarkupOpeningTag(std::wstring& text) {
	wostringstream s;
	int childCount=0;
	for(VBufStorage_fieldNode_t* child=this->firstChild;child!=NULL;child=child->next) {
		childCount++;
	}
	int parentChildCount=1;
	int indexInParent=0;
	for(VBufStorage_fieldNode_t* prev=this->previous;prev!=NULL;prev=prev->previous) {
		indexInParent++;
		parentChildCount++;
	}
	for(VBufStorage_fieldNode_t* next=this->next;next!=NULL;next=next->next) {
		parentChildCount++;
	}
	s<<L"_childcount=\""<<childCount<<L"\" _indexInParent=\""<<indexInParent<<L"\" _parentChildCount=\""<<parentChildCount<<L"\" ";
	text+=s.str();
	for(VBufStorage_attributeMap_t::iterator i=this->attributes.begin();i!=this->attributes.end();i++) {
		text+=i->first;
		text+=L"=\"";
		for(std::wstring::iterator j=i->second.begin();j!=i->second.end();j++) {
			switch(*j) {
				case L'"':
				text+=L"&quot;";
				break;
				case L'<':
				text+=L"&lt;";
				break;
				case L'>':
				text+=L"&gt;";
				break;
				case L'&':
				text+=L"&amp;";
				break;
				default:
				text+=*j;
			}
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
		DEBUG_MSG(L"node has 0 length, not collecting text");
		return;
	}
	DEBUG_MSG(L"getting text between offsets "<<startOffset<<L" and "<<endOffset);
	assert(startOffset>=0); //startOffset can't be negative
	assert(startOffset<endOffset); //startOffset must be before endOffset
	assert(endOffset<=this->length); //endOffset can't be bigger than node length
	if(useMarkup) {
		this->generateMarkupOpeningTag(text);
	}
	assert(this->firstChild!=NULL||this->length==0); //Length of a node with out children can not be greater than 0
	int childStart=0;
	int childEnd=0;
	int childLength=0;
	for(VBufStorage_fieldNode_t* child=this->firstChild;child!=NULL;child=child->next) {
		childLength=child->length;
		assert(childLength>=0); //length can't be negative
		childEnd+=childLength;
		DEBUG_MSG(L"child with offsets of "<<childStart<<L" and "<<childEnd); 
		if(childEnd>startOffset&&endOffset>childStart) {
			DEBUG_MSG(L"child offsets overlap requested offsets");
			child->getTextInRange(max(startOffset,childStart)-childStart,min(endOffset-childStart,childLength),text,useMarkup);
		}
		childStart+=childLength;
		DEBUG_MSG(L"childStart is now "<<childStart);
	}
	if(useMarkup) {
		this->generateMarkupClosingTag(text);
	}
	DEBUG_MSG(L"Generated, text string is now "<<text.length());
}

void VBufStorage_fieldNode_t::disassociateFromBuffer(VBufStorage_buffer_t* buffer) {
	assert(buffer); //Buffer can't be NULL
	DEBUG_MSG(L"Disassociating fieldNode from buffer");
}

VBufStorage_fieldNode_t::VBufStorage_fieldNode_t(int lengthArg, bool isBlockArg): parent(NULL), previous(NULL), next(NULL), firstChild(NULL), lastChild(NULL), length(lengthArg), isBlock(isBlockArg), attributes() {
	DEBUG_MSG(L"field node initialization at "<<this<<L"length is "<<length);
}

VBufStorage_fieldNode_t::~VBufStorage_fieldNode_t() {
	DEBUG_MSG(L"fieldNode being destroied");
}

VBufStorage_controlFieldNode_t* VBufStorage_fieldNode_t::getParent() {
	DEBUG_MSG(L"parent at "<<parent);
	return parent;
}

VBufStorage_fieldNode_t* VBufStorage_fieldNode_t::getPrevious() {
	DEBUG_MSG(L"previous at "<<previous);
	return previous;
}

VBufStorage_fieldNode_t* VBufStorage_fieldNode_t::getNext() {
	DEBUG_MSG(L"next at "<<next);
	return next;
}

VBufStorage_fieldNode_t* VBufStorage_fieldNode_t::getFirstChild() {
	DEBUG_MSG(L"first child at "<<firstChild);
	return firstChild;
}

VBufStorage_fieldNode_t* VBufStorage_fieldNode_t::getLastChild() {
	DEBUG_MSG(L"last child at "<<lastChild);
	return lastChild;
}

bool VBufStorage_fieldNode_t::addAttribute(const std::wstring& name, const std::wstring& value) {
	DEBUG_MSG(L"Adding attribute "<<name<<L" with value "<<value);
	this->attributes[name]=value;
	return true;
}

std::wstring VBufStorage_fieldNode_t::getAttributesString() const {
	std::wstring attributesString;
	for(std::map<std::wstring,std::wstring>::const_iterator i=attributes.begin();i!=attributes.end();i++) {
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
	assert(buffer); //Must be associated with a buffer
	DEBUG_MSG(L"Disassociating controlFieldNode from buffer");
	buffer->forgetControlFieldNode(this);
	this->VBufStorage_fieldNode_t::disassociateFromBuffer(buffer);
}

VBufStorage_controlFieldNode_t::VBufStorage_controlFieldNode_t(int docHandle, int ID, bool isBlockArg): VBufStorage_fieldNode_t(0,isBlockArg), identifier(docHandle,ID) {  
	DEBUG_MSG(L"controlFieldNode initialization at "<<this<<L", with docHandle of "<<identifier.docHandle<<L" and ID of "<<identifier.ID); 
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
	assert(offset<length); //Offset must be in this node
	DEBUG_MSG(L"Node is a textField");
	*relativeOffset=offset;
	return this;
}

void VBufStorage_textFieldNode_t::generateMarkupTagName(std::wstring& text) {
	text+=L"text";
}

void VBufStorage_textFieldNode_t::getTextInRange(int startOffset, int endOffset, std::wstring& text, bool useMarkup) {
	DEBUG_MSG(L"getting text between offsets "<<startOffset<<L" and "<<endOffset);
	if(useMarkup) {
		this->generateMarkupOpeningTag(text);
	}
	assert(startOffset>=0); //StartOffset must be not negative
	assert(startOffset<endOffset); //StartOffset must be less than endOffset
	assert(endOffset<=this->length); //endOffset can't be greater than node length
	if(useMarkup) {
		wchar_t c;
		for(int offset=startOffset;offset<endOffset;offset++) {
			c=this->text[offset];
			switch(c) {
				case L'"':
				text+=L"&quot;";
				break;
				case L'<':
				text+=L"&lt;";
				break;
				case L'>':
				text+=L"&gt;";
				break;
				case L'&':
				text+=L"&amp;";
				break;
				default:
				if (c == 0x9 || c == 0xA || c == 0xD
					|| (c >= 0x20 && c <= 0xD7FF) || (c >= 0xE000 && c <= 0xFFFD)
				) {
					// Valid XML character.
					text+=c;
				} else {
					// Invalid XML character.
					text += 0xfffd; // Unicode replacement character
				}
			}
		}
	} else {
		text.append(this->text,startOffset,endOffset-startOffset);
	}
	if(useMarkup) {
		this->generateMarkupClosingTag(text);
	}
	DEBUG_MSG(L"generated, text string is now of length "<<text.length());
}

VBufStorage_textFieldNode_t::VBufStorage_textFieldNode_t(const std::wstring& textArg): VBufStorage_fieldNode_t(textArg.length(),false), text(textArg) {
	DEBUG_MSG(L"textFieldNode initialization, with text of length "<<length);
}

std::wstring VBufStorage_textFieldNode_t::getDebugInfo() const {
	std::wostringstream s;
	s<<L"text "<<this->VBufStorage_fieldNode_t::getDebugInfo();
	return s.str();
}

//buffer implementation

void VBufStorage_buffer_t::forgetControlFieldNode(VBufStorage_controlFieldNode_t* node) {
	assert(node); //Node can't be NULL
	assert(this->controlFieldNodesByIdentifier.count(node->identifier)==1); //Node must exist in the set
	assert(this->controlFieldNodesByIdentifier[node->identifier]==node); //Remembered node and this node must be equal
	this->controlFieldNodesByIdentifier.erase(node->identifier);
	DEBUG_MSG(L"Forgot controlFieldNode with docHandle "<<node->identifier.docHandle<<L" and ID "<<node->identifier.ID);
}

void VBufStorage_buffer_t::insertNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_fieldNode_t* node) {
	VBufStorage_fieldNode_t* next=NULL;
	assert(node); //node can't be NULL
	assert(previous==NULL||previous!=this->rootNode); //a root node can not have nodes after it on the same level
	//make sure we have a good parent, previous and next
	if(previous!=NULL) parent=previous->parent;
	next=(previous?previous->next:(parent?parent->firstChild:NULL));
	DEBUG_MSG(L"using parent: "<<(parent?parent->getDebugInfo():L"NULL"));
	DEBUG_MSG(L"Using previous: "<<(previous?previous->getDebugInfo():L"NULL"));
	DEBUG_MSG(L"Using next: "<<(next?next->getDebugInfo():L"NULL"));
	if(parent==NULL) {
		assert(this->rootNode==NULL); //A buffer can only have one root node.
		DEBUG_MSG(L"making node root node of buffer");
		this->rootNode=node;
	} else { 
		if(previous==NULL) {
			DEBUG_MSG(L"Making node first child of parent");
			parent->firstChild=node;
		}
		if(next==NULL) {
			DEBUG_MSG(L"Making node last child of parent");
			parent->lastChild=node;
		}
	}
	if(previous) {
		DEBUG_MSG(L"Making node previous's next");
		previous->next=node;
	}
	if(next) {
		DEBUG_MSG(L"Making node next's previous");
		next->previous=node;
	}
	DEBUG_MSG(L"setting node's parent, previous and next");
	node->parent=parent;
	node->previous=previous;
	node->next=next;
	if(node->length>0) {
		DEBUG_MSG(L"Widening ancestors by "<<node->length);
		for(VBufStorage_fieldNode_t* ancestor=node->parent;ancestor!=NULL;ancestor=ancestor->parent) {
			DEBUG_MSG(L"Ancestor: "<<ancestor->getDebugInfo());
			ancestor->length+=node->length;
			assert(ancestor->length>=0); //length must never be negative
			DEBUG_MSG(L"Ancestor length now"<<ancestor->length);
		}
	}
	DEBUG_MSG(L"Inserted subtree");
}

void VBufStorage_buffer_t::deleteSubtree(VBufStorage_fieldNode_t* node) {
	assert(node); //node can't be null
	DEBUG_MSG(L"deleting subtree starting at "<<node->getDebugInfo());
	//Save off next before deleting the subtree 
	for(VBufStorage_fieldNode_t* child=node->firstChild;child!=NULL;) {
		VBufStorage_fieldNode_t* next=child->next;
		deleteSubtree(child);
		child=next;
	}
	node->disassociateFromBuffer(this);
	DEBUG_MSG(L"deleting node at "<<node);
	delete node;
	DEBUG_MSG(L"Deleted subtree");
}

VBufStorage_buffer_t::VBufStorage_buffer_t(): rootNode(NULL), controlFieldNodesByIdentifier(), selectionStart(0), selectionEnd(0), lock() {
	DEBUG_MSG(L"buffer initializing");
}

VBufStorage_buffer_t::~VBufStorage_buffer_t() {
	DEBUG_MSG(L"buffer being destroied");
	if(this->rootNode) {
		this->removeFieldNode(this->rootNode);
	}
}

VBufStorage_controlFieldNode_t*  VBufStorage_buffer_t::addControlFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, int docHandle, int ID, bool isBlock) {
	DEBUG_MSG(L"Add controlFieldNode using parent at "<<parent<<L", previous at "<<previous<<L", docHandle of "<<docHandle<<L", ID of "<<ID);
	if(previous!=NULL&&previous->parent!=parent) {
		DEBUG_MSG(L"previous is not a child of parent, returning NULL");
		return NULL;
	}
	if(parent==NULL&&previous!=NULL) {
		DEBUG_MSG(L"Can not add more than one node at root level");
		return NULL;
	}
	VBufStorage_controlFieldNode_t* controlFieldNode=new VBufStorage_controlFieldNode_t(docHandle,ID,isBlock);
	assert(controlFieldNode); //controlFieldNode must have been allocated
	DEBUG_MSG(L"Created controlFieldNode: "<<controlFieldNode->getDebugInfo());
	DEBUG_MSG(L"Inserting controlFieldNode in to buffer");
	insertNode(parent, previous, controlFieldNode);
	assert(controlFieldNodesByIdentifier.count(controlFieldNode->identifier)==0); //node can't be previously remembered
	controlFieldNodesByIdentifier[controlFieldNode->identifier]=controlFieldNode;
	DEBUG_MSG(L"Added new controlFieldNode, returning node");
	return controlFieldNode;
}

VBufStorage_textFieldNode_t*  VBufStorage_buffer_t::addTextFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, const std::wstring& text) {
	DEBUG_MSG(L"Add textFieldNode using parent at "<<parent<<L", previous at "<<previous);
	if(previous!=NULL&&previous->parent!=parent) {
		DEBUG_MSG(L"previous is not a child of parent, returning NULL");
		return NULL;
	}
	if(parent==NULL) {
		DEBUG_MSG(L"Can not add a text field node at the root of the buffer");
		return NULL;
	}
	VBufStorage_textFieldNode_t* textFieldNode=new VBufStorage_textFieldNode_t(text);
	assert(textFieldNode); //controlFieldNode must have been allocated
	DEBUG_MSG(L"Created textFieldNode: "<<textFieldNode->getDebugInfo());
	DEBUG_MSG(L"Inserting textFieldNode in to buffer");
	insertNode(parent, previous, textFieldNode);
	DEBUG_MSG(L"Added new textFieldNode, returning node");
	return textFieldNode;
}

bool VBufStorage_buffer_t::mergeBuffer(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_buffer_t* buffer) {
	assert(buffer); //Buffer can't be NULL
	assert(buffer!=this); //cannot merge a buffer into itself
	DEBUG_MSG(L"Merging buffer at "<<buffer<<L" in to this buffer with parent at "<<parent<<L" and previous at "<<previous);
	if(buffer->rootNode) {
		DEBUG_MSG(L"Inserting nodes from buffer");
		insertNode(parent,previous,buffer->rootNode);
		controlFieldNodesByIdentifier.insert(buffer->controlFieldNodesByIdentifier.begin(),buffer->controlFieldNodesByIdentifier.end());
		buffer->controlFieldNodesByIdentifier.clear();
		buffer->rootNode=NULL;
	} else {
		DEBUG_MSG(L"Buffer empty");
	}
	DEBUG_MSG(L"mergeBuffer complete");
	return true;
}

bool VBufStorage_buffer_t::removeFieldNode(VBufStorage_fieldNode_t* node) {
	DEBUG_MSG(L"Removing subtree starting at "<<node->getDebugInfo());
	if(node->length>0) {
		DEBUG_MSG(L"collapsing length of ancestors by "<<node->length);
		for(VBufStorage_fieldNode_t* ancestor=node->parent;ancestor!=NULL;ancestor=ancestor->parent) {
			DEBUG_MSG(L"Ancestor: "<<ancestor->getDebugInfo());
			ancestor->length-=node->length;
			assert(ancestor->length>=0); //ancestor length can't be negative
			DEBUG_MSG(L"Ancestor length now"<<ancestor->length);
		}
	}
	DEBUG_MSG(L"Disconnecting node from its siblings and or parent");
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
	DEBUG_MSG(L"Deleting subtree");
	deleteSubtree(node);
	if(node==this->rootNode) {
		DEBUG_MSG(L"Removing root node from buffer ");
		this->rootNode=NULL;
	}
	DEBUG_MSG(L"Removed fieldNode and descendants, returning true");
	return true;
}

bool VBufStorage_buffer_t::getFieldNodeOffsets(VBufStorage_fieldNode_t* node, int *startOffset, int *endOffset) {
	*startOffset=node->calculateOffsetInTree();
	*endOffset=(*startOffset)+node->length;
	DEBUG_MSG(L"node has offsets "<<*startOffset<<L" and "<<*endOffset<<L", returning true");
	return true;
}

bool VBufStorage_buffer_t::isFieldNodeAtOffset(VBufStorage_fieldNode_t* node, int offset) {
	int startOffset, endOffset;
	if(!getFieldNodeOffsets(node,&startOffset,&endOffset)) {
		DEBUG_MSG(L"Could not get offsets for node at "<<node<<L", returning false");
		return false;
	}
	if(offset<startOffset||offset>=endOffset) {
		DEBUG_MSG(L"node is not at offset, returning false");
		return false;
	}
	DEBUG_MSG(L"Node is at offset "<<offset<<L", returning true");
	return true;
}

VBufStorage_textFieldNode_t* VBufStorage_buffer_t::locateTextFieldNodeAtOffset(int offset, int *nodeStartOffset, int *nodeEndOffset) {
	if(this->rootNode==NULL) {
		DEBUG_MSG(L"Buffer is empty, returning NULL");
		return NULL;
	}
	int relativeOffset=0;
	VBufStorage_textFieldNode_t* node=this->rootNode->locateTextFieldNodeAtOffset(offset,&relativeOffset);
	if(node==NULL) {
		DEBUG_MSG(L"Could not locate node, returning NULL");
		return NULL;
	}
	*nodeStartOffset=offset-relativeOffset;
	*nodeEndOffset=*nodeStartOffset+node->length;
	DEBUG_MSG(L"Located node, returning node at "<<node);
	return node;
}

VBufStorage_controlFieldNode_t* VBufStorage_buffer_t::locateControlFieldNodeAtOffset(int offset, int *nodeStartOffset, int * nodeEndOffset, int *docHandle, int *ID) {
	int startOffset, endOffset;
	VBufStorage_textFieldNode_t* node=this->locateTextFieldNodeAtOffset(offset,&startOffset,&endOffset);
	if(node==NULL) {
		DEBUG_MSG(L"Could not locate node at offset, returning NULL");
		return NULL;
	}
	if(node->parent==NULL) {
		DEBUG_MSG(L"text field node has no parents, returning NULL");
		return NULL;
	}
	for(VBufStorage_fieldNode_t* previous=node->previous;previous!=NULL;previous=previous->previous) {
		startOffset-=previous->length;
	}
	endOffset=startOffset+node->parent->length;
	assert(startOffset>=0&&endOffset>=startOffset); //Offsets must not be negative
	VBufStorage_controlFieldNode_t* controlFieldNode = node->parent;
	*nodeStartOffset=startOffset;
	*nodeEndOffset=endOffset;
	*docHandle=controlFieldNode->identifier.docHandle;
	*ID=controlFieldNode->identifier.ID;
	DEBUG_MSG(L"Found node, returning "<<controlFieldNode->getDebugInfo()); 
	return controlFieldNode;
	}

VBufStorage_controlFieldNode_t* VBufStorage_buffer_t::getControlFieldNodeWithIdentifier(int docHandle, int ID) {
	VBufStorage_controlFieldNodeIdentifier_t identifier(docHandle, ID);
	std::map<VBufStorage_controlFieldNodeIdentifier_t,VBufStorage_controlFieldNode_t*>::iterator i=this->controlFieldNodesByIdentifier.find(identifier);
	if(i==this->controlFieldNodesByIdentifier.end()) {
		DEBUG_MSG(L"No controlFieldNode with identifier, returning NULL");
		return false;
	}
	VBufStorage_controlFieldNode_t* node=i->second;
	assert(node); //Node can not be NULL
	DEBUG_MSG(L"returning node at "<<node);
	return node;
}

bool VBufStorage_buffer_t::getSelectionOffsets(int *startOffset, int *endOffset) const {
	assert(this->selectionStart>=0&&this->selectionEnd>=0); //Selection can't be negative
	int minStartOffset=0;
	int maxEndOffset=(this->rootNode)?this->rootNode->length:0;
	*startOffset=max(minStartOffset,this->selectionStart);
	*endOffset=min(this->selectionEnd,maxEndOffset);
	DEBUG_MSG(L"Selection is "<<*startOffset<<L" and "<<*endOffset<<L", returning true");
	return true;
}

bool VBufStorage_buffer_t::setSelectionOffsets(int startOffset, int endOffset) {
	if(startOffset<0||endOffset<0||endOffset<startOffset) {
		DEBUG_MSG(L"invalid offsets of "<<startOffset<<L" and "<<endOffset<<L", returning false");
		return false;
	}
	this->selectionStart=startOffset;
	this->selectionEnd=endOffset;
	DEBUG_MSG(L"Selection set to "<<startOffset<<L" and "<<endOffset<<L", returning true");
	return true;
}

int VBufStorage_buffer_t::getTextLength() const {
	int length=(this->rootNode)?this->rootNode->length:0;
	DEBUG_MSG(L"Returning length of "<<length);
	return length;
}

bool VBufStorage_buffer_t::getTextInRange(int startOffset, int endOffset, std::wstring& text, bool useMarkup) {
	if(this->rootNode==NULL) {
		DEBUG_MSG(L"buffer is empty, returning false");
		return false;
	}
	if(startOffset<0||startOffset>=endOffset||endOffset>this->rootNode->length) {
		DEBUG_MSG(L"Bad offsets of "<<startOffset<<L" and "<<endOffset<<L", returning false");
		return false;
	}
	this->rootNode->getTextInRange(startOffset,endOffset,text,useMarkup);
	DEBUG_MSG(L"Got text between offsets "<<startOffset<<L" and "<<endOffset<<L", returning true");
	return true;
}

VBufStorage_fieldNode_t* VBufStorage_buffer_t::findNodeByAttributes(int offset, VBufStorage_findDirection_t direction, const std::wstring& attribsString, int *startOffset, int *endOffset) {
	if(this->rootNode==NULL) {
		DEBUG_MSG(L"buffer empty, returning NULL");
		return NULL;
	}
	if(offset>=this->rootNode->length) {
		DEBUG_MSG(L" offset "<<offset<<L" is past end of buffer, returning NULL");
		return NULL;
	}
	DEBUG_MSG(L"find node starting at offset "<<offset<<L", with attributes: "<<attribsString);
	int bufferStart, bufferEnd, tempRelativeStart=0;
	VBufStorage_fieldNode_t* node=NULL;
	if(offset==-1) {
		node=this->rootNode;
		bufferStart=0;
		bufferEnd=node->length;
	} else if(offset>=0) {
		node=this->locateTextFieldNodeAtOffset(offset,&bufferStart,&bufferEnd);
	} else {
		DEBUG_MSG(L"Invalid offset: "<<offset);
		return NULL;
	}
	if(node==NULL) {
		DEBUG_MSG(L"Could not find node at offset "<<offset<<L", returning NULL");
		return NULL;
	}
	DEBUG_MSG(L"starting from node "<<node->getDebugInfo());
	DEBUG_MSG(L"initial start is "<<bufferStart<<L" and initial end is "<<bufferEnd);
	if(direction==VBufStorage_findDirection_forward) {
		DEBUG_MSG(L"searching forward");
		for(node=node->nextNodeByDepthFirst(false,NULL,&tempRelativeStart);node!=NULL;node=node->nextNodeByDepthFirst(false,NULL,&tempRelativeStart)) {
			bufferStart+=tempRelativeStart;
			bufferEnd=bufferStart+node->length;
			DEBUG_MSG(L"start is now "<<bufferStart<<L" and end is now "<<bufferEnd);
			DEBUG_MSG(L"Checking node "<<node->getDebugInfo());
			if(node->length>0&&node->matchAttributes(attribsString)) {
				DEBUG_MSG(L"found a match");
				break;
			}
		}
	} else if(direction==VBufStorage_findDirection_back) {
		DEBUG_MSG(L"searching back");
		for(node=node->nextNodeByDepthFirst(true,NULL,&tempRelativeStart);node!=NULL;node=node->nextNodeByDepthFirst(true,NULL,&tempRelativeStart)) {
			bufferStart+=tempRelativeStart;
			bufferEnd=bufferStart+node->length;
			DEBUG_MSG(L"start is now "<<bufferStart<<L" and end is now "<<bufferEnd);
			if(node->length>0&&node->matchAttributes(attribsString)) {
				DEBUG_MSG(L"found match");
				break;
			}
		}
	} else if(direction==VBufStorage_findDirection_up) {
		DEBUG_MSG(L"searching up");
		do {
			for(;node->previous!=NULL;node=node->previous,bufferStart-=node->length);
			DEBUG_MSG(L"start is now "<<bufferStart);
			node=node->parent;
			if(node) {
				bufferEnd=bufferStart+node->length;
			}
		} while(node!=NULL&&!node->matchAttributes(attribsString));
		DEBUG_MSG(L"end is now "<<bufferEnd);
	}
	if(node==NULL) {
		DEBUG_MSG(L"Could not find node, returning NULL");
		return NULL;
	}
	*startOffset=bufferStart;
	*endOffset=bufferEnd;
	DEBUG_MSG(L"returning node at "<<node<<L" with offsets of "<<*startOffset<<L" and "<<*endOffset);
	return node;
}

bool VBufStorage_buffer_t::getLineOffsets(int offset, int maxLineLength, bool useScreenLayout, int *startOffset, int *endOffset) {
	if(this->rootNode==NULL||offset>=this->rootNode->length) {
		DEBUG_MSG(L"Offset of "<<offset<<L" too big for buffer, returning false");
		return false;
	}
	DEBUG_MSG(L"Calculating line offsets, using offset "<<offset<<L", with max line length of "<<maxLineLength<<L", useing screen layout "<<useScreenLayout);
	int initBufferStart, initBufferEnd;
	VBufStorage_fieldNode_t* initNode=locateTextFieldNodeAtOffset(offset,&initBufferStart,&initBufferEnd);
	DEBUG_MSG(L"Starting at node "<<initNode->getDebugInfo());
	std::set<int> possibleBreaks;
	//Find the node at which to limit the search for line endings.
	VBufStorage_fieldNode_t* limitNode=NULL;
	if(useScreenLayout) {
		for(limitNode=initNode->parent;limitNode!=NULL&&!limitNode->isBlock;limitNode=limitNode->parent);
	} else {
		limitNode=initNode->parent;
	}
	DEBUG_MSG(L"limit node is "<<limitNode->getDebugInfo());
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
			for (int i = relative; i < node->length; i++) {
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
		node = node->nextNodeByDepthFirst(false,limitNode,&tempRelativeStart);
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
		node = node->nextNodeByDepthFirst(true,limitNode,&tempRelativeStart);
		//If not using screen layout, make sure not to pass in to another control field node
		if(node&&((!useScreenLayout&&node->firstChild)||node->isBlock)) {
			node=NULL;
		}
		if(node) {
			bufferStart+=tempRelativeStart;
			bufferEnd=bufferStart+node->length;
			relative = node->length;
		}
	} while (node);
	DEBUG_MSG(L"line offsets after searching back and forth for line feeds and block edges is "<<lineStart<<L" and "<<lineEnd);
	//Finally take maxLineLength in to account
	if(maxLineLength>0) {
		set<int> realBreaks;
		realBreaks.insert(lineStart);
		realBreaks.insert(lineEnd);
		for(int i=lineStart,lineCharCounter=0;i<lineEnd;i++,lineCharCounter++) {
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
		DEBUG_MSG(L"limits after fixing for maxLineLength %: start "<<lineStart<<L" end "<<lineEnd);
	}
	*startOffset=lineStart;
	*endOffset=lineEnd;
	DEBUG_MSG(L"Successfully calculated Line offsets of "<<lineStart<<L", "<<lineEnd<<L", returning true");
	return true;
}

bool VBufStorage_buffer_t::hasContent() {
	return (this->rootNode)?true:false;
}

bool VBufStorage_buffer_t::isDescendantNode(VBufStorage_fieldNode_t* parent, VBufStorage_fieldNode_t* descendant) {
	assert(parent);
	assert(descendant);
	DEBUG_MSG(L"is node at "<<descendant<<L" a descendant of node at "<<parent);
	for(VBufStorage_fieldNode_t* tempNode=descendant->parent;tempNode!=NULL;tempNode=tempNode->parent) {
		if(tempNode==parent) {
			DEBUG_MSG(L"Node is a descendant");
			return true;
		}
	}
	DEBUG_MSG(L"Not a descendant");
	return false;
}
 
std::wstring VBufStorage_buffer_t::getDebugInfo() const {
	std::wostringstream s;
	s<<L"buffer at "<<this<<L", selectionStart is "<<selectionStart<<L", selectionEnd is "<<selectionEnd;
	return s.str();
}
