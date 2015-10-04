#Available GPIO's with PiTFT Screen
#GPIO (5,6,12,13,19,16,26,20,21)
#With PWM1 on 23,24 and PWM0 on 26



#from datetime import datetime
from datetime import timedelta, time
import google
import Alarm
from EpochTime import *
from PIL import Image, ImageDraw, ImageFont, ImageTk



fontFilePath = "/usr/share/fonts/truetype/droid/DroidSans.ttf"

w = 320
h = 240

buttonMap = [5]
ledMap = []


class UI:
    DEBUG = 1

    

    #------------Class Variables----------------------#
    origin = []
    destination = []
    selectedRoute = 0
    # The update time between updating routes
    updateTime = timedelta(minutes = 1) #seconds

    #Clock variables
    blinkTime = timedelta(seconds = 1) #Frequency at which clock blinks
    clockFormat = "%I:%M %p" #initialize clock format
    currentStep = 0
    
    verticalScrollTime = timedelta(seconds = 2)




    
    def __init__(self, canvas, image, draw):
        if(self.DEBUG == 0):
            import PTCGPIO
        self.canvas = canvas
        self.image = image
        self.draw = draw

        self.blinkOn = True
        
        self.nextUpdate = get_current_time()
        self.nextBlink = get_current_time() + self.blinkTime
        self.verticalUpdate = get_current_time() +self.verticalScrollTime
        self.origin.append('Surfers Paradise, QLD')
        self.destination.append('Queensland University of Technology')
        self.routes = google.get_directions(self.origin[self.selectedRoute],self.destination[self.selectedRoute],'transit')
        if(self.DEBUG == 0):
            PTCGPIO.setup(ledMap,buttonMap)
        self.buttonStates = [False] * len(buttonMap)
        self.clearScreen()
        self.alarm = Alarm.Alarm()
        self.alarm.setAlarmEpoch(google.departure_time_val(self.routes[self.selectedRoute]))


    # Updates clock with current time
    # Blinks colon to indicate time passing
    def updateClockTime(self):
        self.clearHeader()

        font = self.getFont()

        if((self.nextBlink - get_current_time()).total_seconds() <= 0):
            timeStr = get_current_time().time().strftime(self.clockFormat)
            self.nextBlink = get_current_time() + self.blinkTime
            if(self.blinkOn):
                self.blinkOn = False
            else:
                 self.blinkOn = True 
        else:
            timeStr = get_current_time().time().strftime(self.clockFormat)
        
        self.writeText(timeStr,font,0)
        
        if(not(self.blinkOn)):
            colonX,colonY = font.getsize(timeStr[0:2])
            colonWidth,colonHeight = font.getsize(":")
            self.draw.rectangle((colonX,0,colonX+colonWidth,colonHeight), outline=0, fill=0)
        
        
   
        

    def timeCheck(self,updateTime):
        if((updateTime - get_current_time()).total_seconds() <= 0):
            return True
        else:
            return False

    


#-------------------------------------Clear Functions--------------------------------#

    def clearScreen(self):
         # Draw a white filled box to clear the image.
        self.draw.rectangle((0,0,w,h), outline=0, fill=0)

    def clearHeader(self):
        self.draw.rectangle((0,0,w,32), outline=255, fill=0)

    def clearBody(self):
        self.draw.rectangle((0,32,w,h), outline=255, fill=0)


#----------------------------Buttons-------------------------------------------------#
    def checkInputs(self):
        if(self.DEBUG == 0):
            on = PTCGPIO.buttonCheck(buttonMap)
            self.buttonStates = on

    def resetInputs(self):
        self.buttonStates = [False] * len(buttonMap)

    def checkInput(self, button):
        if(self.DEBUG == 0):
            on = PTCGPIO.buttonCheck(buttonMap)
            return on[button]




#---------------------------------------------List Display-------------------------------------------------#

    def drawList(self):
        font = self.getFont()
        for i in range(google.num_routes(self.routes)):
            numTransfers = google.num_transfers(self.routes[i])
            transitSteps = google.get_transit_steps(self.routes[i])
            if(numTransfers >1):
                step = google.get_step(self.routes[i],transitSteps[0])
                vehicle = google.vehicle_type(step)
                lineName = google.step_transit_details_short_name(step)
                string = vehicle[0] + ":" + lineName
                for j in range(1,numTransfers):
                    step = google.get_step(self.routes[i],transitSteps[j])
                    vehicle = google.vehicle_type(step)
                    lineName = google.step_transit_details_short_name(step)
                    string += ">" + vehicle[0] + ":" + lineName
                self.writeText(string,font,i+1)
                    
            else:
                step = google.get_step(self.routes[i],transitSteps[0])
                vehicle = google.vehicle_type(step)
                lineName = google.step_transit_details_short_name(step)
                string = vehicle[0] + ":" + lineName
                self.writeText(string,font,i+1)
            
    def changeSelectedRoute(self,buttonState):
        if(buttonState):
            #Reinitialize scrolling text index on route change
            self.currentStep = 0
            if(self.selectedRoute<google.num_routes(self.routes)-1):
                self.selectedRoute += 1
            else:
                self.selectedRoute = 0
            self.alarm.setAlarmEpoch(google.departure_time_val(self.routes[self.selectedRoute]))
                                 
     

#----------------------------------Specific Display--------------------------------#


    def fetchIndividual(self):
        return google.routeInfo(self.routes[self.selectedRoute])

    def writeIndividual(self):
        routeInfo = self.fetchIndividual()
        self.clearBody()
        string =""
        times = routeInfo['DepartureTime']+"-"+routeInfo['ArrivalTime']
        duration = routeInfo['DurationTime']
        font = self.getFont(14)
        self.writeText(times,font,x=1,y=34)
        strWidth,strHeight = font.getsize(duration)
        self.writeText(duration,font,x=(w-strWidth),y=34)
        for i in range(routeInfo['NumberSteps']):
                step = routeInfo['Steps'][i] 
                if(step['Type']=='TRANSIT'):
                    string+=step['Vehicle']+":"+step['LineName']+" -> "
        string = string[:-4]
        self.writeText(string,font,x=1,y=60)

        
                
    def drawUI(self):
        #Clock Divider
        self.draw.line([0,31,w,31],fill=255)
        self.draw.line([0,32,w,32],fill=255)
        #Section 1 (below header/clock)
        split = 240/3
        self.writeIndividual()
        self.draw.line([0,split,w,split],fill=255)

        

    def update(self):
        #self.writeIndividual()
        self.updateClockTime()
        self.drawUI()
        #self.updateList()
        if(self.alarm.checkAlarmEpoch(get_current_epoch_time()) == 1):
            self.alarm.Play()
        
        self.changeSelectedRoute(self.buttonStates[0])
        

    def getFont(self,fontSize=None):
        if(fontSize):
            font = ImageFont.truetype(fontFilePath,fontSize)
        else:
            font = ImageFont.truetype(fontFilePath,32)
        return font
        

    #ToDo: Optimize
    def writeText(self,string,font,line=None, x=None,y=None,colour=None):
        # Load default font.
        if(colour == None):
            colour = 255
        fontDimensions = font.getsize(string)
        if(x>=0 and y>=0):
            self.draw.text((x,y),string,font=font,fill=colour)
        elif(x>=0):
            self.draw.text((x,(line*fontDimensions[1])), string, font=font, fill=colour)
        else:
            self.draw.text((0,(line*fontDimensions[1])), string, font=font, fill=colour)


