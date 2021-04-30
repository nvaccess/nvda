/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2007-2016 NV Access Limited
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#ifndef VIRTUALBUFFER_BACKEND_H
#define VIRTUALBUFFER_BACKEND_H

#include <set>
#define WIN32_LEAN_AND_MEAN 
#include <windows.h>
#include "storage.h"
#include <common/lock.h>

class VBufBackend_t;

typedef std::set<VBufBackend_t*> VBufBackendSet_t;

/**
 * Renders content in to a storage buffer for linea access.
 */
class VBufBackend_t  : public VBufStorage_buffer_t {
	private:

/**
 * A callback to handle windows being destroyed.
 */
static LRESULT CALLBACK destroy_callWndProcHook(int code, WPARAM wParam, LPARAM lParam);

/**
 * The ID of the current timer for this backend.
 */
	UINT_PTR renderThreadTimerID;

/**
 * A timer callback that will rerender invalid subtrees
 */
	static void CALLBACK renderThread_timerProc(HWND hwnd, UINT msg, UINT_PTR timerID, DWORD time);

/**
 * A winEvent callback that will watch for destroy of a backend's root window and clear the backend.
 */
	static void CALLBACK renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time);

	protected:

/**
 * the list of control field nodes that should be re-rendered the next time the backend is updated.
 * the list is in an order such that any parent is before any child. 
 */
	VBufStorage_controlFieldNodeList_t pendingInvalidSubtreesList;

/**
 * The list of invalid subtrees currently being re-rendered by update.
  */
	VBufStorage_controlFieldNodeList_t workingInvalidSubtreesList;

/**
 * The set of currently running backends
 */
	static VBufBackendSet_t runningBackends;

/**
 * The thread ID of the rendering thread
 */
	const int renderThreadID;

/**
 * Requests that the backend should update any invalid nodes  when it can in the next little while.
 */
	void requestUpdate();

/**
 * Cancels any pending request to update invalid nodes.
 */
	void cancelPendingUpdate();

/**
 * Sets up any code in the render thread
 */
	virtual void renderThread_initialize();

/**
 * Terminates any code in the render thread
 */
	virtual void renderThread_terminate();

/**
 * Renders content starting from the given doc handle and ID, in to the given buffer.
 * The buffer will always start off empty as even for subtree re-rendering, a temp buffer is provided.
 * @param buffer the buffer to render content in.
 * @param docHandle the doc handle to start from
 * @param ID the ID to start from.
 * @param oldNode an optional node that will be replaced by the rendered content (useful for retreaving cached data) 
 */
	virtual void render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode=NULL)=0;

/**
 * Updates the content of the buffer. 
 * If no content yet exists it renders the entire document. If content exists it only re-renders nodes marked as invalid.
 */
	void update();

/**
 * Destructor, (protected as you must use the destroy method).
 */
	virtual ~VBufBackend_t();

	public:

/**
 * constructor
 * @param docHandle uniquely identifies the document or window containing the content to ve rendered
 * @param ID uniquely identifies where to start rendering from in the document or window
 * @param storageBuffer the storage buffer to render the content in
 */
	VBufBackend_t(int docHandle, int ID);

/**
 * Initializes the state of the backend and performs an initial rendering of content.
 */
	virtual void initialize();

/**
 * identifies the window or document where the backend starts rendering from
 */
	const int rootDocHandle;

/**
 * Represents the ID in the window or document where the backend starts rendering
 */
	const int rootID;

/**
 * marks a particular node as invalid, so that its content is re-rendered on next update.
 * @param node the node that should be invalidated.
 */
	virtual bool invalidateSubtree(VBufStorage_controlFieldNode_t*);

/**
 * Forces any invalidated nodes to be updated right now.
 */
	virtual void forceUpdate();

/**
 * Clears the content of the backend and terminates any code used for rendering.
 */
	virtual void terminate();

/**
 * Destructs and deletes the backend. Must be used rather than delete as this will handle crossing CRT boundaries.
 */
	virtual void destroy();

 /**
 * Useful for cerializing access to the buffer
 */
	LockableObject lock;

/**
 * Fetches an existing node from this backend, so that it can be added to a temporary buffer as a reference node during a partial render.
 * This method should only be called from within a backend's render method.
 * If the node exists but it is currently marked for re-rendering,
 * The node is unmarked for re-rendering, but not returned. 
 * this allows the current render in progress (that called this method) to go ahead and re-render that node itself like it had never existed.
  */
	VBufStorage_controlFieldNode_t* reuseExistingNodeInRender(VBufStorage_controlFieldNode_t* parent, VBufStorage_fieldNode_t* previous, int docHandle, int ID) ;

};

/**
 * a function signature for the VBufBackend_create factory function all backend libraries must implement to create a backend.
 */
typedef VBufBackend_t*(*VBufBackend_create_proc)(int,int);

// The backend creation functions
VBufBackend_t* AdobeAcrobatVBufBackend_t_createInstance(int docHandle, int ID);
VBufBackend_t* GeckoVBufBackend_t_createInstance(int docHandle, int ID);
VBufBackend_t* lotusNotesRichTextVBufBackend_t_createInstance(int docHandle, int ID);
VBufBackend_t* MshtmlVBufBackend_t_createInstance(int docHandle, int ID);
VBufBackend_t* WebKitVBufBackend_t_createInstance(int docHandle, int ID);

#endif
