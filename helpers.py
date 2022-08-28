import time
from time import sleep
import locale

locale.setlocale(locale.LC_ALL, '')

def m(x):
    return locale.currency(x, grouping=True)

def int_(x):
    x = str(x.replace("$", "").replace(" ", "").replace(",", ""))
    for n in x:
        if n not in "0123456789.":
            print("\n. . .\nERROR: Enter a valid number.\n. . .\n")
            return False
        else: 
            return float(x)

def dots(x):
    for z in range(x):
        print('.', end=' ', flush=True)
        time.sleep(0.3)