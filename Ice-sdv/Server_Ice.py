import sys, Ice
import fourApps
import requests

class SDVI(fourApps.SDV):
    def initFourApps(self, s, current=None):
        #Connect to http
        #Connect to http
        
        URL0 = "http://localhost:5010" # vs
        URL1 = "http://localhost:5011" # od
        URL2 = "http://localhost:5012" # hvac
        URL3 = "http://localhost:5013" # ota
  
        # location given here
        location = "container env"
	
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'address':location}
  
        # sending get request and saving the response as response object
        vs = requests.get(url = URL0, params = PARAMS)
        #od = requests.get(url = URL1, params = PARAMS)
        #hvac = requests.get(url = URL2, params = PARAMS)
        #ota = requests.get(url = URL3, params = PARAMS)
        #print(s)
    
 
with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("initApps", "default -p 10000")
    object = SDVI()
    adapter.add(object, communicator.stringToIdentity("initApps"))
    adapter.activate()
    communicator.waitForShutdown()
