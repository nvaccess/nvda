#ifndef NVDAHELPERREMOTE_INPROCESS_H
#define NVDAHELPERREMOTE_INPROCESS_H

//in-process hook callbacks
void CALLBACK inProcess_winEventCallback(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time);
LRESULT CALLBACK inProcess_getMessageHook(int code, WPARAM wParam, LPARAM lParam);
LRESULT CALLBACK inProcess_callWndProcHook(int code, WPARAM wParam,LPARAM lParam);

//Initialization / termination
void inProcess_initialize();
void inProcess_terminate();

#include <functional>
typedef std::function<void()> execInThread_funcType;
bool execInThread(long threadID, execInThread_funcType func);


#endif
