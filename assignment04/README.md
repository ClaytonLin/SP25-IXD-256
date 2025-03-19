### Introduction

My idea is to make a glove for shooting games. When you wear this glove and make shooting movements, it will detect your hand motions and give feedback on the screen, like hitting an enemy.

### State Diagram

My system has several states:

At the beginning, it starts in the "START" state, where the RGB and input pins are initialized. Then, the IMU Pro unit monitors motion data.

If the IMU Pro unit detects a high X-axis value, the system enters the "CHARGING" state. If the unit value then drops below a certain threshold, it transitions to "BLASTING", turning the LEDs red and playing a "BOOM" sound. This action eliminates an enemy.

If the Y-axis value changes very fast, the system enters the "ULTIMATE" state, turning all LEDs white. If all enemies are eliminated, the player wins.

If the Y-axis value exceeds a certain threshold, the system enters the "NEXT" state, where another enemy is eliminated. If all enemies are eliminated within 10 seconds, the player wins. Otherwise, the player loses.

If the IMU Pro unit value remains low, the system stays in "WAITING", keeping the LEDs off.

<img width="3236" alt="Diagram" src="https://github.com/user-attachments/assets/c016acff-7547-48bf-b95a-240a0a9f47f3" />


### Hardware
* M5 Stack: Processing and controlling
* NeoPixel: Show the light on the glove and provide light feedback.
* Copper Tape: Detects hand movement, mainly including X-axis and Y-axis movement.
* Laptop: Coding, uploading firmware, ,monitoring output and providing power.
  
![Sketches_1](https://github.com/user-attachments/assets/585e23f3-e3da-40ea-b9ad-3aee5c910e3d)
![Hardware_1](https://github.com/user-attachments/assets/ef969139-da73-4bd1-86ad-59949c64785f)


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
I used a black glove as the base and cut several hollow circles out of cardboard, stacking them together to form the core part of the emitting rays. The sides of these cardboard pieces feature hollow patterns, allowing light to shine through. An LED strip, IMU Pro, and M5 Stack are attached inside this cardboard-made energy core, with the entire setup affixed to the glove.


### Project Outcomes
This project captures hand movements with high precision, and the on-screen feedback is very responsive. However, in the future, if I have more time, I will refine the physical components, using better materials to enhance the appearance of the energy core. Additionally, I plan to add a targeting icon on the screen to make the aiming process feel more like a targeting game.
![WechatIMG2249](https://github.com/user-attachments/assets/1196e1d5-c437-4f84-8b19-7cf679a74972)
![WechatIMG2248](https://github.com/user-attachments/assets/594a6905-67bc-400b-922c-89618063b60a)
![WechatIMG2247](https://github.com/user-attachments/assets/1b57a5a9-dd78-406b-8558-244713654052)
![WechatIMG2246](https://github.com/user-attachments/assets/f9f953d7-363d-4219-97ba-3b5ac2b47482)




https://drive.google.com/file/d/19bkw-SsjQaKgUjiETXWyZsPTaRwSIf5I/view?usp=drive_link

