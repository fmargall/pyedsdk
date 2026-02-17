from enum import IntEnum

"""ctypes return-type hook for Canon EDSDK functions.

   This function is intended to be assigned to the ``restype`` attribute
   of EDSDK functions that return an ``EdsError`` code. It automatically
   checks the returned value and raises a ``CanonError`` if the call
   did not succeed.

   If the return code corresponds to ``ErrorCode.ERR_OK``, the function
   returns the corresponding ``ErrorCode`` enum value. Otherwise,
   a ``CanonError`` exception is raised.

   This mechanism allows transparent error handling without requiring
   explicit error checks after each SDK function call.

   Parameters
   ----------
   code : int
       The raw return value from the EDSDK function.

   Returns
   -------
   ErrorCode
       The corresponding ErrorCode enum value if the call succeeded.

   Raises
   ------
   CanonError
       If the return code is different from ErrorCode.ERR_OK.
"""
def _error_restype(code):
    if int(code) != ErrorCode.ERR_OK:
        raise CanonError(code)

    return ErrorCode(code)


class CanonError(Exception):
    def __init__(self, code: int):
        try:
            self.code    = ErrorCode(code)
            self.name    = self.code.name
            self.message = self.code.message
        except ValueError:
            self.code    = code
            self.name    = "UNKNOWN_ERROR"
            self.message = "Unknown Canon SDK error."

        super().__init__(f"[{self.name}] (0x{int(code):08X}) {self.message}")


class ErrorCode(IntEnum):
    # Error Code Masks
    ISSPECIFIC_MASK  = 0x80000000
    COMPONENTID_MASK = 0x7F000000
    RESERVED_MASK    = 0x00FF0000
    ERRORID_MASK     = 0x0000FFFF

    # Base Component IDs
    CMP_ID_CLIENT_COMPONENTID = 0x01000000
    CMP_ID_LLSDK_COMPONENTID  = 0x02000000
    CMP_ID_HLSDK_COMPONENTID  = 0x03000000

    # Function Success Code
    ERR_OK = 0x00000000

    # -------- Generic Error IDs --------
    # Miscellaneous errors
    ERR_UNIMPLEMENTED         = 0x00000001
    ERR_INTERNAL_ERROR        = 0x00000002
    ERR_MEM_ALLOC_FAILED      = 0x00000003
    ERR_MEM_FREE_FAILED       = 0x00000004
    ERR_OPERATION_CANCELLED   = 0x00000005
    ERR_INCOMPATIBLE_VERSION  = 0x00000006
    ERR_NOT_SUPPORTED         = 0x00000007
    ERR_UNEXPECTED_EXCEPTION  = 0x00000008
    ERR_PROTECTION_VIOLATION  = 0x00000009
    ERR_MISSING_SUBCOMPONENT  = 0x0000000A
    ERR_SELECTION_UNAVAILABLE = 0x0000000B

    # File errors
    ERR_FILE_IO_ERROR            = 0x00000020
    ERR_FILE_TOO_MANY_OPEN       = 0x00000021
    ERR_FILE_NOT_FOUND           = 0x00000022
    ERR_FILE_OPEN_ERROR          = 0x00000023
    ERR_FILE_CLOSE_ERROR         = 0x00000024
    ERR_FILE_SEEK_ERROR          = 0x00000025
    ERR_FILE_TELL_ERROR          = 0x00000026
    ERR_FILE_READ_ERROR          = 0x00000027
    ERR_FILE_WRITE_ERROR         = 0x00000028
    ERR_FILE_PERMISSION_ERROR    = 0x00000029
    ERR_FILE_DISK_FULL_ERROR     = 0x0000002A
    ERR_FILE_ALREADY_EXISTS      = 0x0000002B
    ERR_FILE_FORMAT_UNRECOGNIZED = 0x0000002C
    ERR_FILE_DATA_CORRUPT        = 0x0000002D
    ERR_FILE_NAMING_NA           = 0x0000002E

    # Directory errors
    ERR_DIR_NOT_FOUND       = 0x00000040
    ERR_DIR_IO_ERROR        = 0x00000041
    ERR_DIR_ENTRY_NOT_FOUND = 0x00000042
    ERR_DIR_ENTRY_EXISTS    = 0x00000043
    ERR_DIR_NOT_EMPTY       = 0x00000044

    # Property errors
    ERR_PROPERTIES_UNAVAILABLE = 0x00000050
    ERR_PROPERTIES_MISMATCH    = 0x00000051
    ERR_PROPERTIES_NOT_LOADED  = 0x00000053

    # Function parameter errors
    ERR_INVALID_PARAMETER  = 0x00000060
    ERR_INVALID_HANDLE     = 0x00000061
    ERR_INVALID_POINTER    = 0x00000062
    ERR_INVALID_INDEX      = 0x00000063
    ERR_INVALID_LENGTH     = 0x00000064
    ERR_INVALID_FN_POINTER = 0x00000065
    ERR_INVALID_SORT_FN    = 0x00000066

    # Device errors
    ERR_DEVICE_NOT_FOUND         = 0x00000080
    ERR_DEVICE_BUSY              = 0x00000081
    ERR_DEVICE_INVALID           = 0x00000082
    ERR_DEVICE_EMERGENCY         = 0x00000083
    ERR_DEVICE_MEMORY_FULL       = 0x00000084
    ERR_DEVICE_INTERNAL_ERROR    = 0x00000085
    ERR_DEVICE_INVALID_PARAMETER = 0x00000086
    ERR_DEVICE_NO_DISK           = 0x00000087
    ERR_DEVICE_DISK_ERROR        = 0x00000088
    ERR_DEVICE_CF_GATE_CHANGED   = 0x00000089
    ERR_DEVICE_DIAL_CHANGED      = 0x0000008A
    ERR_DEVICE_NOT_INSTALLED     = 0x0000008B
    ERR_DEVICE_STAY_AWAKE        = 0x0000008C
    ERR_DEVICE_NOT_RELEASED      = 0x0000008D

    # Stream errors
    ERR_STREAM_IO_ERROR             = 0x000000A0
    ERR_STREAM_NOT_OPEN             = 0x000000A1
    ERR_STREAM_ALREADY_OPEN         = 0x000000A2
    ERR_STREAM_OPEN_ERROR           = 0x000000A3
    ERR_STREAM_CLOSE_ERROR          = 0x000000A4
    ERR_STREAM_SEEK_ERROR           = 0x000000A5
    ERR_STREAM_TELL_ERROR           = 0x000000A6
    ERR_STREAM_READ_ERROR           = 0x000000A7
    ERR_STREAM_WRITE_ERROR          = 0x000000A8
    ERR_STREAM_PERMISSION_ERROR     = 0x000000A9
    ERR_STREAM_COULDNT_BEGIN_THREAD = 0x000000AA
    ERR_STREAM_BAD_OPTIONS          = 0x000000AB
    ERR_STREAM_END_OF_STREAM        = 0x000000AC

    # Communication errors
    ERR_COMM_PORT_IS_IN_USE      = 0x000000C0
    ERR_COMM_DISCONNECTED        = 0x000000C1
    ERR_COMM_DEVICE_INCOMPATIBLE = 0x000000C2
    ERR_COMM_BUFFER_FULL         = 0x000000C3
    ERR_COMM_USB_BUS_ERR         = 0x000000C4

    # Lock / unlock
    ERR_USB_DEVICE_LOCK_ERROR   = 0x000000D0
    ERR_USB_DEVICE_UNLOCK_ERROR = 0x000000D1

    # STI / WIA
    ERR_STI_UNKNOWN_ERROR        = 0x000000E0
    ERR_STI_INTERNAL_ERROR       = 0x000000E1
    ERR_STI_DEVICE_CREATE_ERROR  = 0x000000E2
    ERR_STI_DEVICE_RELEASE_ERROR = 0x000000E3
    ERR_DEVICE_NOT_LAUNCHED      = 0x000000E4

    ERR_ENUM_NA                  = 0x000000F0
    ERR_INVALID_FN_CALL          = 0x000000F1
    ERR_HANDLE_NOT_FOUND         = 0x000000F2
    ERR_INVALID_ID               = 0x000000F3
    ERR_WAIT_TIMEOUT_ERROR       = 0x000000F4

    # PTP
    ERR_SESSION_NOT_OPEN                         = 0x00002003
    ERR_INVALID_TRANSACTIONID                    = 0x00002004
    ERR_INCOMPLETE_TRANSFER                      = 0x00002007
    ERR_INVALID_STRAGEID                         = 0x00002008
    ERR_DEVICEPROP_NOT_SUPPORTED                 = 0x0000200A
    ERR_INVALID_OBJECTFORMATCODE                 = 0x0000200B
    ERR_SELF_TEST_FAILED                         = 0x00002011
    ERR_PARTIAL_DELETION                         = 0x00002012
    ERR_SPECIFICATION_BY_FORMAT_UNSUPPORTED      = 0x00002014
    ERR_NO_VALID_OBJECTINFO                      = 0x00002015
    ERR_INVALID_CODE_FORMAT                      = 0x00002016
    ERR_UNKNOWN_VENDOR_CODE                      = 0x00002017
    ERR_CAPTURE_ALREADY_TERMINATED               = 0x00002018
    ERR_PTP_DEVICE_BUSY                          = 0x00002019
    ERR_INVALID_PARENTOBJECT                     = 0x0000201A
    ERR_INVALID_DEVICEPROP_FORMAT                = 0x0000201B
    ERR_INVALID_DEVICEPROP_VALUE                 = 0x0000201C
    ERR_SESSION_ALREADY_OPEN                     = 0x0000201E
    ERR_TRANSACTION_CANCELLED                    = 0x0000201F
    ERR_SPECIFICATION_OF_DESTINATION_UNSUPPORTED = 0x00002020
    ERR_NOT_CAMERA_SUPPORT_SDK_VERSION           = 0x00002021

    # PTP Vendor
    ERR_UNKNOWN_COMMAND       = 0x0000A001
    ERR_OPERATION_REFUSED     = 0x0000A005
    ERR_LENS_COVER_CLOSE      = 0x0000A006
    ERR_LOW_BATTERY           = 0x0000A101
    ERR_OBJECT_NOTREADY       = 0x0000A102
    ERR_CANNOT_MAKE_OBJECT    = 0x0000A104
    ERR_MEMORYSTATUS_NOTREADY = 0x0000A106

    # Take Picture errors
    ERR_TAKE_PICTURE_AF_NG                   = 0x00008D01
    ERR_TAKE_PICTURE_RESERVED                = 0x00008D02
    ERR_TAKE_PICTURE_MIRROR_UP_NG            = 0x00008D03
    ERR_TAKE_PICTURE_SENSOR_CLEANING_NG      = 0x00008D04
    ERR_TAKE_PICTURE_SILENCE_NG              = 0x00008D05
    ERR_TAKE_PICTURE_NO_CARD_NG              = 0x00008D06
    ERR_TAKE_PICTURE_CARD_NG                 = 0x00008D07
    ERR_TAKE_PICTURE_CARD_PROTECT_NG         = 0x00008D08
    ERR_TAKE_PICTURE_MOVIE_CROP_NG           = 0x00008D09
    ERR_TAKE_PICTURE_STROBO_CHARGE_NG        = 0x00008D0A
    ERR_TAKE_PICTURE_NO_LENS_NG              = 0x00008D0B
    ERR_TAKE_PICTURE_SPECIAL_MOVIE_MODE_NG   = 0x00008D0C
    ERR_TAKE_PICTURE_LV_REL_PROHIBIT_MODE_NG = 0x00008D0D
    ERR_TAKE_PICTURE_MOVIE_MODE_NG           = 0x00008D0E
    ERR_TAKE_PICTURE_RETRUCTED_LENS_NG       = 0x00008D0F

    ERR_LAST_GENERIC_ERROR_PLUS_ONE = 0x000000F5

    @property
    def message(self) -> str:
        return {
            # General errors
            ErrorCode.ERR_UNIMPLEMENTED         : "Not implemented"         ,
            ErrorCode.ERR_INTERNAL_ERROR        : "Internal error"          ,
            ErrorCode.ERR_MEM_ALLOC_FAILED      : "Memory allocation error" ,
            ErrorCode.ERR_MEM_FREE_FAILED       : "Memory release error"    ,
            ErrorCode.ERR_OPERATION_CANCELLED   : "Operation canceled"      ,
            ErrorCode.ERR_INCOMPATIBLE_VERSION  : "Version error"           ,
            ErrorCode.ERR_NOT_SUPPORTED         : "Not supported"           ,
            ErrorCode.ERR_UNEXPECTED_EXCEPTION  : "Unexpected exception"    ,
            ErrorCode.ERR_PROTECTION_VIOLATION  : "Protection violation"    ,
            ErrorCode.ERR_MISSING_SUBCOMPONENT  : "Missing subcomponent"    ,
            ErrorCode.ERR_SELECTION_UNAVAILABLE : "Selection unavailable"   ,

            # File access errors
            ErrorCode.ERR_FILE_IO_ERROR            : "IO error"            ,
            ErrorCode.ERR_FILE_TOO_MANY_OPEN       : "Too many files open" ,
            ErrorCode.ERR_FILE_NOT_FOUND           : "File does not exist" ,
            ErrorCode.ERR_FILE_OPEN_ERROR          : "Open error"          ,
            ErrorCode.ERR_FILE_CLOSE_ERROR         : "Close error"         ,
            ErrorCode.ERR_FILE_SEEK_ERROR          : "Seek error"          ,
            ErrorCode.ERR_FILE_TELL_ERROR          : "Tell error"          ,
            ErrorCode.ERR_FILE_READ_ERROR          : "Read error"          ,
            ErrorCode.ERR_FILE_WRITE_ERROR         : "Write error"         ,
            ErrorCode.ERR_FILE_PERMISSION_ERROR    : "Permission error"    ,
            ErrorCode.ERR_FILE_DISK_FULL_ERROR     : "Disk full"           ,
            ErrorCode.ERR_FILE_ALREADY_EXISTS      : "File already exists" ,
            ErrorCode.ERR_FILE_FORMAT_UNRECOGNIZED : "Format error"        ,
            ErrorCode.ERR_FILE_DATA_CORRUPT        : "Invalid data"        ,
            ErrorCode.ERR_FILE_NAMING_NA           : "File naming error"   ,

            # Directory errors
            ErrorCode.ERR_DIR_NOT_FOUND          : "Directory does not exist"                                   ,
            ErrorCode.ERR_DIR_IO_ERROR           : "I/O error"                                                  ,
            ErrorCode.ERR_DIR_ENTRY_NOT_FOUND    : "No file in directory"                                       ,
            ErrorCode.ERR_DIR_ENTRY_EXISTS       : "File in directory"                                          ,
            ErrorCode.ERR_DIR_NOT_EMPTY          : "Directory full"                                             ,
            ErrorCode.ERR_PROPERTIES_UNAVAILABLE : "Property (and additional property information) unavailable" ,
            ErrorCode.ERR_PROPERTIES_MISMATCH    : "Property mismatch"                                          ,
            ErrorCode.ERR_PROPERTIES_NOT_LOADED  : "Property not loaded"                                        ,

            # Function parameter errors
            ErrorCode.ERR_INVALID_PARAMETER   : "Invalid function parameter" ,
            ErrorCode.ERR_INVALID_HANDLE      : "Handle error"               ,
            ErrorCode.ERR_INVALID_POINTER     : "Pointer error"              ,
            ErrorCode.ERR_INVALID_INDEX       : "Index error"                ,
            ErrorCode.ERR_INVALID_LENGTH      : "Length error"               ,
            ErrorCode.ERR_INVALID_FN_POINTER  : "FN pointer error"           ,
            ErrorCode.ERR_INVALID_SORT_FN     : "Sort FN error"              ,

            # Device errors
            ErrorCode.ERR_DEVICE_NOT_FOUND         : "Device not found"               ,
            ErrorCode.ERR_DEVICE_BUSY              : "Device busy"                    ,
            ErrorCode.ERR_DEVICE_INVALID           : "Device error"                   ,
            ErrorCode.ERR_DEVICE_EMERGENCY         : "Device emergency"               ,
            ErrorCode.ERR_DEVICE_MEMORY_FULL       : "Device memory full"             ,
            ErrorCode.ERR_DEVICE_INTERNAL_ERROR    : "Internal device error"          ,
            ErrorCode.ERR_DEVICE_INVALID_PARAMETER : "Device parameter invalid"       ,
            ErrorCode.ERR_DEVICE_NO_DISK           : "No disk"                        ,
            ErrorCode.ERR_DEVICE_DISK_ERROR        : "Disk error"                     ,
            ErrorCode.ERR_DEVICE_CF_GATE_CHANGED   : "The CF gate has been changed"   ,
            ErrorCode.ERR_DEVICE_DIAL_CHANGED      : "The dial has been changed"      ,
            ErrorCode.ERR_DEVICE_NOT_INSTALLED     : "Device not installed"           ,
            ErrorCode.ERR_DEVICE_STAY_AWAKE        : "Device connected in awake mode" ,
            ErrorCode.ERR_DEVICE_NOT_RELEASED      : "Device not released"            ,

            # Stream errors
            ErrorCode.ERR_STREAM_IO_ERROR               : "Stream I/O error"                      ,
            ErrorCode.ERR_STREAM_NOT_OPEN               : "Stream open error"                     ,
            ErrorCode.ERR_STREAM_ALREADY_OPEN           : "Stream already open"                   ,
            ErrorCode.ERR_STREAM_OPEN_ERROR             : "Failed to open stream"                 ,
            ErrorCode.ERR_STREAM_CLOSE_ERROR            : "Failed to close stream"                ,
            ErrorCode.ERR_STREAM_SEEK_ERROR             : "Stream seek error"                     ,
            ErrorCode.ERR_STREAM_TELL_ERROR             : "Stream tell error"                     ,
            ErrorCode.ERR_STREAM_READ_ERROR             : "Failed to read stream"                 ,
            ErrorCode.ERR_STREAM_WRITE_ERROR            : "Failed to write stream"                ,
            ErrorCode.ERR_STREAM_PERMISSION_ERROR       : "Permission error"                      ,
            ErrorCode.ERR_STREAM_COULDNT_BEGIN_THREAD   : "Could not start reading thumbnail"     ,
            ErrorCode.ERR_STREAM_BAD_OPTIONS            : "Invalid stream option"                 ,
            ErrorCode.ERR_STREAM_END_OF_STREAM          : "Invalid stream termination"            ,

            # Communication errors
            ErrorCode.ERR_COMM_PORT_IS_IN_USE        : "Port in use"          ,
            ErrorCode.ERR_COMM_DISCONNECTED          : "Port disconnected"    ,
            ErrorCode.ERR_COMM_DEVICE_INCOMPATIBLE   : "Incompatible device"  ,
            ErrorCode.ERR_COMM_BUFFER_FULL           : "Buffer full"          ,
            ErrorCode.ERR_COMM_USB_BUS_ERR           : "USB bus error"        ,

            # Camera UI lock/unlock errors
            ErrorCode.ERR_USB_DEVICE_LOCK_ERROR     : "Failed to lock the UI"   ,
            ErrorCode.ERR_USB_DEVICE_UNLOCK_ERROR   : "Failed to unlock the UI" ,

            # STI/WIA errors
            ErrorCode.ERR_STI_UNKNOWN_ERROR          : "Unknown STI"           ,
            ErrorCode.ERR_STI_INTERNAL_ERROR         : "Internal STI error"    ,
            ErrorCode.ERR_STI_DEVICE_CREATE_ERROR    : "Device creation error" ,
            ErrorCode.ERR_STI_DEVICE_RELEASE_ERROR   : "Device release error"  ,
            ErrorCode.ERR_DEVICE_NOT_LAUNCHED        : "Device startup failed" ,

            # Other general errors
            ErrorCode.ERR_ENUM_NA                          : "Enumeration terminated (there was no suitable enumeration item)" ,
            ErrorCode.ERR_INVALID_FN_CALL                  : "Called in a mode when the function could not be used"            ,
            ErrorCode.ERR_HANDLE_NOT_FOUND                 : "Handle not found"                                                ,
            ErrorCode.ERR_INVALID_ID                       : "Invalid ID"                                                      ,
            ErrorCode.ERR_WAIT_TIMEOUT_ERROR               : "Timeout"                                                         ,
            ErrorCode.ERR_LAST_GENERIC_ERROR_PLUS_ONE      : "Not used."                                                       ,

            # PTP errors
            ErrorCode.ERR_SESSION_NOT_OPEN                              : "Session open error"                         ,
            ErrorCode.ERR_INVALID_TRANSACTIONID                         : "Invalid transaction ID"                     ,
            ErrorCode.ERR_INCOMPLETE_TRANSFER                           : "Transfer problem"                           ,
            ErrorCode.ERR_INVALID_STRAGEID                              : "Storage error"                              ,
            ErrorCode.ERR_DEVICEPROP_NOT_SUPPORTED                      : "Unsupported device property"                ,
            ErrorCode.ERR_INVALID_OBJECTFORMATCODE                      : "Invalid object format code"                 ,
            ErrorCode.ERR_SELF_TEST_FAILED                              : "Failed self-diagnosis"                      ,
            ErrorCode.ERR_PARTIAL_DELETION                              : "Failed in partial deletion"                 ,
            ErrorCode.ERR_SPECIFICATION_BY_FORMAT_UNSUPPORTED           : "Unsupported format specification"           ,
            ErrorCode.ERR_NO_VALID_OBJECTINFO                           : "Invalid object information"                 ,
            ErrorCode.ERR_INVALID_CODE_FORMAT                           : "Invalid code format"                        ,
            ErrorCode.ERR_UNKNOWN_VENDER_CODE                           : "Unknown vendor code"                        ,
            ErrorCode.ERR_CAPTURE_ALREADY_TERMINATED                    : "Capture already terminated"                 ,
            ErrorCode.ERR_INVALID_PARENTOBJECT                          : "Invalid parent object"                      ,
            ErrorCode.ERR_INVALID_DEVICEPROP_FORMAT                     : "Invalid property format"                    ,
            ErrorCode.ERR_INVALID_DEVICEPROP_VALUE                      : "Invalid property value"                     ,
            ErrorCode.ERR_SESSION_ALREADY_OPEN                          : "Session already open"                       ,
            ErrorCode.ERR_TRANSACTION_CANCELLED                         : "Transaction canceled"                       ,
            ErrorCode.ERR_SPECIFICATION_OF_DESTINATION_UNSUPPORTED      : "Unsupported destination specification"      ,
            ErrorCode.ERR_UNKNOWN_COMMAND                               : "Unknown command"                            ,
            ErrorCode.ERR_OPERATION_REFUSED                             : "Operation refused"                          ,
            ErrorCode.ERR_LENS_COVER_CLOSE                              : "Lens cover closed"                          ,
            ErrorCode.ERR_OBJECT_NOTREADY                               : "Image data set not ready for live view"     ,

            # TakePicture errors
            ErrorCode.ERR_TAKE_PICTURE_AF_NG                           : "Focus failed"                                                                      ,
            ErrorCode.ERR_TAKE_PICTURE_RESERVED                        : "Reserved"                                                                          ,
            ErrorCode.ERR_TAKE_PICTURE_MIRROR_UP_NG                    : "Currently configuring mirror up"                                                   ,
            ErrorCode.ERR_TAKE_PICTURE_SENSOR_CLEANING_NG              : "Currently cleaning sensor"                                                         ,
            ErrorCode.ERR_TAKE_PICTURE_SILENCE_NG                      : "Currently performing silent operations"                                            ,
            ErrorCode.ERR_TAKE_PICTURE_NO_CARD_NG                      : "Card not installed"                                                                ,
            ErrorCode.ERR_TAKE_PICTURE_CARD_NG                         : "Error writing to card"                                                             ,
            ErrorCode.ERR_TAKE_PICTURE_CARD_PROTECT_NG                 : "Card write protected"                                                              ,
            ErrorCode.ERR_TAKE_PICTURE_MOVIE_CROP_NG                   : "Faild in processing with movie crop"                                               ,
            ErrorCode.ERR_TAKE_PICTURE_STRBO_CHARGE_NG                 : "Faild in flash off"                                                                ,
            ErrorCode.ERR_TAKE_PICTURE_NO_LENS_NG                      : "Lens is not attached"                                                              ,
            ErrorCode.ERR_TAKE_PICTURE_SPECIAL_MOVIE_MODE_NG           : "Movie camera exceeds the limit"                                                    ,
            ErrorCode.ERR_TAKE_PICTURE_LV_REL_PROHIBIT_MODE_NG         : "Faild in live view preparing taking picture for changing AEmode(Candlelight only)" ,
            ErrorCode.ERR_TAKE_PICTURE_MOVIE_MODE_NG                   : "Faild in taking still image with getting ready for movie mode"                     ,
            ErrorCode.ERR_TAKE_PICTURE_RETRUCTED_LENS_NG               : "Retructed lens is retracted"                                                       

        }.get(self, "Unknown Canon SDK error.")