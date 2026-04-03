import ctypes, threading

from .core._errors    import CanonError, _ErrorCode
from .core._functions import _createEvfImageRef, _createMemoryStream, _downloadEvfImage, _getPointer, _getLength, _release

class LiveViewStream:
    def __init__(self, camera):
        self._camera = camera
        self._running = False

        self._stream = None
        self._evfImg = None

        self._thread = None # Callback mode


    def start(self, callback=None, errorCallback=None):
        if self._running:
            return

        # Live view activated on camera
        self._camera._startLiveView()

        # Initialize different buffers
        self._stream = _createMemoryStream()
        self._evfImg = _createEvfImageRef(self._stream)

        self._running = True

        if callback is not None:
            # If a callback is already provided, we will start a new thread to call it on every new frame:
            self._thread = threading.Thread(target=self._loop, args=(callback, errorCallback), daemon=True)
            self._thread.start()


    def stop(self):
        if not self._running:
            return

        self._running = False

        # Deactivate callback loop
        if self._thread is not None:
            self._thread.join()
            self._thread = None

        # Deactivate live view on camera
        self._camera._endLiveView()

        # Free all buffer and ressources
        if self._evfImg is not None:
            _release(self._evfImg)
            self._evfImg = None

        if self._stream is not None:
            _release(self._stream)
            self._stream = None


    def getFrame(self) -> bytes:
        if not self._running:
            raise RuntimeError("Live view not started")

        # Retry loop (safe)
        for _ in range(750):
            try:
                _downloadEvfImage(self._camera._cameraRef, self._evfImg)
                break
            except CanonError as err:
                if err.code == _ErrorCode.ERR_OBJECT_NOTREADY:
                    continue
                raise
        else:
            # After some iterations, we will return a time-out
            raise CanonError(_ErrorCode.ERR_WAIT_TIMEOUT_ERROR)

        ptr  = _getPointer(self._stream)
        size = _getLength (self._stream)

        return ctypes.string_at(ptr.value, size)


    def __iter__(self):
        if self._thread is not None:
            raise RuntimeError("Live view already running in callback mode")

        self.start()
        try:
            while self._running:
                yield self.getFrame()
        finally:
            self.stop()


    def _loop(self, callback, errorCallback=None):
        try:
            while self._running:
                frame = self.getFrame()
                callback(frame)
        except Exception as error:
            self._running = False
            print("LiveViewStream loop error:", error)
            if errorCallback:
                errorCallback(error)