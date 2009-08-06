/**
 * backends/adobeAcrobat/adobeAcrobat.h
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007-2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#ifndef VIRTUALBUFFER_BACKENDS_ADOBEACROBAT_H
#define VIRTUALBUFFER_BACKENDS_ADOBEACROBAT_H

#include <vbufBase/backend.h>

class AdobeAcrobatVBufBackend_t: public VBufBackend_t {
	protected:

	static void CALLBACK renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time);

	virtual void renderThread_initialize();

	virtual void renderThread_terminate();

	virtual void render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode);

	virtual ~AdobeAcrobatVBufBackend_t();

	public:

	AdobeAcrobatVBufBackend_t(int docHandle, int ID);

};

#endif
