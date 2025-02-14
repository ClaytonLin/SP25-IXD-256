from machine import Pin, ADC
from time import *
from neopixel import NeoPixel

# configure pin 1 as input:
analog_pin = Pin(1, Pin.IN)

# configure ADC on an input pin:
adc = ADC(analog_pin)

# configure the ADC sensitivity:
adc.atten(ADC.ATTN_11DB)

# create NeoPixel driver on pin 35 for 1 pixel:
# (built-in RGB LED on AtomS3 Lite)
np = NeoPixel(Pin(35), 1)

# create NeoPixel driver on pin 7 for 30 pixel:
# RGB LED strip connected to pin 7 on AtomS3 Lite
# (black connector on PortABC extension)
np7 = NeoPixel(Pin(7), 30)

while True:
    # read the ADC value:
    analog_val = adc.read()
    #print(analog_val)
    analog_val_8bit = int(analog_val/16)
    print(analog_val_8bit)
    sleep_ms(100)
    
    # set built-in RGB LED blue color to 8-bit analog value:
    np[0] = (0, 0, analog_val_8bit)
    np.write()
    
    # set RGB LED strip green color to 8-bit analog value:
    for i in range(30):
        np7[i] = (0, analog_val_8bit, 0)
    np7.write()
    
    


