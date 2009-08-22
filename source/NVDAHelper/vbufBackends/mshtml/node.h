/**
 * backends/mshtml/node.h
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
*/

#ifndef VIRTUALBUFFER_BACKENDS_NODE_H
#define VIRTUALBUFFER_BACKENDS_NODE_H

#include <mshtml.h>
#include <vbufBase/storage.h>
#include <vbufBase/backend.h>
#include "mshtml.h"

class MshtmlVBufStorage_controlFieldNode_t : public VBufStorage_controlFieldNode_t {

	public:
	MshtmlVBufBackend_t* backend;
	IHTMLElement2* pHTMLElement2;
	IDispatch* propChangeSink;
	IDispatch* loadSink;
	IMarkupContainer2* pMarkupContainer2;
	IHTMLChangeSink* pHTMLChangeSink;
	DWORD HTMLChangeSinkCookey;
	MshtmlVBufStorage_controlFieldNode_t(int docHandle, int ID, bool isBlock, MshtmlVBufBackend_t* backend, IHTMLDOMNode* pHTMLDOMNode);
	~MshtmlVBufStorage_controlFieldNode_t();

};

#endif
