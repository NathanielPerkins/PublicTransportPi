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
            on.append(True)
        else:
            on.append(False)
    return on

""""
ledMap = [21,20,16]
buttonMap = [26,19,13,6]
setup(ledMap,buttonMap)

on = buttonCheck(buttonMap)
GPIO.setup(12,GPIO.OUT)
pwm = GPIO.PWM(12, 1000)

while True:
    on = buttonCheck(buttonMap)
    
    GPIO.output(ledMap[0],True)
    GPIO.output(ledMap[1],False)
    GPIO.output(ledMap[2],False)
    
    if(not on[0]):
        GPIO.output(ledMap[1],True)
    if(not on[1]):
        GPIO.output(ledMap[2],True)
    if(not on[2]):
        pwm.start(50)
    if(not on[3]):
        pwm.stop()
""""