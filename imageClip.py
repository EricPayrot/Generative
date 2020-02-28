import tkinter, glob, random
from PIL import Image, ImageTk, ImageOps, ImageChops
from Observer import*

class ImageClip():
    def __init__(self,source,canvas,generator, mask):
        self.source_image=source
        self.mask = mask
        self.processed_image = None
        self.generator = generator
        self.canvas = canvas
        self.resize_x = 50
        self.resize_y = 50
        self.TKImage = None
        self.TKitem = None
        self.position = [100,100]
        self.old_position = [100,100]
        self.rotation = 0
        self.H_offset = 0
        self.S_offset = 0
        self.V_offset = 0

    def process_and_place(self,canvas):
        self.processed_image = Image.new('RGBA',self.source_image.size,(0,0,0,0))
        self.processed_image.paste(self.source_image,box=(0,0),mask = self.mask.resize(self.source_image.size))
        self.processed_image = self.processed_image.rotate(-self.rotation,expand=True)
        self.processed_image = self.processed_image.resize((self.resize_x,self.resize_y),resample=0)
        self.processed_image = offset_hsl(self.processed_image, H_offset=self.H_offset, S_offset=self.S_offset, V_offset=self.V_offset)
        self.TKImage = ImageTk.PhotoImage(self.processed_image)
        self.TKitem=self.canvas.create_image(self.position,image=self.TKImage,anchor='center',tag=self.generator.tag)

    def update(self):
        self.process_and_place(self.canvas)

    def refresh_position(self):
        dx = self.position[0] - self.old_position[0]
        dy = self.position[1] - self.old_position[1]
        self.canvas.move(self.TKitem, dx, dy)
        self.old_position[0] = self.position[0]
        self.old_position[1] = self.position[1]

class SourceImage():
    def __init__(self, original):
        self.original = original
        self.image = None
        self.zoom_factor = 100
        self.width, self.height = self.original.size
        self.center_x = self.width/2
        self.center_y = self.height/2
        self.crop_original_image()

    def crop_original_image(self):          
        self.x1 = self.center_x-100/self.zoom_factor*100
        self.x2 = self.center_x+100/self.zoom_factor*100
        self.y1 = self.center_y-100/self.zoom_factor*100
        self.y2 = self.center_y+100/self.zoom_factor*100
        bbox=(self.x1,self.y1,self.x2,self.y2)
        self.image = self.original.crop(bbox)

class Mask():
    def __init__(self, original, mode = 'draw'):
        super().__init__()
        self.original = original
        self.image = None
        self.mode = mode
        self.zoom_factor = 100
        self.width, self.height = self.original.size
        self.center_x = self.width/2
        self.center_y = self.height/2
        self.crop_original_image()

    def crop_original_image(self):          
        self.x1 = self.center_x-100/self.zoom_factor*100
        self.x2 = self.center_x+100/self.zoom_factor*100
        self.y1 = self.center_y-100/self.zoom_factor*100
        self.y2 = self.center_y+100/self.zoom_factor*100
        bbox=(self.x1,self.y1,self.x2,self.y2)
        self.image = self.original.crop(bbox)
        if self.mode == 'file':
            self.process_file_image()
    
    def process_file_image(self):
        M = Image.new('RGBA',self.image.size, 'white')
        M.paste(self.image,(0,0), self.image)
        M = M.convert('L')
        N= M.point(lambda x : 255 if (x < 128) else 0)
        self.image = N


def offset_hsl(image, H_offset=0, S_offset=0, V_offset=0):
    A = image.getchannel('A') #save alpha channel

    #extract HSV channels
    image = image.convert('RGB').convert('HSV')
    H, S, V = image.split()
    H_offset_image = Image.new('L',image.size, abs(H_offset))
    S_offset_image = Image.new('L',image.size, abs(S_offset))
    V_offset_image = Image.new('L',image.size, abs(V_offset))

    #add or substract offset
    if H_offset <0:
        H = ImageChops.subtract(H,H_offset_image)
    elif H_offset >0:
        H = ImageChops.add(H,H_offset_image)
    
    if S_offset <0:
        S = ImageChops.subtract(S,S_offset_image)
    elif S_offset >0:
        S = ImageChops.add(S,S_offset_image)
    
    if V_offset <0:
        V = ImageChops.subtract(V,V_offset_image)
    elif V_offset >0:
        V = ImageChops.add(V,V_offset_image)

    # merge back channels, convert and add alpha 
    image = Image.merge('HSV',(H,S,V))
    image = image.convert('RGB')
    R, G, B = image.split()
    image = Image.merge('RGBA', (R,G,B,A))
    
    return image
