/*
A part of NonVisual Desktop Access (NVDA)
Copyright (C) 2025 NV Access Limited, Wang Chong
This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
*/

#include "cppjieba.hpp"

JiebaSingleton& JiebaSingleton::getInstance() {
    // C++11 guarantees thread-safe init of this local static
    static JiebaSingleton instance;
    return instance;
}

JiebaSingleton::JiebaSingleton(): cppjieba::Jieba() { } // call base ctor to load dictionaries, models, etc.

void JiebaSingleton::getOffsets(const std::string& text, std::vector<int>& charOffsets) {
    std::lock_guard<std::mutex> lock(segMutex);
    std::vector<std::string> words;
    this->Cut(text, words, true);

    int cumulative = 0;
    for (auto const& w : words) {
        int wc = 0;
        auto ptr = reinterpret_cast<const unsigned char*>(w.c_str());
        size_t i = 0, len = w.size();
        while (i < len) {
            unsigned char c = ptr[i];
            if      ((c & 0x80) == 0)      i += 1;
            else if ((c & 0xE0) == 0xC0)   i += 2;
            else if ((c & 0xF0) == 0xE0)   i += 3;
            else if ((c & 0xF8) == 0xF0)   i += 4;
            else                           i += 1;
            ++wc;
        }
        cumulative += wc;
        charOffsets.push_back(cumulative);
    }
}

extern "C" {

int initJieba() {
    try {
        // simply force the singleton into existence
        (void)JiebaSingleton::getInstance();
        return 0;
    } catch (...) {
        return -1;
    }
}

int segmentOffsets(const char* text, int** charOffsets, int* outLen) {
    if (!text || !charOffsets || !outLen) return -1;
    // we assume initJieba() has already been called successfully

    std::string input(text);
    std::vector<int> offs;
    JiebaSingleton::getInstance().getOffsets(input, offs);

    int n = static_cast<int>(offs.size());
    int* buf = static_cast<int*>(std::malloc(sizeof(int) * n));
    if (!buf) {
        *outLen = 0;
        return -1;
    }
    for (int i = 0; i < n; ++i) buf[i] = offs[i];
    *charOffsets = buf;
    *outLen = n;
    return 0;
}

void freeOffsets(int* ptr) {
    if (ptr) free(ptr);
}

} // extern "C"
