# secureProcess: Windows Process Isolation for NVDA Add-on Runtime (ART)

NVDA add-ons execute arbitrary Python code supplied by third parties. This flexibility is essential but also introduces a meaningful security risk: compromised or malicious add-ons could read user data, tamper with NVDA's internals, or inject code into other processes.

NVDA’s Add-on Runtime (ART) addresses this by executing add-on code inside *restricted Windows processes* created by the `secureProcess` package. The secureProcess layer uses Windows security primitives—restricted tokens, integrity levels, job objects, isolated desktops, temporary window stations, and controlled environment blocks—to construct a minimal-permission execution environment.

This document explains the design and implementation of this isolation layer.

---

# 1. Goals

The secureProcess sandbox aims to:

1. **Contain compromised add-on code** so it cannot perform damaging operations.
2. **Preserve functionality** for legitimate add-ons: file access to the user’s profile (when permitted), subprocess creation, basic IPC, and access to NVDA’s ART services.
3. **Operate consistently under both the standard user desktop and the Windows Secure Desktop** (e.g., at Winlogon).

The chosen model mirrors the security posture of modern browsers: a low-integrity, privilege-stripped process with strictly limited UI, file, and system access.

---

# 2. Overview of secureProcess

The main entry point is **`SecurePopen`** . It builds a constrained Windows process by:

* Selecting a base token (current user or LocalService)
* Optionally constructing a restricted token
* Setting the token integrity level
* Assigning a custom default DACL for isolated filesystem objects
* Creating an isolated desktop/window station if required
* Building a controlled environment block
* Launching the target Python interpreter using this token
* Assigning the new process to a Job Object with UI restrictions and optional kill-on-close

The ART manager (`ARTAddonProcess`, `ARTManager`) uses `SecurePopen` to start each add-on’s interpreter with the appropriate restrictions.

---

# 3. Windows Security Mechanisms Used

## 3.1 Restricted Tokens

A restricted token limits the process’s identity and privileges. secureProcess can create:

* **Least-Privilege Tokens**
  Produced via `CreateRestrictedToken(..., DISABLE_MAX_PRIVILEGE)` leaving only `SE_CHANGE_NOTIFY` enabled.
  This removes all dangerous privileges that may have existed such as debug, backup, restore, load-driver, shutdown, and TCB.
  Implemented in `createLeastPrivilegedToken`.

* **Restricted SID Tokens**
  Built by `createRestrictedToken`, which constructs a *restricted SID list* containing:

  * The mandatory `Restricted` SID (`S-1-5-12`). Allows for some very basic registry / file access for a Windows process to function.
  * Any interactive group SIDs present on the original token (`Everyone`, `Users`, `INTERACTIVE`, etc.). Enabling read / execute access to system32, program files etc,  and very basic interaction with the window station and desktop. 
  * The Logon SID, allowing further access to the window station/desktop.
  * Optionally the user SID (when *retainUserInRestrictedToken=True*). Allows read/write access to the user's own files / data. However if the integrity level on the token is subsequently set to low, then this access becomes read-only. 

---

## 3.2 Integrity Levels

Mandatory Integrity Control prohibits writes from a lower-integrity process to higher-integrity objects.

Windows supports `"untrusted"`, `"low"`, `"medium"`, `"high"`, and `"system"`.
ART  by default uses **Low integrity** for add-ons. Integrity is set via `setTokenIntegrityLevel`.

Low integrity requires redirecting `TEMP` and `TMP` into `%USERPROFILE%\AppData\LocalLow\Temp`, which is automatically handled by SecurePopen.

---

## 3.3 Default DACL and Isolated Directories

When running with a restricted token *without* the user SID, the process cannot access the user’s profile. secureProcess therefore:

* Creates a unique **sandbox directory** inside the low-integrity temp folder
* Applies a restricted DACL that grants full access only to the Logon SID and other allowed principals
  (See `createRestrictedSecurityDescriptor` and `createRestrictedDacl`.)
* Sets this directory as the process’s TEMP/TMP and possibly CWD
  (Handled by `SandboxDirectory`.)

This ensures the process has a writable location even when the user profile is inaccessible.

---

## 3.4 Isolated Desktops and Window Stations

secureProcess optionally creates:

* A **temporary window station** (`createTempWindowStation`). Only supported when running as Local Service.
* A **temporary desktop** (`createTempDesktop`)

This removes the process from the user’s interactive desktop entirely and blocks it from receiving window messages, reading UI handles, enumerating windows, or interacting with input devices.

ART uses this mode when running at the Windows Secure Desktop (Winlogon), as the Winlogon desktop is System integrity level and can't be interacted with by ART processes that run at a lower integrity level.

---

## 3.5 Job Objects (Memory/UI Restrictions)

Each secure process is assigned to a **Job Object** via `Job.assignProcess`.
Job objects enforce:

* **Kill on job close** (optional)
* **UI restrictions**, including:

  * No switching desktops
  * No reading/writing the clipboard
  * No global atoms
  * No system parameter changes
  * No access to UI handles from other processes (including no hooking processes outside the job) 

These correspond to flags in `JOB_OBJECT_UILIMIT`.

Although not currently used to enforce a hard memory cap, the architecture could support adding per-process memory limits through `JOBOBJECT_EXTENDED_LIMIT_INFORMATION`.

---

# 4. secureProcess Execution Workflow

The `SecurePopen` constructor sequence (simplified):

1. **Base Token Acquisition**

   * Use current primary token, or
   * If running on Winlogon, use LocalService (`createServiceLogon`).

2. **Security Descriptor for Isolation Objects**
   A restricted DACL granting GENERIC_ALL to the session’s Logon SID and selected principals.
   Used for temporary desktops, window stations, and sandbox directories.
   (`createRestrictedSecurityDescriptor`)

3. **Restricted Token Creation**
   Optional; removes privileges and restricts SID membership.

4. **Integrity Level Application**
   Usually `"low"`.

5. **Environment Block Construction**
   Uses `CreateEnvironmentBlock` (win32profile).
   Applies TEMP/TMP redirection for low integrity.

6. **Sandbox Directory Creation**
   When the restricted token lacks the user SID, make a private sandbox folder with matching DACL.

7. **CWD Validation**
   If CWD is unreadable under impersonation, use the sandbox Temp folder.

8. **Process Creation**
   Uses either:

   * `CreateProcessWithToken` (secure logon), or
   * `CreateProcessAsUser`
     through `PopenWithToken`.
     Extended startup info includes handle lists and optional isolated desktop.

9. **Job Assignment & UI Restrictions**

10. **Resume the Suspended Process**

ART then performs a JSON handshake with the new process to initialize encrypted IPC services.

---

# 5. ART Integration

ART starts each add-on process with:

```python
SecurePopen(
    argv,
    stdin=PIPE, stdout=PIPE, stderr=PIPE,
    killOnDelete=True,
    applyUIRestrictions=True,
    integrityLevel="low",
    removePrivileges=True,
    restrictToken=True,
    retainUserInRestrictedToken=not isSecureDesktop,
    runAsLocalService=isSecureDesktop,
    isolateWindowStation=isSecureDesktop,
    hideCriticalErrorDialogs=isSecureDesktop,
)
```

Key policy decisions:

* **Standard Desktop (user session)**:

  * Low integrity
  * Restricted token
  * *User SID retained*

This means:
* Add-ons can read (but not write) the user's configuration and profile directories. Writing to temp is possible.
* Add-ons cannot debug or hook into NVDA or other processes.
* Add-ons do not have UIAccess (cannot send messages to higher-integrity processes, cannot interact with elevated processes).

* **Secure Desktop (Winlogon)**:

  * LocalService logon token
  * Isolated window station/desktop
  * Restricted token
  * User SID not retained
  * Add-ons cannot read user data
  * Used for NVDA at logon / UAC / ctrl+alt+del screens.
  
  This means:
* Add-ons cannot read or write to any  user's configuration or profile directories. 
* Add-ons cannot write to any system locations.
* A temporary sandbox directory is used for temp.
* Add-ons cannot debug or hook into NVDA or other processes on the system.
* Add-ons do not have UIAccess (cannot send messages to higher-integrity processes, cannot interact with elevated processes).
  

---

# 6. Security Impact Summary

## Add-ons Cannot:

* Read high-integrity system files
* Inject into or debug other processes
* Install drivers or modify system settings
* Access clipboard data
* Interact with UI objects outside their desktop
* Write to most of the user profile (unless the user SID is retained)
* Access the real window station / Logon desktop when on Secure Desktops

## Add-ons Can:

* Read/write files the user normally could (only when user SID is retained)
* Use their own isolated TEMP directory
* Spawn subprocesses
* Access NVDA ART services over encrypted Pyro channels
* Run safely in both interactive and Winlogon environments
