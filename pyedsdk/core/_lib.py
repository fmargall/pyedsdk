class _LibProxy:
    def __init__(self):
        self._lib = None

    def load(self, lib):
        self._lib = lib

    def __getattr__(self, name):
        if self._lib is None:
            raise RuntimeError(
                "EDSDK.dll not loaded. Call loadSDKLib(path) first."
            )
        return getattr(self._lib, name)


lib = _LibProxy()