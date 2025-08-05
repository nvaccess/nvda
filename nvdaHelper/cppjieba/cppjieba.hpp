/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2025 NV Access Limited, Wang Chong.
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License version 2.0, as published by
	the Free Software Foundation.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#ifndef CPPJIEBA_DLL_H
#define CPPJIEBA_DLL_H
#pragma once

#include <vector>
#include <string>
#include <mutex>
#include <cstdlib>
#include "Jieba.hpp"

#ifdef _WIN32
#  define JIEBA_API __declspec(dllexport)
#else
#  define JIEBA_API
#endif

using namespace std;

/// @brief Singleton wrapper around cppjieba::Jieba.
class JiebaSingleton : public cppjieba::Jieba {
public:
    /// @brief Returns the single instance, constructing on first call.
    static JiebaSingleton& getInstance();

    /// @brief Do thread-safe segmentation and compute character end offsets.
	/// @param text The input text in UTF-8 encoding.
	/// @param charOffsets Output vector to hold character offsets.
    void getOffsets(const string& text, vector<int>& charOffsets);

private:
    JiebaSingleton();         ///< private ctor initializes base Jieba

	/// Disable copy and move
	JiebaSingleton(const JiebaSingleton&) = delete;
	JiebaSingleton& operator = (const JiebaSingleton&) = delete;
	JiebaSingleton(JiebaSingleton&&) = delete;
	JiebaSingleton& operator = (JiebaSingleton&&) = delete;

    std::mutex segMutex;      ///< guards concurrent Cut() calls
};

extern "C" {

/// @brief Force singleton construction (load dicts, etc.) before any segmentation.
/// @return 0 on success, -1 on failure.
JIEBA_API int initJieba();

/// @brief Segment UTF-8 text into character offsets.
/// @return 0 on success, -1 on failure.
JIEBA_API int segmentOffsets(const char* text, int** charOffsets, int* outLen);

/// @brief Free memory allocated by segmentOffsets.
JIEBA_API void freeOffsets(int* ptr);

} // extern "C"

#endif // CPPJIEBA_DLL_H
