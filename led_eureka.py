import time
from machine import Pin 

class LEDPTK:
    def __init__(self, led):
        self.led = Pin(led, Pin.OUT)    

    def liga(self):
        self.led.on()

    def desliga(self):
        self.led.off()