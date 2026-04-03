# This liveView example works with an OpenCV backend. You will need
# to install both openCV and NumPy in order to use it.
import cv2, numpy as np

from pyedsdk import loadSDKLib

if __name__ == "__main__":
    # For intellectual property and licensing reasons, the EDSDK dynamic
    # libraries (EDSDK.dll) are not distributed with this Python package
    # Before anything else it's mandatory to link the EDSDK.dll manually
    # You can download it for free on official Canon Developer Website :
    # https://www.canon.fr/business/imaging-solutions/sdk/
    pathToDllFile = r"C:\Canon\EDSDK\Dll\EDSDK.dll" # Adapt to your own
    loadSDKLib(pathToDllFile)

    from pyedsdk.camera import EOSCamera

    # You can initialize your camera by giving to the constructor the
    # current index of the wanted camera. If there is only one camera
    # connected, the index will always be set at 0.
    camera = EOSCamera(0)

    # These parameters should be adapted to your current configuration
    camera.shutterSpeed = 1/100
    camera.aperture     = 2.8
    camera.isoSpeed     = 800

    # The live view stream is an iterator, and can be called using a
    # for loop, each iteration being a new frame collected by camera
    for frame in camera.liveViewStream():
        # Convert bytes to numpy buffer
        npBuffer = np.frombuffer(frame, dtype=np.uint8)

        # Decode JPEG image
        img = cv2.imdecode(npBuffer, cv2.IMREAD_COLOR)

        # Display
        cv2.imshow("Live View", img)

        # Exit on ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Cleanup
    cv2.destroyAllWindows()