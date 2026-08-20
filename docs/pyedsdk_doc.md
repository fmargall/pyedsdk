# pyedsdk — Canon EDSDK Python Bindings

pyedsdk is a Python binding for the Canon EDSDK (EOS Digital Software Development Kit), allowing you to control Canon EOS cameras programmatically from Python.

## Installation

```bash
pip install pyedsdk
```

## Prerequisites

### Windows

1. Request and download the EDSDK package from the official Canon developer portal.
2. Place `EDSDK.dll` (64-bit version is located in `EDSDK_64/Dll/`) in one of the following locations:
   - `C:\Windows\System32`
   - Your project's current working directory
   - A path specified by the `EDSDK_PATH` environment variable
3. The library will search these locations automatically when loading.

### macOS / Linux

Currently, `pyedsdk` **only supports Windows**. macOS and Linux support is not yet implemented. Contributions are welcome.

## Quick Start

```python
from pyedsdk.camera import EOSCamera

# Initialize the first camera
camera = EOSCamera(0)

# Read current shutter speed
print(camera.shutterSpeed)

# Set shutter speed to 1/125 sec
camera.shutterSpeed = 1/125

# Set aperture to f/8
camera.aperture = 8.0

# Set ISO to 400
camera.isoSpeed = 400

# Take a photo (saved as image.RAW in current directory)
camera.shot()

# Take a photo with a custom filename
camera.shot("my_photo.RAW")

# Close the camera session (or use a context manager)
camera._close()
```

Using `with` for automatic resource management:

```python
with EOSCamera(0) as camera:
    camera.shot("photo.RAW")
```

## Core API

### EOSCamera

`EOSCamera(cameraIndex)` — Connects to the camera at the specified index.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `shutterSpeed` | `float` | Shutter speed in seconds. Read/write. |
| `aperture` | `float` | Aperture f-number. Read/write. |
| `isoSpeed` | `float` | ISO sensitivity. Read/write. |
| `mirrorLockUp` | `bool` | Mirror lock-up state. Read/write. |
| `afMode` | `str` | Current autofocus mode (read-only). |
| `filename` | `str` | Default filename for the next shot. Read/write. |

**Note**: When setting `shutterSpeed`, `aperture`, or `isoSpeed`, the library automatically rounds your input to the nearest available value supported by the camera.

#### Methods

**`shot(filename: str = None) -> None`**

Triggers the shutter. If `filename` is provided, it overrides the default filename. The image is saved to the current working directory.

**`liveViewStream(callback=None, errorCallback=None) -> LiveViewStream`**

Starts a live view stream. Returns a `LiveViewStream` object.

#### Querying Available Values

```python
camera = EOSCamera(0)

# Get a list of all supported aperture values
print(camera.getAvailableApertures())

# Setting a property automatically snaps to the nearest valid value
camera.aperture = 2.8  # Snaps to the closest supported aperture
```

### LiveViewStream

The object returned by `EOSCamera.liveViewStream()` for handling live view frames.

#### Usage Modes

**Mode 1: Callback-driven**

```python
def on_frame(frame_bytes):
    # frame_bytes is JPEG image data
    with open("frame.jpg", "wb") as f:
        f.write(frame_bytes)

def on_error(err):
    print("Live view error:", err)

stream = camera.liveViewStream(callback=on_frame, errorCallback=on_error)

# ... later
stream.stop()
```

**Mode 2: Iterator**

```python
stream = camera.liveViewStream()
for frame in stream:
    process_frame(frame)
    if some_condition:
        break
# Stream stops automatically when exiting the loop
```

**Mode 3: Manual frame fetching**

```python
stream = camera.liveViewStream()
stream.start()  # Manual start

try:
    frame = stream.getFrame()
    save_frame(frame)
finally:
    stream.stop()
```

### SyncCameraGroup

Synchronizes multiple cameras for array shooting.

```python
from pyedsdk.sync_camera_group import SyncCameraGroup

# Connect cameras at indices 0 and 1
group = SyncCameraGroup([0, 1])

# Set the same parameter on all cameras simultaneously
group.aperture = 5.6
group.shutterSpeed = 1/200

# Control individual cameras
group[0].isoSpeed = 100
group[1].isoSpeed = 400

# Synchronized shooting
group.fireShot(["cam0.RAW", "cam1.RAW"])
```

## Error Handling

All EDSDK errors raise a `CanonError` exception:

```python
from pyedsdk.core._errors import CanonError

try:
    camera.shot()
except CanonError as e:
    print(f"Error code: {e.code}")
    print(f"Error name: {e.name}")
    print(f"Message: {e.message}")
```

Common error codes:

| Error Code | Description |
|------------|-------------|
| `ERR_DEVICE_NOT_FOUND` | No camera found |
| `ERR_DEVICE_BUSY` | Camera is busy |
| `ERR_TAKE_PICTURE_AF_NG` | Autofocus failed |
| `ERR_OBJECT_NOTREADY` | Live view frame not ready yet |

## Important Notes

1. **Always close the camera session**: Use `with` or call `_close()` manually to release resources.
2. **Live view performance**: Each frame download takes about 2-3 seconds, resulting in low FPS.
3. **Mirror lock-up**: When `mirrorLockUp` is enabled, the `shot()` method handles the required additional shutter commands automatically.
4. **File format**: The default format is RAW (`.RAW`). To use other formats, you need to extend `_ImageQuality`.

## Full Example

```python
from pyedsdk.camera import EOSCamera
from pyedsdk.core._errors import CanonError
import time

def main():
    try:
        with EOSCamera(0) as cam:
            print(f"AF Mode: {cam.afMode}")
            print(f"Initial ISO: {cam.isoSpeed}")

            # Set parameters
            cam.shutterSpeed = 1/60
            cam.aperture = 5.6
            cam.isoSpeed = 800

            # Live view callback
            frame_count = 0
            def save_frame(data):
                nonlocal frame_count
                with open(f"lv_frame_{frame_count:03d}.jpg", "wb") as f:
                    f.write(data)
                frame_count += 1

            # Start live view, capture a few frames
            stream = cam.liveViewStream(callback=save_frame)
            time.sleep(3)  # Let the callback capture several frames
            stream.stop()

            # Final shot
            cam.shot("final.RAW")
            print("Done!")

    except CanonError as e:
        print(f"Camera error: {e}")

if __name__ == "__main__":
    main()
```

## Roadmap

- [ ] macOS support
- [ ] Linux support
- [ ] More image format support (JPEG, HEIF)
- [ ] Comprehensive property descriptions
- [ ] Async API

## License

This project is licensed under the Apache License 2.0. The EDSDK itself is governed by Canon's license agreement. Please read and comply with Canon's terms before use.