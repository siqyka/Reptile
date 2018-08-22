from db import *
from config import *
from getproxy import *
from detect import *
import importlib

def run():
    proxy = importlib.import_module(OVERRIDE_MODULE['MODULENAME'])
    str1='proxy.'+OVERRIDE_MODULE['CLASSNAME']+'()'
    class1=eval(str1)
    lproxy = class1.run()

    # db=SaveToDatabase()
    # for data in lproxy:
    #     db.set(data)

    detect=Detect()
    detect.run()


if __name__ == '__main__':
    run()