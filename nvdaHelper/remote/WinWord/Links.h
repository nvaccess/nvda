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
#ifndef WINWORD_LINKS_H
#define WINWORD_LINKS_H

#define WIN32_LEAN_AND_MEAN 
#include <vector>

struct IDispatch;
namespace WinWord {

	typedef std::pair<int, int> range;

	class Links {
	public:
		/**
		* Ctor
		* @param pRange the range to get link information for. All subsequent queries will be on
		*        sub-ranges of this. Most likely, this range should be the paragraph.
		*/
		Links(IDispatch* pRange);

		/*
		* Are there any links that given range intersects with.
		* @param rangeStart start of range to look for links in
		* @param rangeEnd end of the range to look for links in
		* @remarks should be a subset of the range given on construction, otherwise the function is likely to be inaccurate.
		*/
		bool hasLinks(const int rangeStart, const int rangeEnd);

		/*
		* Are there any links in the original range
		*/
		bool hasLinks();

		Links(const Links&) = delete; // Copy constructor disabled, no implementation.
		Links& operator=(const Links&) = delete; // Assignment disabled, no implementation.
	private:
		std::vector<range> m_links; ///< The links contained in the paragraph

	};
}

#endif