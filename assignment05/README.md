### Introduction

My idea is to create a physical companion device for an LLM system that can gather data from the real world and work with the AI on the screen to produce outputs in the physical world. My prototype will focus on using it in a music listening scenario. The physical form is designed as a small flower that can be placed on the user's desk, allowing users to interact with it using their hands.

### State Diagram

<img width="3339" alt="Diagram" src="https://github.com/user-attachments/assets/3b710335-ebf1-439d-a43a-9f405e7478fc" />


### Hardware
* M5 Stack: for processing and controlling.
* NeoPixel: allows individual control of each LED using a single data wire.
* Reflective IR Sensor: Used to detect the distance of the hand.
* Gesture Sensor: Used to detect hand gestures, including up, down, forward, backward, left, and right.
* Servo: Control the flowers to spin.
* Laptop: used for coding, uploading firmware,monitoring output, providing power, listening to voice command and show the AI UI.
  
<img width="1200" alt="Hardware" src="https://github.com/user-attachments/assets/53d6e3d1-33c5-4157-87ca-c712c8affae7" />


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
In ProtoPie, I used over 130 lines of triggers and feedback(Including AI animations, song playback and more):

<img width="1503" alt="Screenshot 2025-04-26 at 11 16 12 PM" src="https://github.com/user-attachments/assets/0ab61626-2256-49a4-8ef8-17010a490a4f" />

In ProtoPie Connect, I connected to OpenAI's API to generate responses. This AI has been fine-tuned to answer only music-related questions and, when executing commands (such as playing a song), it will not generate responses indicating that it cannot play music.

<img width="310" alt="Screenshot 2025-04-26 at 11 29 55 PM" src="https://github.com/user-attachments/assets/1fbcdf56-2638-416f-a42c-ba6dce571b48" />


For Cloud Communication:
The program sends messages to Adafruit and uses IFTTT to create automated workflows. When I activate the AI for the first time each day, an email is sent saying "Clayton is home." Additionally, whenever a song is played, it is automatically added to a Google Sheets document.

![Screenshot 2025-04-26 at 11 25 26 PM](https://github.com/user-attachments/assets/b87dc5e6-7229-4184-81ca-e2bfc887462b)

![Screenshot 2025-04-26 at 11 25 03 PM](https://github.com/user-attachments/assets/00b60a08-1858-4fd9-aaa8-7b1712d9b211)


### Physical Components
I used LEGO to build the flower and its stem, and combined LEGO with other small parts to create the connection between the flower and the stem, ensuring that the flower could be controlled by a servo. I also placed a Reflective IR sensor inside.

For the flowerpot, I designed it in SolidWorks and separated it into different layers. Then, I used a special type of cardboard with translucent stripes along the sides and laser cut 15 layers of varying sizes. By gluing them together, I created a three-dimensional, organic-shaped flowerpot. Most of the hardware was placed inside the pot, and I attached an LED strip closely along the inner wall to ensure that the light could effectively shine through.




### Project Outcomes
I think the final result of the software part is very good. I managed to obtain input from the hardware and produce output on the software side, while simultaneously obtaining input from the software and producing output on the hardware side. This was the effect I initially aimed to achieve — truly realizing seamless communication between software and hardware. Overall, the interaction is also very rich, supporting most scenarios for listening to music. It’s a product that can be used straight away.

However, if I had more time, I would make my prototype more refined — not only by perfectly hiding all the sensors so they wouldn’t be visible from the outside, but also by adding more diverse physical outputs, such as incorporating a servo motor to control the movement of the leaves.

![Final_Outcome](https://github.com/user-attachments/assets/5183ac2d-ba55-401d-a6f5-4bcf401c5556)
![Final_Outcome_2](https://github.com/user-attachments/assets/4bd9c68c-72d4-4ade-a537-37e0cd681a14)



The video:
https://drive.google.com/file/d/1713Js1TaLYeCcfYx0-NBSMUOci7Lz_u1/view?usp=sharing
