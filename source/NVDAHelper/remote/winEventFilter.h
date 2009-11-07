//Copyright (c) 2009 Aleksey Sadovoy <lex@progger.ru>
//This file is covered by the GNU General Public Licence

#ifndef WINEventFILTER_H
#define WINEventFILTER_H

bool winEventFilter_initialize();
void winEventFilter_terminate();
void winEventFilter_inProcess_initialize();
void winEventFilter_inProcess_terminate();

#endif