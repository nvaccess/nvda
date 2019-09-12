/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2019 NV Access Limited, Babbage B.V.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#include "gdiUtils.h"

void logicalPointsToScreenPoints(HDC hdc, POINT* points, int count,bool relative) {
	//Convert from logical points to device points 
	//Includes origins and scaling for window and viewport, and also world transformation 
	LPtoDP(hdc,points,count);
	if(relative) {
		//Do what we did with the points, but with 0,0, and then subtract that from all points
		POINT origPoint={0,0};
		LPtoDP(hdc,&origPoint,1);
		for(int i=0;i<count;++i) {
			points[i].x-=origPoint.x;
			points[i].y-=origPoint.y;
		}
	} else { //absolute
		//LptoDp does not take the final DC origin in to account, so plus that to all points here to make them completely screen absolute
		POINT dcOrgPoint;
		GetDCOrgEx(hdc,&dcOrgPoint);
		for(int i=0;i<count;++i) {
			points[i].x+=dcOrgPoint.x;
			points[i].y+=dcOrgPoint.y;
		}
	}
}

void screenPointsToLogicalPoints(HDC hdc, POINT* points, int count) {
	//Convert from device points to logical points
	//Includes origins and scaling for window and viewport, and also world transformation 
	DPtoLP(hdc,points,count);
	//DPToLP does not take the final DC origin in to account, so subtract that from all points
	POINT dcOrgPoint;
	GetDCOrgEx(hdc,&dcOrgPoint);
	for(int i=0;i<count;++i) {
		points[i].x-=dcOrgPoint.x;
		points[i].y-=dcOrgPoint.y;
	}
}
