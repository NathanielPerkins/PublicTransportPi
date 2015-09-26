import pygame
from EpochTime import *

class Alarm:
    #daysOfWeek = [{"Day":"Monday","Value":0},{"Day":"Tuesday","Value":1},{"Day":"Wednesday","Value":2},{"Day":"Thursday","Value":3},{"Day":"Friday","Value":4},{"Day":"Saturday","Value":5},{"Day":"Sunday","Value":6}]
    alarmSchedule = []
    
    def __init__(self, filename=None):
        if filename:
            self.Load(filename)
        else:
            self.Load()
        self.alarmOn = False
        #self.currentDay = get_current_time().weekday()
        

    def setAlarm(self,time,day = None):
        if day:
            alarm = {"Day":day,"Time":time}
        else:
            # 7 means all days of week
            alarm = {"Day":7,"Time":time}
        self.alarmSchedule.append(alarm)

    def setAlarmEpoch(self,time):
        self.alarmEpoch = time


    def deleteAlarm(self,index):
        self.alarmScehdule.pop(index)

    
    def checkAlarm(self,currentTime):
        if(len(self.alarmSchedule)>0):
            for alarm in self.alarmSchedule:
                if(currentTime.weekday() == alarm["Day"]):
                    newAlarm = datetime.combine(currentTime.date(),alarm["Time"])
                    if((newAlarm - currentTime).total_seconds()<=0):
                        return 1
        else:
           return -1

        return 0

    def checkAlarmEpoch(self,currentTime):
        if((self.alarmEpoch - currentTime)<=0):
            
            return 1
        else:
            return 0


    def Load(self,filename=None):
        pygame.mixer.init()
        if filename:
            pygame.mixer.music.load(filename)
        else:
            pygame.mixer.music.load("alarmSound.mp3")

    def Play(self):
        if(self.alarmOn == False):
            pygame.mixer.music.play()
            self.alarmOn = True
        

    def Stop(self):
        pygame.mixer.music.stop()
        self.alarmOn = False


