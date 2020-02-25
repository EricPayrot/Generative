import tkinter, Observer
from PIL import Image, ImageTk, ImageOps

# resize and mosaic
def mosaic(canv,im,nb_col,nb_lin,siz):
    global TKImg
    PILimgsmall = im.resize((siz,siz))
    TKImg = ImageTk.PhotoImage(PILimgsmall)
    print("tkimg",TKImg) 
    for x in range(1,nb_col):
        for y in range(1,nb_lin):
            cw,ch = (500,500)
            h=int(x/nb_col*cw)
            v=int(y/nb_lin*ch)
            canv.create_image(h,v,image=TKImg,anchor='center',tag='mosaic')
            

def resize_rotate_invert(im):
    global TKImg,TKImg2, size, angle
    ima = im.rotate(angle)
    ima = ima.resize((size,size))
    if invert:
        ima=ima.convert('RGB')
        ima=ImageOps.invert(ima)
    TKImg2 = ImageTk.PhotoImage(ima) 
    items = myCanvas.find_withtag('current')
    for item in items:
        myCanvas.itemconfig(item,image=TKImg2)

def rotate(im,angl):
    global TKImg
    TKImg = ImageTk.PhotoImage(PILimgsmall) 
    items = myCanvas.find_withtag('mosaic')
    for item in items:
        myCanvas.itemconfig(item,image=TKImg)

def select_item(event):
    current_item = myCanvas.find_overlapping(event.x-1, event.y-1,event.x+1, event.y+1)
    print('selected item',current_item)
    return current_item

#def rotate_item(event):


def print_circle(x,y,r):
    myCanvas.create_oval(x-r,y-r,x+r,y+r)

def print_text():
    textcontent="hello my dear"
    myCanvas.create_text(100,100,font=("Arial",15),text = textcontent,activefill='red',width=40)     

def highlight_current_event(event):
    boundingbox = myCanvas.bbox("current")
    highlight_rect=myCanvas.create_rectangle(boundingbox,outline='blue')

def move_item(event):
    x, y = event.x, event.y
    if myCanvas.old_coords:
        x1, y1 = myCanvas.old_coords
        myCanvas.move("current",x-x1,y-y1)    
    myCanvas.old_coords = x, y
    
def remove_item(event):
    myCanvas.delete("current")

def draw(event):
    x, y = event.x, event.y
    if myCanvas.old_coords:
        x1, y1 = myCanvas.old_coords
        myCanvas.create_line(x, y, x1, y1)
    myCanvas.old_coords = x, y

def select_mode(event):
    global mode
    if event.char == 'a':
        mode='add'
        print(event.char, mode)
    elif event.char =='r':
        mode='remove'
        print(event.char, mode)
    elif event.char == 'm':
        mode='move'
        print(event.char, mode)
    elif event.char == 'd':
        mode='draw'
        print(event.char, mode)   

def click_action(event):
    if mode == 'add':
        highlight_current_event(event)
    elif mode =='remove':
        remove_item(event)
    elif mode =='move':
        move_item(event)
    elif mode =='draw':
        draw(event)

def motion_action(event):
    print(current_item,event.x,event.y)
    move_item(event, selected_item)

def mouse_release_action(event):
    myCanvas.old_coords=None

def increase(event):
    global size
    size = size +1
    print(size)
    resize_rotate_invert(PILimg)

def decrease(event):
    global size
    size = size -1
    print(size)
    resize_rotate_invert(PILimg)

def right(event):
    global angle
    angle=angle+10
    print(angle)
    resize_rotate_invert(PILimg)

def left(event):
    global invert
    invert = not invert
    resize_rotate_invert(PILimg)
# init tk
root = tkinter.Tk()

# create canvas
myCanvas = tkinter.Canvas(root, bg="white", height=500, width=500)

# load image
path = r"C:\Users\100004614\python\project1\cross trsp bck.png"
PILimg = Image.open(path)
mode=None
size=30
angle=0
invert=False 

# add to window and show
mosaic(myCanvas,PILimg,14,14,size)

myCanvas.bind('<Button-1>',click_action)
root.bind('<Up>', increase)
root.bind('<Down>', decrease)
root.bind('<Right>',right)
root.bind('<Left>',left)
root.bind('<Key>', select_mode)
myCanvas.bind('<B1-Motion>',click_action)
myCanvas.bind('<ButtonRelease-1>',mouse_release_action)
myCanvas.old_coords = None
myCanvas.pack()
root.mainloop()
