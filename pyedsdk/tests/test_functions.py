import ctypes
import pytest
import threading


from pyedsdk.core._functions import _initializeSDK, _terminateSDK
from pyedsdk.core._functions import _getCameraList
from pyedsdk.core._functions import _getChildCount, _getChildAtIndex
from pyedsdk.core._functions import _getPropertyData, _setPropertyData
from pyedsdk.core._functions import _release
from pyedsdk.core._functions import _getDeviceInfo, _openSession, _closeSession, _sendCommand, _setCapacity
from pyedsdk.core._functions import _getVolumeInfo
from pyedsdk.core._functions import _setObjectEventHandler

from pyedsdk.core._functions import _registerObjectHandler

from pyedsdk.core._types     import _Capacity
from pyedsdk.core._types     import _PropertyID, _SaveTo, _CameraCommand, _ObjectEvent

from pyedsdk.core._callbacks import _waitForEvent


@pytest.fixture(scope="session")
def sdk():
    _initializeSDK()
    yield # All tests are executed here
    _terminateSDK()


@pytest.mark.hardware
def test_list_cameras(sdk):
    # Gets list of detected cameras:
    cameraListRef = _getCameraList()

    try:
        # Gets number of cameras from the list
        count = _getChildCount(cameraListRef)

        if count == 0: # Stop test if no camera
            pytest.skip("No cameras connected")

        # Checking each camera found
        for cameraID in range(count):
            cameraRef = _getChildAtIndex(cameraListRef, cameraID)

            try:
                # Check if _getDeviceInfo returns error
                deviceInfo = _getDeviceInfo(cameraRef)

            finally:
                # Release camera reference
                _release(cameraRef)

    finally:
        # Release camera list reference
        _release(cameraListRef)


@pytest.mark.hardware
def test_access_camera(sdk):
    # Gets list of detected cameras:
    cameraListRef = _getCameraList()

    try:
        # Gets number of cameras from the list
        count = _getChildCount(cameraListRef)

        if count == 0: # Stop test if no camera
            pytest.skip("No cameras connected")

        # Checking each camera found
        for cameraID in range(count):
            cameraRef = _getChildAtIndex(cameraListRef, cameraID)

            try:
                # Open and close session
                _openSession(cameraRef)
                _closeSession(cameraRef)

            finally:
                # Release camera reference
                _release(cameraRef)

    finally:
        # Release camera list reference
        _release(cameraListRef)


@pytest.mark.hardware
def test_access_camera_memory(sdk):
    # Gets list of detected cameras:
    cameraListRef = _getCameraList()

    try:
        # Gets the number of cameras from the list
        cameraCount = _getChildCount(cameraListRef)

        if cameraCount == 0: # Stop test if no camera
            pytest.skip("No cameras connected")

        # Checking each camera found
        for cameraID in range(cameraCount):
            cameraRef = _getChildAtIndex(cameraListRef, cameraID)

            try:
                _openSession(cameraRef)

                # Gets the number of memory cards from the camera
                memoryCount = _getChildCount(cameraRef)

                if memoryCount == 0: # Stop test if no memory card
                    pytest.skip("No memory found inside the camera")

                # Checking each memory found
                for memoryID in range(memoryCount):
                    memoryRef = _getChildAtIndex(cameraRef, memoryID)

                    try:
                        volumeInfo = _getVolumeInfo(memoryRef)

                    finally:
                        # Release memory reference
                        _release(memoryRef)

            finally:
                # Release camera reference
                _closeSession(cameraRef)
                _release(cameraRef)

    finally:
        # Release camera list reference
        _release(cameraListRef)


@pytest.fixture
def camera(sdk):
    # Gets list of detected cameras:
    cameraListRef = _getCameraList()

    try:
        # Gets number of cameras from the list
        count = _getChildCount(cameraListRef)

        if count == 0: # Stop test if no camera
            pytest.skip("No cameras connected")

        # Tests will be run for the first camera found
        cameraRef = _getChildAtIndex(cameraListRef, 0)

        try:
            # Open and close session
            _openSession(cameraRef)
            yield cameraRef

        finally:
            # Release camera reference
            _closeSession(cameraRef)
            _release(cameraRef)

    finally:
        # Release camera list reference
        _release(cameraListRef)


@pytest.mark.hardware
def test_shot_and_save(camera):

    # Setting saving option on PC
    _setPropertyData(camera, _PropertyID._SaveTo, 0, _SaveTo._Host)

    # Setting host capacity to a large enough value
    capacity = _Capacity(
        numberOfFreeClusters = 0x7FFFFFFF, # Quite enough
        bytesPerSector       = 512,
        reset                = 1
    )
    _setCapacity(camera, capacity)

    # Prepare synchronization event
    downloadDone = threading.Event()

    handler = _registerObjectHandler(downloadDone)

    _setObjectEventHandler(
        camera, _ObjectEvent._DirItemRequestTransfer, handler, None)

    # Take picture
    _sendCommand(camera, _CameraCommand._TakePicture, 0)

    _waitForEvent(downloadDone)