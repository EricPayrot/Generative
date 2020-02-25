import tkinter, glob, random
from PIL import Image, ImageTk, ImageOps
import numpy as np
from tkcolorpicker import askcolor

im = Image.open(r"C:\Users\100004614\python\project1\pics color2\Untitled-3.png")
im = im.convert('RGBA')

data = np.array(im)   # "data" is a height x width x 4 numpy array

""" red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

# Replace white with red... (leaves alpha values alone...)
green_areas = (red < 100) & (blue < 100) & (green > 20)
data[..., :-1][green_areas.T] = (255, 255, 0) # Transpose back needed """

im2 = Image.fromarray(data,'RGBA')

def replace_color(color):
    global TK_img2
    r1, g1, b1, a1 = color
    new_color=askcolor(color=color, parent=None, title="Color Chooser", alpha=True)
    print('new_color ',new_color,'color ',color)
    new_color=new_color[0]
    print("new color after",new_color)
    r2, g2, b2, a2 = new_color # Value that we want to replace it with
    red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:,:,:4][mask] = [r2, g2, b2, a2]
    im2 = Image.fromarray(data,'RGBA')
    TK_img2 = ImageTk.PhotoImage(im2)
    myCanvas.itemconfig(TKitem2,image=TK_img2)

def button1(event):
    global picker_color
    picker_x = event.x
    picker_y = event.y
    picker_color = data[picker_x,picker_y]
    print('pixel value',picker_color, picker_color.size)
    replace_color(picker_color)

#init tk ----------------------------------------------------------
root = tkinter.Tk()
myCanvas = tkinter.Canvas(root, bg="white", height=300, width=650)
myCanvas.old_coords = None
picker_color = None

myCanvas.bind('<Button-1>',button1)
# Bindings --------------------------------------------------------
""" root.bind('<Up>',up)
root.bind('<Down>',down)
myCanvas.bind('<Button-1>',button1)
myCanvas.bind('<B1-Motion>',b1motion)
myCanvas.bind('<Button-3>',button3) """

# main ---------------------------------------------
TK_img = ImageTk.PhotoImage(im)
TK_img2 = ImageTk.PhotoImage(im2)
TKitem1 = myCanvas.create_image([0,0],image=TK_img, anchor='nw') 
TKitem2 = myCanvas.create_image([350,0],image=TK_img2, anchor='nw') 

myCanvas.pack()
root.mainloop()