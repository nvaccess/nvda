/**
 * base/libEntry.h
 * Part of the NV  Virtual Buffer Library
 * This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
 * This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
 * http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
 */

#ifndef VIRTUALBUFFER_LIBENTRY_H
#define VIRTUALBUFFER_LIBENTRY_H

#ifdef _WIN32
#ifdef VBUFLIBENTRYTYPE
#if VBUFLIBENTRYTYPE==1
#define VBUFLIBENTRY __declspec(dllexport)
#elif VBUFLIBENTRYTYPE==2
#define VBUFLIBENTRY __declspec(dllimport)
#endif
#else
#define VBUFLIBENTRY
#endif
#endif

#ifdef _POSIX
#define VBUFLIBENTRY 
#endif

#endif
