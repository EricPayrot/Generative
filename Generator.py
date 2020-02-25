from tkinter import*
from PIL import Image, ImageDraw
import os, random, glob
from Observer import Observer, Event
from imageClip import ImageClip
from UserInterface import*
from datetime import datetime

class generator(Observer.Observer):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.canvas = self.parent.canvas
        self.control_panel = self.parent.control_panel
        self.clips = []
        self.coordinates = []
        self.param = []
        self.param_label=[]
        self.param_type=[]
        self.param_default=[]
        self.widgets = []
        #self.observe('param_change',self.param_has_changed)
        self.create_param_widgets()

    def create_param_widgets(self, nb_col=1):
        i=0
        col=0
        self.container = Frame(self.control_panel)
        self.container.grid()
        for p in self.param:
            w=param_widget(parentUI=self.container,generator = self,param=self.param[i],label=self.param_label[i],value=self.param_default[i])
            w.widget.grid(column=col)
            self.widgets.append(w)
            i+=1
            col+=1
            if col >= nb_col:
                col=0

    def delete_param_widgets(self):
        self.container.destroy()
        for widget in self.widgets:
            widget.widget.destroy()

    
    def run(self):
        pass

    def is_int(self,s):
        try:
            int(s)
            return True
        except ValueError:
            pass

class imageSource(generator):
    def __init__(self, parent):
        super().__init__(parent)
        self.source_image = []
        self.mask = []
        self.source_image_width = 300
        self.source_image_height = 300
        
         
    def update(self):
        pass
    
class imageFromFile(imageSource):
    def __init__(self,parent):
        super().__init__(parent)
        self.originals = []
        self.control_panel = self.parent.image_source_panel
        self.source = image_from_fileUI(parent=self, parentUI = self.control_panel)

    def destroyUI(self):
        self.source.frame.destroy()
    
class imageFromScratchpad(imageSource):
    def __init__(self, parent):
        super().__init__(parent)
        self.originals = []
        self.control_panel = self.parent.image_source_panel
        self.source = scratchpad(parent=self, parentUI = self.control_panel)
    
    def destroyUI(self):
        self.source.frame.destroy()

class MaskSource(imageSource):
    def __init__(self, parent):
        super().__init__(parent)
        self.originals = []
        self.mask = []
        self.control_panel = self.parent.mask_panel
        MaskUI(parent=self,parentUI = self.control_panel)

class geometry(generator):
    def __init__(self, parent):
        super().__init__(parent) 
        self.coordinates = []
        self.clip_sizes = []   
        self.centerx = self.canvas.winfo_width()/2
        self.centery = self.canvas.winfo_height()/2
        self.control_panel = self.parent.geometry_panel

    def update(self):
        self.calculatepoints()
        self.calculate_clip_sizes()
        self.create_clips()

    
    def create_clips(self):
        self.source_image = self.parent.image_source.get_source_image()
        print ('create ',len(self.coordinates),' image clips using ', len(self.source_image), 'source images - ', 'for generator', self)
        del self.parent.clips[:]
        self.tag = self.parent.layerID
        self.canvas.delete(self.tag)

        for c in range(0,len(self.coordinates)):
            clip_source_image = Image.new("RGBA",(200,200),(127,127,127,20))
            clip_mask =  Image.new("RGBA",(200,200),(255,255,255,255))
            self.parent.clips.append(ImageClip(source=clip_source_image,canvas=self.canvas,generator=self, mask=clip_mask))          
            x = self.coordinates[c][0]
            y = self.coordinates[c][1]
            self.parent.clips[c].position[0] = x
            self.parent.clips[c].position[1] = y
            self.parent.clips[c].place(self.canvas)
                 
class grid(geometry):
    def __init__(self, parent):
        super().__init__(parent)
        self.nb_col = 3
        self.nb_lin = 3
        self.parent = parent

        # prepare control panel widgets
        self.param.append('nb_col')
        self.param_label.append('nombre colonnes')
        self.param_default.append(self.nb_col)
        self.param.append('nb_lin')
        self.param_label.append('nombre lignes')
        self.param_default.append(self.nb_lin)
        self.create_param_widgets()

    #calculatepoints
    def calculatepoints(self):
        del self.coordinates[:]
        if self.is_int(self.nb_col):
            self.nb_col=int(self.nb_col)
            if self.is_int(self.nb_lin):    
                self.nb_lin=int(self.nb_lin)   
                index = 0
                for x in range(0,self.nb_col):
                    for y in range(0,self.nb_lin):
                        cw,ch = (500,500)
                        h=int((x+1)/(self.nb_col+1)*cw)
                        v=int((y+1)/(self.nb_lin+1)*ch)
                        coords = [h,v]
                        self.coordinates.append(coords)
    
    def calculate_clip_sizes(self):
        pass
    
class tree(geometry):
    def __init__(self, parent):
        super().__init__(parent)
        self.height = 500
        self.width = 500
        self.nb_lin = 3
        self.parent = parent
        self.cells = []

        # prepare control panel widgets
        self.param.append('nb_lin')
        self.param_label.append('nombre lignes')
        self.param_default.append(self.nb_lin)
        self.create_param_widgets()

    #calculatepoints
    def calculatepoints(self):
        del self.coordinates[:]
        del self.cells[:]
        if self.is_int(self.nb_lin):
            self.nb_lin = int(self.nb_lin)
            #index = 0        
            for y in range(0,self.nb_lin):
                nb_col = y*2
                if y == 0:
                    nb_col = 1
                for x in range(0,nb_col):
                        cw,ch = (self.height,self.width)
                        h=int((x+1)/(nb_col+1)*cw)
                        v=int((y+1)/(self.nb_lin+1)*ch)
                        coords = [h,v]
                        self.coordinates.append(coords)
                        cellx1 = int((x)/(nb_col+1)*cw)
                        cellx2 = int((x+1)/(nb_col+1)*cw)
                        celly1 = int((y)/(self.nb_lin+1)*ch)
                        celly2 = int((y+1)/(self.nb_lin+1)*ch)
                        cell_bbox = [cellx1,celly1,cellx2,celly2]
                        self.cells.append(cell_bbox)
            print('generate coordinates for ',len(self.coordinates),' points' )
    
    def calculate_clip_sizes(self):
        del self.clip_sizes[:]
        for c in self.cells:
            index = self.cells.index(c)
            cell_h_size = self.cells[index][2] - self.cells[index][0]
            cell_v_size = self.cells[index][3] - self.cells[index][1]
            self.clip_sizes.append([cell_h_size,cell_v_size])

class modulator(generator):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.observe('param_label_clicked',self.randomize)
        self.control_panel = self.parent.modulator_panel

class clip_source_image(modulator):
    def __init__(self, parent):
        super().__init__(parent)
        self.source_image = self.parent.image_source.get_source_image()
        self.coordinates = self.parent.geometry.get_coordinates()
        self.clips = self.parent.clips
        self.source = 0
        self.param.append('source')
        self.param_label.append('source image')
        self.param_default.append(self.source)
        #self.create_param_widgets()

    def update(self):
        self.source_image = self.parent.image_source.get_source_image()
        for c in range(0,len(self.clips)):
            if len(self.source_image)>0:
                clip_source_image = self.source_image[random.randint(0,len(self.source_image)-1)].image                
                self.parent.clips[c].source_image=clip_source_image
            else :
                clip_source_image = Image.new("RGBA",(200,200),(127,127,127,20))               
                self.parent.clips[c].source_image=clip_source_image
        print('*****************update clips', self)

    def randomize(self, generator):
        if generator == self:
            print('randomize')

class clip_mask(modulator):
    def __init__(self, parent):
        super().__init__(parent)
        self.mask = self.parent.masksource.mask
        self.clips = self.parent.clips

    def update(self):
        for c in range(0,len(self.clips)):
            if len(self.mask)>0:
                clip_mask = self.mask[random.randint(0,len(self.mask)-1)].image               
                self.parent.clips[c].mask=clip_mask
            else :
                clip_mask = Image.new("RGBA",(200,200),(255,255,255,255))               
                self.parent.clips[c].mask=clip_mask
        print('*****************update masks', self)
    
    def randomize(self, generator):
        if generator == self:
            print('randomize')

class resize(modulator):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize = 30
        # prepare control panel widgets
        self.param.append('resize')
        self.param_label.append('clip size')
        self.param_default.append(self.resize)
        self.create_param_widgets()
        self.clip_sizes = parent.geometry.get_clip_sizes()

    def update(self):
        if self.is_int(self.resize):
            self.resize = int(self.resize)
            for clip in self.parent.clips:
                clip.resize_x = self.resize
                clip.resize_y = self.resize
            #Event('generator_change', generator=self)
    
    def randomize(self, generator):
        if generator == self:
            for clip in self.parent.clips:
                s = random.randint(10,self.resize)
                clip.resize_x = s
                clip.resize_y = s
            Event('generator_change', generator=self)
    
    def auto(self, generator, param, value):
        if generator == self:
            if param =='resize':
                if value =='auto':
                    for clip in self.parent.clips:
                        index = self.parent.clips.index(clip)
                        clip.resize_x = self.clip_sizes[index][0]
                        clip.resize_y = self.clip_sizes[index][1]
                    Event('generator_change', generator=self)
    
class rotate(modulator):
    def __init__(self, parent):
        super().__init__(parent)
        self.rotation = 0
        # prepare control panel widgets
        self.param.append('rotation')
        self.param_label.append('rotate')
        self.param_default.append(self.rotation)
        self.create_param_widgets()
    
    def update(self):
         if self.is_int(self.rotation):
            self.rotation = int(self.rotation)
            for clip in self.parent.clips:
                clip.rotation = self.rotation
            #Event('generator_change', generator=self)

    def randomize(self,generator):
        if generator == self:
            for clip in self.parent.clips:
                clip.rotation = random.randint(0,360)*self.rotation
            Event('generator_change', generator=self)

class hsv(modulator):
    def __init__(self, parent):
        super().__init__(parent)
        self.H_offset = 0
        self.S_offset = 0
        self.V_offset = 0
        # prepare control panel widgets
        self.param.append('H_offset')
        self.param_label.append('H')
        self.param_default.append(self.H_offset)
        self.param.append('S_offset')
        self.param_label.append('S')
        self.param_default.append(self.S_offset)
        self.param.append('V_offset')
        self.param_label.append('V')
        self.param_default.append(self.V_offset)
        self.create_param_widgets(3)
    
    def update(self):
         if self.is_int(self.rotation):
            self.rotation = int(self.rotation)
            for clip in self.parent.clips:
                clip.rotation = self.rotation
            #Event('generator_change', generator=self)

    def randomize(self,generator):
        if generator == self:
            for clip in self.parent.clips:
                clip.rotation = random.randint(0,360)*self.rotation
            Event('generator_change', generator=self)     


    
