#ifndef NVDAHELPER_REMOTE_DISPLAYMODEL_H
#define NVDAHELPER_REMOTE_DISPLAYMODEL_H

#include <map>
#include <windows.h>

typedef struct {
	RECT rect;
	std::wstring text;
} displayModelChunk_t;

typedef std::pair<int,int> coord_t;
typedef std::map<std::pair<int,int>,displayModelChunk_t*> displayModelChunksByPointMap_t;

class displayModel_t {
	private:
	ULONG _refCount;
	displayModelChunksByPointMap_t _chunksByXY;
	displayModelChunksByPointMap_t _chunksByYX;

	public:
	displayModel_t();
	~displayModel_t();
	ULONG AddRef();
	ULONG Release();
	void insertChunk(const RECT& rect, const std::wstring& text);
	void clearRectangle(const RECT& rect);
	void copyRectangleToOtherModel(RECT& rect,displayModel_t* otherModel, int otherX, int otherY);
	void renderText(const RECT* rect, std::wstring& text);

};

#endif
