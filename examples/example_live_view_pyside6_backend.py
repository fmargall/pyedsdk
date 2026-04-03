# This liveView example works with a PySide6 backend. You will need
# to install PySide6 in order to use it.
import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui     import QImage, QPixmap
from PySide6.QtCore    import Signal, QObject

from pyedsdk import loadSDKLib

class CameraSignal(QObject):
    frameReady = Signal(QPixmap)

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

    app    = QApplication(sys.argv)
    window = QMainWindow()
    label  = QLabel()
    window.setCentralWidget(label)
    window.show()

    # You can initialize your camera by giving to the constructor the
    # current index of the wanted camera. If there is only one camera
    # connected, the index will always be set at 0.
    camera = EOSCamera(0)

     # These parameters should be adapted to your current configuration
    camera.shutterSpeed = 1/100
    camera.aperture     = 2.8
    camera.isoSpeed     = 800

    sig = CameraSignal()
    sig.frameReady.connect(label.setPixmap)

    def onFrame(frame: bytes):
        image = QImage.fromData(frame)
        sig.frameReady.emit(image.toPixmap())

    stream = camera.liveView(callback=onFrame)

    sys.exit(app.exec())
