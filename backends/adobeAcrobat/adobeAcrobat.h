#ifndef VIRTUALBUFFER_BACKENDS_ADOBEACROBAT_H
#define VIRTUALBUFFER_BACKENDS_ADOBEACROBAT_H

#include <windows.h>
#include <base/backend.h>

class AdobeAcrobatVBufBackend_t: public VBufBackend_t {
	private:
	int rootThreadID;

	public:

	AdobeAcrobatVBufBackend_t(int docHandle, int ID, VBufStorage_buffer_t* storageBuffer);

	~AdobeAcrobatVBufBackend_t();

};

#endif
