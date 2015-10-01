#Available GPIO's with PiTFT Screen
#GPIO (5,6,12,13,19,16,26,20,21)
#With PWM1 on 23,24 and PWM0 on 26

DEBUG = 1

#from datetime import datetime
from datetime import timedelta, time
import google
import Alarm
from EpochTime import *
import Tkinter
from PIL import Image, ImageDraw, ImageFont, ImageTk

if(DEBUG == 0):
    import PTCGPIO

w = 320
h = 240

buttonMap = [5]
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
    
    def __init__(self, canvas, image, draw):
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
        if(DEBUG == 0):
            PTCGPIO.setup(ledMap,buttonMap)
        self.buttonStates = [False] * len(buttonMap)
        self.clearScreen()
        self.alarm = Alarm.Alarm()
        self.alarm.setAlarmEpoch(google.departure_time_val(self.routes[self.selectedRoute]))


    # Updates clock with current time
    # Blinks colon to indicate time passing
    def updateClockTime(self):
        self.clearHeader()
        if((self.nextBlink - get_current_time()).total_seconds() <= 0):
            timeStr = get_current_time().time().strftime(self.clockFormat)
            self.nextBlink = get_current_time() + self.blinkTime
            if(self.blinkOn):
                self.blinkOn = False
            else:
                 self.blinkOn = True 
        else:
            timeStr = get_current_time().time().strftime(self.clockFormat)

        self.writeText(timeStr,0)
        
        if(not(self.blinkOn)):
            self.draw.rectangle((34,0,40,32), outline=0, fill=0)
        
        
   
        

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
        self.draw.rectangle((0,0,320,32), outline=255, fill=0)


#----------------------------Buttons-------------------------------------------------#
    def checkInputs(self):
        if(DEBUG == 0):
            on = PTCGPIO.buttonCheck(buttonMap)
            self.buttonStates = on

    def resetInputs(self):
        self.buttonStates = [False] * len(buttonMap)

    def checkInput(self, button):
        if(DEBUG == 0):
            on = PTCGPIO.buttonCheck(buttonMap)
            return on[button]




#---------------------------------------------List Display-------------------------------------------------#

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
                self.writeText(string,i+1)
                    
            else:
                step = google.get_step(self.routes[i],transitSteps[0])
                vehicle = google.vehicle_type(step)
                lineName = google.step_transit_details_short_name(step)
                string = vehicle[0] + ":" + lineName
                self.writeText(string,i+1)
            


#----------------------------------Specific Display--------------------------------#


    def fetchIndividual(self):
        return google.routeInfo(self.routes[self.selectedRoute])

    def writeIndividual(self):
        routeInfo = self.fetchIndividual()
        self.clearScreen()
        self.writeText(0,`self.selectedRoute`,x=78)
        self.writeText(1,"ETD:"+routeInfo['DepartureTime'])
        self.scrollableVertical(routeInfo)
        self.writeText(5,"ETA:"+routeInfo['ArrivalTime'])


    def scrollableVertical(self,routeInfo):
        if(routeInfo['NumberSteps']<=3):
            for i in range(routeInfo['NumberSteps']):
                step = routeInfo['Steps'][i] 
                if(step['Type']=='TRANSIT'):
                    string = `i+1`+"|"+step['Vehicle']+":"+step['LineName']
                else:
                    string = `i+1`+"|"+step['Type']+":"+step['Distance']
                self.writeText(string,i+2)
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
                self.writeText(string,lineCounter)
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
        


    def changeSelectedRoute(self,buttonState):
        if(buttonState):
            #Reinitialize scrolling text index on route change
            self.currentStep = 0
            if(self.selectedRoute<google.num_routes(self.routes)-1):
                self.selectedRoute += 1
            else:
                self.selectedRoute = 0
            self.alarm.setAlarmEpoch(google.departure_time_val(self.routes[self.selectedRoute]))
                                 
                
    def drawUI(self):
        split = 240/3
        self.draw.line([0,split,w,split],fill=255)
        self.draw.line([0,31,w,31],fill=255)
        self.draw.line([0,32,w,32],fill=255)
        self.writeText("Next Service:",x=2,y=30,fontSize=18)

    def update(self):
        #self.writeIndividual()
        self.updateClockTime()
        self.drawUI()
        #self.updateList()
        if(self.alarm.checkAlarmEpoch(get_current_epoch_time()) == 1):
            self.alarm.Play()
        
        self.changeSelectedRoute(self.buttonStates[0])
        





    #ToDo: Optimize
    def writeText(self,string,line=None, x=None,y=None, fontSize=None,colour=None):
        # Load default font.
        if(fontSize==None):
            fontSize = 32
        font = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf", fontSize)
        if(colour == None):
            colour = 255
        fontHeight = fontSize
        if(x and y):
            self.draw.text((x,y),string,font=font,fill=colour)
        elif(x):
            self.draw.text((x,(line*fontHeight)), string, font=font, fill=colour)
        else:
            self.draw.text((0,(line*fontHeight)), string, font=font, fill=colour)



#Setup Tkinter GUI
root = Tkinter.Tk()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w,h))
#root.focus_set()

canvas = Tkinter.Canvas(root,width=w,height=h)
canvas.pack()


# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (w, h))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

newUI = UI(canvas,image, draw)

try:
    while 1:
        newUI.checkInputs()
        newUI.update()
        newUI.resetInputs()

        disp = ImageTk.BitmapImage(image)
        canvas.create_image(0,0,image=disp,anchor='nw')



        root.update()

except KeyboardInterrupt:
        if(DEBUG == 0):
            PTCGPIO.GPIO.cleanup()
        newUI.alarm.Stop()
        
