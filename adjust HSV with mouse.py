# ne fonctionne pas car il n'y a qu'une variable color picker et quand on passe du rouge au vert il part de la valeur précédente

import tkinter, glob, random, math
from PIL import Image, ImageTk, ImageOps
import numpy as np
from tkcolorpicker import askcolor

im = Image.open(r"C:\Users\100004614\python\project1\pics color2\Untitled-3.png")
im = im.convert('RGBA')

orig_data = np.array(im)   # "data" is a height x width x 4 numpy array
data = orig_data
print('orig data at 164 245 : ',orig_data[164,245])
print('orig data at 215 196 : ',orig_data[164,245])

im2 = Image.fromarray(data,'RGBA')

def replace_color(old_color,new_color):
    global TK_img2, data
    r1, g1, b1, a1 = old_color
    if new_color == None:
        new_color=askcolor(color='red', parent=None, title="Color Chooser", alpha=True)
        new_color=int(new_color[0]) # keep the RGB tuple, remove the Hex color code
    print('new_color ',new_color,'old color ',old_color)
    r2, g2, b2, a2 = new_color # Value that we want to replace it with
    print('r2',r2,'g2',g2,'b2',b2,'a2',a2)
    red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:,:,:4][mask] = [r2, g2, b2, a2]
    im2 = Image.fromarray(data,'RGBA')
    TK_img2 = ImageTk.PhotoImage(im2)
    myCanvas.itemconfig(TKitem2,image=TK_img2)

def button1(event):
    global picker_color, hsv_color
    global im
    picker_x = event.x
    picker_y = event.y
    picker_color = list(im2.getpixel((picker_x,picker_y)))
    #hsv_color=list(rgb_to_hsv(picker_color[0],picker_color[1],picker_color[2],picker_color[3]))
 
def rgb_to_hsv(r, g, b, a):
    r = float(r)
    g = float(g)
    b = float(b)
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, v = high, high, high

    d = high - low
    s = 0 if high == 0 else d/high

    if high == low:
        h = 0.0
    else:
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6

    return h, s, v, a

def hsv_to_rgb(h, s, v, a):
    i = math.floor(h*6)
    f = h*6 - i
    p = v * (1-s)
    q = v * (1-f*s)
    t = v * (1-(1-f)*s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i%6)]
    return r, g, b, a

def change_hue(event,new_color):
    new_HSV_color = rgb_to_hsv(new_color)
    new_hue = h+10
    new_color = hsv_to_rgb(new_hue)

def button3(event):
    global picker_color
    picker_x = event.x
    picker_y = event.y
    picker_color = data[picker_x,picker_y]
    new_color=[0, 0, 0, 255]
    replace_color(picker_color,new_color)


def b1motion(event):
    global picker_color
    global hsv_color
    x = event.x
    y = event.y
    hsv_color=list(rgb_to_hsv(picker_color[0],picker_color[1],picker_color[2],picker_color[3]))
    if myCanvas.old_coords:
        x1, y1 = myCanvas.old_coords
        hsv_color[2]=hsv_color[2]+(y1-y)  
    if hsv_color[2]<0:
        hsv_color[2]=0
    if hsv_color[2]>255:
        hsv_color[2]=255
    myCanvas.old_coords = x, y
    #print('value after ',hsv_color[2], 'y1 ', y1, 'y', y)
    print('old coords',myCanvas.old_coords)
    new_color=list(hsv_to_rgb(hsv_color[0],hsv_color[1],hsv_color[2],hsv_color[3]))
    new_color=list(map(int,new_color))
    print('pick ', picker_color,'new ',new_color)
    replace_color(picker_color,new_color)
    
#init tk ----------------------------------------------------------
root = tkinter.Tk()
myCanvas = tkinter.Canvas(root, bg="white", height=300, width=650)
myCanvas.old_coords = None
picker_color = None
hsv_color = (0,0,0,0)

# Bindings --------------------------------------------------------

myCanvas.bind('<Button-1>',button1)
myCanvas.bind('<B1-Motion>',b1motion)
#root.bind('<up>',up)
#root.bind('<down',down)

# main ---------------------------------------------
TK_img = ImageTk.PhotoImage(im)
TK_img2 = ImageTk.PhotoImage(im2)
TKitem1 = myCanvas.create_image([0,0],image=TK_img, anchor='nw') 
TKitem2 = myCanvas.create_image([350,0],image=TK_img2, anchor='nw') 

myCanvas.pack()
root.mainloop()