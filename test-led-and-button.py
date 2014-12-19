import RPi.GPIO as GPIO
import time  

GPIO.setmode(GPIO.BCM)

SWITCH1 = 23
GPIO.setup(SWITCH1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

LED = 18
GPIO.setup(LED, GPIO.OUT)

def printFunction(channel):
    print(“Button 1 pressed!”)
    #print(“Note how the bouncetime affects the button press”)
    GPIO.output(LED, not GPIO.input(LED))

GPIO.add_event_detect(SWITCH1, GPIO.RISING, callback=printFunction, bouncetime=300)

print("Here we go! Press CTRL+C to exit")
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
