/**
 * A part of NonVisual Desktop Access (NVDA)
 * This file is covered by the GNU General Public License.
 * See the file COPYING for more details.
 * Copyright (C) 2025 NV Access Limited
 *
 * Utilities for Remote Access.
 *
 * Must be linked with Iphlpapi.lib and Ws2_32.lib.
*/
#include <iostream>
#include <memory>
#include <filesystem>
#include <WinSock2.h>
#include <iphlpapi.h>
#include <windows.h>
#include <wil/resource.h>
#include <common/log.h>

using namespace std;
using namespace filesystem;

/**
 * @brief Checks if a local listening socket exists on the specified port and is owned by the specified process.
 *
 * This function iterates through the system's TCP table to determine if there is a listening socket
 * on the given port (bound to 127.0.0.1) that is owned by the process with the specified executable path.
 *
 * @param port The port number to check for a listening socket. Must be in host byte order.
 * @param owningProcImgName The full path to the executable of the process that should own the socket.
 *
 * @return true if a matching listening socket exists, false otherwise.
 *         Returns false in case of unrecoverable error.
 *
 * @note The function performs the following checks:
 *       - The specified executable path must exist.
 *       - The socket must be in the LISTEN state.
 *       - The socket's local address must be loopback (127.0.0.1).
 *       - The socket's local port number must match the specified port.
 *       - The socket's owning process image must match the given path.
 *
 * @remarks The function uses `GetExtendedTcpTable` to retrieve the TCP table and compares
 *          the owning process's executable path using `QueryFullProcessImageNameW`.
 *          It also handles potential errors such as insufficient buffer size, invalid process handles,
 *          and path comparison issues.
 */
bool localListeningSocketExists(const unsigned short port, const wchar_t *owningProcImgName) {
	// Target port and IP address need to be in network order
	// in order to match the values returned by the operating system.
	const unsigned long targetIpAddr = htonl(0x7F000001);  // 127.0.0.1
	const unsigned short targetPort = htons(port);
	path targetPath(owningProcImgName);
	DWORD tableSize = sizeof(MIB_TCPTABLE_OWNER_PID), res;
	const size_t stringBufferLength = MAX_PATH + 1;
	try {
		if (!exists(targetPath)) {
			LOG_DEBUG(L"Target path does not exist.");
			return false;
		}
	} catch ([[maybe_unused]] filesystem_error &err) {
		LOG_DEBUG(L"Failed to check for existence of path. Error #" << err.code() << L": " << err.what() << L".");
		return false;
	}
	auto stringBuffer = make_unique<wchar_t[]>(stringBufferLength);
	// Get the TCP table
	// Allocate minimum table
	auto tableBuffer = make_unique<char[]>(tableSize);
	// Get the table. If the table is larger than the minimum possible (more than likely), it will fail, and output the required size in tableSize.
	if ((res = GetExtendedTcpTable(tableBuffer.get(), &tableSize, false, AF_INET, TCP_TABLE_OWNER_PID_LISTENER, 0)) == ERROR_INSUFFICIENT_BUFFER) {
		// Minimal TCP Table was not big enough. Now allocate the size we were told is sufficient.
		tableBuffer = make_unique<char[]>(tableSize);
		if ((res = GetExtendedTcpTable(tableBuffer.get(), &tableSize, false, AF_INET, TCP_TABLE_OWNER_PID_LISTENER, 0)) != NO_ERROR) {
			LOG_DEBUG(L"Getting TCP table with instructed size failed. Error " << res << L".");
			return false;
		}
	} else if (res != NO_ERROR) {
		LOG_DEBUG(L"Initial attempt to get TCP table failed with an error other than insufficient buffer. Error " << res << L".");
		return false;
	}
	PMIB_TCPTABLE_OWNER_PID pTcpTable = (MIB_TCPTABLE_OWNER_PID*)tableBuffer.get();
	// Now, iterate over the TCP table, comparing each row to the values we've been given.
	for (DWORD i = 0; i < pTcpTable->dwNumEntries; i++) {
		auto row = pTcpTable->table[i];

		// We only care about rows in the LISTEN state.
		// Using TCP_TABLE_OWNER_PID_LISTENER should mean that all returned rows are in this state,
		// but this check guarantees it and is inexpensive.
		if (row.dwState != MIB_TCP_STATE_LISTEN) {
			continue;
		}

		// We only want ports on the target IP.
		if (row.dwLocalAddr != targetIpAddr) {
				continue;
		}

		// We only care about connections with the same port number
		// We have to convert the port to an unsigned short,
		// as it is stored as a DWORD,
		// and the value of the extraneous bits is undefined.
		if((unsigned short)row.dwLocalPort != targetPort) {
			continue;
		}

		// We only care about connections with a matching owner.
		// Get the full name of the executable in the connection's owning process.
		// First, get a handle to the process.
		wil::unique_process_handle procHandle (OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, false, row.dwOwningPid));
		if (!procHandle.is_valid()) {
			LOG_DEBUG(L"Failed to get handle to process with PID " << row.dwOwningPid << L". Error " << GetLastError() << L".");
			continue;
		}
		// Then, use that handle to get the process image.
		DWORD written = stringBufferLength;
		if (!QueryFullProcessImageNameW(procHandle.get(), 0, stringBuffer.get(), &written)) {
			LOG_DEBUG(L"Failed to get process name. Error " << GetLastError() << L".");
			continue;
		}
		path rowPath(stringBuffer.get());
		try {
			if (!equivalent(targetPath, rowPath)) {
				continue;
			}
		} catch ([[maybe_unused]] filesystem_error &err) {
			LOG_DEBUG(L"Error comparing paths. Error " << err.code() << L": " << err.what() << L".");
			continue;
		}

		// If we have made it this far, this row is a match.
		return true;
	}
	return false;
}
