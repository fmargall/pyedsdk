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


# --------- Image quality ---------
# Image type
class _ImageType(IntEnum):
    _Unknown = 0x00000000
    _JPEG    = 0x00000001
    _CRW     = 0x00000002
    _RAW     = 0x00000004
    _CR2     = 0x00000006
    _HEIF    = 0x00000008

# Image size
class _ImageSize(IntEnum):
    _Large   = 0
    _Middle  = 1
    _Small   = 2
    _Middle1 = 5
    _Middle2 = 6
    _Small1  = 14
    _Small2  = 15
    _Small3  = 16
    _Unknown = 0xFFFFFFFF

# Image compress quality
class _ImageCompressQuality(IntEnum):
    _Normal    = 2
    _Fine      = 3
    _Lossless  = 4
    _Superfine = 5
    _Unknown   = 0xFFFFFFFF

# Image quality
class _ImageQuality(IntEnum):
    # --------- Image quality --------
    # Number of values binded: 1 / 143
    _LR = 0x0064FF0F # RAW


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

    # --------- Image properties --------
    # Number of properties binded: 1 / 11
    _ImageQuality = 0x00000100

    # ------- Capture properties --------
    # Number of properties binded: 3 / 38
    _ISOSpeed = 0x00000402
    _AFMode   = 0x00000404 # Autofocus
    _Av       = 0x00000405 # Aperture
    _Tv       = 0x00000406 # Shutter speed

# Save To
class _SaveTo(IntEnum):
    # ---------- Save-to ----------
    _Camera = 1
    _Host   = 2
    _Both   = 3