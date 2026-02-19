import ctypes
import time

from ._errors import _ErrorCode
from ._types  import _BaseRef
from ._types  import _ObjectEvent


_ObjectEventHandler = ctypes.WINFUNCTYPE(
    ctypes.c_uint32,   # _ErrorCode
    ctypes.c_uint32,   # _ObjectEvent
    _BaseRef,
    ctypes.c_void_p
)

_PM_REMOVE = 0x0001
_user32    = ctypes.windll.user32

class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd"   , ctypes.c_void_p),
        ("message", ctypes.c_uint),
        ("wParam" , ctypes.c_void_p),
        ("lParam" , ctypes.c_void_p),
        ("time"   , ctypes.c_uint32),
        ("pt_x"   , ctypes.c_long),
        ("pt_y"   , ctypes.c_long),
]

def _pumpWindowsMessages():
    msg = MSG()

    while _user32.PeekMessageW(
        ctypes.byref(msg), None, 0, 0, _PM_REMOVE):
        _user32.TranslateMessage(ctypes.byref(msg))
        _user32.DispatchMessageW(ctypes.byref(msg))

def _waitForEvent(event, timeout=15):
    start = time.time()

    while not event.is_set():
        _pumpWindowsMessages()
        time.sleep(0.01)

        if time.time() - start > timeout:
            raise TimeoutError(f"EDSDK event timeout after {timeout} seconds")