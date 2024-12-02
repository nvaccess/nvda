/*
 * liblouis/liblouis#1685: liblouis started using strncasecmp, which is not available on Windows.
 * Neither can Gnulib be used with NVDA's buildssystem.
 * Therefore, use _strnicmp as a drop-in replacement.
*/

#define strncasecmp _strnicmp
