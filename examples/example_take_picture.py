from pyedsdk import loadSDKLib

if __name__ == "__main__":
    # For intellectual property and licensing reasons, the EDSDK dynamic
    # libraries (EDSDK.dll) are not distributed with this Python package
    # Before anything else it's mandatory to link the EDSDK.dll manually
    # You can download it for free on official Canon Developer Website :
    # https://www.canon.fr/business/imaging-solutions/sdk/
    pathToDllFile = r"C:\Canon\EDSDK\Dll\EDSDK.dll" # Adapt to your own
    loadSDKLib(pathToDllFile)

    # Note that the EOSCamera import is done after loading SDK library,
    # as it relies on the SDK functions.
    from pyedsdk.camera import EOSCamera

    # You can initialize your camera by giving to the constructor the
    # current index of the wanted camera. If there is only one camera
    # connected, the index will always be set at 0.
    camera = EOSCamera(0)

    # These parameters should be adapted to your current configuration
    camera.shutterSpeed = 1/8000
    camera.aperture     = 8.
    camera.isoSpeed     = 100

    # Taking a picture is made by calling the 'shot' camera function:
    camera.shot(filename="output.RAW")
