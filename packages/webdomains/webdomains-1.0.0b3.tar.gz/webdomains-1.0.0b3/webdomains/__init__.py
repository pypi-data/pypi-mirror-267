import importlib.metadata

try:
    __version__ = importlib.metadata.version("webdomains")
except importlib.metadata.PackageNotFoundError:  # pragma: no cover
    pass
