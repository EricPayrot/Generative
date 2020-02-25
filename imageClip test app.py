import tkinter, glob, random
from PIL import Image, ImageTk, ImageOps


class ImageClip:
    def __init__(self,source):
        super().__init__()
        self.source_image=source
        self.source_image_index= None
        self.resize = 30
        self.TKImage = None
        self.TKitem = None
        self.position = [100,100]
        self.rotation = 0
    
    def re_process(self):
        global TKImage
        self.processed_image = self.source_image.rotate(self.rotation,expand=False)
        self.processed_image = self.processed_image.resize((self.resize,self.resize),resample=0)
    
    def place(self):
        global TKImage
        self.TKImage = ImageTk.PhotoImage(self.processed_image)
        self.TKitem=myCanvas.create_image(self.position,image=self.TKImage,anchor='center',tag='mosaic')

    def update(self):
        self.TKImage = ImageTk.PhotoImage(self.processed_image)
        myCanvas.itemconfig(self.TKitem,image=self.TKImage)


# Generator -----------------------------------

def mosaic(im,nb_col,nb_lin,siz):
    global index
    for x in range(1,nb_col):
        for y in range(1,nb_lin):
            index=index+1
            if index>=len(PILimg):
                index=0
            #index = random.randint(0,len(PILimg)-1)
            clips.append(ImageClip(PILimg[index]))
            ImageClip.source_image_index=index
            cw,ch = (500,500)
            h=int(x/nb_col*cw)
            v=int(y/nb_lin*ch)
            clips[-1].position[0]=h
            clips[-1].position[1]=v
            clips[-1].rotation=random.randint(0,3)*90
            clips[-1].resize=siz
            clips[-1].re_process()
            clips[-1].place()

# UI functions -------------------------------------
def up(event):
    for i in range(len(clips)):
        clips[i].resize = clips[i].resize +1
        clips[i].re_process()
        clips[i].update()

def down(event):
    for i in range(len(clips)):
        clips[i].resize = clips[i].resize -1
        clips[i].re_process()
        clips[i].update()

def button1(event):
    myCanvas.old_coords = None
    items=myCanvas.find_withtag('current')
    for i in range(len(clips)):
        if clips[i].TKitem in items:
            clips[i].resize=clips[i].resize+1
            clips[i].re_process()
            clips[i].update()
    print(items)

def b1motion(event):
    x, y = event.x, event.y
    if myCanvas.old_coords:
        x1, y1 = myCanvas.old_coords
        myCanvas.move("current",x-x1,y-y1)    
    myCanvas.old_coords = x, y

def button3(event):
    items=myCanvas.find_withtag('current')
    global next_image
    for i in range(len(clips)):
        if clips[i].TKitem in items:
            next_image=next_image+1
            if next_image>len(PILimg)-1:
                next_image=0
            clips[i].source_image=PILimg[next_image]
            clips[i].re_process()
            clips[i].update()    

# init tk ----------------------------------------------------------
root = tkinter.Tk()
myCanvas = tkinter.Canvas(root, bg="white", height=500, width=500)
myCanvas.old_coords = None
next_image=0
clips=[]

# Bindings --------------------------------------------------------
root.bind('<Up>',up)
root.bind('<Down>',down)
myCanvas.bind('<Button-1>',button1)
myCanvas.bind('<B1-Motion>',b1motion)
myCanvas.bind('<Button-3>',button3)

# main ---------------------------------------------
path = r"C:\Users\100004614\python\project1\pics color2\*"
PILimg = []
index = 0

for filename in glob.iglob(path):
    im=Image.open(filename)
    im = im.convert('RGBA')
    PILimg.append(im)
    
mosaic(PILimg,20,20,20)

myCanvas.pack()
root.mainloop()

