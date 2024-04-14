from __future__ import annotations

import ctypes
from collections import namedtuple
from ctypes import wintypes
from list2tree import treedict
from mymulti_key_dict import MultiKeyDict
from flatten_any_dict_iterable_or_whatsoever import fla_tu
import subprocess
import sys
import re
import contextlib
from typing import Literal, Generator

windll = ctypes.LibraryLoader(ctypes.WinDLL)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
ntdll = windll.ntdll

RtlNtStatusToDosError = ntdll.RtlNtStatusToDosError
NtResumeProcess = ntdll.NtResumeProcess
NtSuspendProcess = ntdll.NtSuspendProcess


def errcheck_ntstatus(status, *etc):
    if status < 0:
        raise ctypes.WinError(RtlNtStatusToDosError(status))
    return status


RtlNtStatusToDosError.argtypes = (wintypes.LONG,)
RtlNtStatusToDosError.restype = wintypes.ULONG
# RtlNtStatusToDosError cannot fail

NtResumeProcess.argtypes = (wintypes.HANDLE,)
NtResumeProcess.restype = wintypes.LONG
NtResumeProcess.errcheck = errcheck_ntstatus


NtSuspendProcess.argtypes = (wintypes.HANDLE,)
NtSuspendProcess.restype = wintypes.LONG
NtSuspendProcess.errcheck = errcheck_ntstatus

ERROR_ACCESS_DENIED = 5
ERROR_INSUFFICIENT_BUFFER = 122
ERROR_NO_TOKEN = 1008
ERROR_NOT_ALL_ASSIGNED = 1300

# TOKEN_TYPE
TokenPrimary = 1
TokenImpersonation = 2

# SECURITY_IMPERSONATION_LEVEL
SecurityAnonymous = 0
SecurityIdentification = 1
SecurityImpersonation = 2
SecurityDelegation = 3

# TOKEN_INFORMATION_CLASS
TokenUser = 1
TokenGroups = 2
TokenPrivileges = 3
TokenOwner = 4

# WELL_KNOWN_SID_TYPE
WinBuiltinAdministratorsSid = 26

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

TOKEN_ASSIGN_PRIMARY = 0x0001
TOKEN_DUPLICATE = 0x0002
TOKEN_IMPERSONATE = 0x0004
TOKEN_QUERY = 0x0008
TOKEN_QUERY_SOURCE = 0x0010
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_ADJUST_GROUPS = 0x0040
TOKEN_ADJUST_DEFAULT = 0x0080
TOKEN_ADJUST_SESSIONID = 0x0100
TOKEN_ALL_ACCESS = 0x000F0000 | 0x01FF

SE_PRIVILEGE_ENABLED_BY_DEFAULT = 0x00000001
SE_PRIVILEGE_ENABLED = 0x00000002
SE_PRIVILEGE_REMOVED = 0x00000004
SE_PRIVILEGE_USED_FOR_ACCESS = 0x80000000

SE_GROUP_MANDATORY = 0x00000001
SE_GROUP_ENABLED_BY_DEFAULT = 0x00000002
SE_GROUP_ENABLED = 0x00000004
SE_GROUP_OWNER = 0x00000008
SE_GROUP_USE_FOR_DENY_ONLY = 0x00000010
SE_GROUP_INTEGRITY = 0x00000020
SE_GROUP_INTEGRITY_ENABLED = 0x00000040
SE_GROUP_LOGON_ID = 0xC0000000
SE_GROUP_RESOURCE = 0x20000000

SE_CREATE_TOKEN_NAME = "SeCreateTokenPrivilege"
SE_ASSIGNPRIMARYTOKEN_NAME = "SeAssignPrimaryTokenPrivilege"
SE_LOCK_MEMORY_NAME = "SeLockMemoryPrivilege"
SE_INCREASE_QUOTA_NAME = "SeIncreaseQuotaPrivilege"
SE_MACHINE_ACCOUNT_NAME = "SeMachineAccountPrivilege"
SE_TCB_NAME = "SeTcbPrivilege"
SE_SECURITY_NAME = "SeSecurityPrivilege"
SE_TAKE_OWNERSHIP_NAME = "SeTakeOwnershipPrivilege"
SE_LOAD_DRIVER_NAME = "SeLoadDriverPrivilege"
SE_SYSTEM_PROFILE_NAME = "SeSystemProfilePrivilege"
SE_SYSTEMTIME_NAME = "SeSystemtimePrivilege"
SE_PROF_SINGLE_PROCESS_NAME = "SeProfileSingleProcessPrivilege"
SE_INC_BASE_PRIORITY_NAME = "SeIncreaseBasePriorityPrivilege"
SE_CREATE_PAGEFILE_NAME = "SeCreatePagefilePrivilege"
SE_CREATE_PERMANENT_NAME = "SeCreatePermanentPrivilege"
SE_BACKUP_NAME = "SeBackupPrivilege"
SE_RESTORE_NAME = "SeRestorePrivilege"
SE_SHUTDOWN_NAME = "SeShutdownPrivilege"
SE_DEBUG_NAME = "SeDebugPrivilege"
SE_AUDIT_NAME = "SeAuditPrivilege"
SE_SYSTEM_ENVIRONMENT_NAME = "SeSystemEnvironmentPrivilege"
SE_CHANGE_NOTIFY_NAME = "SeChangeNotifyPrivilege"
SE_REMOTE_SHUTDOWN_NAME = "SeRemoteShutdownPrivilege"
SE_UNDOCK_NAME = "SeUndockPrivilege"
SE_SYNC_AGENT_NAME = "SeSyncAgentPrivilege"
SE_ENABLE_DELEGATION_NAME = "SeEnableDelegationPrivilege"
SE_MANAGE_VOLUME_NAME = "SeManageVolumePrivilege"
SE_IMPERSONATE_NAME = "SeImpersonatePrivilege"
SE_CREATE_GLOBAL_NAME = "SeCreateGlobalPrivilege"
SE_TRUSTED_CREDMAN_ACCESS_NAME = "SeTrustedCredManAccessPrivilege"
SE_RELABEL_NAME = "SeRelabelPrivilege"
SE_INC_WORKING_SET_NAME = "SeIncreaseWorkingSetPrivilege"
SE_TIME_ZONE_NAME = "SeTimeZonePrivilege"
SE_CREATE_SYMBOLIC_LINK_NAME = "SeCreateSymbolicLinkPrivilege"


class HANDLE(wintypes.HANDLE):
    __slots__ = ("closed",)

    def detach(self):
        if not getattr(self, "closed", False):
            self.closed = True
            value = int(self)
            self.value = None
            return value
        raise ValueError("already closed")

    def close(self, *, CloseHandle=kernel32.CloseHandle):
        if self and not getattr(self, "closed", False):
            CloseHandle(self.detach())

    def __enter__(self):
        return self

    def __exit__(self, cls, value, traceback):
        self.close()

    def __int__(self):
        return self.value or 0

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__name__, int(self))

    __del__ = close


PHANDLE = ctypes.POINTER(HANDLE)


class LUID(ctypes.Structure):
    _fields_ = (("LowPart", wintypes.DWORD), ("HighPart", wintypes.LONG))

    @property
    def value(self):
        return ctypes.c_longlong.from_buffer(self).value

    @value.setter
    def value(self, v):
        ctypes.c_longlong.from_buffer(self).value = v


PLUID = ctypes.POINTER(LUID)


class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = (("Luid", LUID), ("Attributes", wintypes.DWORD))


class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = (
        ("PrivilegeCount", wintypes.DWORD),
        ("_Privileges", LUID_AND_ATTRIBUTES * 0),
    )

    def __init__(self, PrivilegeCount=1, *args):
        super(TOKEN_PRIVILEGES, self).__init__(PrivilegeCount, *args)
        if PrivilegeCount < 0:
            raise ValueError("PrivilegeCount must be non-negative.")
        if PrivilegeCount > 0:
            ctypes.resize(
                self,
                ctypes.sizeof(self)
                + PrivilegeCount * ctypes.sizeof(LUID_AND_ATTRIBUTES),
            )

    @property
    def Privileges(self):
        dtype = LUID_AND_ATTRIBUTES * self.PrivilegeCount
        offset = type(self)._Privileges.offset
        return dtype.from_buffer(self, offset)


PTOKEN_PRIVILEGES = ctypes.POINTER(TOKEN_PRIVILEGES)


class SID_IDENTIFIER_AUTHORITY(ctypes.Structure):
    _fields_ = (("Value", ctypes.c_ubyte * 6),)


class SID(ctypes.Structure):
    _fields_ = (
        ("Revision", ctypes.c_ubyte),
        ("SubAuthorityCount", ctypes.c_ubyte),
        ("IdentifierAuthority", SID_IDENTIFIER_AUTHORITY),
        ("_SubAuthority", wintypes.DWORD * 0),
    )

    def __init__(self, Revision=1, SubAuthorityCount=1, *args):
        super(SID, self).__init__(Revision, SubAuthorityCount, *args)
        if SubAuthorityCount < 0:
            raise ValueError("SubAuthorityCount must be non-negative.")
        if SubAuthorityCount > 0:
            ctypes.resize(self, ctypes.sizeof(self) + 4 * SubAuthorityCount)

    @property
    def SubAuthority(self):
        dtype = wintypes.DWORD * self.SubAuthorityCount
        offset = type(self)._SubAuthority.offset
        address = ctypes.addressof(self) + offset
        array = dtype.from_address(address)
        array._obj = self
        return array

    def __bytes__(self):
        size = ctypes.sizeof(SID) + 4 * self.SubAuthorityCount
        array = (ctypes.c_char * size).from_address(ctypes.addressof(self))
        return array[:]


PSID = ctypes.POINTER(SID)


class SID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = (("Sid", PSID), ("Attributes", wintypes.DWORD))


class TOKEN_GROUPS(ctypes.Structure):
    _fields_ = (("GroupCount", wintypes.DWORD), ("_Groups", SID_AND_ATTRIBUTES * 0))

    def __init__(self, GroupCount=1, *args):
        super(TOKEN_GROUPS, self).__init__(GroupCount, *args)
        if GroupCount < 0:
            raise ValueError("GroupCount must be non-negative.")
        if GroupCount > 0:
            ctypes.resize(
                self,
                ctypes.sizeof(self) + GroupCount * ctypes.sizeof(SID_AND_ATTRIBUTES),
            )

    @property
    def Groups(self):
        dtype = SID_AND_ATTRIBUTES * self.GroupCount
        offset = type(self)._Groups.offset
        return dtype.from_buffer(self, offset)


PTOKEN_GROUPS = ctypes.POINTER(TOKEN_GROUPS)


def _nonzero_success(result, func, args):
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


advapi32.LookupPrivilegeValueW.errcheck = _nonzero_success
advapi32.LookupPrivilegeValueW.argtypes = (
    wintypes.LPCWSTR,  # _In_opt_ lpSystemName
    wintypes.LPCWSTR,  # _In_     lpName
    PLUID,
)  # _Out_    lpLuid

advapi32.CreateWellKnownSid.errcheck = _nonzero_success
advapi32.CreateWellKnownSid.argtypes = (
    wintypes.DWORD,  # WellKnownSidType,
    ctypes.c_char_p,  # DomainSid
    ctypes.c_char_p,  # pSid
    wintypes.PDWORD,
)  # cbSid

kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
kernel32.GetCurrentProcess.restype = wintypes.HANDLE
kernel32.GetCurrentThread.restype = wintypes.HANDLE

kernel32.OpenProcess.errcheck = _nonzero_success
kernel32.OpenProcess.restype = HANDLE
kernel32.OpenProcess.argtypes = (
    wintypes.DWORD,  # _In_ dwDesiredAccess
    wintypes.BOOL,  # _In_ bInheritHandle
    wintypes.DWORD,
)  # _In_ dwProcessId

advapi32.OpenProcessToken.errcheck = _nonzero_success
advapi32.OpenProcessToken.argtypes = (
    wintypes.HANDLE,  # _In_  ProcessHandle
    wintypes.DWORD,  # _In_  DesiredAccess
    PHANDLE,
)  # _Out_ TokenHandle

advapi32.OpenThreadToken.errcheck = _nonzero_success
advapi32.OpenThreadToken.argtypes = (
    wintypes.HANDLE,  # _In_ ThreadHandle
    wintypes.DWORD,  # _In_ DesiredAccess
    wintypes.BOOL,  # _In_ OpenAsSelf
    PHANDLE,
)  # _Out_ TokenHandle

advapi32.SetThreadToken.errcheck = _nonzero_success
advapi32.SetThreadToken.argtypes = (
    wintypes.PHANDLE,  # Thread
    wintypes.HANDLE,
)  # Token

advapi32.DuplicateTokenEx.argtypes = (
    wintypes.HANDLE,  # hExistingToken
    wintypes.DWORD,  # dwDesiredAccess
    wintypes.LPVOID,  # lpTokenAttributes
    wintypes.DWORD,  # ImpersonationLevel
    wintypes.DWORD,  # TokenType
    PHANDLE,
)  # phNewToken

advapi32.GetTokenInformation.errcheck = _nonzero_success
advapi32.GetTokenInformation.argtypes = (
    wintypes.HANDLE,  # _In_      TokenHandle
    wintypes.DWORD,  # _In_      TokenInformationClass
    wintypes.LPVOID,  # _Out_opt_ TokenInformation
    wintypes.DWORD,  # _In_      TokenInformationLength
    wintypes.PDWORD,
)  # _Out_     ReturnLength

advapi32.CheckTokenMembership.errcheck = _nonzero_success
advapi32.CheckTokenMembership.argtypes = (
    wintypes.HANDLE,  # TokenHandle
    ctypes.c_char_p,  # SidToCheck
    wintypes.PBOOL,
)  # IsMember

advapi32.AdjustTokenPrivileges.errcheck = _nonzero_success
advapi32.AdjustTokenPrivileges.argtypes = (
    wintypes.HANDLE,  # _In_      TokenHandle
    wintypes.BOOL,  # _In_      DisableAllPrivileges
    PTOKEN_PRIVILEGES,  # _In_opt_  NewState
    wintypes.DWORD,  # _In_      BufferLength
    PTOKEN_PRIVILEGES,  # _Out_opt_ PreviousState
    wintypes.PDWORD,
)  # _Out_opt_ ReturnLength


def create_well_known_sid(sid_type):
    sid = (ctypes.c_char * 1)()
    cbSid = wintypes.DWORD()
    try:
        advapi32.CreateWellKnownSid(sid_type, None, sid, ctypes.byref(cbSid))
    except OSError as e:
        if e.winerror != ERROR_INSUFFICIENT_BUFFER:
            raise
        sid = (ctypes.c_char * cbSid.value)()
        advapi32.CreateWellKnownSid(sid_type, None, sid, ctypes.byref(cbSid))
    return sid[:]


def adjust_token_privileges(
    hToken, new_state=(), disable_all=False, return_previous_state=True
):
    pNewState = PTOKEN_PRIVILEGES()
    pPreviousState = PTOKEN_PRIVILEGES()
    pReturnLength = wintypes.PDWORD()
    bufferLength = 0
    if not disable_all:
        newState = TOKEN_PRIVILEGES(len(new_state))
        pNewState.contents = newState
        for priv, (luid, attr) in zip(newState.Privileges, new_state):
            priv.Luid.value = luid
            priv.Attributes = attr
    if return_previous_state:
        previousState = TOKEN_PRIVILEGES(len(new_state))
        returnLength = wintypes.DWORD()
        bufferLength = ctypes.sizeof(previousState)
        pPreviousState.contents = previousState
        pReturnLength.contents = returnLength
    while True:
        try:
            advapi32.AdjustTokenPrivileges(
                hToken,
                disable_all,
                pNewState,
                bufferLength,
                pPreviousState,
                pReturnLength,
            )
            break
        except OSError as e:
            if not return_previous_state or e.winerror != ERROR_INSUFFICIENT_BUFFER:
                raise
            bufferLength = returnLength.value
            ctypes.resize(previousState, bufferLength)
            pPreviousState.contents = previousState
    if not return_previous_state:
        return []
    return [(p.Luid.value, p.Attributes) for p in previousState.Privileges]


def enable_token_privileges(hToken, *privilege_names):
    luid = LUID()
    state = []
    for name in privilege_names:
        advapi32.LookupPrivilegeValueW(None, name, ctypes.byref(luid))
        state.append((luid.value, SE_PRIVILEGE_ENABLED))
    return adjust_token_privileges(hToken, state)


@contextlib.contextmanager
def open_effective_token(access, open_as_self=True):
    hThread = kernel32.GetCurrentThread()
    hToken = HANDLE()
    access |= TOKEN_IMPERSONATE
    try:
        advapi32.OpenThreadToken(hThread, access, open_as_self, ctypes.byref(hToken))
        impersonated_self = False
    except OSError as e:
        if e.winerror != ERROR_NO_TOKEN:
            raise
        hProcess = kernel32.GetCurrentProcess()
        hTokenProcess = HANDLE()
        advapi32.OpenProcessToken(
            hProcess, TOKEN_DUPLICATE, ctypes.byref(hTokenProcess)
        )
        with hTokenProcess:
            advapi32.DuplicateTokenEx(
                hTokenProcess,
                access,
                None,
                SecurityImpersonation,
                TokenImpersonation,
                ctypes.byref(hToken),
            )
        advapi32.SetThreadToken(None, hToken)
        impersonated_self = True
    try:
        yield hToken
    finally:
        with hToken:
            if impersonated_self:
                advapi32.SetThreadToken(None, None)


@contextlib.contextmanager
def enable_privileges(*privilege_names):
    """Enable a set of privileges for the current thread."""
    access = TOKEN_QUERY | TOKEN_ADJUST_PRIVILEGES
    with open_effective_token(access) as hToken:
        prev_state = enable_token_privileges(hToken, *privilege_names)
        try:
            yield
        finally:
            if prev_state:
                adjust_token_privileges(hToken, prev_state)


def get_primary_token(pid, access=TOKEN_QUERY):
    hToken = HANDLE()
    with enable_privileges(SE_DEBUG_NAME):
        hProcess = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    with hProcess:
        advapi32.OpenProcessToken(hProcess, access, ctypes.byref(hToken))
    return hToken


def get_identification_token(pid, access=TOKEN_QUERY):
    hToken = HANDLE()
    with enable_privileges(SE_DEBUG_NAME):
        hProcess = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    with hProcess:
        hTokenProcess = HANDLE()
        advapi32.OpenProcessToken(
            hProcess, TOKEN_DUPLICATE, ctypes.byref(hTokenProcess)
        )
        with hTokenProcess:
            advapi32.DuplicateTokenEx(
                hTokenProcess,
                access,
                None,
                SecurityIdentification,
                TokenImpersonation,
                ctypes.byref(hToken),
            )
    return hToken


def check_token_membership(hToken, pSid):
    isAdmin = wintypes.BOOL()
    advapi32.CheckTokenMembership(hToken, pSid, ctypes.byref(isAdmin))
    return bool(isAdmin)


def get_token_groups(hToken):
    tokenGroups = TOKEN_GROUPS()
    returnLength = wintypes.DWORD()
    while True:
        try:
            advapi32.GetTokenInformation(
                hToken,
                TokenGroups,
                ctypes.byref(tokenGroups),
                ctypes.sizeof(tokenGroups),
                ctypes.byref(returnLength),
            )
            break
        except OSError as e:
            if e.winerror != ERROR_INSUFFICIENT_BUFFER:
                raise
            ctypes.resize(tokenGroups, returnLength.value)
    return [(bytes(g.Sid[0]), g.Attributes) for g in tokenGroups.Groups]


def is_process_user_an_admin(pid: int) -> bool:
    """
    Checks if the process user identified by the given process ID is an administrator.

    Args:
        pid (int): The process ID to check for administrator privileges.

    Returns:
        bool: True if the process user is an administrator, False otherwise.
    """
    adminSid = create_well_known_sid(WinBuiltinAdministratorsSid)
    try:
        with get_identification_token(pid) as hToken:
            return check_token_membership(hToken, adminSid)
    except OSError as e:
        if e.winerror != ERROR_ACCESS_DENIED:
            raise
    with get_primary_token(pid) as hToken:
        groups = get_token_groups(hToken)
    for sid, attributes in groups:
        if sid == adminSid:
            return bool(attributes & SE_GROUP_ENABLED)
    return False


startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}


class MODULEENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("th32ModuleID", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("GlblcntUsage", wintypes.DWORD),
        ("ProccntUsage", wintypes.DWORD),
        ("modBaseAddr", wintypes.PBYTE),
        ("modBaseSize", wintypes.DWORD),
        ("hModule", wintypes.HMODULE),
        ("szModule", wintypes.WCHAR * 256),
        ("szExePath", wintypes.WCHAR * 260),
    ]


class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.c_uint64),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", wintypes.WCHAR * 260),
    ]


class THREADENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ThreadID", wintypes.DWORD),
        ("th32OwnerProcessID", wintypes.DWORD),
        ("tpBasePri", wintypes.LONG),
        ("tpDeltaPri", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
    ]


CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = ctypes.c_int

OpenProcess = windll.kernel32.OpenProcess
OpenProcess.argtypes = [wintypes.DWORD, ctypes.c_int, wintypes.DWORD]
OpenProcess.restype = wintypes.HANDLE

GetPriorityClass = windll.kernel32.GetPriorityClass
GetPriorityClass.argtypes = [wintypes.HANDLE]
GetPriorityClass.restype = wintypes.DWORD

CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
CreateToolhelp32Snapshot.restype = wintypes.HANDLE

Module32FirstW = windll.kernel32.Module32FirstW
Module32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(MODULEENTRY32W)]
Module32FirstW.restype = ctypes.c_int

Module32NextW = windll.kernel32.Module32NextW
Module32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(MODULEENTRY32W)]
Module32NextW.restype = ctypes.c_int

Process32FirstW = windll.kernel32.Process32FirstW
Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
Process32FirstW.restype = ctypes.c_int

Process32NextW = windll.kernel32.Process32NextW
Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
Process32NextW.restype = ctypes.c_int

Thread32First = windll.kernel32.Thread32First
Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(THREADENTRY32)]
Thread32First.restype = ctypes.c_int

Thread32Next = windll.kernel32.Thread32Next
Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(THREADENTRY32)]
Thread32Next.restype = ctypes.c_int

INVALID_HANDLE_VALUE = -1
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPTHREAD = 0x00000004
DELETE = 0x00010000
READ_CONTROL = 0x00020000
WRITE_DAC = 0x00040000
WRITE_OWNER = 0x00080000
SYNCHRONIZE = 0x00100000

STANDARD_RIGHTS_REQUIRED = 0x000F0000

STANDARD_RIGHTS_READ = READ_CONTROL
STANDARD_RIGHTS_WRITE = READ_CONTROL
STANDARD_RIGHTS_EXECUTE = READ_CONTROL

STANDARD_RIGHTS_ALL = 0x001F0000

SPECIFIC_RIGHTS_ALL = 0x0000FFFF

ACCESS_SYSTEM_SECURITY = 0x01000000

MAXIMUM_ALLOWED = 0x02000000

GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
GENERIC_EXECUTE = 0x20000000
GENERIC_ALL = 0x10000000
PROCESS_TERMINATE = 0x0001
PROCESS_CREATE_THREAD = 0x0002
PROCESS_SET_SESSIONID = 0x0004
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_DUP_HANDLE = 0x0040
PROCESS_CREATE_PROCESS = 0x0080
PROCESS_SET_QUOTA = 0x0100
PROCESS_SET_INFORMATION = 0x0200
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_SUSPEND_RESUME = 0x0800
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_SET_LIMITED_INFORMATION = 0x2000

PROCESS_ALL_ACCESS = STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFFF


Module = namedtuple(
    "Module",
    [
        "dwSize",
        "th32ModuleID",
        "th32ProcessID",
        "GlblcntUsage",
        "ProccntUsage",
        "modBaseAddr",
        "modBaseSize",
        "hModule",
        "szModule",
        "szExePath",
    ],
)

Process = namedtuple(
    "Process",
    [
        "dwSize",
        "cntUsage",
        "th32ProcessID",
        "th32DefaultHeapID",
        "th32ModuleID",
        "cntThreads",
        "th32ParentProcessID",
        "pcPriClassBase",
        "dwFlags",
        "szExeFile",
    ],
)

Thread = namedtuple(
    "Thread",
    [
        "dwSize",
        "cntUsage",
        "th32ThreadID",
        "th32OwnerProcessID",
        "tpBasePri",
        "tpDeltaPri",
        "dwFlags",
    ],
)


def module_to_tuple(mod):
    return Module(
        mod.dwSize,
        mod.th32ModuleID,
        mod.th32ProcessID,
        mod.GlblcntUsage,
        mod.ProccntUsage,
        mod.modBaseAddr,
        mod.modBaseSize,
        mod.hModule,
        mod.szModule,
        mod.szExePath,
    )


def process_to_tuple(process):
    return Process(
        process.dwSize,
        process.cntUsage,
        process.th32ProcessID,
        process.th32DefaultHeapID,
        process.th32ModuleID,
        process.cntThreads,
        process.th32ParentProcessID,
        process.pcPriClassBase,
        process.dwFlags,
        process.szExeFile,
    )


def thread_to_tuple(thread):
    return Thread(
        thread.dwSize,
        thread.cntUsage,
        thread.th32ThreadID,
        thread.th32OwnerProcessID,
        thread.tpBasePri,
        thread.tpDeltaPri,
        thread.dwFlags,
    )


class ModuleIter:
    @classmethod
    def from_ptr(cls, snap_shot: wintypes.HANDLE) -> ModuleIter:
        """
        A class method that creates a new ModuleIter instance from a snap_shot handle.

        Args:
            cls: The class object.
            snap_shot: A handle to the snapshot.

        Returns:
            ModuleIter: A new ModuleIter instance.
        """
        cl = cls()
        cl.snap_shot = snap_shot
        cl.mod = MODULEENTRY32W()
        cl.mod.dwSize = ctypes.sizeof(MODULEENTRY32W)
        cl.entered = False
        return cl

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        CloseHandle(self.snap_shot)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.entered:
            more = Module32FirstW(self.snap_shot, ctypes.byref(self.mod))
            if not more:
                raise StopIteration
            self.entered = True
            return module_to_tuple(self.mod)
        else:
            more = Module32NextW(self.snap_shot, ctypes.byref(self.mod))
            if not more:
                raise StopIteration
            return module_to_tuple(self.mod)


class ThreadIter:
    @classmethod
    def from_ptr(cls, snap_shot: wintypes.HANDLE) -> ThreadIter:
        """
        A class method that creates a new ThreadIter instance from a snap_shot handle.

        Args:
            cls: The class object.
            snap_shot: A handle to the snapshot.

        Returns:
            ThreadIter: A new ThreadIter instance.
        """
        cl = cls()
        cl.snap_shot = snap_shot
        cl.thread = THREADENTRY32()
        cl.thread.dwSize = ctypes.sizeof(THREADENTRY32)
        cl.entered = False
        return cl

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        CloseHandle(self.snap_shot)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.entered:
            more = Thread32First(self.snap_shot, ctypes.byref(self.thread))
            if not more:
                raise StopIteration
            self.entered = True
            return thread_to_tuple(self.thread)
        else:
            more = Thread32Next(self.snap_shot, ctypes.byref(self.thread))
            if not more:
                raise StopIteration
            return thread_to_tuple(self.thread)


class ProcessIter:
    @classmethod
    def from_ptr(cls, snap_shot: wintypes.HANDLE) -> ProcessIter:
        """
        A class method that creates a new ProcessIter instance from a snap_shot handle.

        Args:
            cls: The class object.
            snap_shot: A handle to the snapshot.

        Returns:
            ProcessIter: A new ProcessIter instance.
        """
        cl = cls()
        cl.snap_shot = snap_shot
        cl.process = PROCESSENTRY32W()
        cl.process.dwSize = ctypes.sizeof(PROCESSENTRY32W)
        cl.entered = False
        return cl

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        CloseHandle(self.snap_shot)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.entered:
            more = Process32FirstW(self.snap_shot, ctypes.byref(self.process))
            if not more:
                raise StopIteration
            self.entered = True
            return process_to_tuple(self.process)
        else:
            more = Process32NextW(self.snap_shot, ctypes.byref(self.process))
            if not more:
                raise StopIteration
            return process_to_tuple(self.process)


def iter_module(pid: int) -> Generator:
    """
    A function that iterates over the modules of a specified process.

    Args:
        pid (int): The process ID for which to iterate over the modules.

    Yields:
        Generator: Yields the module information obtained from the snapshot.
    """
    snap_shot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, pid)
    if snap_shot == INVALID_HANDLE_VALUE:
        sys.stderr.write("INVALID_HANDLE_VALUE\n")
        sys.stderr.flush()
        return
    with ModuleIter.from_ptr(snap_shot) as it:
        yield from it


def iter_process() -> Generator:
    """
    A function that iterates over the processes from a snapshot and yields them.
    """
    # pid=0
    snap_shot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap_shot == INVALID_HANDLE_VALUE:
        sys.stderr.write("INVALID_HANDLE_VALUE\n")
        sys.stderr.flush()
        return
    with ProcessIter.from_ptr(snap_shot) as it:
        yield from it


def iter_threads() -> Generator:
    """
    A function that iterates over the threads from a snapshot and yields them.
    """
    snap_shot = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
    if snap_shot == INVALID_HANDLE_VALUE:
        sys.stderr.write("INVALID_HANDLE_VALUE\n")
        sys.stderr.flush()
        return
    with ThreadIter.from_ptr(snap_shot) as it:
        yield from it


def get_kids_dict(pid: int, bi_rl_lr: Literal["rl", "lr", "bi"] = "lr") -> dict:
    """
    A function that constructs a dictionary of processes and their children based on the provided process ID.

    Args:
        pid (int): The process ID for which to build the dictionary.
        bi_rl_lr (Literal["rl", "lr", "bi"], optional): The direction of the process hierarchy. Defaults to "lr" (left to right).

    Returns:
        dict: A dictionary mapping the processes and their children along with module information.
    """
    allcombs = []

    def getpr(pid):
        snap_shot1 = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, pid)
        for x in ProcessIter.from_ptr(snap_shot1):
            if x.th32ParentProcessID == pid:
                allcombs.append((str(pid), str(x.th32ProcessID)))
                getpr(x.th32ProcessID)

    getpr(pid)
    mapped, airvar = treedict(
        pairs_list=allcombs, main_mapping_keys=(str(pid),), bi_rl_lr=bi_rl_lr
    )

    dict2 = {}
    d = MultiKeyDict(dict2)
    mappeddi = sorted(mapped, key=lambda x: len(x[1]), reverse=True)
    for k, v in mappeddi:
        tmpdict = {"modules": {}, "depth": len(v), "pid": int(v[-1])}
        for ini, kkvv in enumerate(iter_module(int(v[-1]))):
            try:
                tmpdict["modules"][ini] = {
                    "GlblcntUsage": kkvv.GlblcntUsage,
                    "ProccntUsage": kkvv.ProccntUsage,
                    "modBaseSize": kkvv.modBaseSize,
                    "hModule": kkvv.hModule,
                    "szModule": kkvv.szModule,
                    "szExePath": kkvv.szExePath,
                }
            except Exception as e:
                sys.stderr.write(f"{e}\n")
                sys.stderr.flush()

        d[list(map(int, v))] = tmpdict
    return d.to_dict()


def kill_process_and_children(
    pid: int, taskkillargs: tuple = ("/f",)
) -> list[list[bytes, bytes, int]]:
    """
    A function to kill a process and its children based on the given process ID (starting from the deepest child).
    Args:
        pid (int): The process ID of the parent process to be killed.
        taskkillargs (tuple, optional): Additional arguments for the taskkill command. Defaults to ("/f",).

    Returns:
        list[list[bytes, bytes, int]]: A list containing information about the executed kill process and its children after termination.
    """
    results = []
    di = get_kids_dict(pid, bi_rl_lr="lr")
    for v, k in fla_tu(di):
        if k[-1] == "pid":
            p = subprocess.run(
                ["taskkill", "/pid", str(v), *taskkillargs],
                **invisibledict,
                capture_output=True,
            )
            results.append([p.stdout, p.stderr, p.returncode])
    subprocess.run(
        ["taskkill", "/pid", str(pid), *taskkillargs],
        **invisibledict,
        capture_output=True,
    )
    results.append([p.stdout, p.stderr, p.returncode])
    return results


def get_all_procs_with_children() -> list[dict]:
    """
    A function to get all processes with their children.
    Returns a list of dictionaries containing information about processes and their children (except pid 0 and pid 4).
    """
    zeroproc = list(iter_process())
    zeroprocmain = [x.th32ProcessID for x in zeroproc]
    zeroprocmain2 = [x.th32ParentProcessID for x in zeroproc]
    allprocs = sorted(set(zeroprocmain + zeroprocmain2))
    allprocschild = []

    for x in allprocs[2:]:
        try:
            allprocschild.append(get_kids_dict(pid=x, bi_rl_lr="lr"))
        except Exception as e:
            sys.stderr.write(str(e) + "\n")
            sys.stderr.flush()

    return allprocschild


def wmic_process_active(pid: int) -> dict:
    """
    Retrieves information about an active process based on the provided process ID.
    Args:
        pid (int): The process ID for which to retrieve information.

    Returns:
        dict: A dictionary containing information about the active process, including CommandLine, Caption, and ProcessId.
    """
    resultdict = {}

    try:
        pro = subprocess.run(
            f"""wmic process where (ProcessId={pid}) get CommandLine,Caption,ProcessId""",
            capture_output=True,
            **invisibledict,
        )
        res = [
            x for x in (pro.stdout.decode("utf-8", "replace").splitlines()) if x.strip()
        ]
        first = 0
        second = res[0].find("CommandLine")
        third = res[0].find("ProcessId")
        alltog = sorted([first, second, third, len(res[1])])
        for x in zip(alltog[:-1], alltog[1:]):
            try:
                key, value = (res[0][x[0] : x[1]].strip(), res[1][x[0] : x[1]].strip())
                if re.match(r"^\d+$", value):
                    value = int(value)

                resultdict[key] = value
            except Exception:
                pass
    except Exception:
        pass
    return resultdict


def suspend_subprocess(proc: subprocess.Popen) -> None:
    """
    Suspend a subprocess by calling NtSuspendProcess with the handle of the provided subprocess.

    Parameters:
        proc (subprocess.Popen): The subprocess to be suspended.

    Returns:
        None
    """
    NtSuspendProcess(int(proc._handle))


def resume_subprocess(proc: subprocess.Popen) -> None:
    """
    Resumes a subprocess based on the given process handle.

    Args:
        proc (subprocess.Popen): The subprocess to be resumed.

    Returns:
        None
    """
    NtResumeProcess(int(proc._handle))
