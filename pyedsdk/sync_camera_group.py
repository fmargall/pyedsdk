import queue, threading

from ._threading import _CameraProxy, _CameraWorker


class SyncCameraGroup:
    def __init__(self, cameraIndices):
        # Bypass our own __setattr__ to initialize the workers list itself.
        object.__setattr__(self, "workers", [])
        for i in cameraIndices:
            worker = _CameraWorker(i, {})
            worker.start()
            worker.ready.wait()
            self.workers.append(worker)

    def __setattr__(self, name, value):
        # Broadcasts a property set to every camera in parallel.
        dones = [w.submitSet(name, value) for w in self.workers]
        for d in dones: d.wait()

    def __getattr__(self, name):
        # Called only when normal lookup fails (i.e. not a method, defined
        # on this class). Returns a callable that broadcasts a method call
        workers = self.__dict__["workers"]
        def broadcastCall(**kwargs):
            dones = [w.submitCall(name, **kwargs) for w in workers]
            for d in dones: d.wait()
        return broadcastCall

    def __getitem__(self, index):
        # Uses a _CameraProxy instance tp allow for the user
        # to call methods on a specific camera, for instance
        # group[0].aperture = 8., group[1].shutterSpeed = 1.
        return _CameraProxy(self.workers[index])

    def fireShot(self, filenames):
        barrier = threading.Barrier(len(self.workers))

        def task(worker, filename):
            barrier.wait()
            # fireShot will call every worker associated to one
            # Camera instance, and then submit a "shot" command
            done = worker.submitCall("shot", filename=filename)
            done.wait()

        threads = [threading.Thread(target=task, args=(w, f))
                   for w, f in zip(self.workers, filenames)]

        for t in threads: t.start()
        for t in threads: t.join()
