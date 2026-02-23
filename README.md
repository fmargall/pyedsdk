## Installation

> [!WARNING]
> - `pyedsdk` currently only supports Windows. 
> - You must download and install the Canon EDSDK separatly from Canon directly. 
> -  For intellectual property and licensing reasons, the EDSDK dynamic libraries (`EDSDK.dll`) are not distributed with this Python package.

Canon requires developers to request access to the SDK directly from them.
Please visit the official [Canon Developer website](https://www.canon.fr/business/imaging-solutions/sdk/) and obtain the EDSDK before using this module. This may take a few days before you can have access.

### 1. Install Canon EDSDK

After downloading the SDK from Canon:
1. Install or extract the SDK on your machine
1. Locate the `EDSDK.dll` associated to your architecture (for Windows, either inside `EDSDK` or `EDSDK_64` folder). You can choose to paste it for instance in a new folder located at `C:\Canon\EDSDK\Dll\EDSDK.dll`.

### 2. Make the DLL discoverable

#### (Recommended) Set environment variable

Simply run in your terminal the following command with the path to the DLL:

```bash
setx EDSDK_PATH "C:\Canon\EDSDK\Dll\EDSDK.dll"
```
And restart your terminal afterwards.

#### (Alternative) Add SDK folder to your PATH

Add the directory containing `EDSDK.dll` to your Windows `PATH` environment variable.

#### (Alternative) Pass the path explicitly in Python

Simply jump to the next part for the installation of the `pyedsdk` package, and when calling it, initialize the DLL with the following code:

```python
from pyedsdk.core.loader import loadSDKLib

loadSDKLib(r"C:\Canon\EDSDK\Dll\EDSDK.dll")
```

### Installing `pyedsdk`

#### (Recommended) Using `pip`

The safest and easiest way to install the latest version is via PyPI:

```bash
pip install pyedsdk
```

## License

This package is an independent, unofficial Python binding for Canon EDSDK. Canon EDSDK is proprietary software owned by Canon Inc. This project:
 - does **not** redistribute Canon binaries
 - does **not** modify Canon SDK files
 - **requires** users to agree to Canon's license separately
 - is **not affiliated with, endorsed by, or sponsored by Canon Inc.**

Canon EDSDK remains the exclusive property of Canon Inc. Users are responsible for complying with Canon’s SDK License Agreement.

PyEDSDK is distributed under the MIT License. See `License.txt` for more information.