import ctypes
import platform
import os

from ._errors    import _error_restype, _ErrorCode

from ._types     import _BaseRef, _CameraListRef, _CameraRef, _VolumeRef, _DirectoryItemRef, _StreamRef
from ._types     import _DeviceInfo, _VolumeInfo, _DirectoryItemInfo, _PropertyDesc, _Capacity
from ._types     import _Access, _CameraCommand, _ObjectEvent, _FileCreateDisposition, _PropertyID

from ._callbacks import _ObjectEventHandler


# Chosing and reading correct dll
"""
arch = platform.architecture()[0]

dllPath = os.path.join(os.path.dirname(__file__), '../dependencies', 'EDSDK_64' if arch == '64bit' else 'EDSDK', 'Dll', 'EDSDK.dll')
lib     = ctypes.windll.LoadLibrary(dllPath)
"""
from .loader import loadSDKLib
lib = loadSDKLib()


# Number of functions binded: 21 / 56


# -------- Basic functions --------
# Number of functions binded: 2 / 2

# Defining EdsError EDSAPI EdsInitializeSDK()
lib.EdsInitializeSDK.restype  = _error_restype
lib.EdsInitializeSDK.argtypes = []
def _initializeSDK() -> None:
    lib.EdsInitializeSDK()

# Defining EdsError EDSAPI EdsTerminateSDK()
lib.EdsTerminateSDK.restype  = _error_restype
lib.EdsTerminateSDK.argtypes = []
def _terminateSDK() -> None:
    lib.EdsTerminateSDK()


# -------- Reference-counter operating --------
# Number of functions binded: 1 / 2

# Defining EdsUInt32 EDSAPI EdsRelease(EdsBaseRef inRef)
lib.EdsRelease.restype  =  _error_restype
lib.EdsRelease.argtypes = [_BaseRef]
def _release(ref: _BaseRef) -> None:
    lib.EdsRelease(ref)


# -------- Item-tree operating functions --------
# Number of functions binded: 2 / 3

# Defining EdsError EDSAPI EdsGetChildCount(EdsBaseRef inRef,
#                                           EdsUInt32* outCount)
lib.EdsGetChildCount.restype  =  _error_restype
lib.EdsGetChildCount.argtypes = [_BaseRef, ctypes.POINTER(ctypes.c_uint32)]
def _getChildCount(ref: _BaseRef) -> int:
    count = ctypes.c_uint32()
    lib.EdsGetChildCount(ref, ctypes.byref(count))
    return int(count.value)

# Defining EdsError EDSAPI EdsGetChildAtIndex(EdsBaseRef  inRef,
#                                             EdsInt32    inIndex,
#                                             EdsBaseRef* outRef)
lib.EdsGetChildAtIndex.restype  =  _error_restype
lib.EdsGetChildAtIndex.argtypes = [_BaseRef, ctypes.c_int32, ctypes.POINTER(_BaseRef)]
def _getChildAtIndex(ref: _BaseRef, index: int):
    child = _BaseRef()
    lib.EdsGetChildAtIndex(ref, ctypes.c_int32(index), ctypes.byref(child))
    return child


# -------- Property operating functions --------
# Number of functions binded: 3 / 5

# Defining EdsError EDSAPI EdsGetPropertyData(EdsBaseRef    inRef,
#                                             EdsPropertyID inPropertyID,
#                                             EdsInt32      inParam,
#                                             EdsUInt32     inPropertySize,
#                                             EdsVoid*      outPropertyData)
lib.EdsGetPropertyData.restype  =  _error_restype
lib.EdsGetPropertyData.argtypes = [_BaseRef, ctypes.c_uint32, ctypes.c_int32, ctypes.c_uint32, ctypes.c_void_p]
def _getPropertyData(
    ref: _BaseRef, propertyID: _PropertyID, additionalParam: int) -> int:
    propertyData = ctypes.c_uint32()
    lib.EdsGetPropertyData(ref, 
                           ctypes.c_uint32(int(propertyID)), 
                           ctypes.c_int32(additionalParam), 
                           ctypes.sizeof(ctypes.c_uint32), 
                           ctypes.byref(propertyData))
    return propertyData.value

# Defining EdsError EDSAPI EdsSetPropertyData(EdsBaseRef     inRef,
#                                             EdsPropertyID  inPropertyID,
#                                             EdsInt32       inParam,
#                                             EdsUInt32      inPropertySize,
#                                             const EdsVoid* inPropertyData)
lib.EdsSetPropertyData.restype  =  _error_restype
lib.EdsSetPropertyData.argtypes = [_BaseRef, ctypes.c_uint32, ctypes.c_int32, ctypes.c_uint32, ctypes.c_void_p]
def _setPropertyData(
        ref: _BaseRef, propertyID: _PropertyID, additionalParam: int, propertyValue) -> None:
    propertyData = ctypes.c_uint32(int(propertyValue))
    lib.EdsSetPropertyData(ref, 
                           ctypes.c_uint32(int(propertyID)), 
                           ctypes.c_int32(additionalParam), 
                           ctypes.sizeof(ctypes.c_uint32), 
                           ctypes.byref(propertyData))

# Defining EdsError EDSAPI EdsGetPropertyDesc(EdsBaseRef       inRef,
#                                             EdsPropertyID    inPropertyID,
#                                             EdsPropertyDesc* outPropertyDesc)
lib.EdsGetPropertyDesc.restype  =  _error_restype
lib.EdsGetPropertyDesc.argtypes = [_BaseRef, ctypes.c_uint32, ctypes.POINTER(_PropertyDesc)]
def _getPropertyDesc(ref: _BaseRef, propertyID: _PropertyID) -> _PropertyDesc:
    propertyDesc = _PropertyDesc()
    lib.EdsGetPropertyDesc(ref, ctypes.c_uint32(int(propertyID)), ctypes.byref(propertyDesc))
    return propertyDesc


# -------- Device-list and device operating functions --------
# Number of functions binded: 1 / 1

# Defining EdsError EDSAPI EdsGetCameraList(EdsCameraListRef*  outCameraListRef)
lib.EdsGetCameraList.restype  =  _error_restype
lib.EdsGetCameraList.argtypes = [ctypes.POINTER(_CameraListRef)]
def _getCameraList() -> _CameraListRef:
    cameraListRef = _CameraListRef()
    lib.EdsGetCameraList(ctypes.byref(cameraListRef))
    return cameraListRef


# -------- Camera operating functions --------
# Number of functions binded: 5 / 6

# Defining EdsError EDSAPI EdsGetDeviceInfo(EdsCameraRef   inCameraRef,
#                                           EdsDeviceInfo* outDeviceInfo)
lib.EdsGetDeviceInfo.restype  = _error_restype
lib.EdsGetDeviceInfo.argtypes = [_CameraRef, ctypes.POINTER(_DeviceInfo)]
def _getDeviceInfo(cameraRef: _CameraRef) -> _DeviceInfo:
    deviceInfo = _DeviceInfo()
    lib.EdsGetDeviceInfo(cameraRef, ctypes.byref(deviceInfo))
    return deviceInfo

# Defining EdsError EDSAPI EdsOpenSession(EdsCameraRef inCameraRef)
lib.EdsOpenSession.restype  =  _error_restype
lib.EdsOpenSession.argtypes = [_CameraRef]
def _openSession(cameraRef: _CameraRef) -> None:
    lib.EdsOpenSession(cameraRef)

# Defining EdsError EDSAPI EdsCloseSession(EdsCameraRef inCameraRef)
lib.EdsCloseSession.restype  =  _error_restype
lib.EdsCloseSession.argtypes = [_CameraRef]
def _closeSession(cameraRef: _CameraRef) -> None:
    lib.EdsCloseSession(cameraRef)

# Defining EdsError EDSAPI EdsSendCommand(EdsCameraRef     inCameraRef,
#                                         EdsCameraCommand inCommand,
#                                         EdsInt32         inParam)
lib.EdsSendCommand.restype  =  _error_restype
lib.EdsSendCommand.argtypes = [_CameraRef, ctypes.c_uint32, ctypes.c_int32]
def _sendCommand(cameraRef: _CameraRef, command: _CameraCommand, param: int) -> None:
    lib.EdsSendCommand(cameraRef, ctypes.c_uint32(int(command)),  ctypes.c_int32(param))

# Defining EdsError EDSAPI EdsSetCapacity(EdsCameraRef inCameraRef,
#                                         EdsCapacity  inCapacity)
lib.EdsSetCapacity.restype  =  _error_restype
lib.EdsSetCapacity.argtypes = [_CameraRef, _Capacity]
def _setCapacity(cameraRef: _CameraRef, capacity: _Capacity) -> None:
    lib.EdsSetCapacity(cameraRef, capacity)


# -------- Volume operating functions --------
# Number of functions binded: 1 / 4

# Defining EdsError EDSAPI EdsGetVolumeInfo(EdsVolumeRef   inVolumeRef,
#                                           EdsVolumeInfo* outVolumeInfo)
lib.EdsGetVolumeInfo.restype  =  _error_restype
lib.EdsGetVolumeInfo.argtypes = [_VolumeRef, ctypes.POINTER(_VolumeInfo)]
def _getVolumeInfo(volumeRef: _VolumeRef) -> _VolumeInfo:
    volumeInfo = _VolumeInfo()
    lib.EdsGetVolumeInfo(volumeRef, ctypes.byref(volumeInfo))
    return volumeInfo


# -------- Directory-item operating functions --------
# Number of functions binded: 3 / 9

# Defining EdsError EDSAPI EdsGetDirectoryItemInfo(EdsDirectoryItemRef   inDirItemRef,
#                                                  EdsDirectoryItemInfo* outDirItemInfo)
lib.EdsGetDirectoryItemInfo.restype  =  _error_restype
lib.EdsGetDirectoryItemInfo.argtypes = [_DirectoryItemRef, ctypes.POINTER(_DirectoryItemInfo)]
def _getDirectoryItemInfo(directoryItemRef: _DirectoryItemRef) -> _DirectoryItemInfo:
    directoryItemInfo = _DirectoryItemInfo()
    lib.EdsGetDirectoryItemInfo(directoryItemRef, ctypes.byref(directoryItemInfo))
    return directoryItemInfo

# Defining EdsError EDSAPI EdsDownload(EdsDirectoryItemRef inDirItemRef,
#                                      EdsUInt64           inReadSize,
#                                      EdsStreamRef        outStream)
lib.EdsDownload.restype  =  _error_restype
lib.EdsDownload.argtypes = [_DirectoryItemRef, ctypes.c_uint64, _StreamRef]
def _download(directoryItemRef: _DirectoryItemRef, readSize: int, streamRef: _StreamRef) -> None:
    lib.EdsDownload(directoryItemRef, ctypes.c_uint64(readSize), streamRef)

# Defining EdsError EDSAPI EdsDownloadCancel(EdsDirectoryItemRef inDirItemRef)
lib.EdsDownloadCancel.restype  =  _error_restype
lib.EdsDownloadCancel.argtypes = [_DirectoryItemRef]
def _downloadCancel(directoryItemRef: _DirectoryItemRef) -> None:
    lib.EdsDownloadCancel(directoryItemRef)

# Defining EdsError EDSAPI EdsDownloadComplete(EdsDirectoryItemRef inDirItemRef)
lib.EdsDownloadComplete.restype  =  _error_restype
lib.EdsDownloadComplete.argtypes = [_DirectoryItemRef]
def _downloadComplete(directoryItemRef: _DirectoryItemRef) -> None:
    lib.EdsDownloadComplete(directoryItemRef)

# -------- Stream operating functions --------
# Number of functions binded: 1 / 12

# Defining EdsError EDSAPI EdsCreateFileStream(const EdsChar*           inFileName,
#                                              EdsFileCreateDisposition inCreateDisposition,
#                                              EdsAccess                inDesiredAccess,
#                                              EdsStreamRef*            outStream)
lib.EdsCreateFileStream.restype  =  _error_restype
lib.EdsCreateFileStream.argtypes = [ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(_StreamRef)]
def _createFileStream(filename: str, fileCreateDisposition: _FileCreateDisposition, desiredAccess: _Access) -> _StreamRef:
    streamRef = _StreamRef()
    lib.EdsCreateFileStream(filename.encode("utf-8"),
        ctypes.c_uint32(int(fileCreateDisposition)),
        ctypes.c_uint32(int(desiredAccess)),
        ctypes.byref(streamRef)
    )
    return streamRef


# -------- Image operating functions --------
# Number of functions binded: 0 / 5


# -------- Event handler registering functions --------
# Number of functions binded: 1 / 7

# Defining EdsError EDSAPI EdsSetObjectEventHandler(EdsCameraRef          inCameraRef, 
#                                                   EdsObjectEvent        inEvent,           
#                                                   EdsObjectEventHandler inObjectEventHandler,
#                                                   EdsVoid*              inContext)
lib.EdsSetObjectEventHandler.restype  =  _error_restype
lib.EdsSetObjectEventHandler.argtypes = [_CameraRef, ctypes.c_uint32, _ObjectEventHandler, ctypes.c_void_p]
def _setObjectEventHandler(cameraRef: _CameraRef, objectEvent: _ObjectEvent, handler, context: ctypes.c_void_p) -> None:
    lib.EdsSetObjectEventHandler(cameraRef, ctypes.c_uint32(int(objectEvent)), handler, context)



# ----------- Event handlers -----------
_downloadDoneEvent = None

# -------- Object Event handler --------

# Internal storage used to avoid GC
_registeredObjectEventHandlers = []

def _objectEventHandler(event: _ObjectEvent, ref: _BaseRef, context: ctypes.c_void_p) -> _ErrorCode:
    if event == _ObjectEvent._DirItemRequestTransfer:

        itemInfo = _getDirectoryItemInfo(ref)
        itemSize = itemInfo.size

        stream = _createFileStream(
            "image.jpg",
            _FileCreateDisposition._CreateAlways,
            _Access._Write
        )

        try:
            _download(ref, itemSize, stream)
            _downloadComplete(ref)

        finally:
            _release(stream)
            _release(ref)

        if _downloadDoneEvent:
            _downloadDoneEvent.set()

    return int(_ErrorCode.ERR_OK)

def _registerObjectHandler(doneEvent):

    global _downloadDoneEvent
    _downloadDoneEvent = doneEvent

    c_handler = _ObjectEventHandler(_objectEventHandler)
    _registeredObjectEventHandlers.append(c_handler)

    return c_handler