import Config
from builtins import print as pp

def print(message):
    """
    prints a message if verbose mode is activated
    """
    if Config.verbose:
        pp(message)
