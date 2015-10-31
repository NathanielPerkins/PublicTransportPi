import Tkinter
import WifiConfig
import SettingsConfig
from GUIScreen import *

w = 320
h = 240

SKIP_CHECK = 0
SKIP_SETTINGS = 0

if(SKIP_CHECK == 0):
    connection = google.get_directions("Brisbane","Gold Coast",'transit')

    while(connection == 0):
        #Error if not connected to net
        connection = google.get_directions("Brisbane","Gold Coast",'transit')
        if(connection == 0):
            WifiConfig.wifi()

if(SKIP_SETTINGS == 0):
    root = SettingsConfig.Open()
else:
    root = Tkinter.Tk()

#Setup Tkinter GUI
#root = Tkinter.Tk()

#Final Layout    
root.attributes('-fullscreen', True)

#Testing Layout
root.overrideredirect(1)
#root.geometry("%dx%d+0+0" % (w,h))
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
        if(newUI.DEBUG == 0):
            PTCGPIO.GPIO.cleanup()
        newUI.alarm.Stop()
        
