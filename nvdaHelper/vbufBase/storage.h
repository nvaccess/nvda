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

#ifndef VIRTUALBUFFER_STORAGE_H
#define VIRTUALBUFFER_STORAGE_H

#include <string>
#include <map>
#include <set>
#include <list>
#include <vector>
#include <regex>

/**
 * values to indicate a direction for searching
 */
typedef enum {
	VBufStorage_findDirection_forward,
	VBufStorage_findDirection_back,
	VBufStorage_findDirection_up
} VBufStorage_findDirection_t;

/**
 * values defining the direction to walk a tree
 */
typedef enum {
	TREEDIRECTION_FORWARD,
	TREEDIRECTION_BACK,
	TREEDIRECTION_SYMMETRICAL_BACK
} TreeDirection;

class VBufStorage_textContainer_t: protected std::wstring {
	protected:
	~VBufStorage_textContainer_t();

	public:
	VBufStorage_textContainer_t(std::wstring str);
	virtual const std::wstring& getString();
	virtual void destroy();

};

class VBufStorage_buffer_t;
class VBufStorage_fieldNode_t;
class VBufStorage_controlFieldNode_t;
class VBufStorage_textFieldNode_t;
class VBufStorage_controlFieldNodeIdentifier_t;

typedef std::list<std::pair<VBufStorage_controlFieldNodeIdentifier_t,int>> VBufStorage_relativeSelection_t;

/**
 * a list of control field nodes.
 */
typedef std::list<VBufStorage_controlFieldNode_t*> VBufStorage_controlFieldNodeList_t; 

/** 
 * Holds values that can together uniquely identify a control field in a buffer. 
 * It can also be compaired with others of its type as being less, greater, equal, or not equal, based on its values.
 */
class VBufStorage_controlFieldNodeIdentifier_t {
	public:

/**
 * a value which uniquely identifies the window or document this control is in.
 */
	const int docHandle;

/**
 * A value which uniquely identifies the control, relative to a window or document.
 */
	const int ID;

/**
 * constructor.
 * @param docHandle the value you wish for the C{docHandle} member.
 * @param ID the value you wish for the C{ID} member.
 */ 
	VBufStorage_controlFieldNodeIdentifier_t(int docHandle=0, int ID=0);

	bool operator<(const VBufStorage_controlFieldNodeIdentifier_t&) const;
	bool operator!=(const VBufStorage_controlFieldNodeIdentifier_t&) const;
	bool operator==(const VBufStorage_controlFieldNodeIdentifier_t&) const;

};

/**
 * A type  for a map that can hold a set of name,value attributes.
 */
typedef std::map<std::wstring,std::wstring> VBufStorage_attributeMap_t;

/**
 * a node that represents a field in a buffer.
 * Nodes have relationships with other nodes (giving the ability to form a tree structure), they have a length in characters (how many characters they span in the buffer), and they can hold name value attribute paires. Their constructor is protected and their only friend is a buffer, thus they can only be created by a buffer. 
 */
class VBufStorage_fieldNode_t {
	protected:

/**
 * points to this node's parent control field node.
 * it is garenteed that this node will be one of the parent's children (firstChild [next next...] or lastChild [previous previous...]).
 */
	VBufStorage_controlFieldNode_t* parent;

/**
 * points to the node directly before this node that shares the same parent as this node. 
 */
	VBufStorage_fieldNode_t* previous;

/**
 * points to the node directly after this node that shares the same parent as this node.
 */
	VBufStorage_fieldNode_t* next;

/**
 * points to this node's first child. 
 * The child will have no previous node, and it will have this node as its parent.
 */
	VBufStorage_fieldNode_t* firstChild;

/**
 * points to this node's last child.
 * the child will have no next node, and it will have this node as its parent.
 */
	VBufStorage_fieldNode_t* lastChild;

/**
 * The length of this node in characters.
 * represents the amount of characters this node spans in its buffer. Node lengths could be used together to calculate an actual character offset for a particular node in a buffer.
 */
	int length;

/**
 * a map to hold attributes for this field.
 */
	VBufStorage_attributeMap_t attributes;

/**
 * moves to the next node, in depth-first order.
* @param direction the direction to walk
 * @param limitNode the node which can not be passed
 * @param relativeStartOffset memory to place the start offset of the next node relative to the start offset of the original node
 * @return the next node.
 */
	VBufStorage_fieldNode_t* nextNodeInTree(int direction, VBufStorage_fieldNode_t* limitNode, int *relativeStartOffset);

/**
 * Calculates the offset for this node relative to the surrounding tree. 
 * @return the offset of the node.
 */
	int calculateOffsetInTree() const;

/**
 * Locates the descendant textFieldNode that is positioned at the given offset in this node.
 * @param offset the offset with in this node.
 * @param relativeOffset memory where the   offset relative to the  found node can be placed
 * @return the descendant textFieldNode at that offset, or NULL if none there.
 */ 
	virtual VBufStorage_textFieldNode_t*locateTextFieldNodeAtOffset(int offset, int *relativeOffset);

/**
 * generates this field's markup tag name
 * @param text where to place the generated name
 */
	virtual void generateMarkupTagName(std::wstring& text)=0;

/**
 * Generates the attributes within a markup opening tag.
 * @param text where to place the generated text
 * @param the offset within the node where text is being requested from 
 * @param the offset within the node the text is being requested to. 
 */
	virtual void generateAttributesForMarkupOpeningTag(std::wstring& text, int startOffset, int endOffset);

/**
 * generates a markup opening tag for this field.
 * @param text a string to append the tag to.
 * @param the offset within the node where text is being requested from 
 * @param the offset within the node the text is being requested to. 
 */
	 void generateMarkupOpeningTag(std::wstring& text,int startOffset, int endOffset);

/**
 * generates a markup closing tag for this field.
 * @param text a string to append the tag to.
 */
	void generateMarkupClosingTag(std::wstring& text);

/**
 * Disassociates this node from its buffer.
 * @param buffer the buffer to disassociate from
 */
	virtual void disassociateFromBuffer(VBufStorage_buffer_t* buffer);

/**
 * constructor.
 * @param length the length in characters this node should be, usually left as  its default.
 * @param isBlock true if this node should be a block element, false otherwise
 */
	VBufStorage_fieldNode_t(int length, bool isBlock);

/**
 * destructor
 */
	virtual ~VBufStorage_fieldNode_t();

	friend class VBufStorage_buffer_t;

	public:

/**
 * true if this field should cause a line break at its start and end when a buffer is calculating lines.
 */
	bool isBlock;

	/**
 * work out if the attributes in the given string exist on this node.
 * @param attribsString the string containing the attributes, each attribute can have multiple values to match on.
  * @return true if the attributes exist, false otherwize.
 */
	bool matchAttributes(const std::vector<std::wstring>& attribs, const std::wregex& regexp);

	/**
	* True if this node his hidden - searches will not locate this node.
	*/
	bool isHidden;

/**
 * points to this node's parent control field node.
 * it is garenteed that this node will be one of the parent's children (firstChild [next next...] or lastChild [previous previous...]).
 */
	inline VBufStorage_controlFieldNode_t* getParent() { return this->parent; }

/**
 * points to the node directly before this node that shares the same parent as this node. 
 */
	inline VBufStorage_fieldNode_t* getPrevious() { return this->previous; }

/**
 * points to the node directly after this node that shares the same parent as this node.
 */
	inline VBufStorage_fieldNode_t* getNext() { return this->next; }


/**
 * points to this node's first child. 
 * The child will have no previous node, and it will have this node as its parent.
 */
	inline VBufStorage_fieldNode_t* getFirstChild() { return this->firstChild; }

/**
 * points to this node's last child.
 * the child will have no next node, and it will have this node as its parent.
 */
	inline VBufStorage_fieldNode_t* getLastChild() { return this->lastChild; }

/**
 * Adds an attribute to this field.
 * @param name the name of the attribute
 * @param value the value of the attribute.
 * @return true if the attribute was added, false if there was an error.
 */
	bool addAttribute(const std::wstring& name, const std::wstring& value);

/**
 * @return a string of all the attributes in this field, format of name:value pares separated by a semi colon.
 */
	std::wstring getAttributesString() const;

/**
 * fetches the text between given offsets in this node and its descendants, with optional markup.
 * @param startOffset the offset to start from.
 * @param endOffset the offset to end at. Use -1 to mean node's end offset. 
 * @param text a string in whish to append the text.
 * @param useMarkup if true then markup indicating opening and closing of fields will be included.
 * @param filter: a function that takes the current recursive node and returns true if text should be fetched and false if it should be skipped.
 * @return true if successfull, false otherwize.
 */ 
	virtual void getTextInRange(int startOffset, int endOffset, std::wstring& text, bool useMarkup=false,bool(*filter)(VBufStorage_fieldNode_t*)=NULL);

/**
 * @return a string providing information about this node's type, and its state.
 */
	virtual std::wstring getDebugInfo() const;

/**
 * Retreave the length of this node.
 */
	inline int getLength() { return this->length; }

};

/**
 * a a field node that represents a control in a buffer.
 * Control fields contain other control fields or text fields, they can also be uniquely identified.
 */
class VBufStorage_controlFieldNode_t : public VBufStorage_fieldNode_t {
	protected:

	virtual void generateMarkupTagName(std::wstring& text);

	virtual void generateAttributesForMarkupOpeningTag(std::wstring& text, int startOffset, int endOffset);

	virtual void disassociateFromBuffer(VBufStorage_buffer_t* buffer);

/**
 * constructor.
 * @param docHandle the docHandle of the control
 * @param ID the ID of the control
 * @param isBlock lines lines should always break at the start and end of this control in a buffer.
 */
	VBufStorage_controlFieldNode_t(int docHandle, int ID, bool isBlock);

	friend class VBufStorage_buffer_t;

/**
 * uniquely identifies this control in its buffer.
 */
	VBufStorage_controlFieldNodeIdentifier_t identifier;

	public:

/**
 * If true, When this node is invalidated in a backend, its parent will be invalidated instead. 
 * Parent invalidation is also recursive, so that if the parent node sets this variable to true, then the first ancestor that does not set this to true is used for invalidation. 
 * An example where this might be set is on parts of a table where it is necessary for the table itself to be re-rendered if any part changes.
 */
	bool requiresParentUpdate {false};

/**
 * If true, this node is allowing itself to be reused within a subtree that is being re-rendered. 
 * This is true by default, but may be set to false if this node or a descendant needs to be re-rendered but its requiresParentUpdate is true.
 * In that case, the re-render will happen higher up in the ancestors, but ensures that this node is not reused. 
 */
	bool allowReuseInAncestorUpdate {true};

/**
 * If True, this node cannot be moved and reused within a subtree being re-rendered, if its previous siblings have changed in anyway.
 * An example might be where a table is re-rendered and a new row is added in the middle. 
 * In this case, all rows and cells after the new row must not be reused as their table coordinates would have changed.
 */
	bool denyReuseIfPreviousSiblingsChanged {false};

/**
 * If true, this node's children will always be re-rendered along with this node when being re-rendered.
 * For example: a table row might set this to ensure that if it is re-rendered, all its cells are as well.
 */
	bool alwaysRerenderChildren {false};

/**
 * If true, all this node's descendants will always be re-rendered along with this node when being re-rendered.
 */
	bool alwaysRerenderDescendants {false};

/**
 * retreaves the node's doc handle and ID.
  * @param docHandle a memory location in which the doc handle will be placed.
 * @param ID the memory location in which the ID will be placed.
 */
	bool getIdentifier(int* docHandle, int* ID);

	virtual std::wstring getDebugInfo() const;

};

/**
 * a node that represents a field of text in a buffer.
 * It holds the actual text it represents, and also sets its length accordingly. 
 */
class VBufStorage_textFieldNode_t : public VBufStorage_fieldNode_t {
	protected:

	virtual VBufStorage_textFieldNode_t*locateTextFieldNodeAtOffset(int offset, int *relativeOffset);

	virtual void generateMarkupTagName(std::wstring& text);

	virtual void getTextInRange(int startOffset, int endOffset, std::wstring& text, bool useMarkup=false,bool(*filter)(VBufStorage_fieldNode_t*)=NULL);

/**
 * constructor.
 * @param text the text this field should contain.
 */
	VBufStorage_textFieldNode_t(const std::wstring& text);

	friend class VBufStorage_buffer_t;

	public:

	/**
 * The text this field contains.
 */
	const std::wstring text;

	virtual std::wstring getDebugInfo() const;

};

/**
 * A node that references another fieldNode.
 * When rendering a subtree in a temporary buffer to update existing content,
 * This node class is used to indicate where an existing node should be reused.
 */
class VBufStorage_referenceNode_t: public VBufStorage_controlFieldNode_t {
	public:
	VBufStorage_controlFieldNode_t* referenceNode;
	VBufStorage_referenceNode_t(int docHandle, int ID, VBufStorage_controlFieldNode_t* r): VBufStorage_controlFieldNode_t(docHandle,ID,false), referenceNode(r) {};
	void generateMarkupTagName(std::wstring& text) { text.append(L"reference"); }; 
};

/**
 * a buffer that can store text with overlaying fields.
 * it stores the text and fields in an internal tree of nodes.
 */ 
class VBufStorage_buffer_t {
	protected:

/**
 * Holds all the reference nodes for this buffer.
 */
	std::list<VBufStorage_referenceNode_t*> referenceNodes;

/**
 * Unlinks this node from its parent and siblings.
 * Note that this does not actually delete the node, nore unregister it from the buffer in any other way.
 * This is used internally by removeFieldNode and replaceSubtrees.
 * @param node the node to unlink
 * @param removeDescendants if true then its simblings will be appropriately linked to close the gab, but if false, this node's children will be reparented on this node's parent, linking with this node's siblings.
 */
	bool unlinkFieldNode(VBufStorage_fieldNode_t* node, bool removeDescendants=true);

/**
 * points to the first node in the tree of nodes.
 */
	VBufStorage_fieldNode_t* rootNode;

/**
 * Holds pointers to all nodes in the buffer
 */
	std::set<VBufStorage_fieldNode_t*> nodes;

/**
 * holds pointers to all control field nodes in this buffer, searchable by  the control's unique identifier.
 */
	std::map<VBufStorage_controlFieldNodeIdentifier_t,VBufStorage_controlFieldNode_t*> controlFieldNodesByIdentifier;

/**
 * the offset at where the current selection starts.
 */ 
	int selectionStart;

/**
 * The length of the selection.
 */
	int selectionLength;

/**
 * removes the controlFieldNode from the buffer's controlFieldNodesByIdentifier set.
 */
	void forgetControlFieldNode(VBufStorage_controlFieldNode_t* node);

/**
 * Inserts the given fieldNode in to the buffer's tree of nodes. Makes all needed connections with other nodes in the buffer's node tree.
 * @param parent a control field already in the buffer that should be the inserted node's parent, note if also specifying previous then parent can be NULL.
 * @param previous the field already in the buffer that the inserted node will come directly after, note previous's parent will always be used over the parent argument.
 * @param node the node being inserted.
 */ 
	bool insertNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_fieldNode_t* node);

/**
 * disassociates the given node and its descendants from this buffer and deletes the node and its descendants.
 * @param node the node you wish to delete.
 */
	void deleteSubtree(VBufStorage_fieldNode_t* node);

/**
 * disassociates the given node from this buffer and deletes the node.
 * @param node the node you wish to delete.
 */
	void deleteNode(VBufStorage_fieldNode_t* node);

	friend class VBufStorage_fieldNode_t;
	friend class VBufStorage_controlFieldNode_t;
	friend class VBufStorage_textFieldNode_t;

	public:

/*
 * constructor.
 */
	VBufStorage_buffer_t();

/**
 * Destructor
 */
	~VBufStorage_buffer_t();

/**
 * Adds a control field in to the buffer.
 * @param parent the control field which should be the new field's parent, note that if also specifying previous parent can be NULL.
 * @param previous the field which the new field  should come directly after, note that previous's parent  will be used over the parent argument, and previous can also not be the buffer's root node (first field added).
 * @param docHandle the docHandle you wish the new control field node to have
 * @param ID the ID you wish the new control field node to have.  
 * @param isBlock if true then the buffer will force a line break at the start and end of the new control.
 * @return the newly added control field.
 */
	VBufStorage_controlFieldNode_t* addControlFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, int docHandle, int ID, bool isBlock);
 
	VBufStorage_controlFieldNode_t* addControlFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_controlFieldNode_t* node); 

/**
 * Adds a text field in to the buffer.
 * @param parent the control field which should be the new field's parent, note that if also specifying previous, parent can be NULL.
 * @param previous the field which the new field  should come directly after, note that previous's parent  will be used over the parent argument, and previous can also not be the buffer's root node (first field added).
 * @param text the text that this field will contain.
 * @return the newly added text field.
 */
	VBufStorage_textFieldNode_t* addTextFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, const std::wstring& text);

	VBufStorage_textFieldNode_t* addTextFieldNode(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_textFieldNode_t* node);

/**
 * finds out if the given node exists in this buffer.
 * @param node the node you wish to check.
 * @return true if it is in the buffer, false otherwise.
 */
	virtual bool isNodeInBuffer(VBufStorage_fieldNode_t* node);

/**
 * Removes the given nodes from the buffer and then merges the content of the new buffers in the removed node's position. It also tries to keep the selection relative to the control field it was in before the replacement.
 * @param m the map of nodes to buffers 
 */
	bool replaceSubtrees(std::map<VBufStorage_fieldNode_t*,VBufStorage_buffer_t*>& m);

/**
 * disassociates from this buffer, and deletes, the given field and its descendants.
 * @param node the node you wish to remove.
	* @param removeDescedants true if descendants should be removed, false otherwise.
 * @return true if the node was removed, false otherwise.
 */
	bool removeFieldNode(VBufStorage_fieldNode_t* node, bool removeDescendants=true);

/*
 * Removes all nodes from the buffer.
 */
	void clearBuffer();

/**
 * Calculates the start and end character offsets of the given node in the buffer.
 * @param node the node you want the offsets of.
 * @param startOffset memory where this method can place the found start offset.
 * @param endOffset memory where this method can place the found end offset.
 * @return true if successful, false otherwize.
 */
	virtual bool getFieldNodeOffsets(VBufStorage_fieldNode_t* node, int *startOffset, int *endOffset);

/**
 * finds out if a given field is positioned at a given character offset in this buffer.
 * @param node the field you are interested in.
 * @param offset the character offset you are interested in.
 * @return true if the field is at the offset, false otherwise.
 */
	virtual bool isFieldNodeAtOffset(VBufStorage_fieldNode_t* node, int offset);

/**
 * locates the text field node at the given offset
 * @param offset the offset to use
 * @param nodeStartOffset memory where the found text field's start offset will be placed.
 * @param nodeEndOffset memory where the found text field's end offset will be placed.
 * @return the located text field node.
 */
	virtual VBufStorage_textFieldNode_t* locateTextFieldNodeAtOffset(int offset, int *nodeStartOffset, int *nodeEndOffset);

/**
 * locates the deepest control field node at the given offset
 * @param offset the offset to use
 * @param startOffset memory where the found text field's start offset will be placed.
 * @param endOffset memory where the found text field's end offset will be placed.
 * @param docHandle memory where the docHandle of the found control field node will be placed.
 * @param ID memory where the ID of the found control field node will be placed.
 * @return the located control field node.
 */
	virtual VBufStorage_controlFieldNode_t* locateControlFieldNodeAtOffset(int offset, int *startOffset, int *endOffset, int* docHandle, int* ID);
 
/**
 * locates the controlFieldNode with the given identifier
 * @param docHandle the docHandle of the control field node you wish to find
 * @param ID the ID of the control field node you wish to find
 * @return the controlFieldNode with the given identifier
 */
	virtual VBufStorage_controlFieldNode_t* getControlFieldNodeWithIdentifier(int docHandle, int ID);

/**
 * Retreaves the identifier for the given controlFieldNode.
 * @param node the controlFieldNode who's identifier should be retreaved.
 * @param docHandle a memory address where the docHandle should be placed.
 * @param ID a memory address where the ID should be placed.
 * @return true if successfull
 */
	virtual bool getIdentifierFromControlFieldNode(VBufStorage_controlFieldNode_t*node, int* docHandle, int* ID);

/**
 * Finds a field node that contains particular attributes.
 * @param offset offset in the buffer to start searching from, if -1 then starts at the root of the buffer.
 * @param direction which direction to search
 * @param attribs the attributes to search
 * @param regexp regular expression the requested attributes must match
 * @param startOffset memory where the start offset of the found node can be placed
 * @param endOffset memory where the end offset of the found node will be placed
 * @return the found field node
 */
	virtual VBufStorage_fieldNode_t* findNodeByAttributes(int offset, VBufStorage_findDirection_t  direction, const std::wstring &attribs, const std::wstring &regexp, int *startOffset, int *endOffset);

/**
 * Retreaves the current selection offsets for the buffer
 * @param startOffset memory where the start offset of the selection will be placed
 * @param endOffset memory where the end offset of the selection will be placed
 * @return true if successfull, false otherwize.
 */
	virtual bool getSelectionOffsets(int* startOffset, int *endOffset) const;

/**
 * sets the selection offsets for the buffer.
 * @param startOffset the offset the start of the selection should be set to.
 * @param endOffset the offset the end of the selection should be set to.
 * @return true if successfull, false otherwize.
 */
	virtual bool setSelectionOffsets(int startOffset, int endOffset);

/**
 * retreaves the length of all the text in the buffer.
 * @return the length in characters of the text
 */
	virtual int getTextLength() const;

/**
 * Retreaves the text in the buffer between given offsets, optionally containing markup.
 * @param startOffset the offset to start from
 * @param endOffset the offset to end at. Use -1 to mean end of buffer.
 * @param text where to place the found text
 * @param useMarkup if true then markup is included in the text denoting field starts and ends.
 * @return the text.
 */
	virtual VBufStorage_textContainer_t*  getTextInRange(int startOffset, int endOffset, bool useMarkup=false);

/**
 * Expands the given offset to the start and end offsets of the containing line.
 * @param offset the offset to expand.
 * @param maxLineLength the maximum length of a line.
 * @param useScreenLayout if true then lines will only break on block controls or line feed characters, if false then lines will break on all field nodes.
 * @param startOffset memory to place the calculated line start offset
 * @param endOffset memory to place the calculated line end offset
  * @return true if successfull, false otherwize.
 */ 
	virtual bool getLineOffsets(int offset, int maxLineLength, bool useScreenLayout, int *startOffset, int *endOffset);

/**
 * Does this buffer have content?
 * true if there is content, false otherwise.
 */
	virtual bool hasContent();

/**
 * Is one node a descendant of another.
 * @param parent the parent node.
 * @param descendant the descendant node.
 * @returns True if descendant is a descendant of parent, false otherwise.
 */
	virtual bool isDescendantNode(VBufStorage_fieldNode_t* parent, VBufStorage_fieldNode_t* descendant);

/**
 * Adds a reference node to the buffer at the location given by parent and previous, pointing to the given existing node in another buffer.
 * @param parent the parent in this buffer of the added reference node.
 * @param previous the previous node in this buffer of the added reference node.
 * @param node the existing node from another buffer that the reference node should point to.
 */
	VBufStorage_referenceNode_t*  addReferenceNodeToBuffer(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, VBufStorage_controlFieldNode_t* node); 

	virtual std::wstring getDebugInfo() const;

};

#endif
