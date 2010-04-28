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
	if(text.length()==0) return;
	assert(characterXArray.size()!=0);
	deque<int>::iterator c=characterXArray.begin();
	wstring::iterator t=text.begin();
	if(truncateBefore&&rect.left<truncatePointX) {
		for(;t!=text.end()&&(*c)<truncatePointX;c++,t++);
		if(c!=characterXArray.end()) rect.left=*c; else rect.left=rect.right; 
		characterXArray.erase(characterXArray.begin(),c);
		text.erase(text.begin(),t);
	} else if(!truncateBefore&&truncatePointX<rect.right) {
		for(;t!=text.end()&&(*c)<=truncatePointX;c++,t++);
		if(t!=text.begin()) {
			--c;
			--t;
		}
		rect.right=*c;
		characterXArray.erase(c,characterXArray.end());
		text.erase(t,text.end());
	}
}

displayModel_t::displayModel_t(): _refCount(1), chunksByYX() {
	LOG_DEBUG(L"created instance at "<<this);
}

displayModel_t::~displayModel_t() {
	LOG_DEBUG(L"destroying instance at "<<this);
	for(displayModelChunksByPointMap_t::iterator i=chunksByYX.begin();i!=chunksByYX.end();) {
		LOG_DEBUG(L"deleting chunk at "<<i->second);
		delete i->second;
		chunksByYX.erase(i++);
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
	return chunksByYX.size();
}

void displayModel_t::insertChunk(const RECT& rect, int baselineFromTop, const wstring& text, int* characterEndXArray, const RECT* clippingRect) {
	displayModelChunk_t* chunk=new displayModelChunk_t;
	LOG_DEBUG(L"created new chunk at "<<chunk);
	chunk->rect=rect;
	chunk->baselineFromTop=baselineFromTop;
	chunk->text=text;
	chunk->characterXArray.push_back(rect.left);
	for(int i=0;i<(text.length()-1);i++) chunk->characterXArray.push_back(characterEndXArray[i]+rect.left); 
	LOG_DEBUG(L"filled in chunk with rectangle from "<<rect.left<<L","<<rect.top<<L" to "<<rect.right<<L","<<rect.bottom<<L" with text of "<<text);
	//If a clipping rect is specified, and the chunk falls outside the clipping rect
	//Truncate the chunk so that it stays inside the clipping rect.
	if(clippingRect) {
		if(clippingRect->left>chunk->rect.left) chunk->truncate(clippingRect->left,TRUE);
		if(clippingRect->right<chunk->rect.right) chunk->truncate(clippingRect->right,FALSE);
	}
	//Its possible there is now no text in the chunk
	//Only insert it if there is text.
	if(chunk->text.length()>0) {
		insertChunk(chunk);
	} else {
		delete chunk;
	}
}

void displayModel_t::insertChunk(displayModelChunk_t* chunk) {
	chunksByYX[make_pair(chunk->rect.top+chunk->baselineFromTop,chunk->rect.left)]=chunk;
}

void displayModel_t::clearAll() {
	for(displayModelChunksByPointMap_t::iterator i=chunksByYX.begin();i!=chunksByYX.end();) {
		delete i->second;
		chunksByYX.erase(i++);
	}
}

void displayModel_t::clearRectangle(const RECT& rect, BOOL clearForText) {
	LOG_DEBUG(L"Clearing rectangle from "<<rect.left<<L","<<rect.top<<L" to "<<rect.right<<L","<<rect.bottom);
	set<displayModelChunk_t*> chunksForInsertion;
	displayModelChunksByPointMap_t::iterator i=chunksByYX.begin();
	RECT tempRect;
	while(i!=chunksByYX.end()) {
		displayModelChunksByPointMap_t::iterator nextI=i;
		nextI++; 
		displayModelChunk_t* chunk=i->second;
		int baseline=i->first.first;
		if(IntersectRect(&tempRect,&rect,&(chunk->rect))) {
			//The clearing rectangle intercects the chunk's rectangle in some way.
			if(tempRect.bottom<=baseline) {
				//The clearing rectangle some how covers the chunk below its baseline.
				//If we're clearing to make room for text, or the clearing rectangle starts from the very top of the chunk
				//Then we should shrink the chunk down so it stays below the clearing rectangle.
				//If not, then we pretend the clearRectangle did not happen (the chunk was only parcially cleared vertically so we don't care).
				if(clearForText||tempRect.top==chunk->rect.top) {
					chunk->rect.top=tempRect.bottom;
				}
			} else if(tempRect.top>baseline) {
				//The clearing rectangle some how covers the chunk above its baseline.
				//If we're clearing to make room for text, or the clearing rectangle starts from the very bottom of the chunk
				//Then we should shrink the chunk up so it stays above the clearing rectangle.
				//If not, then we pretend the clearRectangle did not happen (the chunk was only parcially cleared vertically so we don't care).
				if(clearForText||tempRect.bottom==chunk->rect.bottom) {
					chunk->rect.bottom=tempRect.top;
				}
			} else {
				//The clearing rectangle covers the chunk's baseline, so remove the part of the chunk covered horozontally by the clearing rectangle.
				if(tempRect.left==chunk->rect.left&&tempRect.right==chunk->rect.right) {
					chunksByYX.erase(i);
					delete chunk;
				} else if(tempRect.left>chunk->rect.left&&tempRect.right==chunk->rect.right) {
					chunk->truncate(tempRect.left,FALSE);
					if(chunk->text.length()==0) {
						chunksByYX.erase(i);
						delete chunk;
					}
				} else if(tempRect.right<chunk->rect.right&&tempRect.left==chunk->rect.left) {
					chunksByYX.erase(i);
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
						chunksByYX.erase(i);
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
		}
		i=nextI;
	}
	for(set<displayModelChunk_t*>::iterator i=chunksForInsertion.begin();i!=chunksForInsertion.end();i++) {
		insertChunk(*i);
	}
	LOG_DEBUG(L"complete");
}

void displayModel_t::copyRectangleToOtherModel(RECT& rect, displayModel_t* otherModel, BOOL clearEntireRectangle, int otherX, int otherY) {
	if(!otherModel) otherModel=this;
	set<displayModelChunk_t*> chunks;
	RECT tempRect;
	RECT clearRect=rect;
	int deltaX=otherX-rect.left;
	int deltaY=otherY-rect.top;
	//Shift the clearing rectangle so its where it is requested to be in the destination model
	clearRect.left+=deltaX;
	clearRect.top+=deltaY;
	clearRect.right+=deltaX;
	clearRect.bottom+=deltaY;
	//Clear the rectangle in the destination model to make space for the chunks
	if(clearEntireRectangle) otherModel->clearRectangle(clearRect);
	//Collect all the chunks that should be copied in to a temporary set, and expand the clearing rectangle to bound them all completely.
	for(displayModelChunksByPointMap_t::iterator i=chunksByYX.begin();i!=chunksByYX.end();i++) {
		if(IntersectRect(&tempRect,&rect,&(i->second->rect))) {
			chunks.insert(i->second);
		}
	}
	if(chunks.size()>0) {
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
				if(!clearEntireRectangle) otherModel->clearRectangle(chunk->rect);
				otherModel->insertChunk(chunk);
			}
		}
	}
}

void displayModel_t::renderText(const RECT& rect, int minHorizontalWhitespace, int minVerticalWhitespace, wstring& text, deque<RECT>& characterRects) {
	RECT tempRect;
	wstring curLineText;
	deque<RECT> curLineCharacterRects;
	int curLineMinTop=-1;
	int curLineMaxBottom=-1;
	int curLineBaseline=-1;
	int lastChunkRight=rect.left;
	int lastLineBottom=rect.top;
	//Walk through all the chunks looking for any that intersect the rectangle
	displayModelChunksByPointMap_t::iterator chunkIt=chunksByYX.begin();
	while(chunkIt!=chunksByYX.end()) {
		displayModelChunk_t* chunk=NULL;
		BOOL isTempChunk=FALSE;
		if(IntersectRect(&tempRect,&rect,&(chunkIt->second->rect))) {
			chunk=chunkIt->second;
			//If this chunk is not fully covered by the rectangle
			//Copy it and truncate it so that it is fully covered
			if(chunk->rect.left<tempRect.left||chunk->rect.right>tempRect.right) {
				chunk=new displayModelChunk_t(*chunk);
				isTempChunk=TRUE;
				if(chunk->rect.left<tempRect.left) chunk->truncate(tempRect.left,TRUE);
				if(chunk->rect.right>tempRect.right) chunk->truncate(tempRect.right,FALSE);
			}
		}
		//Find out the current line's baseline
		curLineBaseline=chunkIt->first.first;
		//Iterate to the next possible chunk
		++chunkIt;
		//If we have a valid chunk then add it to the current line
		if(chunk&&chunk->text.length()>0) {
			//Update the maximum height of the line
			if(curLineText.length()==0) {
				curLineMinTop=chunk->rect.top;
				curLineMaxBottom=chunk->rect.bottom;
			} else {
				if(chunk->rect.top<curLineMinTop) curLineMinTop=chunk->rect.top;
				if(chunk->rect.bottom>curLineMaxBottom) curLineMaxBottom=chunk->rect.bottom;
			}
			//Add space before this chunk if necessary
			if((chunk->rect.left-lastChunkRight)>=minHorizontalWhitespace) {
				curLineText+=L" ";
				tempRect.left=lastChunkRight;
				tempRect.top=curLineBaseline-1;
				tempRect.right=chunk->rect.left;
				tempRect.bottom=curLineBaseline+1;
				curLineCharacterRects.push_back(tempRect);
			}
			//Add text from this chunk to the current line
			curLineText.append(chunk->text);
			//Copy the character X positions from this chunk  in to the current line
			deque<int>::const_iterator cxaIt=chunk->characterXArray.begin();
			while(cxaIt!=chunk->characterXArray.end()) {
				tempRect.left=*cxaIt;
				tempRect.top=chunk->rect.top;
				++cxaIt;
				tempRect.right=(cxaIt!=chunk->characterXArray.end())?*cxaIt:chunk->rect.right;
				tempRect.bottom=chunk->rect.bottom;
				curLineCharacterRects.push_back(tempRect);
			}
		lastChunkRight=chunk->rect.right;
		}
		if((chunkIt==chunksByYX.end()||chunkIt->first.first>curLineBaseline)&&curLineText.length()>0) {
			//This is the end of the line
			if((curLineMinTop-lastLineBottom)>=minVerticalWhitespace) {
				//There is space between this line and the last,
				//Insert a blank line in between.
				text+=L"\n";
				tempRect.left=rect.left;
				tempRect.top=lastLineBottom;
				tempRect.right=rect.right;
				tempRect.bottom=curLineMinTop;
				characterRects.push_back(tempRect);
			}
			//Insert this line in to the output.
			text.append(curLineText);
			characterRects.insert(characterRects.end(),curLineCharacterRects.begin(),curLineCharacterRects.end());
			//Add a linefeed to complete the line
			text+=L"\n";
			tempRect.left=lastChunkRight;
			tempRect.top=curLineBaseline-1;
			tempRect.right=rect.right;
			tempRect.bottom=curLineBaseline+1;
			characterRects.push_back(tempRect);
			//Reset the current line values
			curLineText.clear();
			curLineCharacterRects.clear();
			lastChunkRight=rect.left;
			lastLineBottom=curLineMaxBottom;
			if(chunk&&isTempChunk) delete chunk;
		}
	}
	if((rect.bottom-lastLineBottom)>=minVerticalWhitespace) {
		//There is a gap between the bottom of the final line and the bottom of the requested rectangle,
		//So add a blank line.
		text+=L"\n";
		tempRect.left=rect.left;
		tempRect.top=lastLineBottom;
		tempRect.right=rect.right;
		tempRect.bottom=rect.bottom;
		characterRects.push_back(tempRect);
	}
}
