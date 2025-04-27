import os, sys, io
import M5
from M5 import *
from hardware import I2C, Pin, ADC
from neopixel import NeoPixel
from time import sleep_ms
from machine import PWM
import network
from umqtt import MQTTClient
from unit import GestureUnit
import uos
import select

ssid = 'name'
password = 'password'
aio_user_name = 'name'
aio_password = 'password'

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)
print('Connecting to WiFi...')
while not wifi.isconnected():
    print('.', end='')
    sleep_ms(100)
print('\nWiFi connected!')

mqtt_client = MQTTClient(
    'client-' + aio_user_name,
    'io.adafruit.com',
    port=1883,
    user=aio_user_name,
    password=aio_password,
    keepalive=60
)
mqtt_client.connect()

M5.begin()

adc = ADC(Pin(6))
adc.atten(ADC.ATTN_11DB)

np = NeoPixel(Pin(7), 30)

servo = PWM(Pin(38), freq=50)

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
gesture_sensor = GestureUnit(i2c)
gesture_sensor.set_gesture_highrate(True)

def set_servo_speed(speed_percent):
    duty_stop = 77
    duty_max = 100
    duty = duty_stop + int((duty_max - duty_stop) * (speed_percent / 100))
    servo.duty(duty)

def interpolate_color(ir_val):
    ir_val = max(0, min(ir_val, 2400))
    green_strength = int(255 * (1 - ir_val / 2400))
    return (255 - green_strength, 255, 255 - green_strength)

def set_leds(color):
    for i in range(30):
        np[i] = color
    np.write()

def scifi_effect():
    for i in range(30):
        np[i] = (0, 255, 255)  # cyan
    np.write()

def rnb_effect():
    for i in range(30):
        np[i] = (255, 20, 147)  # deep pink
    np.write()

def rap_effect():
    for i in range(30):
        np[i] = (255, 215, 0)  # gold
    np.write()

def piano_effect():
    for i in range(30):
        np[i] = (255, 255, 255)  # white
    np.write()

welcome_sent = False
green_enabled = False
last_state = None
gesture_timer = 0

left_count = 0
right_count = 0

pause_printed = False

current_breathing_color = None
breathing_mode = False
breathing_brightness = 0
breathing_direction = 1
breathing_step = 3

special_effect_mode = False
special_effect_name = ""

while True:
    M5.update()
    ir_val = adc.read()

    list = select.select([sys.stdin], [], [], 0)
    if list[0]:
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

    if special_effect_mode:
        mqtt_client.check_msg()
        sleep_ms(50)
        gesture_timer += 50
        continue

    if ir_val < 1000:
        if not pause_printed:
            print("pause")
            pause_printed = True
    else:
        pause_printed = False

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

    if right_count == 1:
        current_breathing_color = (255, 255, 0)
        breathing_mode = True
    elif right_count == 2:
        current_breathing_color = (255, 0, 0)
        breathing_mode = True
    elif right_count == 3:
        current_breathing_color = (0, 255, 0)
        breathing_mode = True
    elif right_count == 4:
        set_leds((255, 255, 0))
        breathing_mode = False
        current_breathing_color = None
    else:
        breathing_mode = False
        current_breathing_color = None

    if breathing_mode and current_breathing_color:
        breathing_brightness += breathing_direction * breathing_step
        if breathing_brightness >= 255:
            breathing_brightness = 255
            breathing_direction = -1
        if breathing_brightness <= 0:
            breathing_brightness = 0
            breathing_direction = 1
        scaled_color = tuple(int(c * breathing_brightness / 255) for c in current_breathing_color)
        set_leds(scaled_color)

    if not breathing_mode:
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

        if current_state != last_state:
            if current_state == "green" and green_enabled:
                print("green")
            elif current_state == "default":
                print("default")
            last_state = current_state

    mqtt_client.check_msg()
    sleep_ms(50)
    gesture_timer += 50
