/**
 * base/backend.h
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#ifndef VIRTUALBUFFER_BACKEND_H
#define VIRTUALBUFFER_BACKEND_H

#include <set>
#include "storage.h"
#include "lock.h"

class VBufBackend_t;

/**
 * a type for A set of backends
 */
typedef std::set<VBufBackend_t*> VBufBackendSet_t;

/**
 * Renders content in to a storage buffer for linea access.
 */
class VBufBackend_t  : public VBufStorage_buffer_t {
	protected:

/**
 * identifies the window or document where the backend starts rendering from
 */
	int rootDocHandle;

/**
 * Represents the ID in the window or document where the backend starts rendering
 */
	int rootID;

/**
 * The storage buffer the backend uses for rendering
 */

/**
 * the set of control field nodes that should be re-rendered the next time the backend is updated.
 */
	VBufStorage_controlFieldNodeSet_t invalidSubtrees;

/**
 * Renders content starting from the given doc handle and ID, in to the given buffer.
 * The buffer will always start off empty as even for subtree re-rendering, a temp buffer is provided.
 * @param buffer the buffer to render content in.
 * @param docHandle the doc handle to start from
 * @param ID the ID to start from.
 * @param oldNode an optional node that will be replaced by the rendered content (useful for retreaving cached data) 
 */
	virtual void render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode=NULL)=0;

	public:

/**
 * constructor
 * @param docHandle uniquely identifies the document or window containing the content to ve rendered
 * @param ID uniquely identifies where to start rendering from in the document or window
 * @param storageBuffer the storage buffer to render the content in
 */
	VBufBackend_t(int docHandle, int ID);

/**
 * identifies the window or document where the backend starts rendering from
 */
	int getRootDocHandle();

/**
 * Represents the ID in the window or document where the backend starts rendering
 */
	int getRootID();

/**
 * marks a particular node as invalid, so that its content is re-rendered on next update.
 * @param node the node that should be invalidated.
 */
	virtual void invalidateSubtree(VBufStorage_controlFieldNode_t*);

/**
 * Updates the content of the buffer. 
 * If no content yet exists it renders the entire document. If content exists it only re-renders nodes marked as invalid.
 */
	void update();

/**
 * Destructor
 */
	virtual ~VBufBackend_t();

	/**
 * Useful for cerializing access to the buffer
 */
	VBufLock_t lock;

};

/**
 * a function signature for the VBufBackend_create factory function all backend libraries must implement to create a backend.
 */
typedef VBufBackend_t*(*VBufBackend_create_proc)(int,int);

#endif
