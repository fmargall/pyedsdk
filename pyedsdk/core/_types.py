import ctypes

from enum import IntEnum


# -------- Reference types --------
# Number of types binded: 8 / 9

_BaseRef = ctypes.c_void_p

_CameraListRef    = ctypes.c_void_p
_CameraRef        = ctypes.c_void_p
_VolumeRef        = ctypes.c_void_p
_FlashRef         = ctypes.c_void_p
_DirectoryItemRef = ctypes.c_void_p

_StreamRef        = ctypes.c_void_p

_EvfImageRef      = ctypes.c_void_p


# File and Properties Access
class _Access(IntEnum):
    _Read      = 0
    _Write     = 1
    _ReadWrite = 2
    _Error     = 0xFFFFFFFF

class _Rational(ctypes.Structure):
    _fields_ = [
        ("numerator"  , ctypes.c_int32),
        ("denominator", ctypes.c_uint32)
    ]

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
class ImageQuality(IntEnum):
    # --------- Image quality --------
    LJ = 0x0010FF0F
    MJ = 0x0110FF0F
    M1J = 0x0510FF0F
    M1F = 0x0513FF0F
    M1N = 0x0512FF0F
    M2J = 0x0610FF0F
    M2F = 0x0613FF0F
    M2N = 0x0612FF0F
    SJ = 0x0210FF0F
    S1J = 0x0E10FF0F
    S2J = 0x0F10FF0F
    LJF = 0x0013FF0F
    LJN = 0x0012FF0F
    MJF = 0x0113FF0F
    MJN = 0x0112FF0F
    SJF = 0x0213FF0F
    SJN = 0x0212FF0F
    S1JF = 0x0E13FF0F
    S1JN = 0x0E12FF0F
    S2JF = 0x0F13FF0F
    S3JF = 0x1013FF0F
    LR = 0x0064FF0F
    LRLJF = 0x00640013
    LRLJN = 0x00640012
    LRMJF = 0x00640113
    LRMJN = 0x00640112
    LRSJF = 0x00640213
    LRSJN = 0x00640212
    LRS1JF = 0x00640E13
    LRS1JN = 0x00640E12
    LRS2JF = 0x00640F13
    LRS3JF = 0x00641013
    LRLJ = 0x00640010
    LRMJ = 0x00640110
    LRM1J = 0x00640510
    LRM1F = 0x00640513
    LRM1N = 0x00640512
    LRM2J = 0x00640610
    LRM2F = 0x00640613
    LRM2N = 0x00640612
    LRSJ = 0x00640210
    LRS1J = 0x00640E10
    LRS2J = 0x00640F10
    MR = 0x0164FF0F
    MRLJF = 0x01640013
    MRLJN = 0x01640012
    MRMJF = 0x01640113
    MRMJN = 0x01640112
    MRSJF = 0x01640213
    MRSJN = 0x01640212
    MRS1JF = 0x01640E13
    MRS1JN = 0x01640E12
    MRS2JF = 0x01640F13
    MRS3JF = 0x01641013
    MRLJ = 0x01640010
    MRM1J = 0x01640510
    MRM1F = 0x01640513
    MRM1N = 0x01640512
    MRM2J = 0x01640610
    MRM2F = 0x01640613
    MRM2N = 0x01640612
    MRSJ = 0x01640210
    SR = 0x0264FF0F
    SRLJF = 0x02640013
    SRLJN = 0x02640012
    SRMJF = 0x02640113
    SRMJN = 0x02640112
    SRSJF = 0x02640213
    SRSJN = 0x02640212
    SRS1JF = 0x02640E13
    SRS1JN = 0x02640E12
    SRS2JF = 0x02640F13
    SRS3JF = 0x02641013
    SRLJ = 0x02640010
    SRM1J = 0x02640510
    SRM1F = 0x02640513
    SRM1N = 0x02640512
    SRM2J = 0x02640610
    SRM2F = 0x02640613
    SRM2N = 0x02640612
    SRSJ = 0x02640210
    CR = 0x0063FF0F
    CRLJF = 0x00630013
    CRMJF = 0x00630113
    CRM1JF = 0x00630513
    CRM2JF = 0x00630613
    CRSJF = 0x00630213
    CRS1JF = 0x00630E13
    CRS2JF = 0x00630F13
    CRS3JF = 0x00631013
    CRLJN = 0x00630012
    CRMJN = 0x00630112
    CRM1JN = 0x00630512
    CRM2JN = 0x00630612
    CRSJN = 0x00630212
    CRS1JN = 0x00630E12
    CRLJ = 0x00630010
    CRMJ = 0x00630110
    CRM1J = 0x00630510
    CRM2J = 0x00630610
    CRSJ = 0x00630210
    CRS1J = 0x00630E10
    CRS2J = 0x00630F10
    HEIFL = 0x0080FF0F
    HEIFM = 0x0180FF0F
    HEIFM1 = 0x0580FF0F
    HEIFM2 = 0x0680FF0F
    HEIFLF = 0x0083FF0F
    HEIFLN = 0x0082FF0F
    HEIFMF = 0x0183FF0F
    HEIFMN = 0x0182FF0F
    HEIFS1 = 0x0E80FF0F
    HEIFS1F = 0x0E83FF0F
    HEIFS1N = 0x0E82FF0F
    HEIFS2 = 0x0F80FF0F
    HEIFS2F = 0x0F83FF0F
    RHEIFL = 0x00640080
    RHEIFLF = 0x00640083
    RHEIFLN = 0x00640082
    RHEIFM = 0x00640180
    RHEIFM1 = 0x00640580
    RHEIFM2 = 0x00640680
    RHEIFMF = 0x00640183
    RHEIFMN = 0x00640182
    RHEIFS1 = 0x00640E80
    RHEIFS1F = 0x00640E83
    RHEIFS1N = 0x00640E82
    RHEIFS2 = 0x00640F80
    RHEIFS2F = 0x00640F83
    CRHEIFL = 0x00630080
    CRHEIFLF = 0x00630083
    CRHEIFLN = 0x00630082
    CRHEIFM = 0x00630180
    CRHEIFMF = 0x00630183
    CRHEIFMN = 0x00630182
    CRHEIFM1 = 0x00630580
    CRHEIFM2 = 0x00630680
    CRHEIFS1 = 0x00630E80
    CRHEIFS1F = 0x00630E83
    CRHEIFS1N = 0x00630E82
    CRHEIFS2 = 0x00630F80
    CRHEIFS2F = 0x00630F83
    Unknown = 0xFFFFFFFF

# Save To
class _SaveTo(IntEnum):
    # ---------- Save-to ----------
    _Camera = 1
    _Host   = 2
    _Both   = 3

# Mirror lockup state
class _MirrorLockUpState(IntEnum):
    _Disable        = 0
    _Enable         = 1
    _DuringShooting = 2

# Mirror up setting
class _MirrorUpSetting(IntEnum):
    _Off = 0
    _On  = 1

# Camera commands
class _CameraCommand(IntEnum):
    # --------- Send commands ---------
    # Number of commands binded: 2 / 15
    _TakePicture = 0x00000000

    _PressShutterButton = 0x00000004

# Shutter button
class _ShutterButton(IntEnum):
    # Number of status binded: 5 / 5
    _OFF              = 0x00000000
    _Halfway          = 0x00000001
    _Completely       = 0x00000003
    _Halfway_NonAF    = 0x00010001
    _Completely_NonAF = 0x00010003

# Camera Status commands
class _CameraStatusCommand(IntEnum):
    # Number of status commands binded: 4 / 4
    _UILock              = 0x00000000
    _UIUnlock            = 0x00000001
    _EnterDirectTransfer = 0x00000002
    _ExitDirectTransfer  = 0x00000003

class _PropertyEvent(IntEnum):
    # Number of events binded: 4 / 4
    _All                   = 0x00000100
    _PropertyChanged       = 0x00000101
    _PropertyDescChanged   = 0x00000102
    _PropertyDescExChanged = 0x00000110

class _ObjectEvent(IntEnum):
    # Number of events binded: 2 / 13

    # Notifies all object events
    _All = 0x00000200

    # Notifies that objects on camera are waiting for transfer
    # It is then mandatory to execute either EdsDownloadCancel
    # EdsDownload to continue
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
    # Number of properties binded: 7 / 38
    _ISOSpeed    = 0x00000402
    _AFMode      = 0x00000404 # Autofocus
    _Av          = 0x00000405 # Aperture
    _Tv          = 0x00000406 # Shutter speed
    _FocalLength = 0x00000409
    _FlashOn     = 0x00000412
    _FlashMode   = 0x00000414

    # --------- EVF properties ----------
    # Number of properties binded: 2 / 22
    _Evf_OutputDevice = 0x00000500
    _Evf_Mode         = 0x00000501

    # -------- Limited properties -------
    # Number of properties binded: 5 / 39
    _MirrorLockUpState = 0x01000421
    _MirrorUpSetting   = 0x01000438
    _RegisterFocusEdge = 0x0100046C 
    _DriveFocusToEdge  = 0x0100046D
    _FocusPosition     = 0x0100046E

    # -------- Flash properties ---------
    # Number of properties binded:  2 / 2
    _Flash_Firing = 0x0000200D
    _Flash_Target = 0x0000201E
