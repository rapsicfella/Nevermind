import sys, Ice
import fourApps
 
with Ice.initialize(sys.argv) as communicator:
    base = communicator.stringToProxy("initApps:default -p 10000")
    sdv = fourApps.SDVPrx.checkedCast(base)
    if not sdv:
        raise RuntimeError("Invalid proxy")
 
    sdv.initFourApps("All the apps initialized")
