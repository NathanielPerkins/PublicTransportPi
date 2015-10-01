import Tkinter
from PIL import ImageTk, Image, ImageDraw, ImageFont
import time

root = Tkinter.Tk()
w = 320
h = 240

#w, h  = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w,h))
root.focus_set()



image = Image.new('1', (w, h))

canvas = Tkinter.Canvas(root,width=w,height=h)
canvas.pack()

draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

i = 0;
while 1:
    draw.point([i,11],fill=255)
    draw.point([i,10],fill=255)
    draw.point([i-1,10],fill=255)
    draw.point([i-1,11],fill=255)

    draw.text((50,50),"Hello World", font=font, fill=255)

    disp = ImageTk.BitmapImage(image)
    canvas.create_image(0,0,image=disp,anchor='nw')
    root.update()
    i+=1
    if(i>320):
        i=0
    #time.sleep(0.01)
    
    draw.rectangle((0,0,w,h), outline=255, fill=0)
