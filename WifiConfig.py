from Tkinter import *


filePath = "/etc/wpa_supplicant.conf"

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
            self.SSID = self.textBox.get("1.0",END)[:-1]
            self.destroyWindow()
            self.createWindowTwo()
            self.window = 2
        elif(self.window == 2):
            self.SECURITY_TYPE = self.textBox.get("1.0",END)[:-1]
            self.destroyWindow()
            self.createWindowThree()
            self.window = 3
        elif(self.window == 3):
            self.SECURITY_PASSWORD = self.textBox.get()
            self.destroyWindow()
            #print("SSID: "+self.SSID+", Security Type: "+self.SECURITY_TYPE+", Password: "+self.SECURITY_PASSWORD)
            self.destroy()
            self.master.quit()
            self.saveNetwork(self.SSID,self.SECURITY_TYPE,self.SECURITY_PASSWORD)

    def createWindowOne(self):
        self.label = Label(self, text="Enter SSID:")
        self.label.pack()
        
        self.textBox = Text(self, height=2, width=self.w/2)
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

        self.label = Label(self, text="Enter Secutiry Type:")
        self.label.pack()
        
        self.textBox = Text(self, height=2, width=self.w/2)
        self.textBox.bind("<Return>",self.keyPress)
        self.textBox.pack()


        self.OK = Button(self,text="OK",command=self.button_callback)
        self.OK.pack()
        self.textBox.focus()

    def createWindowThree(self):

        self.label = Label(self, text="Enter WiFi password:")
        self.label.pack()
        
        self.textBox = Entry(self, show="*", width=self.w/2)
        self.textBox.bind("<Return>",self.keyPress)
        self.textBox.pack()

        self.OK = Button(self,text="OK",command=self.button_callback)
        self.OK.pack()
        self.textBox.focus()


    def saveNetwork(self,ssid,keyType,key):
        f = open(filePath,'a')
        string = '\nnetwork={\n	ssid:"'+ssid+'"\n'
        string+= '	key_mgmt='+keyType+'\n'
        string+= '	psk="'+key+'"\n}'

        f.write(string)
        f.close()

def wifi():
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    restart()

def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
