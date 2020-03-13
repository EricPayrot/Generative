import tkinter, glob, random
from PIL import Image, ImageTk, ImageOps, ImageChops
#from Observer import Observer, Event
import os

class ImageClip():
    def __init__(self,source=None,canvas=None,generator=None, mask=None):
        self.source_image=source
        self.mask = mask
        self.processed_image = None
        self.generator = generator
        self.tag = generator.tag
        self.canvas = canvas
        self.resize_x = 120
        self.resize_y = 120
        #self.TKImage = None
        self.TKitem = None
        self.position = [100,100]
        self.display_scaled_position = [100,100]
        self.file_scaled_position = [1000,1000]
        self.old_position = [100,100]
        self.rotation = 0
        self.H_offset = 0
        self.S_offset = 0
        self.V_offset = 0
        self.invert_mask = False
    
    def getdict(self):
        dict = {}
        dict['source'] = 'source'+str(id(self.source_image))
        if self.mask != None:
            dict['mask'] = 'mask'+str(id(self.mask))
        dict['tag'] = self.tag
        dict['resize_x'] = self.resize_x
        dict['resize_y'] = self.resize_y
        dict['position'] = self.position
        dict['rotation'] = self.rotation
        dict['H_offset'] = self.H_offset
        dict['S_offset'] = self.S_offset
        dict['V_offset'] = self.V_offset
        dict['invert_mask'] = self.invert_mask
        return dict

    def setdict(self, dict):
        self.tag = dict['tag']
        self.resize_x = dict['resize_x']
        self.resize_y = dict['resize_y']
        self.position = dict['position']
        self.rotation = dict['rotation']
        self.H_offset = dict['H_offset']
        self.S_offset = dict['S_offset']
        self.V_offset = dict['V_offset']
        self.invert_mask = dict['invert_mask']

    def process(self, mode = 'display'):
        self.canvas_scalefactor = self.generator.parent.parent.canvas_scalefactor
        self.display_to_file_factor = self.generator.parent.parent.display_to_file_factor

        processed_image = Image.new('RGBA',self.source_image.size,(0,0,0,0))

        if mode == 'display':
            self.display_scaled_position = [int(self.position[0]*self.canvas_scalefactor), int(self.position[1]*self.canvas_scalefactor)]
        elif mode == 'file' :
            self.file_scaled_position = [int(self.position[0]*self.display_to_file_factor), int(self.position[1]*self.display_to_file_factor)]
        if self.mask == None:
            mask = Image.new("L",(200,200),255)
        else:
            mask = self.mask

        if self.invert_mask == True:
            self.processed_mask = invert_mask(mask)
        else:
            self.processed_mask = mask
        processed_image.paste(self.source_image,box=(0,0),mask = self.processed_mask.resize(self.source_image.size))
        processed_image = processed_image.rotate(-self.rotation,expand=True)
        if mode == 'display':
            processed_image = processed_image.resize((self.resize_x,self.resize_y),resample=0)
        elif mode == 'file':
            processed_image = processed_image.resize((self.resize_x*self.display_to_file_factor,self.resize_y*self.display_to_file_factor),resample=0)
        processed_image = offset_hsl(processed_image, H_offset=self.H_offset, S_offset=self.S_offset, V_offset=self.V_offset)
        return processed_image

    def place(self):
        self.canvas.delete(self.TKitem)
        self.TKImage = ImageTk.PhotoImage(self.processed_image.resize((int(self.resize_x*self.canvas_scalefactor),int(self.resize_y*self.canvas_scalefactor)),resample=0))
        self.TKitem=self.canvas.create_image(self.display_scaled_position,image=self.TKImage,anchor='center',tag=self.tag, state='normal')

    def update(self):
        self.processed_image = self.process(mode='display')
        self.place()

    def refresh_position(self):
        dx = int((self.position[0] - self.old_position[0])*self.canvas_scalefactor)
        dy = int((self.position[1] - self.old_position[1])*self.canvas_scalefactor)
        self.canvas.move(self.TKitem, dx, dy)
        self.old_position[0] = self.position[0]
        self.old_position[1] = self.position[1]

class SourceImage():
    def __init__(self, original):
        self.original = original
        self.file_name = None
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
    
    def getdict(self):
        dict = {}
        dict['file_name'] = self.file_name
        dict['zoom_factor'] = self.zoom_factor
        dict['center_x'] = self.center_x
        dict['center_y'] = self.center_y
        return dict
        
    def setdict(self, dict):
        self.file_name = dict['file_name']
        self.zoom_factor = dict['zoom_factor']
        self.center_x = dict['center_x']
        self.center_y = dict['center_y']
    
    def save_original(self, fp=None):
        self.savepath = fp
        self.file_name = self.savepath + '/' + 'source_' + str(id(self.original)) + '.png'
        self.original.save(self.file_name)

class Mask():
    def __init__(self, original, mode = 'draw'):
        super().__init__()
        self.original = original
        self.file_name = None
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

    def getdict(self):
        dict = {}
        dict['original'] = id(self.original)
        dict['mode'] = self.mode
        dict['file_name'] = self.file_name
        dict['zoom_factor'] = self.zoom_factor
        dict['center_x'] = self.center_x
        dict['center_y'] = self.center_y
        return dict
    
    def setdict(self, dict):
        self.mode = dict['mode']
        self.file_name = dict['file_name']
        self.zoom_factor = dict['zoom_factor']
        self.center_x = dict['center_x']
        self.center_y = dict['center_y']
        
    def save_original(self, fp=None):
        self.savepath = fp
        self.file_name = self.savepath + '/' + 'mask_' + str(id(self.original)) + '.png'
        self.original.save(self.file_name)


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

def invert_mask(image):
    image= image.point(lambda x : 255-x)
    return image
