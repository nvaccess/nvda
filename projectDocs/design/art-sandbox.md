# Windows Process Sandboxing in NVDA

NVDA addons run arbitrary Python code from the internet. That's both a feature and a security problem. 

The ART (Addon Runtime) process runs addons in a restricted Windows environment. Addons get the Python environment they need, but Windows locks them down so they can't wreck your system or steal your data.

This sandbox uses several Windows security mechanisms to create a restricted environment where addon code can run without full system access.

## Windows Security Mechanisms

The sandbox combines multiple Windows security features:

### 1. Restricted Tokens

`CreateRestrictedToken` creates a modified version of a process's security token. The restricted token removes dangerous privileges, disables certain SIDs, and limits file/registry access. 

When used with `CreateProcessAsUser`, no special privileges like `SE_ASSIGNPRIMARYTOKEN_NAME` are required if the restricted token derives from the caller's own token.

### 2. Security Identifiers (SIDs)

The sandbox selectively disables group SID memberships while preserving essential ones needed for basic functionality. Essential SIDs like Everyone (`S-1-1-0`) and Users (`S-1-5-32-545`) remain enabled, while non-essential groups like Performance Log Users or Power Users are disabled.

The user SID remains active to allow addon access to personal files and addon directories.

### 3. Privilege Removal

Windows gives processes special privileges to do dangerous things. We strip most of these away because addons shouldn't need them.

No more `SE_DEBUG_NAME` means malicious code can't attach debuggers to other processes and steal their memory. `SE_BACKUP_NAME` and `SE_RESTORE_NAME` are gone too - these let programs read and write any file on the system, bypassing all permissions. That's way too much power for an addon.

We also remove `SE_SHUTDOWN_NAME` (can't shut down the computer), `SE_LOAD_DRIVER_NAME` (can't install kernel drivers), and `SE_TCB_NAME` (can't pretend to be part of Windows itself). If an addon gets compromised, it can't take over your machine.

### 4. Integrity Levels

Integrity levels override standard file permissions with a simple rule: processes can't write to objects at higher integrity levels, regardless of other permissions.

Four levels exist: System (kernel), High (admin processes), Medium (normal user programs), and Low (sandboxed processes like Internet Explorer's Protected Mode). Processes can only write down the hierarchy, never up.

We run ART at Medium integrity instead of Low. Why? Because Low integrity would lock addons out of most user files. They couldn't read your NVDA settings, save their own configuration, or access addon directories. Medium integrity gives them reasonable file access while still blocking writes to system locations.

Implementation uses `SYSTEM_MANDATORY_LABEL_ACE` entries with `NO_WRITE_UP` policies - addons can't modify Windows system files even if regular file permissions would allow it.

### 5. Job Objects

Job objects group related processes and enforce resource limits and behavioral restrictions on the entire group.

The 100MB memory limit per process prevents runaway addons from consuming system RAM. Windows terminates processes that exceed this limit.

The UI restrictions are particularly important. `JOB_OBJECT_UILIMIT_WRITECLIPBOARD` and `JOB_OBJECT_UILIMIT_READCLIPBOARD` mean addons can't steal passwords you copied or inject malicious content into your clipboard. `JOB_OBJECT_UILIMIT_DESKTOP` prevents them from creating hidden desktops where they could run invisible malware.

`JOB_OBJECT_UILIMIT_HANDLES` is sneaky but important - it stops addons from broadcasting window messages to other applications or installing global hooks that could spy on your activity system-wide.

### 6. Parent Process Attribution

`PROC_THREAD_ATTRIBUTE_PARENT_PROCESS` allows specifying a different parent process during creation. The created process inherits handles, security context, memory quotas, and processor affinity from the specified parent rather than the actual creator.

Security implications:
- Enables parent PID spoofing to bypass process relationship analysis
- Can facilitate privilege escalation if the specified parent has elevated rights  
- Commonly used by malware to masquerade as legitimate system processes
- ETW events still record the actual parent, preserving forensic evidence

NVDA's sandbox doesn't use parent process attribution - addon processes maintain their legitimate relationship to the main NVDA process.

### 7. Token Integrity Labels

`TOKEN_MANDATORY_LABEL` contains the integrity level SID for mandatory access control. Retrieved via `GetTokenInformation` with `TokenIntegrityLevel`.

Standard integrity levels:
- `S-1-16-0`: Untrusted
- `S-1-16-4096`: Low (IE protected mode, sandboxed apps)  
- `S-1-16-8192`: Medium (normal user programs)
- `S-1-16-12288`: High (elevated admin programs)
- `S-1-16-16384`: System (kernel and system services)

Processes can read down the hierarchy but cannot write up. A medium integrity process cannot modify high integrity files regardless of regular permissions.

### 8. Process Access Rights

Process security tokens define access rights to other processes. Sandboxed processes retain standard rights (query, read, terminate) needed for basic system interaction.

Additional rights granted for addon functionality:
- `PROCESS_CREATE_PROCESS`: Launch external tools and helper processes
- `PROCESS_CREATE_THREAD`: Inject threads for accessibility hooks  
- `PROCESS_DUP_HANDLE`: Share file handles between processes

These rights control what sandboxed processes can do to other processes, not what can be done to them. The configuration balances security restrictions with addon functionality requirements.

## NVDA Sandbox Configuration

**Enabled Restrictions:**

- **Restricted tokens**: Remove `SE_DEBUG_NAME`, `SE_LOAD_DRIVER_NAME`, `SE_BACKUP_NAME`, `SE_RESTORE_NAME`, `SE_SHUTDOWN_NAME`, `SE_TCB_NAME`
- **Memory limits**: 100MB per process hard limit enforced by job objects
- **UI restrictions**: Block clipboard access (`JOB_OBJECT_UILIMIT_WRITECLIPBOARD/READCLIPBOARD`) and desktop creation
- **SID restrictions**: Disable unnecessary group memberships (Performance Log Users, Remote Desktop Users)

**Disabled Restrictions:**

- **Low integrity level**: Would prevent access to user files and NVDA configuration
- **Process count limits**: ART architecture requires multiple Python subprocesses
- **User SID restrictions**: Addons need access to user files and addon directories (see `processManager.py:85`)
- **Full process creation blocking**: The Python launcher itself launches subprocesses. When you run python in a virtualenv it ends up launching the actual python.exe and cannot if this is enabled. Also, some addons require external tool integration

**Security Impact:**

Compromised addons cannot:
- Escalate to system privileges
- Access clipboard data  
- Consume unlimited system memory
- Install drivers or system-level components

Compromised addons can still:
- Read user files within normal permissions
- Create additional processes
- Access addon directories and NVDA configuration

ART processes terminate when NVDA exits, preventing orphaned addon processes.

## Implementation Details

For the actual implementation of these sandbox features, see [`source/sandbox.py`](source/sandbox.py) which contains the `SandboxConfig` class and all the Windows API calls that make this magic happen. The comments in that file explain the technical details of each restriction.

## References

### Core Windows Security APIs
- [CreateRestrictedToken API - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-createrestrictedtoken)
- [CreateProcessAsUser API - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasuserw)
- [Restricted Tokens - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/secauthz/restricted-tokens)

### Access Control and Security Identifiers  
- [Security Identifiers - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/secauthz/security-identifiers)
- [Access Control Lists - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-control-lists)
- [Privilege Constants - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/secauthz/privilege-constants)

### Integrity Control and Job Objects
- [Mandatory Integrity Control - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control)
- [SYSTEM_MANDATORY_LABEL_ACE Structure - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-system_mandatory_label_ace)
- [TOKEN_MANDATORY_LABEL Structure - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_mandatory_label)
- [Job Objects - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [JOBOBJECT_BASIC_UI_RESTRICTIONS Structure - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_ui_restrictions)

### Extended Process Creation
- [UpdateProcThreadAttribute Function - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute)
- [Process Security and Access Rights - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights)