/*
A part of NonVisual Desktop Access (NVDA)
Copyright (C) 2025 NV Access Limited, Wang Chong
This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
*/

#include "cppjieba.hpp"


using namespace std;

// static members for singleton bookkeeping
JiebaSingleton* JiebaSingleton::instance = nullptr;
std::once_flag JiebaSingleton::initFlag;

JiebaSingleton& JiebaSingleton::getInstance(const char* dictDir) {
    // convert incoming C-string+length to std::string (handles dictDir == nullptr)
    std::string dir = dictDir;

    // ensure singleton is constructed exactly once
    std::call_once(JiebaSingleton::initFlag, [&]() {
        // allocate on heap, so we avoid copy/move and control lifetime
        JiebaSingleton::instance = new JiebaSingleton(dir.c_str());
        // optional: register deleter at exit
        std::atexit([]() {
            delete JiebaSingleton::instance;
            JiebaSingleton::instance = nullptr;
        });
    });

    // after call_once, instance must be non-null
    return *JiebaSingleton::instance;
}

JiebaSingleton& JiebaSingleton::getInstance() {
    if (!JiebaSingleton::instance) {
        throw std::runtime_error("JiebaSingleton::getInstance() called before initialization. Call getInstance(dictDir) or initJieba() first.");
    }
    return *JiebaSingleton::instance;
}

JiebaSingleton::JiebaSingleton(const char* dictDir)
: cppjieba::JiebaSegmenter(
    std::string(dictDir),
    std::string(dictDir),
    std::string(dictDir)
  )
{
    // base class ctor will load dictionaries/models
}

void JiebaSingleton::getWordEndOffsets(const std::string& text, std::vector<int>& wordEndOffsets) {
    std::lock_guard<std::mutex> lock(segMutex);
    wordEndOffsets.clear();
    std::vector<cppjieba::Word> words;
    this->Cut(text, words, true);

    for (const auto& word : words) {
        wordEndOffsets.push_back(word.unicode_offset + word.unicode_length);
    }
}

extern "C" {

bool initJieba(const char* dictDir) {
    try {
        // simply force the singleton into existence
        (void)JiebaSingleton::getInstance(dictDir);
        return true;
    } catch (...) {
        return false;
    }
}

bool calculateWordOffsets(const char* text, int** wordEndOffsets, int* outLen) {
    if (!text || !wordEndOffsets || !outLen) return false;

    try {
        std::string textStr(text);
        std::vector<int> offs;
        JiebaSingleton::getInstance().getWordEndOffsets(textStr, offs);

        int n = static_cast<int>(offs.size());
        if (n == 0) {
            *wordEndOffsets = nullptr;
            *outLen = 0;
            return true; // success, but no offsets
        }

        int* buf = static_cast<int*>(std::malloc(sizeof(int) * n));
        if (!buf) {
            *wordEndOffsets = nullptr;
            *outLen = 0;
            return false;
        }
        for (int i = 0; i < n; ++i) buf[i] = offs[i];
        *wordEndOffsets = buf;
        *outLen = n;
        return true;
    } catch (...) {
        *wordEndOffsets = nullptr;
        *outLen = 0;
        return false;
    }
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
    if (ptr) std::free(ptr);
}

} // extern "C"
