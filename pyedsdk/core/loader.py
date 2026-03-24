import ctypes, os, platform

from pathlib import Path

from ._lib import lib


def _defaultSearchPaths() -> list[Path]:
    paths = []

    # Explicit environment variable
    env = os.getenv("EDSDK_PATH")
    if env:
        paths.append(Path(env))

    # PATH Windows
    for p in os.getenv("PATH", "").split(os.pathsep):
        candidate = Path(p) / "EDSDK.dll"
        if candidate.exists():
            paths.append(candidate)

    # Current folder
    paths.append(Path.cwd() / "EDSDK.dll")

    return paths


def loadSDKLib(customPath: str | None = None):
    if platform.system() != "Windows":
        raise RuntimeError("Canon EDSDK Python binding currently only supports Windows.")

    if customPath:
        realLib = ctypes.windll.LoadLibrary(customPath)
        lib.load(realLib)
        return realLib

    for path in _defaultSearchPaths():
        if path.exists():
            realLib = ctypes.windll.LoadLibrary(str(path))
            lib.load(realLib)
            return realLib

    raise RuntimeError("EDSDK.dll not found.")