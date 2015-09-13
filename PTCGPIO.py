import RPi.GPIO as GPIO
from time import sleep

def setup(ledMap,buttonMap):
    GPIO.setmode(GPIO.BCM)
    for x in ledMap:
        GPIO.setup(x,GPIO.OUT)
    for x in buttonMap:
        GPIO.setup(x,GPIO.IN)

def buttonCheck(buttonMap):
    on = []
    for x in buttonMap:
        if GPIO.input(x):
            on.append(1)
        else:
            on.append(0)
    return on
        
ledMap = []
buttonMap = [12,14]
setup(ledMap,buttonMap)

"""
print buttonCheck(buttonMap)
while True:
    on = buttonCheck(buttonMap)
    if on[0] == 1:
        print "DICKS"
    if on[1] == 1:
        print "BALLS"
    sleep(0.5)

while True:
    if GPIO.input(14):
        GPIO.output(12,True)
    if not GPIO.input(14):
        GPIO.output(12,False)
   """ 
