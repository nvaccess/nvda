#include <string>
#include <sstream>
#include <set>
#include "nvdaControllerInternal.h"
#include <common/log.h>
#include "displayModel.h"

using namespace std;

displayModel_t::displayModel_t(): _refCount(1), _chunksByXY(), _chunksByYX() {
	LOG_DEBUG(L"created instance at "<<this);
}

displayModel_t::~displayModel_t() {
	LOG_DEBUG(L"destroying instance at "<<this);
	_chunksByYX.clear();
	for(displayModelChunksByPointMap_t::iterator i=_chunksByXY.begin();i!=_chunksByXY.end();) {
		LOG_DEBUG(L"deleting chunk at "<<i->second);
		delete i->second;
		_chunksByXY.erase(i++);
	}
}

long displayModel_t::AddRef() {
		return InterlockedIncrement(&_refCount);
}

long displayModel_t::Release() {
	long refCount=InterlockedDecrement(&_refCount);
	if(refCount==0) delete this;
	return refCount; 
}

int displayModel_t::getChunkCount() {
	return _chunksByXY.size();
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

void displayModel_t::copyRectangleToOtherModel(RECT& rect, displayModel_t* otherModel, int otherX, int otherY) {
	if(!otherModel) otherModel=this;
	set<displayModelChunk_t*> chunks;
	RECT tempRect;
	RECT clearRect=rect;
	int deltaX=otherX-rect.left;
	int deltaY=otherY-rect.top;
	//Collect all the chunks that should be copied in to a temporary set, and expand the clearing rectangle to bound them all completely.
	for(displayModelChunksByPointMap_t::iterator i=_chunksByYX.begin();i!=_chunksByYX.end();i++) {
		if(IntersectRect(&tempRect,&rect,&(i->second->rect))) {
			chunks.insert(i->second);
			if(i->second->rect.left<clearRect.left) clearRect.left=i->second->rect.left;
			if(i->second->rect.top<clearRect.top) clearRect.top=i->second->rect.top;
			if(i->second->rect.right>clearRect.right) clearRect.right=i->second->rect.right;
			if(i->second->rect.bottom>clearRect.bottom) clearRect.bottom=i->second->rect.bottom;
		}
	}
	if(chunks.size()>0) {
		//Shift the clearing rectangle so its where it is requested to be in the destination model
		clearRect.left+=deltaX;
		clearRect.top+=deltaY;
		clearRect.right+=deltaX;
		clearRect.bottom+=deltaY;
		//Clear the rectangle in the destination model to make space for the chunks
		otherModel->clearRectangle(clearRect);
		//Insert each chunk previously selected, in to the destination model shifting the chunk's rectangle to where it should be in the destination model
		for(set<displayModelChunk_t*>::iterator i=chunks.begin();i!=chunks.end();i++) {
			RECT newChunkRect={((*i)->rect.left)+=deltaX,((*i)->rect.top)+deltaY,((*i)->rect.right)+deltaX,((*i)->rect.bottom)+deltaY};
			otherModel->insertChunk(newChunkRect,(*i)->text);
		}
	}
}

void displayModel_t::renderText(const RECT* rect, wstring& text) {
	wostringstream s;
	RECT tempRect;
	int lastRight; 
	int lastTop;
	BOOL hasAddedText=FALSE;
	//Walk through all the chunks looking for one that intersects the rectangle
	for(displayModelChunksByPointMap_t::iterator i=_chunksByYX.begin();i!=_chunksByYX.end();i++) {
		if(!rect||IntersectRect(&tempRect,rect,&(i->second->rect))) {
			if(hasAddedText&&i->second->rect.top>lastTop) s<<endl;
			else if(hasAddedText&&i->second->rect.left>lastRight) s<<" ";
			s<<i->second->text;
			lastRight=i->second->rect.right;
			lastTop=i->second->rect.top;
			hasAddedText=TRUE;
		}
	}
	text.append(s.str());
}
