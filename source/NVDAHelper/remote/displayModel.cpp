#include <iostream>
#include <string>
#include <sstream>
#include "displayModel.h"

using namespace std;

displayModel_t::displayModel_t(): _chunksByXY(), _chunksByYX() {
	cerr<<"displayModel_t::displayModel_t: created instance at "<<this<<endl;
}

displayModel_t::~displayModel_t() {
	cerr<<"displayModel_t::~displayModel_t: destroying instance at "<<this<<endl;
	_chunksByYX.clear();
	for(displayModelChunksByPointMap_t::iterator i=_chunksByXY.begin();i!=_chunksByXY.end();i++) {
		cerr<<"displayModel_t::~displayModel_t: deleting chunk at "<<i->second<<endl;
		delete i->second;
		_chunksByXY.erase(i);
	}
}

void displayModel_t::insertChunk(const RECT& rect, const wstring& text) {
	displayModelChunk_t* chunk=new displayModelChunk_t;
	cout<<"displayModel_t::insertChunk: created new chunk at "<<chunk<<endl;
	chunk->rect=rect;
	chunk->text=text;
	wcout<<L"displayModel_t::insertChunk: filled in chunk with rectangle from "<<rect.left<<L","<<rect.top<<L" to "<<rect.right<<L","<<rect.bottom<<L" with text of "<<text<<endl;
	_chunksByXY[make_pair(rect.left,rect.top)]=chunk;
	_chunksByYX[make_pair(rect.top,rect.left)]=chunk;
}

void displayModel_t::clearRectangle(const RECT& rect) {
	cout<<"Clearing rectangle from "<<rect.left<<","<<rect.top<<" to "<<rect.right<<","<<rect.bottom<<endl;
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
			cout<<"displayModel_t::clearRectangle: removing chunk that horizontally overlaps completely, with rectangle from "<<chunk->rect.left<<","<<chunk->rect.top<<" to "<<chunk->rect.right<<","<<chunk->rect.bottom<<endl;
			_chunksByXY.erase(curI);
			_chunksByYX.erase(make_pair(chunk->rect.top,chunk->rect.left));
			delete chunk;
		} else {
			//The chunk is partly overlapped horizontally.
			//For now just remove the chunk
			cout<<"displayModel_t::clearRectangle: removing chunk that horizontally overlaps partially, with rectangle from "<<chunk->rect.left<<","<<chunk->rect.top<<" to "<<chunk->rect.right<<","<<chunk->rect.bottom<<endl;
			_chunksByXY.erase(curI);
			_chunksByYX.erase(make_pair(chunk->rect.top,chunk->rect.left));
			delete chunk;
		}
	}
	cout<<"displayModel_t::clearRectangle: complete"<<endl;
}

void displayModel_t::renderText(wstring& text) {
	wostringstream s;
	for(displayModelChunksByPointMap_t::iterator i=_chunksByYX.begin();i!=_chunksByYX.end();i++) {
		s<<L"Chunk from "<<i->second->rect.left<<L","<<i->second->rect.top<<L" to "<<i->second->rect.right<<L","<<i->second->rect.bottom<<L":"<<endl<<i->second->text<<endl;
	}
	text.append(s.str());
}
