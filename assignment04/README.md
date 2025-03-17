### Introduction

My idea is to make a glove for shooting games. When you wear this glove and make shooting movements, it will detect your hand motions and give feedback on the screen, like hitting an enemy.

### State Diagram

My lantern has three states. At the beginning, it checks if the copper tape is touching. If not, all LEDs will pulsate in RGB green. Once it touches, all lights will turn off, and the LEDs will light up one by one in RGB yellow. If the copper tape stops touching during this process, all LEDs will go back to pulsating in RGB green. When all LEDs are lit in yellow, they will turn red. At this point, even if the copper tape is released, the red light will stay.

<img width="3236" alt="Diagram" src="https://github.com/user-attachments/assets/c016acff-7547-48bf-b95a-240a0a9f47f3" />




### Hardware
* M5 Stack: Processing and controlling
* NeoPixel: Show the light on the glove and provide light feedback.
* Copper Tape: Detects hand movement, mainly including X-axis and Y-axis movement.
* Laptop: Coding, uploading firmware, ,monitoring output and providing power.
  

![Diagram](https://github.com/user-attachments/assets/1838d6e0-8f60-4695-a479-3a1e2c08c368)

![Hardware_2](https://github.com/user-attachments/assets/aed63ed6-a413-4264-85da-44d5d8d6654f)


### Firmware
IMU Data Processing:
``` Python 
if (ticks_ms() > imu_timer + 100):
    imu_timer = ticks_ms()
    imu_val = imu.get_accelerometer()
    imu_x = imu_val[0]
    imu_y = imu_val[1]

    message = "a"
    r_final, g_final, b_final = 0, 0, 0
    
    if abs(imu_y) > 0.5:
        r_final = 255
        message = "b"
    elif abs(imu_x) > 0.5:
        r_final = 255
        g_final = 255
        message = "c"

```

LED Color Transition:
``` Python 
step = 10  
if r < r_final:
    r += step
elif r > r_final:
    r -= step
if g < g_final:
    g += step
elif g > g_final:
    g -= step
if b < b_final:
    b += step
elif b > b_final:
    b -= step
     
red = int(r * brightness / 100)
green = int(g * brightness / 100)
blue = int(b * brightness / 100)
for i in range(30):
    np[i] = (red, green, blue)
np.write()

```

White Light Effect:
``` Python 
def white_fade():
    print("White light for 3 seconds")
    for i in range(30):
        np[i] = (255, 255, 255)
    np.write()
    sleep(3)

    print("e")

    for brightness in range(255, -1, -10):
        for i in range(30):
            np[i] = (brightness, brightness, brightness)
        np.write()
        sleep_ms(50)

    reset_counters()


```

### Physical Components
I used white paper to build the shape. Since my LED has three different colors, I wanted the lantern itself to not affect the LED colors in different states.

I rolled a piece of paper into a cylinder to hold the LED strip and other parts. In the middle, I added a cardboard piece to support the cylinder and components. This way, the LEDs won’t appear as sharp circular spots on the paper but will create a more blurred and soft light effect.

For the outer shape, I used paper to make the curved form of the lantern. I cut a piece of paper into strips with about 0.5 inches spacing (leaving the top and bottom uncut). Then, I attached it to the cylinder and adjusted it by hand to make it more three-dimensional.

For the tassels at the bottom, I used white paper. I cut it into thin strips about 0.1 inches apart (keeping the top part uncut), rolled it up, and attached it to a wire.


### Project Outcomes
The final result is very good. When the lantern is green and yellow, it makes you want it to turn red.

In the future, if I have time, I hope to decorate the copper tape with small bells and add more interesting animations to the color changes.

![Outcome_1](https://github.com/user-attachments/assets/449f0059-b9b1-4725-9bc3-ac5bf61e90ae)
![Outcome 2](https://github.com/user-attachments/assets/5f333076-9f8b-4169-8631-f70c06008b51)


https://drive.google.com/file/d/19bkw-SsjQaKgUjiETXWyZsPTaRwSIf5I/view?usp=drive_link

