from ._functions import _initializeSDK, _terminateSDK

class _SDK:
    _initialized = False
    _refCounter  = 0

    @classmethod
    def _initialize(cls):
        if not cls._initialized:
            _initializeSDK()
            cls._initialized = True

        cls._refCounter += 1

    @classmethod
    def _terminate(cls):
        cls._refCounter -= 1

        if cls._refCounter == 0 and cls._initialized:
            cls._initialized = False
            _terminateSDK()