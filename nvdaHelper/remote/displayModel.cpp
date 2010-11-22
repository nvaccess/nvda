/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2010 NVDA contributers.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <cassert>
#include <string>
#include <sstream>
#include <deque>
#include <list>
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
		for(;t!=text.end()&&(*c)<truncatePointX;++c,++t);
		if(c!=characterXArray.end()) rect.left=*c; else rect.left=rect.right; 
		characterXArray.erase(characterXArray.begin(),c);
		text.erase(text.begin(),t);
	} else if(!truncateBefore&&truncatePointX<rect.right) {
		for(;t!=text.end()&&(*c)<=truncatePointX;++c,++t);
		if(t!=text.begin()) {
			--c;
			--t;
		}
		rect.right=*c;
		characterXArray.erase(c,characterXArray.end());
		text.erase(t,text.end());
	}
}

displayModel_t::displayModel_t(): LockableAutoFreeObject(), chunksByYX() {
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
	for(int i=0;i<(text.length()-1);++i) chunk->characterXArray.push_back(characterEndXArray[i]+rect.left); 
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
		++nextI; 
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
	for(set<displayModelChunk_t*>::iterator i=chunksForInsertion.begin();i!=chunksForInsertion.end();++i) {
		insertChunk(*i);
	}
	LOG_DEBUG(L"complete");
}

void displayModel_t::copyRectangle(const RECT& srcRect, BOOL removeFromSource, BOOL opaqueCopy, int destX, int destY, const RECT* destClippingRect, displayModel_t* destModel) {
	if(!destModel) destModel=this;
	RECT tempRect;
	int deltaX=destX-srcRect.left;
	int deltaY=destY-srcRect.top;
	RECT destRect={srcRect.left+deltaX,srcRect.top+deltaY,srcRect.right+deltaX,srcRect.bottom+deltaY};
	//If a clipping rectangle is provided, clip the destination rectangle
	if(destClippingRect) {
		IntersectRect(&tempRect,&destRect,destClippingRect);
		destRect=tempRect;
	}
	//Make copies of all the needed chunks, tweek their rectangle coordinates, truncate if needed, and store them in a temporary list
	list<displayModelChunk_t*> copiedChunks;
	for(displayModelChunksByPointMap_t::iterator i=chunksByYX.begin();i!=chunksByYX.end();++i) {
		//We only care about chunks that are overlapped by the source rectangle 
		if(!IntersectRect(&tempRect,&srcRect,&(i->second->rect))) continue; 
		//Copy the chunk
		displayModelChunk_t* chunk=new displayModelChunk_t(*(i->second));
		//Tweek its rectangle coordinates to match where its going in the destination model
		(chunk->rect.left)+=deltaX;
		(chunk->rect.top)+=deltaY;
		(chunk->rect.right)+=deltaX;
		(chunk->rect.bottom)+=deltaY;
		//Tweek its character x coordinates to match where its going in the destination model
		for(deque<int>::iterator x=chunk->characterXArray.begin();x!=chunk->characterXArray.end();++x) (*x)+=deltaX;
		//Truncate the chunk so it does not stick outside of the destination rectangle
		if(chunk->rect.left<destRect.left) {
			chunk->truncate(destRect.left,TRUE);
		}
		if(chunk->rect.right>destRect.right) {
			chunk->truncate(destRect.right,FALSE);
		}
		//if the chunk is now empty due to truncation then just delete it and move on to the next 
		if(chunk->text.length()==0) {
			delete chunk;
			continue;
		}
		//Insert the chunk in to the temporary list
		copiedChunks.insert(copiedChunks.end(),chunk);
	}
	//Clear the source rectangle if requested to do so (move rather than copy)
	if(removeFromSource) this->clearRectangle(srcRect);
	//Clear the entire destination rectangle if requested to do so
	if(opaqueCopy) destModel->clearRectangle(destRect);
	//insert the copied chunks in to the destination model
	for(list<displayModelChunk_t*>::iterator i=copiedChunks.begin();i!=copiedChunks.end();++i) {
		if(!opaqueCopy) destModel->clearRectangle((*i)->rect);
		destModel->insertChunk(*i);
	}
}

void displayModel_t::renderText(const RECT& rect, const int minHorizontalWhitespace, const int minVerticalWhitespace, const bool stripOuterWhitespace, wstring& text, deque<RECT>& characterRects) {
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
			if(((chunk->rect.left-lastChunkRight)>=minHorizontalWhitespace)&&(lastChunkRight>rect.left||!stripOuterWhitespace)) {
				curLineText+=L'\0';
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
			if(((curLineMinTop-lastLineBottom)>=minVerticalWhitespace)&&(lastLineBottom>rect.top||!stripOuterWhitespace)) {
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
	if(!stripOuterWhitespace&&(rect.bottom-lastLineBottom)>=minVerticalWhitespace) {
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
