/**
 * backends/adobeAcrobat/adobeAcrobat.h
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007-2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#ifndef VIRTUALBUFFER_BACKENDS_ADOBEACROBAT_H
#define VIRTUALBUFFER_BACKENDS_ADOBEACROBAT_H

#include <windows.h>
#include <base/backend.h>

class AdobeAcrobatVBufBackend_t: public VBufBackend_t {
	private:
	int rootThreadID;
	virtual void render(VBufStorage_buffer_t* buffer, int docHandle, int ID);

	public:

	AdobeAcrobatVBufBackend_t(int docHandle, int ID, VBufStorage_buffer_t* storageBuffer);

	~AdobeAcrobatVBufBackend_t();

};

#endif
