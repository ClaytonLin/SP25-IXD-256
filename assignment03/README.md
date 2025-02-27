### Introduction

My idea is to create a Chinese lantern, as it was recently Chinese New Year. Typically, people use lanterns during the New Year, but once the celebration ends, they have to wait an entire year before using them again. I want to incorporate this symbolism into my installation, allowing people to experience the slow passage of time and the hardships of life while interacting with it.

### State Diagram

My lantern has three states. At the beginning, it checks if the copper tape is touching. If not, all LEDs will pulsate in RGB green. Once it touches, all lights will turn off, and the LEDs will light up one by one in yellow. If the copper tape stops touching during this process, all LEDs will go back to pulsating in RGB green. When all LEDs are lit in yellow, they will turn red. At this point, even if the copper tape is released, the red light will stay.
<img width="1920" alt="State Diagram" src="https://github.com/user-attachments/assets/d37b1776-1ba0-4dfb-9622-5ce1388e998a" />




