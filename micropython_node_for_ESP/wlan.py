import network
import time

class WLAN:
    def __init__(self, ssid="", password="", ap=False):
        self.ssid = ssid
        self.password = password
        self.ap = ap
        if self.ap:
            self.wlan = network.WLAN(network.AP_IF)
        else:
            self.wlan = network.WLAN(network.STA_IF)
        
    def set_ssid(self, ssid):
        self.ssid = ssid
        
    def set_password(self, password):
        self.password = password 
        
    def connect(self):
        self.wlan.active(True)
        if self.ap:
            self.wlan.config(essid=self.ssid, password=self.password)
        else:
            if not self.wlan.isconnected():
                print('connecting to network...')
                self.wlan.connect(self.ssid, self.password)
                start = time.time()
                while not self.wlan.isconnected():
                    if (time.time()-start)>100:
                        print("network connection failed!")
                        break
        print('network config:', self.wlan.ifconfig())
    
    def getmac(self):
        return self.wlan.config('mac')
    
    def getip(self):
        return self.wlan.ifconfig()[0]
    
    def getmacid(self):
        macid=self.wlan.config('mac')[3]+self.wlan.config('mac')[4]+self.wlan.config('mac')[5]
        return macid