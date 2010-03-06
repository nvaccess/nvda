#include <string>
#include <sstream>
#include "nvdaControllerInternal.h"
#include <common/log.h>
#include "displayModel.h"

using namespace std;

displayModel_t::displayModel_t(): _chunksByXY(), _chunksByYX() {
	LOG_DEBUG(L"created instance at "<<this);
}

displayModel_t::~displayModel_t() {
	LOG_DEBUG(L"destroying instance at "<<this);
	_chunksByYX.clear();
	for(displayModelChunksByPointMap_t::iterator i=_chunksByXY.begin();i!=_chunksByXY.end();i++) {
		LOG_DEBUG(L"deleting chunk at "<<i->second);
		delete i->second;
		_chunksByXY.erase(i);
	}
}

void displayModel_t::insertChunk(const RECT& rect, const wstring& text) {
	displayModelChunk_t* chunk=new displayModelChunk_t;
	LOG_DEBUG(L"created new chunk at "<<chunk);
	chunk->rect=rect;
	chunk->text=text;
	LOG_DEBUG(L"filled in chunk with rectangle from "<<rect.left<<L","<<rect.top<<L" to "<<rect.right<<L","<<rect.bottom<<L" with text of "<<text);
	_chunksByXY[make_pair(rect.left,rect.top)]=chunk;
	_chunksByYX[make_pair(rect.top,rect.left)]=chunk;
}

void displayModel_t::clearRectangle(const RECT& rect) {
	LOG_DEBUG(L"Clearing rectangle from "<<rect.left<<L","<<rect.top<<L" to "<<rect.right<<L","<<rect.bottom);
	displayModelChunksByPointMap_t::iterator i=_chunksByXY.begin();
	while(i!=_chunksByXY.end()) {
		displayModelChunksByPointMap_t::iterator curI=i++;
		displayModelChunk_t* chunk=curI->second;
		//Ignore any chunks not overlapping vertically
		if(rect.bottom<=chunk->rect.top||rect.top>=chunk->rect.bottom) {
			continue;
		}
		//Ignore any chunks not overlapping horizontally
		if(rect.right<=chunk->rect.left||rect.left>=chunk->rect.right) {
			continue;
		}
		//This chunk is definitely overlapping vertically.
		//Remove any chunk completely covered horizontally
		if((rect.left<=chunk->rect.left)&&(rect.right>=chunk->rect.right)) {
			LOG_DEBUG(L"removing chunk that horizontally overlaps completely, with rectangle from "<<chunk->rect.left<<L","<<chunk->rect.top<<L" to "<<chunk->rect.right<<L","<<chunk->rect.bottom);
			_chunksByXY.erase(curI);
			_chunksByYX.erase(make_pair(chunk->rect.top,chunk->rect.left));
			delete chunk;
		} else {
			//The chunk is partly overlapped horizontally.
			//For now just remove the chunk
			LOG_DEBUG(L"removing chunk that horizontally overlaps partially, with rectangle from "<<chunk->rect.left<<L","<<chunk->rect.top<<L" to "<<chunk->rect.right<<L","<<chunk->rect.bottom);
			_chunksByXY.erase(curI);
			_chunksByYX.erase(make_pair(chunk->rect.top,chunk->rect.left));
			delete chunk;
		}
	}
	LOG_DEBUG(L"complete");
}

void displayModel_t::renderText(const RECT* rect, wstring& text) {
	wostringstream s;
	RECT tempRect;
	for(displayModelChunksByPointMap_t::iterator i=_chunksByYX.begin();i!=_chunksByYX.end();i++) {
		if(!rect||IntersectRect(&tempRect,rect,&(i->second->rect))) {
			s<<i->second->text<<endl;
		}
	}
	text.append(s.str());
}
