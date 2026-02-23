
from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("pyedsdk")
except PackageNotFoundError:
    __version__ = "?.?.?"