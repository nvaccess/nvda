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

JiebaSingleton::JiebaSingleton(): cppjieba::JiebaSegmenter() { } // call base ctor to load dictionaries, models, etc.

void JiebaSingleton::getWordEndOffsets(const std::string& text, std::vector<int>& wordEndOffsets) {
    std::lock_guard<std::mutex> lock(segMutex);
    std::vector<cppjieba::Word> words;
    this->Cut(text, words, true);

    for (auto const& word : words) {
        wordEndOffsets.push_back(word.unicode_offset + word.unicode_length);
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

bool calculateWordOffsets(const char* text, int** wordEndOffsets, int* outLen) {
    if (!text || !wordEndOffsets || !outLen) return false;
    // we assume initJieba() has already been called successfully

    std::string textStr(text);
    std::vector<int> offs;
    JiebaSingleton::getInstance().getWordEndOffsets(textStr, offs);

    int n = static_cast<int>(offs.size());
    int* buf = static_cast<int*>(std::malloc(sizeof(int) * n));
    if (!buf) {
        *outLen = 0;
        return false;
    }
    for (int i = 0; i < n; ++i) buf[i] = offs[i];
    *wordEndOffsets = buf;
    *outLen = n;
    return true;
}

bool insertUserWord(const char* word, int freq, const char* tag = cppjieba::UNKNOWN_TAG) {
	return JiebaSingleton::getInstance().InsertUserWord(string(word), freq, string(tag));
}

bool deleteUserWord(const char* word, const char* tag = cppjieba::UNKNOWN_TAG) {
	return JiebaSingleton::getInstance().DeleteUserWord(string(word), string(tag));
}

bool find(const char* word) {
	return JiebaSingleton::getInstance().Find(string(word));
}

void freeOffsets(int* ptr) {
    if (ptr) free(ptr);
}

} // extern "C"
