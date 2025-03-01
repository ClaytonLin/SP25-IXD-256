from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms, ticks_ms

print("NeoPixel LED + Copper Tape Contact Example")

contact_pin = Pin(1, Pin.IN, Pin.PULL_UP)  # Copper tape touch sensor

NUM_PIXELS = 30  
np = NeoPixel(Pin(7, Pin.OUT), NUM_PIXELS)  # Initialize LED strip

state = "WAITING"
yellow_count = 0  
last_yellow_time = ticks_ms()  
last_print_time = ticks_ms()  

yellow_speed = 250  
print_speed = 250  

def set_strip_color(r, g, b):  # Set all LEDs to a color
    for i in range(NUM_PIXELS):
        np[i] = (r, g, b)
    np.write()

def pulse_green():  # Green breathing effect
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
                np[yellow_count] = (255, 255, 0)  # Gradually turn LEDs yellow
                np.write()
                yellow_count += 1
                last_yellow_time = ticks_ms()
            else:
                state = "FINISH"  # All LEDs are yellow
                print("All LEDs turned yellow, switching to FINISH state.")

        if contact_state == 1:  # Touch detected
            state = "RUN"
            print("Copper tape contact detected, switching to RUN state.")

    elif state == "FINISH":
        set_strip_color(255, 0, 0)  # Turn LEDs red
        print("All LEDs turned red. FINISH state reached.")
    
    elif state == "RUN":
        pulse_green()  # Run green effect

        if contact_state == 0:  # No contact, reset to WAITING
            state = "WAITING"
            yellow_count = 0  
            print("Contact lost, switching back to WAITING state.")
