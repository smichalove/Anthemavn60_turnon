# Anthme60_turnon

uses https://github.com/nugget/python-anthemav/blob/master/example.py
Pulse conversion from constant 12V input
This assumes your Mark Levinson APM is on Standby as start state
Your input to the Mark Levinson Should connect to GPIO21 for + and a GRND
The control Signal from constant high or low should connect to a 12 V relay
the switch signals from the relay to toggle on/off should be connected to GPIO26 and GRND
Radpberry Pico connected to USB on TV
 Pico siglnalling pin connected on GPIO20 pico (GP16) of Pi
uses
https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython
Conntect USB-C of pico to USB on TV
Using Circuit Python on Rasbarry Pico code.py =
GP16 on pico connected to GPIO21 on pi
