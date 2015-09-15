import time

from datetime import datetime
from datetime import timedelta
import google
import PTCGPIO

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI


from EpochTime import *

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont



buttonMap = [21]
ledMap = []


class UI:

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
    
    def __init__(self, disp, draw):
        self.disp = disp
        self.draw = draw
        self.nextUpdate = get_current_time()
        self.nextBlink = get_current_time() + self.blinkTime
        self.verticalUpdate = get_current_time() +self.verticalScrollTime
        self.origin.append('Surfers Paradise, QLD')
        self.destination.append('Queensland University of Technology')
        self.routes = google.get_directions(self.origin[self.selectedRoute],self.destination[self.selectedRoute],'transit')
        PTCGPIO.setup(ledMap,buttonMap)
        self.buttonStates = [False] * len(buttonMap)
        self.clearScreen()


    # Updates clock with current time
    # Blinks colon to indicate time passing
    def updateClockTime(self):
        self.clearHeader()
        if((self.nextBlink - get_current_time()).total_seconds() <= 0):
            timeStr = get_current_time().time().strftime(self.clockFormat)
            self.nextBlink = get_current_time() + self.blinkTime
            if(self.clockFormat == "%I:%M %p"):
                self.clockFormat = "%I %M %p"
            else:
                 self.clockFormat = "%I:%M %p"
        else:
            timeStr = get_current_time().time().strftime(self.clockFormat)
            
        writeText(0, timeStr)



    def timeCheck(self,updateTime):
        if((updateTime - get_current_time()).total_seconds() <= 0):
            return True
        else:
            return False

    
    def updateList(self):
        if(timeCheck(self.nextUpdate)):
            self.routes = google.get_directions(self.route[self.selectedRoute],self.destination[self.selectedRoute],'transit')
            self.nextUpdate = get_current_time() + self.updateTime
            self.clearScreen()
            self.drawList()


    def drawList(self):
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
                writeText(i+1,string)
                    
            else:
                step = google.get_step(self.routes[i],transitSteps[0])
                vehicle = google.vehicle_type(step)
                lineName = google.step_transit_details_short_name(step)
                string = vehicle[0] + ":" + lineName
                writeText(i+1,string)
            
    def drawIndividual(self):
        self.clearScreen()
        writeText(0,`self.selectedRoute`,offset=13)
        departureTime = google.departure_time_str(self.routes[self.selectedRoute])
        writeText(1,"ETD:"+departureTime)
        counter = 0
        for step in google.get_steps(self.routes[self.selectedRoute]):
            if(google.travel_type(step)=='TRANSIT'):
                vehicle = google.vehicle_type(step)
                lineName = google.step_transit_details_short_name(step)
                string = vehicle + ":" + lineName
            else:#travel type is walking
                string = "Walk:"+google.step_walking_distance_str(step)
            writeText(counter+2,string,offset=2)
            counter +=1

        arrivalTime = google.arrival_time_str(self.routes[self.selectedRoute])
        writeText(5,"ETA:"+arrivalTime)

    def fetchIndividual(self):
        return google.routeInfo(self.routes[self.selectedRoute])

    def writeIndividual(self):
        routeInfo = self.fetchIndividual()
        self.clearScreen()
        writeText(0,`self.selectedRoute`,x=78)
        writeText(1,"ETD:"+routeInfo['DepartureTime'])
        self.scrollableVertical(routeInfo)
        writeText(5,"ETA:"+routeInfo['ArrivalTime'])


    def scrollableVertical(self,routeInfo):
        if(routeInfo['NumberSteps']<=3):
            for i in range(routeInfo['NumberSteps']):
                step = routeInfo['Steps'][i] 
                if(step['Type']=='TRANSIT'):
                    string = `i+1`+"|"+step['Vehicle']+":"+step['LineName']
                else:
                    string = `i+1`+"|"+step['Type']+":"+step['Distance']
                writeText(i+2,string)
        else:
            if(self.timeCheck(self.verticalUpdate)):
                if(self.currentStep<routeInfo['NumberSteps']-1):
                    self.currentStep += 1
                else:
                    self.currentStep = 0
                self.verticalUpdate = get_current_time() + self.verticalScrollTime

            lineCounter = 2
            for i in self.scrollIndexRange(routeInfo['NumberSteps'],self.currentStep):
                #print("Current Step: "+`self.currentStep`)
                #print(self.scrollIndexRange(routeInfo['NumberSteps'],self.currentStep))
                step = routeInfo['Steps'][i] 
                if(step['Type']=='TRANSIT'):
                    string = `i+1`+"|"+step['Vehicle']+":"+step['LineName']
                else:
                    string = `i+1`+"|"+step['Type']+":"+step['Distance']
                writeText(lineCounter,string)
                lineCounter +=1
            lineCounter = 2

    def scrollIndexRange(self,numSteps,chosenStep):
        definedRange = [chosenStep]
        if(chosenStep+1>=numSteps):
            definedRange += range(2)
        elif(chosenStep+2>=numSteps):
            definedRange += [chosenStep+1,0]
        else:
            definedRange = range(chosenStep,chosenStep+3)
        return definedRange
        
            

    def update(self):
        self.writeIndividual()
        self.updateClockTime()
        
        #self.updateList()
        if(self.buttonStates[0]):
            #Reinitialize scrolling text index on route change
            self.currentStep = 0
            if(self.selectedRoute<google.num_routes(self.routes)-1):
                self.selectedRoute += 1
            else:
                self.selectedRoute = 0

        self.disp.image(image)
        self.disp.display()

    def clearScreen(self):
         # Draw a white filled box to clear the image.
        self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

    def clearHeader(self):
        self.draw.rectangle((0,0,9*5,7), outline=255, fill=255)


        
    def checkInputs(self):
        on = PTCGPIO.buttonCheck(buttonMap)
        self.buttonStates = on

    def resetInputs(self):
        self.buttonStates = [False] * len(buttonMap)

    def checkInput(self, button):
        on = PTCGPIO.buttonCheck(buttonMap)
        return on[button]


#ToDo: Optimize
def writeText(line, string, offset=None, x=None):
    # Load default font.
    font = ImageFont.load_default()

    maxLines = 5
    maxChars = 14

    if(line<=maxLines):
        if(offset):
            if(len(string)+offset<=maxChars):
                draw.text(((offset*5),(line*8)-2), string, font=font)
            else:
                draw.text(((offset*5),(line*8)-2), "Error Fit", font=font)
        else:
            if(x):
                if(len(string)<=maxChars):
                    draw.text((x,(line*8)-2), string, font=font)
                else:
                    draw.text((x,(line*8)-2), "Error Fit", font=font)
            else:
                if(len(string)<=maxChars):
                    draw.text((0,(line*8)-2), string, font=font)
                else:
                    draw.text((0,(line*8)-2), "Error Fit", font=font)




# Raspberry Pi software SPI config:
SCLK = 4
DIN = 17
DC = 23
RST = 24
CS = 8

# Software SPI usage (defaults to bit-bang SPI interface):
disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Initialize library.
disp.begin(contrast=60)

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

newUI = UI(disp, draw)

while 1:
    newUI.checkInputs()
    newUI.update()
    newUI.resetInputs()
    
    
