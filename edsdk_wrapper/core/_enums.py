from enum import IntEnum


class _Aperture(IntEnum):
    _f1      = 0x08
    _f1_1    = 0x0B
    _f1_2    = 0x0C
    _f1_2_p  = 0x0D
    _f1_4    = 0x10
    _f1_6    = 0x13
    _f1_8    = 0x14
    _f1_8_p  = 0x15
    _f2      = 0x18
    _f2_2    = 0x1B
    _f2_5    = 0x1C
    _f2_5_p  = 0x1D
    _f2_8    = 0x20
    _f3_2    = 0x23
    _f3_4    = 0x85
    _f3_5    = 0x24
    _f3_5_p  = 0x25
    _f4      = 0x28
    _f4_5    = 0x2B
    _f5      = 0x2D
    _f5_6    = 0x30
    _f6_3    = 0x33
    _f6_7    = 0x34
    _f7_1    = 0x35
    _f8      = 0x38
    _f9      = 0x3B
    _f9_5    = 0x3C
    _f10     = 0x3D
    _f11     = 0x40
    _f13_p   = 0x43
    _f13     = 0x44
    _f14     = 0x45
    _f16     = 0x48
    _f18     = 0x4B
    _f19     = 0x4C
    _f20     = 0x4D
    _f22     = 0x50
    _f25     = 0x53
    _f27     = 0x54
    _f29     = 0x55
    _f32     = 0x58
    _f36     = 0x5B
    _f38     = 0x5C
    _f40     = 0x5D
    _f45     = 0x60
    _f51     = 0x63
    _f54     = 0x64
    _f57     = 0x65
    _f64     = 0x68
    _f72     = 0x6B
    _f76     = 0x6C
    _f80     = 0x6D
    _f91     = 0x70

    _Invalid = 0xFFFFFFFF

    @property
    def f_number(self) -> float | None:
        if self is self._Invalid:
            return None

        mapping = {
            self._f1    : 1.0,
            self._f1_1  : 1.1,
            self._f1_2  : 1.2,
            self._f1_2_p: 1.2 * (2 ** (1/6)),
            self._f1_4  : 1.4,
            self._f1_6  : 1.6,
            self._f1_8  : 1.8,
            self._f1_8_p: 1.8 * (2 ** (1/6)),
            self._f2    : 2.0,
            self._f2_2  : 2.2,
            self._f2_5  : 2.5,
            self._f2_5_p: 2.5 * (2 ** (1/6)),
            self._f2_8  : 2.8,
            self._f3_2  : 3.2,
            self._f3_4  : 3.4,
            self._f3_5  : 3.5,
            self._f3_5_p: 3.5 * (2 ** (1/6)),
            self._f4    : 4.0,
            self._f4_5  : 4.5,
            self._f5    : 5.0,
            self._f5_6  : 5.6,
            self._f6_3  : 6.3,
            self._f6_7  : 6.7,
            self._f7_1  : 7.1,
            self._f8    : 8.0,
            self._f9    : 9.0,
            self._f9_5  : 9.5,
            self._f10   : 10.0,
            self._f11   : 11.0,
            self._f13_p : 13.0 * (2 ** (1/6)),
            self._f13   : 13.0,
            self._f14   : 14.0,
            self._f16   : 16.0,
            self._f18   : 18.0,
            self._f19   : 19.0,
            self._f20   : 20.0,
            self._f22   : 22.0,
            self._f25   : 25.0,
            self._f27   : 27.0,
            self._f29   : 29.0,
            self._f32   : 32.0,
            self._f36   : 36.0,
            self._f38   : 38.0,
            self._f40   : 40.0,
            self._f45   : 45.0,
            self._f51   : 51.0,
            self._f54   : 54.0,
            self._f57   : 57.0,
            self._f64   : 64.0,
            self._f72   : 72.0,
            self._f76   : 76.0,
            self._f80   : 80.0,
            self._f91   : 91.0,
        }
        return mapping.get(self, None)

    @property
    def label(self) -> str:
        if self is self._Invalid:
            return "Not valid"

        return f"f/{self.f_number}"


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
            self._30s  : 30.0,
            self._25s  : 25.0,
            self._20s  : 20.0,
            self._20s_p: 20.0 * (2 ** (-1/3)),
            self._15s  : 15.0,
            self._13s  : 13.0,
            self._10s  : 10.0,
            self._10s_p: 10.0 * (2 ** (-1/3)),
            self._8s   : 8.0,
            self._6s   : 6.0,
            self._6s_p : 6.0 * (2 ** (-1/3)),
            self._5s   : 5.0,
            self._4s   : 4.0,
            self._3s2  : 3.2,
            self._3s   : 3.0,
            self._2s5  : 2.5,
            self._2s   : 2.0,
            self._1s6  : 1.6,
            self._1s5  : 1.5,
            self._1s3  : 1.3,
            self._1s   : 1.0,
            self._0s8  : 0.8,
            self._0s7  : 0.7,
            self._0s6  : 0.6,
            self._0s5  : 0.5,
            self._0s4  : 0.4,
            self._0s3  : 0.3,
            self._0s3_p: 0.3 * (2 ** (-1/3)),

            # Fractions
            self._1_4    : 1/4,
            self._1_5    : 1/5,
            self._1_6    : 1/6,
            self._1_6_p  : (1/6) * (2 ** (-1/3)),
            self._1_8    : 1/8,
            self._1_10   : 1/10,
            self._1_10_p : (1/10) * (2 ** (-1/3)),
            self._1_13   : 1/13,
            self._1_15   : 1/15,
            self._1_20   : 1/20,
            self._1_20_p : (1/20) * (2 ** (-1/3)),
            self._1_25   : 1/25,
            self._1_30   : 1/30,
            self._1_40   : 1/40,
            self._1_45   : 1/45,
            self._1_50   : 1/50,
            self._1_60   : 1/60,
            self._1_80   : 1/80,
            self._1_90   : 1/90,
            self._1_100  : 1/100,
            self._1_125  : 1/125,
            self._1_160  : 1/160,
            self._1_180  : 1/180,
            self._1_200  : 1/200,
            self._1_250  : 1/250,
            self._1_320  : 1/320,
            self._1_350  : 1/350,
            self._1_400  : 1/400,
            self._1_500  : 1/500,
            self._1_640  : 1/640,
            self._1_750  : 1/750,
            self._1_800  : 1/800,
            self._1_1000 : 1/1000,
            self._1_1250 : 1/1250,
            self._1_1500 : 1/1500,
            self._1_1600 : 1/1600,
            self._1_2000 : 1/2000,
            self._1_2500 : 1/2500,
            self._1_3000 : 1/3000,
            self._1_3200 : 1/3200,
            self._1_4000 : 1/4000,
            self._1_5000 : 1/5000,
            self._1_6000 : 1/6000,
            self._1_6400 : 1/6400,
            self._1_8000 : 1/8000,
            self._1_10000: 1/10000,
            self._1_12800: 1/12800,
            self._1_16000: 1/16000,
            self._1_20000: 1/20000,
            self._1_25600: 1/25600,
            self._1_32000: 1/32000,
        }
        return mapping.get(self, None)


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

    @property
    def value(self) -> float:
        if self is _ISOSpeed._ISO_Auto:
            return float("nan")

        # Enum name is always like "_ISO_6400"
        return float(self.name.split("_")[-1])