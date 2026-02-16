import ctypes
import platform
import os

# Chosing and reading correct dll
arch = platform.architecture()[0]

dllPath = os.path.join(os.path.dirname(__file__), 'dependencies', 'EDSDK_64' if arch == '64bit' else 'EDSDK', 'Dll', 'EDSDK.dll')
lib     = ctypes.windll.LoadLibrary(dllPath)


CameraRef     = ctypes.c_void_p
CameraListRef = ctypes.c_void_p

ObjectEventHandler = ctypes.WINFUNCTYPE(
    ctypes.c_uint32,
    ctypes.c_uint32,
    ctypes.c_void_p,
    ctypes.c_void_p)


# Defining EdsError EDSAPI EdsInitializeSDK()
lib.EdsInitializeSDK.restype  = ctypes.c_uint32
lib.EdsInitializeSDK.argtypes = []
def initializeSDK():
    return lib.EdsInitializeSDK()

# Defining EdsError EDSAPI EdsTerminateSDK()
lib.EdsTerminateSDK.restype  = ctypes.c_uint32
lib.EdsTerminateSDK.argtypes = []
def terminateSDK():
    return lib.EdsTerminateSDK()

# Defining EdsError EDSAPI EdsGetCameraList(EdsCameraListRef* outCameraListRef)
lib.EdsGetCameraList.restype  =  ctypes.c_uint32
lib.EdsGetCameraList.argtypes = [ctypes.POINTER(CameraListRef)]
def getCameraList():
    cameraList = CameraListRef()
    lib.EdsGetCameraList(ctypes.byref(cameraList))
    return cameraList

# Defining EdsError EDSAPI EdsGetChildCount(EdsBaseRef inRef,
#                                           EdsUInt32* outCount)
lib.EdsGetChildCount.restype  =  ctypes.c_uint32
lib.EdsGetChildCount.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32)]
def getChildCount(ref: ctypes.c_void_p):
    count = ctypes.c_uint32()
    lib.EdsGetChildCount(ref, ctypes.byref(count))
    return count.value

# Defining EdsError EDSAPI EdsGetChildAtIndex(EdsBaseRef  inRef,
#                                             EdsInt32    inIndex,
#                                             EdsBaseRef* outRef)
lib.EdsGetChildAtIndex.restype  =  ctypes.c_uint32
lib.EdsGetChildAtIndex.argtypes = [ctypes.c_void_p,
                                   ctypes.c_int32,
                                   ctypes.POINTER(ctypes.c_void_p)]
def getChildAdIndex(ref  : ctypes.c_void_p, 
                    index: int) -> ctypes.c_void_p:
    child = ctypes.c_void_p()
    lib.EdsGetChildAtIndex(ref, ctypes.c_int32(index), ctypes.byref(child))
    return child

# Defining EdsError EDSAPI EdsOpenSession(EdsCameraRef inCameraRef)
lib.EdsOpenSession.restype  =  ctypes.c_uint32
lib.EdsOpenSession.argtypes = [CameraRef]
def openSession(camera: CameraRef):
    return lib.EdsOpenSession(camera)

# Defining EdsError EDSAPI EdsCloseSession(EdsCameraRef inCameraRef)
lib.EdsCloseSession.restype  =  ctypes.c_uint32
lib.EdsCloseSession.argtypes = [CameraRef]
def closeSession(camera: CameraRef):
    return lib.EdsCloseSession(camera)

# Defining EdsUInt32 EDSAPI EdsRelease(EdsBaseRef inRef)
lib.EdsRelease.restype  =  ctypes.c_uint32
lib.EdsRelease.argtypes = [ctypes.c_void_p]
def release(ref: ctypes.c_void_p):
    return lib.EdsRelease(ref)

# Defining EdsError EDSAPI EdsSendCommand(EdsCameraRef     inCameraRef,
#                                         EdsCameraCommand inCommand,
#                                         EdsInt32         inParam)
lib.EdsSendCommand.restype  =  ctypes.c_uint32
lib.EdsSendCommand.argtypes = [CameraRef, ctypes.c_uint32, ctypes.c_uint32]
def sendCommand(camera, command, param):
    return lib.EdsSendCommand(camera, ctypes.c_uint32(command), ctypes.c_uint32(param))

# Defining EdsError EDSAPI EdsSetPropertyData(EdsBaseRef     inRef,
#                                             EdsPropertyID  inPropertyID,
#                                             EdsInt32       inParam,
#                                             EdsUInt32      inPropertySize,
#                                             const EdsVoid* inPropertyData)
lib.EdsSetPropertyData.restype  =  ctypes.c_uint32
lib.EdsSetPropertyData.argtypes = [ctypes.c_void_p,
                                   ctypes.c_uint32,
                                   ctypes.c_int32 ,
                                   ctypes.c_uint32,
                                   ctypes.c_void_p]
def setPropertyData(ref, propertyID, value, dataType):
    data = dataType(value)
    return lib.EdsSetPropertyData(ref, 
                                  ctypes.c_uint32(propertyID), 
                                  ctypes.c_int32(0), 
                                  ctypes.c_uint32(ctypes.sizeof(data)), 
                                  ctypes.byref(data))

# Defining EdsError EDSAPI EdsSetObjectEventHandler(EdsCameraRef          inCameraRef, 
#                                                   EdsObjectEvent        inEvent,           
#                                                   EdsObjectEventHandler inObjectEventHandler,
#                                                   EdsVoid*              inContext)
lib.EdsSetObjectEventHandler.restype  =  ctypes.c_uint32
lib.EdsSetObjectEventHandler.argtypes = [CameraRef         ,
                                         ctypes.c_uint32   ,
                                         ObjectEventHandler,
                                         ctypes.c_void_p]
def setObjectEventHandler(camera, event, handler, context):
    callback = ObjectEventHandler(handler)
    lib.EdsSetObjectEventHandler(camera,
                                 ctypes.c_uint32(event),
                                 callback,
                                 context)
    return callback
