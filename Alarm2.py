import pygame
from EpochTime import *
import RPi.GPIO as GPIO

class Alarm:
    pwmPin = 12
   
    def __init__(self):
        self.Load()
        self.alarmOn = False
        
    def setAlarmEpoch(self,time):
        self.alarmEpoch = time


    def checkAlarmEpoch(self,currentTime):
        if((self.alarmEpoch - currentTime)<=300):
            return 2
        elif((self.alarmEpoch - currentTime)<=600):#number of seconds in 5 minutes
            return 1
        else:
            return 0


    def Load(self):
        GPIO.setup(self.pwmPin,GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwmPin, 1000)

    def Play(self):
        if(self.alarmOn == False):
            self.pwm.start(50)
            self.alarmOn = True
        

    def Stop(self):
        self.pwm.stop()
        self.alarmOn = False


