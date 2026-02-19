import ctypes

from enum import IntEnum


# -------- Reference types --------
# Number of types binded: 5 / 9

_BaseRef = ctypes.c_void_p

_CameraListRef    = ctypes.c_void_p
_CameraRef        = ctypes.c_void_p
_VolumeRef        = ctypes.c_void_p
_DirectoryItemRef = ctypes.c_void_p

_StreamRef        = ctypes.c_void_p


# File and Properties Access
class _Access(IntEnum):
    _Read      = 0
    _Write     = 1
    _ReadWrite = 2
    _Error     = 0xFFFFFFFF


class _DeviceInfo(ctypes.Structure):
    _fields_ = [
        ("szPortName"         , ctypes.c_char * 256),
        ("szDeviceDescription", ctypes.c_char * 256),
        ("deviceSubType"      , ctypes.c_uint32),
        ("reserved"           , ctypes.c_uint32)
    ]

class _VolumeInfo(ctypes.Structure):
    _fields_ = [
        ("storageType"     , ctypes.c_uint32),
        ("_access"         , ctypes.c_uint32),
        ("maxCapacity"     , ctypes.c_uint64),
        ("freeSpaceInBytes", ctypes.c_uint64),
        ("szVolumeLabel"   , ctypes.c_char * 256)
    ]

    @property
    def access(self) -> _Access:
        return _Access(ctypes.c_uint32(self._access).value)

class _DirectoryItemInfo(ctypes.Structure):
    _fields_ = [
        ("size"      , ctypes.c_uint64),
        ("isFolder"  , ctypes.c_int32),
        ("groupID"   , ctypes.c_uint32),
        ("option"    , ctypes.c_uint32),
        ("szFileName", ctypes.c_char * 256),

        ("format"    , ctypes.c_uint32),
        ("dateTime"  , ctypes.c_uint32)

    ]

class _PropertyDesc(ctypes.Structure):
    _fields_ = [
        ("form"       , ctypes.c_int32),
        ("access"     , ctypes.c_int32),
        ("numElements", ctypes.c_int32),
        ("propDesc"   , ctypes.c_int32 * 128)
    ]

    @property
    def values(self) -> list:
        return [self.propDesc[i] for i in range(self.numElements)]

class _Capacity(ctypes.Structure):
    _fields_ = [
        ("numberOfFreeClusters", ctypes.c_int32),
        ("bytesPerSector"      , ctypes.c_int32),
        ("reset"               , ctypes.c_int32)
    ]


# Camera commands
class _CameraCommand(IntEnum):
    # --------- Send commands ---------
    # Number of commands binded: 1 / 15
    _TakePicture = 0x00000000

class _ObjectEvent(IntEnum):
    # Number of events binded: 2 / 13

    # Notifies all object events.
    _All = 0x00000200

    # Notifies that objects on camera are waiting for transfer
    # It is then mandatory to execute either EdsDownloadCancel
    # EdsDownload to continue.
    _DirItemRequestTransfer = 0x00000208

# File create disposition
class _FileCreateDisposition(IntEnum):
    _CreateNew        = 0
    _CreateAlways     = 1
    _OpenExisting     = 2
    _OpenAlways       = 3
    _TruncateExisting = 4


# Property IDs
class _PropertyID(IntEnum):
    # --------- Camera settings ---------
    # Number of properties binded: 1 / 13
    _SaveTo = 0x0000000b

    # ------- Capture properties --------
    # Number of properties binded: 1 / 38
    _ISOSpeed = 0x00000402

class _ISOSpeed(IntEnum):
    _ISO_Auto   = 0x00000000
    _ISO_6      = 0x00000028
    _ISO_12     = 0x00000030
    _ISO_25     = 0x00000038
    _ISO_50     = 0x00000040
    _ISO_100    = 0x00000048
    _ISO_125    = 0x0000004B
    _ISO_160    = 0x0000004D
    _ISO_200    = 0x00000050
    _ISO_250    = 0x00000053
    _ISO_320    = 0x00000055
    _ISO_400    = 0x00000058
    _ISO_500    = 0x0000005B
    _ISO_640    = 0x0000005D
    _ISO_800    = 0x00000060
    _ISO_1000   = 0x00000063
    _ISO_1250   = 0x00000065
    _ISO_1600   = 0x00000068
    _ISO_2000   = 0x0000006B
    _ISO_2500   = 0x0000006D
    _ISO_3200   = 0x00000070
    _ISO_4000   = 0x00000073
    _ISO_5000   = 0x00000075
    _ISO_6400   = 0x00000078
    _ISO_8000   = 0x0000007B
    _ISO_10000  = 0x0000007D
    _ISO_12800  = 0x00000080
    _ISO_16000  = 0x00000083
    _ISO_20000  = 0x00000085
    _ISO_25600  = 0x00000088
    _ISO_32000  = 0x0000008B
    _ISO_40000  = 0x0000008D
    _ISO_51200  = 0x00000090
    _ISO_64000  = 0x00000093
    _ISO_80000  = 0x00000095
    _ISO_102400 = 0x00000098
    _ISO_204800 = 0x000000A0
    _ISO_409600 = 0x000000A8
    _ISO_819200 = 0x000000B0

# Save To
class _SaveTo(IntEnum):
    # ---------- Save-to ----------
    _Camera = 1
    _Host   = 2
    _Both   = 3