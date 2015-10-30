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
fontFilePath2 = "/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf"
settingsFilePath = "settings.conf"

w = 320
h = 240

buttonMap = [5]
ledMap = []


class UI:
    DEBUG = 1

    

    #------------Class Variables----------------------#
    destination = []
    routes = []
    selectedRoute = 0
    # The update time between updating routes
    updateTime = timedelta(minutes = 1) #minutes

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
        
        self.nextUpdate = get_current_time() + self.updateTime
        self.nextBlink = get_current_time() + self.blinkTime
        self.verticalUpdate = get_current_time() +self.verticalScrollTime
        self.saveInformation()
        self.getRoutes()
        #self.routes = google.get_directions(self.origin[0],self.destination[self.selectedRoute],'transit')
        if(self.DEBUG == 0):
            PTCGPIO.setup(ledMap,buttonMap)
        self.buttonStates = [False] * len(buttonMap)
        self.clearScreen()
        self.alarm = Alarm.Alarm()
        self.alarm.setAlarmEpoch(google.departure_time_val(self.routes[self.selectedRoute]))

        
    def getRoutes(self):
        self.routes = []
        self.routes.append(google.get_directions(self.origin,self.destination[self.selectedRoute],'transit',self.arrivalTime)[0])
        self.routes += google.get_directions(self.origin,self.destination[self.selectedRoute],'transit')


    def updateAlarm(self,time):
        if(type(time)==str):
            date = get_current_utc_time().date()
            day = date.day
            month = date.month
            year = date.year
           
            hour = int(time.split(":",1)[0])
            minute = int(time.split(":",1)[1])
            return get_epoch_time(day,month,year,hour,minute)
        elif(type(time)==datetime):
            date = get_current_utc_time().date()
            day = date.day
            month = date.month
            year = date.year
           
            hour = time.hour
            minute = time.minute
            return get_epoch_time(day,month,year,hour,minute)
           
        
    def saveInformation(self):
        self.origin = self.readInformation(1)
        self.destination.append(self.readInformation(2))

        date = get_current_time().date()
        day = date.day
        month = date.month
        year = date.year
        time = self.readInformation(3)
        hour = int(time.split(":",1)[0])
        minute = int(time.split(":",1)[1])
        self.arrivalTime = get_epoch_time(day,month,year,hour,minute)

    
    def readInformation(self,infoType):
        f = open(settingsFilePath,'r')
        i = 1
        for line in f:
            if(i == infoType):
               return line.split(":",1)[1]
            i += 1
        f.close()

        
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
        list_num = 3
        starting_y = (2*h)/5
        blockHeight = (h-starting_y)/(list_num)
        font = self.getFont(14)
        #fontBold = self.getFont(14,bold=True)
        fontWidth,fontHeight = font.getsize("H|")
        line_x = 20
        line_x2 = 5
        current_y = starting_y
        for i in range(1,list_num+1):
            if(i<len(self.routes)):
                padding = (blockHeight + fontHeight)/2
                routeInfo = self.fetchIndividual(i)

                string1 = "Option "+`i`+":"
                x,y = self.writeText(string1,font,x=line_x2,y=current_y+5)
                line_x2 += x
                
                string1 = "  ("+`routeInfo['Transfers']`+ " Transfers)"
                self.writeText(string1,font,x=line_x2,y=current_y+5)

                string2 = routeInfo['DepartureTime']+"-"+routeInfo['ArrivalTime']+" | "
                x,y = self.writeText(string2,font,x=line_x,y=current_y+padding-5)
                line_x += x

                x,y = self.drawImage(routeInfo['FirstTrip']['Vehicle'],(line_x,current_y+padding-5),y)
                line_x += x+5

                string2 = routeInfo['FirstTrip']['LineName']+" | "
                x,y = self.writeText(string2,font,x=line_x,y=current_y+padding-5)
                line_x += x

                string2 = routeInfo['DurationTime']
                x,y = self.writeText(string2,font,x=line_x,y=current_y+padding-5)
                line_x += x
                
                current_y += blockHeight
                self.draw.line([0,current_y,w,current_y],fill=255)

                line_x = 20
                line_x2 = 5
                
            
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


    def fetchIndividual(self,routeIndex):
        return google.routeInfo(self.routes[routeIndex])

    def writeIndividual(self):
        line1_y = 34 
        routeInfo = self.fetchIndividual(0)
        self.clearBody()
        string = ""
        times = routeInfo['DepartureTime']+"-"+routeInfo['ArrivalTime']
        duration = routeInfo['DurationTime']
        transfers = " Transfers: " + `routeInfo['Transfers']`
        font = self.getFont(14)

       
        
        self.writeText(times,font,x=1,y=line1_y)
        strWidth,strHeight = font.getsize(duration)

        line2_y = line1_y + strHeight + 10

        self.writeText(duration,font,x=(w-strWidth),y=line1_y)
        
        transfersX,transfersY = font.getsize(transfers)

        line3_y = line2_y+transfersY +5
        
        self.writeText(transfers,font,x=0,y=line2_y)

        lineLength = 25 #starting position

        self.write_transfers(routeInfo,(lineLength,line3_y),font)

    def write_transfers(self,routeInfo,startingLocation,font):
        #Capital 'H' hits high, '|' hits low. Maximizing height
        lineWidth,lineHeight = font.getsize("H|") 
        pixelSpacing = 0
        nextTransferSymbol = " > "
        lineLength = startingLocation[0]

        
        for i in range(routeInfo['NumberSteps']):
            if(i == routeInfo['NumberSteps']-1):
                nextTransferSymbol = ""
            step = routeInfo['Steps'][i] 
            if(step['Type']=='TRANSIT'):
                x,y = self.drawImage(step['Vehicle'],(lineLength,startingLocation[1]),lineHeight)
                lineLength += x + 5
                string = step['LineName']+nextTransferSymbol
                x,y = self.writeText(string,font,x=lineLength,y=startingLocation[1])
                lineLength += x
            else: #is walking
                x,y = self.drawImage(step['Type'],(lineLength,startingLocation[1]),lineHeight)
                lineLength += x + pixelSpacing
                x,y = self.writeText(nextTransferSymbol,font,x=lineLength,y=startingLocation[1])
                lineLength += x
        
        
                
    def drawUI(self):
        #Clock Divider
        self.draw.line([0,31,w,31],fill=255)
        self.draw.line([0,32,w,32],fill=255)
        #Section 1 (below header/clock)
        split = (2*h)/5
        self.writeIndividual()
        self.draw.line([0,split,w,split],fill=255)
        self.draw.line([0,split+1,w,split+1],fill=255)

        self.drawList()

        

    def drawImage(self,image,location,height):
        if(image == "Train"):
            im = Image.open("rail.png")
        elif(image == "Walk"):
            im = Image.open("walk.png")
        elif(image == "Bus"):
            im = Image.open("bus.png")
        elif(image == "Tram"):
            im = Image.open("tram.png")
        else:
            return -1
        
        iwidth,iheight = im.size
        aspectRatio = iwidth/iheight
        im = im.resize((height*aspectRatio,height), Image.NEAREST)
        self.draw.bitmap(location,im,fill=255)
        return im.size

    def update(self):
        #self.writeIndividual()
        self.updateClockTime()
        self.drawUI()
        #self.updateList()
        checkedAlarm = self.alarm.checkAlarmEpoch(get_current_epoch_time())
        if(checkedAlarm == 1):
            #Make LED's RED
            self.alarm.Play()
        elif(checkedAlarm == 2):
            #Make LED's Yellow
            self.alarm.Play() #Placeholder
        else:
            #LED's Green
            self.alarm.Stop() #placeholder

        if(self.timeCheck(self.nextUpdate)):
            self.nextUpdate = get_current_time() + self.updateTime
            self.getRoutes()
            print("Updated")
            
        self.changeSelectedRoute(self.buttonStates[0])
        

    def getFont(self,fontSize=None,bold=None):
        if(fontSize==None):
            fontSize = 32
        if(bold):
            filePath = fontFilePath2
        else:
            filePath = fontFilePath
            
        font = ImageFont.truetype(filePath,fontSize)
        
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

        return fontDimensions

