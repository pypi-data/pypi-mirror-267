from importlib import metadata

if __package__ == "cephalon":
    __package__ = "cephalon-client"
__version__ = metadata.version("cephalon-client")
