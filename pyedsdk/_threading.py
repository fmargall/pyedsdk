import queue, threading

from .core._callbacks import _pumpWindowsMessages


class _CameraWorker(threading.Thread):
    def __init__(self, cameraIndex, settings):
        super().__init__(daemon=True)
        self._cameraIndex = cameraIndex
        self._settings    = settings
        self._cmdQueue    = queue.Queue()
        self.ready        = threading.Event()

    def run(self):
        from pyedsdk.camera import EOSCamera
        camera = EOSCamera(self._cameraIndex)
        for key, value in self._settings.items():
            setattr(camera, key, value)
        self.ready.set()

        while True:
            try:
                cmd = self._cmdQueue.get(timeout=0.01)
            except queue.Empty:
                _pumpWindowsMessages()
                continue

            if cmd is None:
                break

            kind, name, payload, done = cmd
            try:
                if kind == "call":
                    getattr(camera, name)(**payload)
                elif kind == "set":
                    setattr(camera, name, payload)
            finally:
                done.set()

    def submitCall(self, name, **kwargs):
        done = threading.Event()
        self._cmdQueue.put(("call", name, kwargs, done))
        return done

    def submitSet(self, name, value):
        done = threading.Event()
        self._cmdQueue.put(("set", name, value, done))
        return done

class _CameraProxy:
    def __init__(self, worker):
        object.__setattr__(self, "_worker", worker)

    def __setattr__(self, name, value):
        self._worker.submitSet(name, value).wait()

    def __getattr__(self, name):
        worker = self.__dict__["_worker"]
        def call(**kwargs):
            worker.submitCall(name, **kwargs).wait()
        return call
