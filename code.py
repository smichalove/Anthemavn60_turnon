#boot file code.py on Raspberry pico
import time
import board
import digitalio

led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
