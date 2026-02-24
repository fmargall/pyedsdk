import ctypes, math, threading


from .core._sdk import _SDK

from .core._functions import _getCameraList
from .core._functions import _getChildCount, _getChildAtIndex
from .core._functions import _getPropertyData, _setPropertyData, _getPropertyDesc
from .core._functions import _release
from .core._functions import _openSession, _closeSession, _sendCommand, _setCapacity
from .core._functions import _getDirectoryItemInfo, _download, _downloadComplete
from .core._functions import _createFileStream
from .core._functions import _setObjectEventHandler, _getEvent

from .core._types     import _BaseRef
from .core._types     import _Capacity
from .core._types     import _Access, _PropertyID, _SaveTo, _CameraCommand, _ObjectEvent, _FileCreateDisposition, _ImageQuality

from .core._enums     import _Aperture, _ShutterSpeed, _ISOSpeed, _AFMode

from .core._callbacks import _ObjectEventHandler
from .core._callbacks import _waitForEvent


class EOSCamera:
    # --------- Init function ---------

    def __init__(self, cameraIndex):
        _SDK._initialize()

        # Check if cameraIndex is valid
        cameraListRef = _getCameraList()
        cameraCount   = _getChildCount(cameraListRef)
        if cameraIndex >= cameraCount:
            raise IndexError(f"Camera index {cameraIndex} out of range (available cameras: {cameraCount})")

        self._cameraIndex = cameraIndex
        self._cameraRef   = _getChildAtIndex(cameraListRef, cameraIndex)

        # Releasing camera list
        _release(cameraListRef)

        _openSession(self._cameraRef)
        self._isClosed = False


        # ----- End of instanciation -----
        # Following code is needed to end initialization correctly

        # It is mandatory to define the saving parameters on the host PC machine
        _setPropertyData(self._cameraRef, _PropertyID._SaveTo, 0, _SaveTo._Host)

        # Some of the Canons need to know that there is enough capacity on host.
        capacity = _Capacity(numberOfFreeClusters = 0x7FFFFFFF,  # Large enough
            bytesPerSector = 512,
            reset          = 1)
        _setCapacity(self._cameraRef, capacity)

        # Event management for download right after shot will be done using
        # threadings and SDK object event handler. One needs to define them
        self._downloadEvent = None

        # It is absolutely necessary to declare the _handler as part of the
        # class instance, in order to save it from Python garbage collector
        self._handler = _ObjectEventHandler(self._objectEventHandler)

        _setObjectEventHandler(
            self._cameraRef, _ObjectEvent._DirItemRequestTransfer, self._handler, None)


        # ----- End of initialization -----
        # Following code will initialize all the important parameters of the camera
        
        # Shutter speed (set at the minimum)
        availableShutterSpeedList      = _getPropertyDesc(self._cameraRef, _PropertyID._Tv).values
        self.availableShutterSpeedList = [_ShutterSpeed(val) for val in availableShutterSpeedList]
        self.shutterSpeed = self.availableShutterSpeedList[-1].seconds

        # Aperture (set at the minimum)
        availableApertureList      = _getPropertyDesc(self._cameraRef, _PropertyID._Av).values
        self.availableApertureList = [_Aperture(val) for val in availableApertureList]
        self.aperture = self.availableApertureList[-1].f_number

        # ISO (set at the minium)
        availableISOList      = _getPropertyDesc(self._cameraRef, _PropertyID._ISOSpeed).values
        self.availableISOList = [_ISOSpeed(val) for val in availableISOList]
        self.isoSpeed = self.availableISOList[-1].value

        # Output file (set initially at RAW, lossless, without compressions)
        self._filename     = "image.RAW"
        self._imageQuality = _ImageQuality._LR # RAW
        _setPropertyData(self._cameraRef, _PropertyID._ImageQuality, 0, _ImageQuality._LR)


    def __enter__(self):
        return self


    # --------- Building an object event handler ---------
    def _objectEventHandler(self, event: _ObjectEvent, ref: _BaseRef, context: ctypes.c_void_p) -> int:
        if event == _ObjectEvent._DirItemRequestTransfer:

            itemInfo = _getDirectoryItemInfo(ref)
            itemSize = itemInfo.size

            stream = _createFileStream(
                self._filename,
                _FileCreateDisposition._CreateAlways,
                _Access._Write
            )

            try:
                _download(ref, itemSize, stream)
                _downloadComplete(ref)

            finally:
                _release(stream)
                _release(ref)

            if self._downloadEvent:
                self._downloadEvent.set()

        return 0


    # --------- Property (getter and setters) functions ---------
    @property
    def imageQuality(self):
        pass

    @imageQuality.setter
    def imageQuality(self, imageQualityValue):
        pass

    @property
    def isoSpeed(self) -> float:
        return _ISOSpeed(_getPropertyData(self._cameraRef, _PropertyID._ISOSpeed, 0)).value

    @isoSpeed.setter
    def isoSpeed(self, isoSpeedValue: float):
         # Available ISO are discrete. Find the closest available for this camera
         candidates = [s for s in self.availableISOList if math.isnan(s.value)]
         isoSpeed   = min(candidates, key= lambda s: abs(math.log2(s.value) - math.log2(isoSpeedValue)))

         _setPropertyData(self._cameraRef, _PropertyID._ISOSpeed, 0, isoSpeed)

    @property
    def aperture(self) -> float:
        return _Aperture(_getPropertyData(self._cameraRef, _PropertyID._Av, 0)).f_number

    @aperture.setter
    def aperture(self, apertureFNumber: float):
        # Available aperture are discrete. Find the closest available for this camera
        candidates = [s for s in self.availableApertureList if s.f_number is not None]
        aperture   = min(candidates, key= lambda s: abs(math.log2(s.f_number) - math.log2(apertureFNumber)))

        _setPropertyData(self._cameraRef, _PropertyID._Av, 0, aperture)

    def getAvailableApertures(self) -> list:
        return [val.f_number for val in self.availableApertureList]

    @property
    def shutterSpeed(self) -> float:
        return _ShutterSpeed(_getPropertyData(self._cameraRef, _PropertyID._Tv, 0)).seconds

    @shutterSpeed.setter
    def shutterSpeed(self, valueInSeconds: float):
        # Available shutter speeds are discrete. Find the closest available for this camera
        candidates   = [s for s in self.availableShutterSpeedList if s.seconds is not None]
        shutterSpeed = min(candidates, key= lambda s: abs(math.log2(s.seconds) - math.log2(valueInSeconds)))

        _setPropertyData(self._cameraRef, _PropertyID._Tv, 0, shutterSpeed)

    @property
    def exposureCompensation(self):
        pass

    @exposureCompensation.setter
    def exposureCompensation(self, exposureCompensationValue):
        pass

    @property
    def noiseReduction(self):
        pass

    @noiseReduction.setter
    def noiseReduction(self, noiseReductionValue):
        pass

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, filename: str) -> None:
        self._filename = filename

    @property
    def afMode(self) -> str:
        return _AFMode(_getPropertyData(self._cameraRef, _PropertyID._AFMode, 0)).label


    # --------- End users functions ---------
    def shot(self, filename: str = None):
        # Updating filename output, if it is required
        if filename != None: self.filename = filename 

        # Preparing the synchronization event
        self._downloadEvent = threading.Event()

        _sendCommand(self._cameraRef, _CameraCommand._TakePicture, 0)
        _waitForEvent(self._downloadEvent)

        self._downloadEvent = None

    # --------- Exit and closing functions ---------

    # Camera should always be closed after use
    # in order to free all resources. Usually,
    # it will be called automatically.
    def _close(self):
        if not self._isClosed:
            _closeSession(self._cameraRef)
            _release(self._cameraRef)
            _SDK._terminate()

            self._isClosed = True

    def __del__(self):
        self._close()

    def __exit__(self, exceptionType, exceptionValue, traceback):
        self._close()