import pytest


from edsdk_wrapper.camera import EOSCamera


@pytest.mark.hardware
def test_instance_and_shot():
    camera = EOSCamera(0)
    
    camera.shot()
    print("Shutter speed:", camera.shutterSpeed)

    camera.shutterSpeed = 1.
    camera.shot()
    print("Shutter speed:", camera.shutterSpeed)