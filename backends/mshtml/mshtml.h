/**
 * backends/ie_mshtml/ie_mshtml.h
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#ifndef VIRTUALBUFFER_BACKENDS_MSHTML_H
#define VIRTUALBUFFER_BACKENDS_MSHTML_H

#include <windows.h>
#include <base/storage.h>
#include <base/backend.h>

class MshtmlVBufBackend_t: public VBufBackend_t {
	private:

	int rootThreadID;

	virtual void render(VBufStorage_buffer_t* buffer, int docHandle, int ID);

	public:

	MshtmlVBufBackend_t(int docHandle, int ID, VBufStorage_buffer_t* storageBuffer);

	VBufStorage_fieldNode_t* fillVBuf(VBufStorage_buffer_t* buffer, VBufStorage_controlFieldNode_t* parentNode, VBufStorage_fieldNode_t* previousNode, IHTMLDOMNode* pHTMLDOMNode, int docHandle, int tableID, long rowIndex, int* LIIndexPtr);

	VBufStorage_controlFieldNode_t* getDeepestControlFieldNodeForHTMLElement(IHTMLElement* pHTMLElement);
	~MshtmlVBufBackend_t();

	virtual void invalidateSubtree(VBufStorage_controlFieldNode_t* node);

};

#endif
