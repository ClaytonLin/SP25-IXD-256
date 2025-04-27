### Introduction

My idea is to create a physical companion device for an LLM system that can gather data from the real world and work with the AI on the screen to produce outputs in the physical world. My prototype will focus on using it in a music listening scenario. The physical form is designed as a small flower that can be placed on the user's desk, allowing users to interact with it using their hands.

### State Diagram

<img width="3339" alt="Diagram" src="https://github.com/user-attachments/assets/3b710335-ebf1-439d-a43a-9f405e7478fc" />


### Hardware
* M5 Stack: for processing and controlling.
* NeoPixel: allows individual control of each LED using a single data wire.
* Reflective IR Sensor: Used to detect the distance of the hand.
* Gesture Sensor: Used to detect hand gestures, including up, down, forward, backward, left, and right.
* Laptop: used for coding, uploading firmware,monitoring output, providing power, listening to voice command and show the AI UI.
  
<img width="567" alt="Screenshot 2025-04-26 at 9 25 56 PM" src="https://github.com/user-attachments/assets/4ce36000-96a6-42ec-8743-13c3e9f46094" />


### Firmware
Green Pulse Effect:
``` Python 

def pulse_green():
    for brightness in range(0, 256, 5): 
        for i in range(NUM_PIXELS):
            np[i] = (0, brightness, 0)
        np.write()![Uploading WechatIMG2221.jpeg…]()

        sleep_ms(10)
    for brightness in range(255, -1, -5): 
        for i in range(NUM_PIXELS):
            np[i] = (0, brightness, 0)
        np.write()
        sleep_ms(10)
```

LED Turning Yellow in WAITING State:
``` Python 
if state == "WAITING":
    if ticks_ms() - last_yellow_time >= yellow_speed:
        if yellow_count < NUM_PIXELS: # Gradually turn LEDs yellow
            np[yellow_count] = (255, 255, 0)  
            np.write()
            yellow_count += 1
            last_yellow_time = ticks_ms()
        else: # All LEDs are yellow
            state = "FINISH"
            print("All LEDs turned yellow, switching to FINISH state.")
```

Red LEDs in FINISH State:
``` Python 
elif state == "FINISH":
    set_strip_color(255, 0, 0) 
    print("All LEDs turned red. FINISH state reached.")

```

### Physical Components
I used LEGO to build the flower and its stem, and combined LEGO with other small parts to create the connection between the flower and the stem, ensuring that the flower could be controlled by a servo. I also placed a Reflective IR sensor inside.

For the flowerpot, I designed it in SolidWorks and separated it into different layers. Then, I used a special type of cardboard with translucent stripes along the sides and laser cut 15 layers of varying sizes. By gluing them together, I created a three-dimensional, organic-shaped flowerpot. Most of the hardware was placed inside the pot, and I attached an LED strip closely along the inner wall to ensure that the light could effectively shine through.




### Project Outcomes
The final result is very good. When the lantern is green and yellow, it makes you want it to turn red.

In the future, if I have time, I hope to decorate the copper tape with small bells and add more interesting animations to the color changes.

![Outcome_1](https://github.com/user-attachments/assets/449f0059-b9b1-4725-9bc3-ac5bf61e90ae)
![Outcome 2](https://github.com/user-attachments/assets/5f333076-9f8b-4169-8631-f70c06008b51)


https://drive.google.com/file/d/19bkw-SsjQaKgUjiETXWyZsPTaRwSIf5I/view?usp=drive_link
