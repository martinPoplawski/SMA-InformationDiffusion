import Config
from builtins import print as pp
import shutil

def print(message):
    """
    prints a message if verbose mode is activated
    """
    if Config.verbose:
        pp(message)

def progress(amount, max, steps=1, length=None):
    """
    prints a progress bar
    amount: the current amount of progress
    max: the maximum amount of progress
    [steps=1: for optimization, not to call IO too much]
    [length=100: the length of the progress bar]
    """

    if Config.verbose:
        if length is None:
            length, _ = shutil.get_terminal_size()
            length = length - 8 #fixed amount of characters
            length = length - len(f"{(max+1):,}") -len(f"{amount:,}")
        if amount > max:
            pp("cant print progress bar")
            return                    
        if amount % steps == 0 or amount == max-1:                  
            percent = int(amount *100 / max)
            estimatedProgress = ("~" if steps != 1 else "") + f"{amount:,}/{(max):,}".replace(",", "'")
            prog = "[" + "#" * int(percent/100*length) + "-" * int(length - (percent/100*length)) + "]"
            endNl = "\n" if amount == max-1 else ""                       
            pp("\r" + prog + f"{percent}% {estimatedProgress}", end=endNl)



if __name__ == "__main__":
    """
    test cases
    """

    Config.verbose = True
    print("this is a test")
    progress(50, 100)
    print("")

    progress(50, 100)
    progress(100, 100)   

    progress(50000, 100000, steps=1000)
    print("")

    progress(812811, 3251245) #about 25%