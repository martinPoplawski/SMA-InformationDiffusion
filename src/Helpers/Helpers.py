import Config
from builtins import print as pp

def print(message):
    """
    prints a message if verbose mode is activated
    """
    if Config.verbose:
        pp(message)

def progress(amount, max, steps=1, length=100):
    """
    prints a progress bar
    """
    if Config.verbose:
        max -= 1
        if amount > max:
            print("cant print progress bar")
            return                    
        if amount % steps == 0 or amount == max:                  
            percent = int(amount *length / max)
            estimatedProgress = ("~" if steps != 1 else "") + f"{amount:,}/{max:,}".replace(",", "'")
            prog = "[" + "#" * percent + "-" * (length - percent)
            endNl = "\n" if amount == max else ""                       
            pp("\r" + prog + f"]{percent}% {estimatedProgress}", end=endNl)



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