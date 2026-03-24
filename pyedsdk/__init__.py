
from .core.loader import loadSDKLib
from  camera      import EOSCamera


from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("pyedsdk")
except PackageNotFoundError:
    __version__ = "?.?.?"