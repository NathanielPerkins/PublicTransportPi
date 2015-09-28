import Tkinter
from PIL import ImageTk, Image, ImageDraw

root = Tkinter.Tk()
w, h  = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w,h))
root.focus_set()
root.bind("<Escape>", lambda e: root.destroy())


image = Image.new('1', (w, h))

canvas = Tkinter.Canvas(root,width=w,height=h)
canvas.pack()


draw = ImageDraw.Draw(image)

draw.rectangle([0,0,50,50],fill=128)


disp = ImageTk.BitmapImage(image)
canvas.create_image(w,h,image=disp)

root.mainloop()
