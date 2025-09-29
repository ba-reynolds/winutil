import ctypes
import ctypes.wintypes

u32 = ctypes.windll.user32
k32 = ctypes.windll.kernel32
wnt = ctypes.wintypes


OpenClipboard = u32.OpenClipboard
OpenClipboard.argtypes = (wnt.HWND,)
OpenClipboard.restype = wnt.BOOL

GetClipboardData = u32.GetClipboardData
GetClipboardData.argtypes = (wnt.UINT,)
GetClipboardData.restype = wnt.HANDLE

# https://stackoverflow.com/a/31120103
IsClipboardFormatAvailable = u32.IsClipboardFormatAvailable
IsClipboardFormatAvailable.argtypes = (wnt.UINT,)
IsClipboardFormatAvailable.restype = wnt.BOOL

EmptyClipboard = u32.EmptyClipboard
EmptyClipboard.argtypes = None
EmptyClipboard.restype = wnt.BOOL

SetClipboardData = u32.SetClipboardData
SetClipboardData.argtypes = (wnt.UINT, wnt.HANDLE)
SetClipboardData.restype = wnt.HANDLE

CloseClipboard = u32.CloseClipboard
CloseClipboard.argtypes = None
CloseClipboard.restype = wnt.BOOL

GlobalLock = k32.GlobalLock
GlobalLock.argtypes = (wnt.HGLOBAL,)
GlobalLock.restype = wnt.LPVOID

GlobalUnlock = k32.GlobalUnlock
GlobalUnlock.argtypes = (wnt.HGLOBAL,)
GlobalUnlock.restype = wnt.BOOL

GlobalAlloc = k32.GlobalAlloc
GlobalAlloc.argtypes = (wnt.UINT, ctypes.c_size_t)
GlobalAlloc.restype = wnt.HGLOBAL

GlobalFree = k32.GlobalFree
GlobalFree.argtypes = (wnt.HGLOBAL,)
GlobalFree.restype = wnt.HGLOBAL

GetLastError = k32.GetLastError
GetLastError.argtypes = None
GetLastError.restype = wnt.DWORD

# https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/memcpy-wmemcpy?view=msvc-170
# https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-rtlcopymemory
# Realistically we should be using the actual `wmemcpy`, but for some reason
# it cannot be found so we use this instead
memcpy = k32.RtlCopyMemory
memcpy.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)
memcpy.restype = None



class Clipboard:
    CF_UNICODETEXT = 13
    GMEM_MOVEABLE = 2

    @staticmethod
    def get() -> str:
        if not OpenClipboard(None):
            return ""

        if not IsClipboardFormatAvailable(Clipboard.CF_UNICODETEXT):
            CloseClipboard()
            return ""

        h_data = GetClipboardData(Clipboard.CF_UNICODETEXT)
        p_text = ctypes.c_wchar_p(GlobalLock(h_data))
        text = p_text.value
        GlobalUnlock(h_data)
        CloseClipboard()

        return text

    @staticmethod
    def set(text: str) -> bool:
        # Encode it as utf-16 little endian as that's what Windows uses
        # https://learn.microsoft.com/en-us/cpp/cpp/char-wchar-t-char16-t-char32-t?view=msvc-170
        # Add null terminator
        as_bytes = text.encode("utf-16-le") + ctypes.c_wchar("\0")
        size_in_bytes = len(as_bytes)

        # Allocate memory, lock it so we can write to it later on
        h_mem = GlobalAlloc(Clipboard.GMEM_MOVEABLE, size_in_bytes)
        p_mem = ctypes.c_wchar_p(GlobalLock(h_mem))

        # Copy bytes into memory gotten from `GlobalAlloc` and unlock memory
        memcpy(p_mem, as_bytes, size_in_bytes)
        GlobalUnlock(h_mem)

        if OpenClipboard(None):
            EmptyClipboard()
            SetClipboardData(Clipboard.CF_UNICODETEXT, h_mem)
            CloseClipboard()
            GlobalFree(h_mem)
            return True
        return False
