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
    # Number of properties binded: 2 / 38
    _ISOSpeed = 0x00000402
    _Tv       = 0x00000406 # Shutter speed

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

class _ShutterSpeed(IntEnum):
    # Long exposures
    _Bulb  = 0x0C
    _30s   = 0x10
    _25s   = 0x13
    _20s   = 0x14
    _20s_p = 0x15 # 20" (1/3)
    _15s   = 0x18
    _13s   = 0x1B
    _10s   = 0x1C
    _10s_p = 0x1D # 10" (1/3)
    _8s    = 0x20
    _6s    = 0x23
    _6s_p  = 0x24 #  6" (1/3)
    _5s    = 0x25
    _4s    = 0x28
    _3s2   = 0x2B
    _3s    = 0x2C
    _2s5   = 0x2D
    _2s    = 0x30
    _1s6   = 0x33
    _1s5   = 0x34
    _1s3   = 0x35
    _1s    = 0x38
    _0s8   = 0x3B
    _0s7   = 0x3C
    _0s6   = 0x3D
    _0s5   = 0x40
    _0s4   = 0x43
    _0s3   = 0x44
    _0s3_p = 0x45

    # Fractions
    _1_4       = 0x48
    _1_5       = 0x4B
    _1_6       = 0x4C
    _1_6_p     = 0x4D
    _1_8       = 0x50
    _1_10_p    = 0x53
    _1_10      = 0x54
    _1_13      = 0x55
    _1_15      = 0x58
    _1_20_p    = 0x5B
    _1_20      = 0x5C
    _1_25      = 0x5D
    _1_30      = 0x60
    _1_40      = 0x63
    _1_45      = 0x64
    _1_50      = 0x65
    _1_60      = 0x68
    _1_80      = 0x6B
    _1_90      = 0x6C
    _1_100     = 0x6D
    _1_125     = 0x70
    _1_160     = 0x73
    _1_180     = 0x74
    _1_200     = 0x75
    _1_250     = 0x78
    _1_320     = 0x7B
    _1_350     = 0x7C
    _1_400     = 0x7D
    _1_500     = 0x80
    _1_640     = 0x83
    _1_750     = 0x84
    _1_800     = 0x85
    _1_1000    = 0x88
    _1_1250    = 0x8B
    _1_1500    = 0x8C
    _1_1600    = 0x8D
    _1_2000    = 0x90
    _1_2500    = 0x93
    _1_3000    = 0x94
    _1_3200    = 0x95
    _1_4000    = 0x98
    _1_5000    = 0x9B
    _1_6000    = 0x9C
    _1_6400    = 0x9D
    _1_8000    = 0xA0
    _1_10000   = 0xA3
    _1_12800   = 0xA5
    _1_16000   = 0xA8
    _1_20000   = 0xAB
    _1_25600   = 0xAD
    _1_32000   = 0xB0

    _Invalid   = 0xFFFFFFFF

    @property
    def label(self) -> str:
        mapping = {
            self._Bulb   : "Bulb",
            self._30s    : '30"',
            self._25s    : '25"',
            self._20s    : '20"',
            self._20s_p  : '20" (1/3)',
            self._15s    : '15"',
            self._13s    : '13"',
            self._10s    : '10"',
            self._10s_p  : '10" (1/3)',
            self._8s     : '8"',
            self._6s     : '6"',
            self._6s_p   : '6" (1/3)',
            self._5s     : '5"',
            self._4s     : '4"',
            self._3s2    : '3"2',
            self._3s     : '3"',
            self._2s5    : '2"5',
            self._2s     : '2"',
            self._1s6    : '1"6',
            self._1s5    : '1"5',
            self._1s3    : '1"3',
            self._1s     : '1"',
            self._0s8    : '0"8',
            self._0s7    : '0"7',
            self._0s6    : '0"6',
            self._0s5    : '0"5',
            self._0s4    : '0"4',
            self._0s3    : '0"3',
            self._0s3_p  : '0"3 (1/3)',
            self._1_4    : "1/4",
            self._1_5    : "1/5",
            self._1_6    : "1/6",
            self._1_6_p  : "1/6 (1/3)",
            self._1_8    : "1/8",
            self._1_10   : "1/10",
            self._1_10_p : "1/10 (1/3)",
            self._1_13   : "1/13",
            self._1_15   : "1/15",
            self._1_20   : "1/20",
            self._1_20_p : "1/20 (1/3)",
            self._1_25   : "1/25",
            self._1_30   : "1/30",
            self._1_40   : "1/40",
            self._1_45   : "1/45",
            self._1_50   : "1/50",
            self._1_60   : "1/60",
            self._1_80   : "1/80",
            self._1_90   : "1/90",
            self._1_100  : "1/100",
            self._1_125  : "1/125",
            self._1_160  : "1/160",
            self._1_180  : "1/180",
            self._1_200  : "1/200",
            self._1_250  : "1/250",
            self._1_320  : "1/320",
            self._1_350  : "1/350",
            self._1_400  : "1/400",
            self._1_500  : "1/500",
            self._1_640  : "1/640",
            self._1_750  : "1/750",
            self._1_800  : "1/800",
            self._1_1000 : "1/1000",
            self._1_1250 : "1/1250",
            self._1_1500 : "1/1500",
            self._1_1600 : "1/1600",
            self._1_2000 : "1/2000",
            self._1_2500 : "1/2500",
            self._1_3000 : "1/3000",
            self._1_3200 : "1/3200",
            self._1_4000 : "1/4000",
            self._1_5000 : "1/5000",
            self._1_6000 : "1/6000",
            self._1_6400 : "1/6400",
            self._1_8000 : "1/8000",
            self._1_10000: "1/10000",
            self._1_12800: "1/12800",
            self._1_16000: "1/16000",
            self._1_20000: "1/20000",
            self._1_25600: "1/25600",
            self._1_32000: "1/32000",
            self._Invalid: "Not valid",
        }
        return mapping.get(self, "Unknown")

    @property
    def seconds(self) -> float | None:

        if self in {self._Bulb, self._Invalid}:
            return None

        mapping = {

            # Long exposures
            self._30s: 30.0,
            self._25s: 25.0,
            self._20s: 20.0,
            self._20s_p: 20.0 * (2 ** (-1/3)),
            self._15s: 15.0,
            self._13s: 13.0,
            self._10s: 10.0,
            self._10s_p: 10.0 * (2 ** (-1/3)),
            self._8s: 8.0,
            self._6s: 6.0,
            self._6s_p: 6.0 * (2 ** (-1/3)),
            self._5s: 5.0,
            self._4s: 4.0,
            self._3s2: 3.2,
            self._3s: 3.0,
            self._2s5: 2.5,
            self._2s: 2.0,
            self._1s6: 1.6,
            self._1s5: 1.5,
            self._1s3: 1.3,
            self._1s: 1.0,
            self._0s8: 0.8,
            self._0s7: 0.7,
            self._0s6: 0.6,
            self._0s5: 0.5,
            self._0s4: 0.4,
            self._0s3: 0.3,
            self._0s3_p: 0.3 * (2 ** (-1/3)),

            # Fractions
            self._1_4: 1/4,
            self._1_5: 1/5,
            self._1_6: 1/6,
            self._1_6_p: (1/6) * (2 ** (-1/3)),
            self._1_8: 1/8,
            self._1_10: 1/10,
            self._1_10_p: (1/10) * (2 ** (-1/3)),
            self._1_13: 1/13,
            self._1_15: 1/15,
            self._1_20: 1/20,
            self._1_20_p: (1/20) * (2 ** (-1/3)),
            self._1_25: 1/25,
            self._1_30: 1/30,
            self._1_40: 1/40,
            self._1_45: 1/45,
            self._1_50: 1/50,
            self._1_60: 1/60,
            self._1_80: 1/80,
            self._1_90: 1/90,
            self._1_100: 1/100,
            self._1_125: 1/125,
            self._1_160: 1/160,
            self._1_180: 1/180,
            self._1_200: 1/200,
            self._1_250: 1/250,
            self._1_320: 1/320,
            self._1_350: 1/350,
            self._1_400: 1/400,
            self._1_500: 1/500,
            self._1_640: 1/640,
            self._1_750: 1/750,
            self._1_800: 1/800,
            self._1_1000: 1/1000,
            self._1_1250: 1/1250,
            self._1_1500: 1/1500,
            self._1_1600: 1/1600,
            self._1_2000: 1/2000,
            self._1_2500: 1/2500,
            self._1_3000: 1/3000,
            self._1_3200: 1/3200,
            self._1_4000: 1/4000,
            self._1_5000: 1/5000,
            self._1_6000: 1/6000,
            self._1_6400: 1/6400,
            self._1_8000: 1/8000,
            self._1_10000: 1/10000,
            self._1_12800: 1/12800,
            self._1_16000: 1/16000,
            self._1_20000: 1/20000,
            self._1_25600: 1/25600,
            self._1_32000: 1/32000,
        }

        return mapping.get(self, None)

# Save To
class _SaveTo(IntEnum):
    # ---------- Save-to ----------
    _Camera = 1
    _Host   = 2
    _Both   = 3