/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2021 NV Access Limited, Julien Nabet
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include <string>
#include <sstream>
#include <deque>
#include <list>
#include <set>
#include <algorithm>
#include <common/xml.h>
#include <remote/nvdaControllerInternal.h>
#include <common/log.h>
#include "displayModel.h"

using namespace std;


std::wostream& operator<<(std::wostream& out, displayModelFormatColor_t const& color) {
	// pack into a 4 byte DWORD: 0xTTbbggrr
	// TT bit flags, only bit 1 used: set for transparent.
	// Encoding alpha in TT was considered (eg 0xaabbggrr for aa == 0xFF for opaque),
	// but this would break compatibility with code that continues to pass
	// 0x00bbggrr for opaque, all usages would need to be fixed.
	COLORREF packed = RGB(color.red, color.green, color.blue);
	packed |= color.isTransparent ?
		displayModelFormatColor_t::TRANSPARENT_BIT
		:
		0;
	return out << packed;
}

void displayModelChunk_t::generateXML(wstring& text) {
	wstringstream s;
	s<<L"<text ";
	s<<L"hwnd=\""<<hwnd<<L"\" ";
	s<<L"baseline=\""<<baseline<<L"\" ";
	s<<L"direction=\""<<direction<<L"\" ";
	s<<L" font-name=\""<<formatInfo.fontName<<L"\" ";
	s<<L" font-size=\""<<formatInfo.fontSize<<L"pt\" ";
	if(this->formatInfo.bold) s<<L" bold=\"true\"";
	if(this->formatInfo.italic) s<<L" italic=\"true\"";
	if(this->formatInfo.underline) s<<L" underline=\"true\"";
	s<<L" color=\""<<this->formatInfo.color<<L"\"";
	s<<L" background-color=\""<<this->formatInfo.backgroundColor<<L"\"";
	s<<L">";
	text.append(s.str());
	for(wstring::iterator i=this->text.begin();i!=this->text.end();++i) appendCharToXML(*i,text);
	text.append(L"</text>");
}

void displayModelChunk_t::truncate(int truncatePointX, BOOL truncateBefore) {
	if(text.length()==0) return;
	nhAssert(characterXArray.size()!=0);
	deque<long>::iterator c=characterXArray.begin();
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

displayModel_t::displayModel_t(HWND w): LockableAutoFreeObject(), chunksByYX(), hwnd(w), focusRect(NULL)  {
	LOG_DEBUG(L"created instance at "<<this);
}

displayModel_t::~displayModel_t() {
	LOG_DEBUG(L"destroying instance at "<<this);
	for(displayModelChunksByPointMap_t::iterator i=chunksByYX.begin();i!=chunksByYX.end();) {
		LOG_DEBUG(L"deleting chunk at "<<i->second);
		delete i->second;
		chunksByYX.erase(i++);
	}
	setFocusRect(NULL);
}

size_t displayModel_t::getChunkCount() {
	return chunksByYX.size();
}

void displayModel_t::insertChunk(const RECT& rect, int baseline, const wstring& text, POINT* characterExtents, const displayModelFormatInfo_t& formatInfo, int direction, const RECT* clippingRect) {
	displayModelChunk_t* chunk=new displayModelChunk_t;
	LOG_DEBUG(L"created new chunk at "<<chunk);
	chunk->rect=rect;
	chunk->baseline=baseline;
	chunk->text=text;
	chunk->formatInfo=formatInfo;
	chunk->direction=direction;
	chunk->characterXArray.push_back(rect.left);
	for(unsigned int i=0;i<(text.length()-1);++i) chunk->characterXArray.push_back(characterExtents[i].x+rect.left); 
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
	chunksByYX[make_pair(chunk->baseline,chunk->rect.left)]=chunk;
	if(hwnd) chunk->hwnd=hwnd; 
}

void displayModel_t::setFocusRect(const RECT* rect) {
	if(!rect&&this->focusRect) {
		delete this->focusRect;
		this->focusRect=NULL;
	} else if(rect) {
		if(!this->focusRect) this->focusRect=new RECT;
		memcpy(this->focusRect,rect,sizeof(RECT));
	}
}

bool displayModel_t::getFocusRect(RECT* rect) {
	if(!rect||!this->focusRect) return false;
	memcpy(rect,this->focusRect,sizeof(RECT));
	return true;
}

void displayModel_t::clearAll() {
	for(displayModelChunksByPointMap_t::iterator i=chunksByYX.begin();i!=chunksByYX.end();) {
		delete i->second;
		chunksByYX.erase(i++);
	}
	setFocusRect(NULL);
}

void displayModel_t::clearRectangle(const RECT& rect, BOOL clearForText) {
	LOG_DEBUG(L"Clearing rectangle from "<<rect.left<<L","<<rect.top<<L" to "<<rect.right<<L","<<rect.bottom);
	set<displayModelChunk_t*> chunksForInsertion;
	displayModelChunksByPointMap_t::iterator i=chunksByYX.begin();
	RECT tempRect;
	//If the rectangle we are clearing completely covers any current focus rectangle, then get rid of the focus rectangle.
	if(focusRect&&IntersectRect(&tempRect,&rect,focusRect)&&EqualRect(&tempRect,focusRect)) {
		setFocusRect(NULL);
	}
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

void displayModel_t::copyRectangle(const RECT& srcRect, BOOL removeFromSource, BOOL opaqueCopy, BOOL srcInvert, const RECT& destRect, const RECT* destClippingRect, displayModel_t* destModel) {
	//Make sure neither source or destination rectangle is collapsed. Pointless and can cause zero division errors. #2885 
	if(srcRect.left==srcRect.right||srcRect.top==srcRect.bottom||destRect.left==destRect.right||destRect.top==destRect.bottom) return;
	if(!destModel) destModel=this;
	RECT tempRect;
	float scaleX=(float)(destRect.right-destRect.left)/(float)(srcRect.right-srcRect.left);
	float scaleY=(float)(destRect.bottom-destRect.top)/(float)(srcRect.bottom-srcRect.top);
	//If a clipping rectangle is provided, clip the destination rectangle
	RECT clippedDestRect=destRect;
	if(destClippingRect) {
		IntersectRect(&clippedDestRect,&destRect,destClippingRect);
	}
	//Make copies of all the needed chunks, tweek their rectangle coordinates, truncate if needed, and store them in a temporary list
	list<displayModelChunk_t*> copiedChunks;
	for(displayModelChunksByPointMap_t::iterator i=chunksByYX.begin();i!=chunksByYX.end();++i) {
		//We only care about chunks that are overlapped by the source rectangle 
		if(!IntersectRect(&tempRect,&srcRect,&(i->second->rect))) continue; 
		//Copy the chunk
		displayModelChunk_t* chunk=new displayModelChunk_t(*(i->second));
		if(srcInvert) {
			chunk->formatInfo.color = chunk->formatInfo.color.inverted();
			chunk->formatInfo.backgroundColor = chunk->formatInfo.backgroundColor.inverted();
		}
		//Tweek its rectangle coordinates to match where its going in the destination model
		transposAndScaleCoordinate(srcRect.left,destRect.left,scaleX,chunk->rect.left);
		transposAndScaleCoordinate(srcRect.left,destRect.left,scaleX,chunk->rect.right);
		transposAndScaleCoordinate(srcRect.top,destRect.top,scaleY,chunk->rect.top);
		transposAndScaleCoordinate(srcRect.top,destRect.top,scaleY,chunk->rect.bottom);
		transposAndScaleCoordinate(srcRect.top,destRect.top,scaleY,chunk->baseline);
		//Tweek its character x coordinates to match where its going in the destination model
		for(deque<long>::iterator x=chunk->characterXArray.begin();x!=chunk->characterXArray.end();++x) transposAndScaleCoordinate(srcRect.left,destRect.left,scaleX,*x);
		//Truncate the chunk so it does not stick outside of the clipped destination rectangle
		if(chunk->rect.left<clippedDestRect.left) {
			chunk->truncate(clippedDestRect.left,TRUE);
		}
		if(chunk->rect.right>clippedDestRect.right) {
			chunk->truncate(clippedDestRect.right,FALSE);
		}
		//if the chunk is now empty due to truncation then just delete it and move on to the next 
		if(chunk->text.length()==0) {
			delete chunk;
			continue;
		}
		//Insert the chunk in to the temporary list
		copiedChunks.insert(copiedChunks.end(),chunk);
	}
	//Save the old source focus rectangle
	RECT* srcFocusRect=NULL;
	if(focusRect) {
		srcFocusRect=new RECT;
		*srcFocusRect=*focusRect;
	}
	//Clear the source rectangle if requested to do so (move rather than copy)
	if(removeFromSource) this->clearRectangle(srcRect);
	//Clear the entire destination rectangle if requested to do so
	if(opaqueCopy) destModel->clearRectangle(clippedDestRect);
	//insert the copied chunks in to the destination model
	for(list<displayModelChunk_t*>::iterator i=copiedChunks.begin();i!=copiedChunks.end();++i) {
		if(!opaqueCopy) destModel->clearRectangle((*i)->rect);
		destModel->insertChunk(*i);
	}
	// If a focus rectangle was also contained in the source area, copy the focus rectangle as well
	if(srcFocusRect) {
		if(IntersectRect(&tempRect,&srcRect,srcFocusRect)&&EqualRect(&tempRect,srcFocusRect)) {
			RECT newFocusRect=*srcFocusRect;
			transposAndScaleCoordinate(srcRect.left,destRect.left,scaleX,newFocusRect.left);
			transposAndScaleCoordinate(srcRect.left,destRect.left,scaleX,newFocusRect.right);
			transposAndScaleCoordinate(srcRect.top,destRect.top,scaleY,newFocusRect.top);
			transposAndScaleCoordinate(srcRect.top,destRect.top,scaleY,newFocusRect.bottom);
			if(IntersectRect(&tempRect,&clippedDestRect,&newFocusRect)&&EqualRect(&tempRect,&newFocusRect)) {
				destModel->setFocusRect(&newFocusRect);
			}
		}
		delete srcFocusRect;
	}
}

void displayModel_t::generateWhitespaceXML(HWND hwnd, long baseline, wstring& text) {
	wstringstream s;
	s<<L"<text ";
	s<<L"hwnd=\""<<hwnd<<L"\" ";
	s<<L"baseline=\""<<baseline<<L"\" ";
	s<<L">";
	text.append(s.str());
	text.append(L" ");
	text.append(L"</text>");
}

void displayModel_t::renderText(const RECT& rect, const int minHorizontalWhitespace, const int minVerticalWhitespace, const bool stripOuterWhitespace, wstring& text, deque<RECT>& characterLocations) {
	RECT tempCharLocation;
	RECT tempRect;
	wstring curLineText;
	deque<RECT> curLineCharacterLocations;
	int curLineMinTop=-1;
	int curLineMaxBottom=-1;
	int curLineBaseline=-1;
	int lastChunkRight=rect.left;
	HWND lastChunkHwnd=NULL;
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
				generateWhitespaceXML((chunk->hwnd==lastChunkHwnd)?lastChunkHwnd:hwnd,curLineBaseline,curLineText);
				tempCharLocation.left=lastChunkRight;
				tempCharLocation.top=curLineBaseline-1;
				tempCharLocation.right=chunk->rect.left;
				tempCharLocation.bottom=curLineBaseline+1;
				curLineCharacterLocations.push_back(tempCharLocation);
			}
			//Add text from this chunk to the current line
			chunk->generateXML(curLineText);
			//Copy the character X positions from this chunk  in to the current line
			deque<long>::const_iterator cxaIt=chunk->characterXArray.begin();
			deque<RECT>::iterator curLineCharacterLocationsOldEnd=curLineCharacterLocations.end();
			while(cxaIt!=chunk->characterXArray.end()) {
				tempCharLocation.left=*cxaIt;
				tempCharLocation.top=chunk->rect.top;
				++cxaIt;
				tempCharLocation.right=(cxaIt!=chunk->characterXArray.end())?*cxaIt:chunk->rect.right;
				tempCharLocation.bottom=chunk->rect.bottom;
				curLineCharacterLocations.push_back(tempCharLocation);
			}
			lastChunkRight=chunk->rect.right;
			lastChunkHwnd=chunk->hwnd;
		}
		if((chunkIt==chunksByYX.end()||chunkIt->first.first>curLineBaseline)&&curLineText.length()>0) {
			//This is the end of the line
			if(((curLineMinTop-lastLineBottom)>=minVerticalWhitespace)&&(lastLineBottom>rect.top||!stripOuterWhitespace)) {
				//There is space between this line and the last,
				//Insert a blank line in between.
				generateWhitespaceXML(hwnd,-1,text);
				tempCharLocation.left=rect.left;
				tempCharLocation.top=lastLineBottom;
				tempCharLocation.right=rect.right;
				tempCharLocation.bottom=curLineMinTop;
				characterLocations.push_back(tempCharLocation);
			}
			//Insert this line in to the output.
			text.append(curLineText);
			characterLocations.insert(characterLocations.end(),curLineCharacterLocations.begin(),curLineCharacterLocations.end());
			//Add a linefeed to complete the line
			if(!stripOuterWhitespace) {
				generateWhitespaceXML(hwnd,curLineBaseline,text);
				tempCharLocation.left=lastChunkRight;
				tempCharLocation.top=curLineBaseline-1;
				tempCharLocation.right=rect.right;
				tempCharLocation.bottom=curLineBaseline+1;
				characterLocations.push_back(tempCharLocation);
			}
			//Reset the current line values
			curLineText.clear();
			curLineCharacterLocations.clear();
			lastChunkRight=rect.left;
			lastChunkHwnd=NULL;
			lastLineBottom=curLineMaxBottom;
			if(chunk&&isTempChunk) delete chunk;
		}
	}
	if(!stripOuterWhitespace&&(rect.bottom-lastLineBottom)>=minVerticalWhitespace) {
		//There is a gap between the bottom of the final line and the bottom of the requested rectangle,
		//So add a blank line.
		generateWhitespaceXML(hwnd,-1,text);
		tempCharLocation.left=rect.left;
		tempCharLocation.top=lastLineBottom;
		tempCharLocation.right=rect.right;
		tempCharLocation.bottom=rect.bottom;
		characterLocations.push_back(tempCharLocation);
	}
}
