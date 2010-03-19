#include <cassert>
#include <string>
#include <sstream>
#include <deque>
#include <set>
#include "nvdaControllerInternal.h"
#include <common/log.h>
#include "displayModel.h"

using namespace std;

void displayModelChunk_t::truncate(int truncatePointX, BOOL truncateBefore) {
	assert(text.length()!=0);
	assert(characterXArray.size()!=0);
	deque<int>::iterator c=characterXArray.begin();
	wstring::iterator t=text.begin();
	if(truncateBefore) {
		for(;t!=text.end()&&(*c)<truncatePointX;c++,t++);
		rect.left=*c;
		characterXArray.erase(characterXArray.begin(),c);
		text.erase(text.begin(),t);
	} else {
		for(;t!=text.end()&&(*c)<=truncatePointX;c++,t++);
		--c;
		--t;
		rect.right=*c;
		characterXArray.erase(c,characterXArray.end());
		text.erase(t,text.end());
	}
}

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

void displayModel_t::insertChunk(const RECT& rect, const wstring& text, int* characterEndXArray) {
	displayModelChunk_t* chunk=new displayModelChunk_t;
	LOG_DEBUG(L"created new chunk at "<<chunk);
	chunk->rect=rect;
	chunk->text=text;
	chunk->characterXArray.push_back(rect.left);
	for(int i=0;i<text.length();i++) chunk->characterXArray.push_back(characterEndXArray[i]+rect.left); 
	LOG_DEBUG(L"filled in chunk with rectangle from "<<rect.left<<L","<<rect.top<<L" to "<<rect.right<<L","<<rect.bottom<<L" with text of "<<text);
	insertChunk(chunk);
}

void displayModel_t::insertChunk(displayModelChunk_t* chunk) {
	_chunksByXY[make_pair(chunk->rect.left,chunk->rect.top)]=chunk;
	_chunksByYX[make_pair(chunk->rect.top,chunk->rect.left)]=chunk;
}

void displayModel_t::clearRectangle(const RECT& rect) {
	LOG_DEBUG(L"Clearing rectangle from "<<rect.left<<L","<<rect.top<<L" to "<<rect.right<<L","<<rect.bottom);
	set<displayModelChunk_t*> chunksForInsertion;
	displayModelChunksByPointMap_t::iterator i=_chunksByXY.begin();
	RECT tempRect;
	while(i!=_chunksByXY.end()) {
		displayModelChunksByPointMap_t::iterator nextI=i;
		nextI++; 
		displayModelChunk_t* chunk=i->second;
		if(IntersectRect(&tempRect,&rect,&(chunk->rect))) {
			if(tempRect.left==chunk->rect.left&&tempRect.right==chunk->rect.right) {
				_chunksByXY.erase(i);
				_chunksByYX.erase(make_pair(chunk->rect.top,chunk->rect.left));
				delete chunk;
			} else if(tempRect.left>chunk->rect.left&&tempRect.right==chunk->rect.right) {
				chunk->truncate(tempRect.left,FALSE);
				if(chunk->text.length()==0) {
					_chunksByXY.erase(i);
					_chunksByYX.erase(make_pair(chunk->rect.top,chunk->rect.left));
					delete chunk;
				}
			} else if(tempRect.right<chunk->rect.right&&tempRect.left==chunk->rect.left) {
				_chunksByXY.erase(i);
				_chunksByYX.erase(make_pair(chunk->rect.top,chunk->rect.left));
				chunk->truncate(tempRect.right,TRUE);
				if(chunk->text.length()==0) {
					delete chunk;
				} else {
					chunksForInsertion.insert(chunk);
				}
			} else {
				displayModelChunk_t* newChunk=new displayModelChunk_t(*chunk);
				chunk->truncate(tempRect.left,FALSE);
				if(chunk->text.length()==0) {
					_chunksByXY.erase(i);
					_chunksByYX.erase(make_pair(chunk->rect.top,chunk->rect.left));
					delete chunk;
				}
				newChunk->truncate(tempRect.right,TRUE);
				if(newChunk->text.length()==0) {
					delete newChunk;
				} else {
					chunksForInsertion.insert(newChunk);
				}
			}
		}
		i=nextI;
	}
	for(set<displayModelChunk_t*>::iterator i=chunksForInsertion.begin();i!=chunksForInsertion.end();i++) {
		insertChunk(*i);
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
			displayModelChunk_t* chunk=new displayModelChunk_t(**i);
			chunk->rect.left=(chunk->rect.left)+deltaX;
			chunk->rect.top=(chunk->rect.top)+deltaY;
			chunk->rect.right=(chunk->rect.right)+deltaX;
			chunk->rect.bottom=(chunk->rect.bottom)+deltaY;
			for(deque<int>::iterator x=chunk->characterXArray.begin();x!=chunk->characterXArray.end();x++) (*x)+=deltaX;
			if(chunk->rect.left<clearRect.left) {
				chunk->truncate(clearRect.left,TRUE);
			}
			if(chunk->rect.right>clearRect.right) {
				chunk->truncate(clearRect.right,FALSE);
			}
			if(chunk->text.length()==0) {
				delete chunk;
			} else {
				otherModel->insertChunk(chunk);
			}
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
