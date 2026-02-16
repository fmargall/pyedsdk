import pytest, time

from edsdk_wrapper._bindings import initializeSDK, terminateSDK
from edsdk_wrapper._bindings import getCameraList, getChildCount, getChildAtIndex, getDeviceInfo, release, openSession, closeSession, sendCommand

from edsdk_wrapper._bindings import cameraCommand_takePicture, cameraCommand_pressShutterButton, cameraCommand_ShutterButton_OFF, cameraCommand_ShutterButton_Completely

@pytest.fixture(scope="session")
def sdk():
    errorCode = initializeSDK()
    assert errorCode == 0

    yield # Rest of the tests will be executed

    errorCode = terminateSDK()
    assert errorCode == 0

@pytest.mark.hardware
def test_list_cameras(sdk):
    # Gets list of detected cameras from SDK
    errorCode, cameraList = getCameraList()

    assert errorCode == 0

    try:
        # Gets number of camers from the camera list
        errorCode, count = getChildCount(cameraList)
        assert errorCode == 0

        if count == 0: # Stop test if no camera
            pytest.skip("No camera connected")

        for cameraID in range(count):
            errorCode, camera = getChildAtIndex(cameraList, cameraID)
            assert errorCode == 0

            try:
                errorCode, deviceInfo = getDeviceInfo(camera)
                assert errorCode == 0

                print("Camera name:", deviceInfo.szDeviceDescription.decode("cp1252"))
            finally:
                errorCode = release(camera)
                assert errorCode == 0

    finally:
        errorCode = release(cameraList)
        assert errorCode == 0

@pytest.mark.hardware
def test_open_close_session(sdk):
    # Gets list of detected cameras from SDK
    errorCode, cameraList = getCameraList()

    assert errorCode == 0

    try:
        # Gets number of camers from the camera list
        errorCode, count = getChildCount(cameraList)
        assert errorCode == 0

        if count == 0: # Stop test if no camera
            pytest.skip("No camera connected")

        for cameraID in range(count):
            errorCode, camera = getChildAtIndex(cameraList, cameraID)
            assert errorCode == 0

            try:
                errorCode = openSession(camera)
                assert errorCode == 0

                errorCode = closeSession(camera)
                assert errorCode == 0

            finally:
                errorCode = release(camera)
                assert errorCode == 0

    finally:
        errorCode = release(cameraList)
        assert errorCode == 0

@pytest.fixture
def camera(sdk):
    # Gets list of detected cameras from SDK
    errorCode, cameraList = getCameraList()

    assert errorCode == 0

    try:
        # Gets number of camers from the camera list
        errorCode, count = getChildCount(cameraList)
        assert errorCode == 0

        if count == 0: # Stop test if no camera
            pytest.skip("No camera connected")

        errorCode, camera = getChildAtIndex(cameraList, 0)
        assert errorCode == 0

        try:
            errorCode = openSession(camera)
            assert errorCode == 0

            yield camera # Rest of the tests will be executed here

        finally:
            errorCode = closeSession(camera)

            errorCode = release(camera)

    finally:
        errorCode = release(cameraList)
        assert errorCode == 0

@pytest.mark.hardware
@pytest.mark.timeout(15)
def test_take_picture_press_shutter_button_command(camera):
    
    errorCode = sendCommand(
        camera,
        cameraCommand_pressShutterButton,
        cameraCommand_ShutterButton_Completely
    )
    assert errorCode == 0

    errorCode = sendCommand(
        camera,
        cameraCommand_pressShutterButton,
        cameraCommand_ShutterButton_OFF
    )
    assert errorCode == 0

@pytest.mark.hardware
@pytest.mark.timeout(15)
def test_take_picture_direct_send_command(camera):

    errorCode = sendCommand(
        camera,
        cameraCommand_takePicture,
        0
    )
    assert errorCode == 0

@pytest.mark.hardware
def test_