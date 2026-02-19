import pytest


from edsdk_wrapper.camera import EOSCamera


@pytest.mark.hardware
def test_instance_and_shot():
    camera = EOSCamera(0)
    
    camera.shot()
    print("Shutter speed:", camera.shutterSpeed)

    camera.shutterSpeed = 2.
    camera.shot()
    print("Shutter speed:", camera.shutterSpeed)
    print("Aperture:", camera.aperture)

    camera.aperture = 2.8
    camera.shot()
    print("Aperture:", camera.aperture)
    print("ISO speed:", camera.isoSpeed)