import Tkinter
from GUIScreen import *

w = 320
h = 240

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
        if(newUI.DEBUG == 0):
            PTCGPIO.GPIO.cleanup()
        newUI.alarm.Stop()
        
