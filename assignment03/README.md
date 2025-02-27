### Introduction

My idea is to create a Chinese lantern because it was recently Chinese New Year. People usually use lanterns during the New Year, so after the festival ends, they have to wait a whole year to use them again. I want to bring this meaning into my project, so when people use it, they can feel the slow passing of time and the difficulties of life.

### State Diagram

My lantern has three states. At the beginning, it checks if the copper tape is touching. If not, all LEDs will pulsate in RGB green. Once it touches, all lights will turn off, and the LEDs will light up one by one in RGB yellow. If the copper tape stops touching during this process, all LEDs will go back to pulsating in RGB green. When all LEDs are lit in yellow, they will turn red. At this point, even if the copper tape is released, the red light will stay.
<img width="1920" alt="State Diagram" src="https://github.com/user-attachments/assets/d37b1776-1ba0-4dfb-9622-5ce1388e998a" />


### Hardware
* M5 Stack: for processing and controlling
* NeoPixel: allows individual control of each LED using a single data wire
* Copper Tape: used as a button sensor or for electrical connections.
* Laptop: used for coding, uploading firmware, ,monitoring output and providing power.

### Firmware

``` Python 
from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms, ticks_ms

print("NeoPixel LED + Copper Tape Contact Example")


contact_pin = Pin(1, Pin.IN, Pin.PULL_UP) 


NUM_PIXELS = 30  
np = NeoPixel(Pin(7, Pin.OUT), NUM_PIXELS)


state = "WAITING"
yellow_count = 0  
last_yellow_time = ticks_ms()   
last_print_time = ticks_ms()  

yellow_speed = 250  
print_speed = 250  

def set_strip_color(r, g, b):
    for i in range(NUM_PIXELS):
        np[i] = (r, g, b)
    np.write()

def pulse_green():
    for brightness in range(0, 256, 5): 
        for i in range(NUM_PIXELS):
            np[i] = (0, brightness, 0)
        np.write()
        sleep_ms(10)
    for brightness in range(255, -1, -5): 
        for i in range(NUM_PIXELS):
            np[i] = (0, brightness, 0)
        np.write()
        sleep_ms(10)

while True:
    contact_state = contact_pin.value()  

    if ticks_ms() - last_print_time >= print_speed:
        print("Copper tape state =", contact_state)
        last_print_time = ticks_ms()

    if state == "WAITING":
        if ticks_ms() - last_yellow_time >= yellow_speed:
            if yellow_count < NUM_PIXELS:
                np[yellow_count] = (255, 255, 0)  
                np.write()
                yellow_count += 1
                last_yellow_time = ticks_ms()
            else:
                state = "FINISH"
                print("All LEDs turned yellow, switching to FINISH state.")

        if contact_state == 1: 
            state = "RUN"
            print("Copper tape contact detected, switching to RUN state.")

    elif state == "FINISH":
        set_strip_color(255, 0, 0) 
        print("All LEDs turned red. FINISH state reached.")
    
    elif state == "RUN":
        pulse_green() 

        if contact_state == 0:  
            state = "WAITING"
            yellow_count = 0  
            print("Contact lost, switching back to WAITING state.")
```



