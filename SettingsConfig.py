from Tkinter import *


filePath = "/home/pi/PublicTransportPi/settings.conf"

class Application(Frame):


    def __init__(self, master=None):
        master.attributes('-fullscreen', True)
        self.w,self.h = 320,240
        self.master = master
        Frame.__init__(self, master)

        self.pack()
        self.createWindowOne()
        self.window = 1


    def keyPress(self,event):
        self.button_callback()

    def button_callback(self):
        if(self.window == 1):
            self.Departure = self.textBox.get("1.0",END)[:-1]
            self.saveInformation(2,self.Departure)
            self.destroyWindow()
            self.createWindowTwo()
            self.window = 2
        elif(self.window == 2):
            self.Destination = self.textBox.get("1.0",END)[:-1]
            self.saveInformation(3,self.Destination)
            self.destroyWindow()
            self.createWindowThree()
            self.window = 3
        elif(self.window == 3):
            self.Alarm = self.textBox.get("1.0",END)[:-1]
            self.saveInformation(1,self.Alarm)
            self.destroyWindow()
            self.destroy()
            self.master.quit()
            
    def createWindowOne(self):
        self.label = Label(self, text="Enter Departure Address:")
        self.label.pack()
        
        self.textBox = Text(self, height=2, width=self.w/2)
        self.textBox.insert(INSERT,self.readInformation(2)[:-1])
        self.textBox.bind("<Return>",self.keyPress)
        self.textBox.pack()


        self.OK = Button(self,text="OK",command=self.button_callback)
        self.OK.pack()
        self.textBox.focus()
        #self.OK.pack({"side": "left"})

    def destroyWindow(self):
        self.label.destroy()
        self.textBox.destroy()
        self.OK.destroy()

    def createWindowTwo(self):

        self.label = Label(self, text="Enter Destination Address:")
        self.label.pack()
        
        self.textBox = Text(self, height=8, width=self.w/2)
        self.textBox.insert(INSERT,self.readInformation(3)[:-1])
        self.textBox.bind("<Return>",self.keyPress)
        self.textBox.pack()


        self.OK = Button(self,text="OK",command=self.button_callback)
        self.OK.pack()
        self.textBox.focus()

    def createWindowThree(self):

        self.label = Label(self, text="Enter an Alarm Time:")
        self.label.pack()
        
        self.textBox = Text(self, height=2, width=self.w/2)
        self.textBox.insert(INSERT,self.readInformation(1)[:-1])
        self.textBox.bind("<Return>",self.keyPress)
        self.textBox.pack()


        self.OK = Button(self,text="OK",command=self.button_callback)
        self.OK.pack()
        self.textBox.focus()


    def readInformation(self,infoType):
        f = open(filePath,'r')
        i = 1
        for line in f:
            if(i == infoType):
               return line.split(":",1)[1]
            i += 1
        f.close()
        
    def saveInformation(self,infoType,info):
        string = ''
        with open(filePath,'r') as file:
            data = file.readlines()
        file.close()
        
        if(infoType == 1):
            #Write alarm to third line fo file
            string = 'Alarm:'+info+'\n'
            data[0] = string

        if(infoType == 2):
            #Write address to first line of file
            string = 'Departure:'+info+'\n'
            data[1]= string

        if(infoType == 3):
            #Write destination address to second line of file
            string = 'Destination:'+info+'\n'
            data[2] = string



        with open(filePath, 'w') as file:
            file.writelines(data)
        file.close()

def Open():
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    return root

