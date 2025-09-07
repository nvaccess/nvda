/*
A part of NonVisual Desktop Access (NVDA)
Copyright (C) 2025 NV Access Limited, Wang Chong
This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
*/

#ifndef CPPJIEBA_DLL_H
#define CPPJIEBA_DLL_H
#pragma once

#include <vector>
#include <string>
#include <cstring>
#include <mutex>
#include <cstdlib>
#include "QuerySegment.hpp"

using namespace std;

namespace cppjieba {  // copied from Jieba.hpp and modified to drop off its keyword extractor we don't use

class JiebaSegmenter {
 public:
  JiebaSegmenter(const string& dict_path = "",
        const string& model_path = "",
        const string& user_dict_path = "")
    : dict_trie_(getPath(dict_path, "jieba.dict.utf8"), getPath(user_dict_path, "user.dict.utf8")),
      model_(getPath(model_path, "hmm_model.utf8")),
      mix_seg_(&dict_trie_, &model_) {
  }
  ~JiebaSegmenter() {
  }

  void Cut(const string& sentence, vector<Word>& words, bool hmm = true) const {
    mix_seg_.Cut(sentence, words, hmm);
  }

  bool InsertUserWord(const string& word,int freq, const string& tag = UNKNOWN_TAG) {
    return dict_trie_.InsertUserWord(word,freq, tag);
  }

  bool DeleteUserWord(const string& word, const string& tag = UNKNOWN_TAG) {
    return dict_trie_.DeleteUserWord(word, tag);
  }

  bool Find(const string& word)
  {
    return dict_trie_.Find(word);
  }

  void ResetSeparators(const string& s) {
    mix_seg_.ResetSeparators(s);
  }

  const DictTrie* GetDictTrie() const {
    return &dict_trie_;
  }

  const HMMModel* GetHMMModel() const {
    return &model_;
  }

  void LoadUserDict(const vector<string>& buf)  {
    dict_trie_.LoadUserDict(buf);
  }

  void LoadUserDict(const set<string>& buf)  {
    dict_trie_.LoadUserDict(buf);
  }

  void LoadUserDict(const string& path)  {
    dict_trie_.LoadUserDict(path);
  }

 private:
  static string pathJoin(const string& dir, const string& filename) {
    if (dir.empty()) {
        return filename;
    }

    char last_char = dir[dir.length() - 1];
    if (last_char == '/' || last_char == '\\') {
        return dir + filename;
    } else {
        #ifdef _WIN32
        return dir + '\\' + filename;
        #else
        return dir + '/' + filename;
        #endif
    }
  }

  static string getCurrentDirectory() {
    string path(__FILE__);
    size_t pos = path.find_last_of("/\\");
    return (pos == string::npos) ? "" : path.substr(0, pos);
  }

  static string getPath(const string& path, const string& default_file) {
    if (path.empty()) {
      string current_dir = getCurrentDirectory();
      string parent_dir = current_dir.substr(0, current_dir.find_last_of("/\\"));
      string grandparent_dir = parent_dir.substr(0, parent_dir.find_last_of("/\\"));
      string root_dir = grandparent_dir.substr(0, grandparent_dir.find_last_of("/\\"));
      return pathJoin(pathJoin(pathJoin(root_dir, "include\\cppjieba"), "dict"), default_file);
    }
    return path;
  }

  DictTrie dict_trie_;
  HMMModel model_;

  MixSegment mix_seg_;
}; // class JiebaSegmenter

} // namespace cppjieba


/// @brief Singleton wrapper around cppjieba::Jieba.
class JiebaSingleton : public cppjieba::JiebaSegmenter {
public:
    /// @brief Returns the single instance, constructing on first call.
    static JiebaSingleton& getInstance();

    /// @brief Do thread-safe segmentation and compute word end offsets.
	/// @param text The input text in UTF-8 encoding.
	/// @param wordEndOffsets Output vector to hold word offsets.
    void getOffsets(const string& text, vector<int>& wordEndOffsets);

private:
    JiebaSingleton();         ///< private ctor initializes base Jieba

	/// Disable copy and move
	JiebaSingleton(const JiebaSingleton&) = delete;
	JiebaSingleton& operator = (const JiebaSingleton&) = delete;
	JiebaSingleton(JiebaSingleton&&) = delete;
	JiebaSingleton& operator = (JiebaSingleton&&) = delete;

    std::mutex segMutex;      ///< guards concurrent Cut() calls
};

#ifdef _WIN32
#  define JIEBA_API __declspec(dllexport)
#else
#  define JIEBA_API
#endif

extern "C" {

/// @brief Force singleton construction (load dicts, etc.) before any segmentation.
/// @return 0 on success, -1 on failure.
JIEBA_API int initJieba();

/// @brief Segment UTF-8 text into character offsets.
/// @return 0 on success, -1 on failure.
JIEBA_API int segmentOffsets(const char* text, int** wordEndOffsets, int* outLen);

/// Wrapper for word management
JIEBA_API bool insertUserWord(const char* word, int freq, const char* tag);
JIEBA_API bool deleteUserWord(const char* word, const char* tag);
JIEBA_API bool find(const char* word);

/// @brief Free memory allocated by segmentOffsets.
JIEBA_API void freeOffsets(int* ptr);

} // extern "C"

#endif // CPPJIEBA_DLL_H
