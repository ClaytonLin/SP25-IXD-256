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
Gesture Control:
``` Python 

    if gesture_timer >= 200:
        gesture_code = gesture_sensor.get_hand_gestures()
        if gesture_code:
            gesture_text = gesture_sensor.gesture_description(gesture_code).lower()

            if gesture_text == "left":
                if right_count > 0:
                    right_count -= 1
                    print(f"right{right_count}")
                else:
                    left_count += 1
                    print(f"left{left_count}")

            elif gesture_text == "right":
                if left_count > 0:
                    left_count -= 1
                    print(f"left{left_count}")
                else:
                    right_count += 1
                    print(f"right{right_count}")

            elif gesture_text in ["up", "down", "forward", "backward", "clockwise", "anticlockwise", "wave"]:
                left_count = 0
                right_count = 0
                print(gesture_text)

        gesture_timer = 0
```

Distance map to servo speed & LED stripe light:
``` Python 
        if ir_val < 2400:
            current_state = "green"
            if not welcome_sent:
                print("welcome")
                mqtt_client.publish(aio_user_name + '/feeds/welcomefeed', 'welcome', qos=0)
                welcome_sent = True
                last_state = "green"
                continue

            green_enabled = True
            color = interpolate_color(ir_val)
            set_leds(color)
            speed_percent = int((2400 - ir_val) / 2400 * 100)
            set_servo_speed(speed_percent)
        else:
            current_state = "default"
            set_leds((255, 255, 255))
            servo.duty(77)
```

Receive message from protopie:
``` Python 
        ch = sys.stdin.readline().strip()
        if ch != '':
            if ch == "scifi":
                scifi_effect()
                special_effect_mode = True
                special_effect_name = "scifi"
            elif ch == "rnb":
                rnb_effect()
                special_effect_mode = True
                special_effect_name = "rnb"
            elif ch == "rap":
                rap_effect()
                special_effect_mode = True
                special_effect_name = "rap"
            elif ch == "piano":
                piano_effect()
                special_effect_mode = True
                special_effect_name = "piano"
            else:
                special_effect_mode = False
                special_effect_name = ""

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
