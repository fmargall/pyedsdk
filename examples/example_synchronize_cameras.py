from pyedsdk import loadSDKLib

if __name__ == "__main__":
    # For intellectual property and licensing reasons, the EDSDK dynamic
    # libraries (EDSDK.dll) are not distributed with this Python package
    # Before anything else it's mandatory to link the EDSDK.dll manually
    # You can download it for free on official Canon Developer Website :
    # https://www.canon.fr/business/imaging-solutions/sdk/
    pathToDllFile = r"C:\Canon\EDSDK\Dll\EDSDK.dll" # Adapt to your own
    loadSDKLib(pathToDllFile)

    # Note that the SyncCameraGroup import is done after loading the SDK
    # library, as it relies on the SDK functions.
    from pyedsdk.sync_camera_group import SyncCameraGroup

    # Rather than instancing and controlling each camera separately, you
    # can use a SyncCameraGroup instance to access and control them, all
    # at once. The constructor takes a list of camera indices.
    group = SyncCameraGroup([0, 1])

    # These parameters should be adapted to your current configuration
    # You can modify modify them at any time, and when called from the
    # group instance, they will be applied to all cameras at once.
    group.shutterSpeed = 1/10
    group.aperture     = 8.0
    group.isoSpeed     = 100

    # You can also modify parameters for each camera separately
    group[0].shutterSpeed = 10

    # You can then call the fire shot method to take a synchronized picture
    # /!\ Please note that the synchronization is not perfect, and that the
    # delay between the first and last camera can be up to 100 ms. We don't
    # recommend using this method if you need a perfect synchronization!
    group.fireShot(["testOne1.RAW", "testTwo2.RAW"])
