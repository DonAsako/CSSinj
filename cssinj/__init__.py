from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version('cssinj')
except PackageNotFoundError:  # editable install without metadata
    __version__ = '0.0.0+unknown'
