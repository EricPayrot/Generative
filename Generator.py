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
        self.create_param_widgets(nb_col=1)

    def getdict(self):
            dict = {}
            for p in self.param:
                dict[str(p)] = getattr(self,p)
            return dict

    def setdict(self,dict):
            for p in self.param:
                setattr(self,p,dict[str(p)])

    def create_param_widgets(self, nb_col=1):
        i=0
        col=0
        row=0
        self.container = Frame(self.control_panel)
        self.container.grid(sticky='w')
        #self.container.columnconfigure(0,minsize=120)
        self.container.columnconfigure(0, weight=1)
        for p in self.param:
            w=param_widget(parentUI=self.container,generator = self,param=self.param[i],label=self.param_label[i],value=self.param_default[i])
            w.widget.grid(row=row,column=col, sticky='ew')
            self.widgets.append(w)
            #w.widget.columnconfigure(col,minsize=100/nb_col)
            w.widget.columnconfigure(col, weight=1)
            i+=1
            col+=1
            if col >= nb_col:
                col=0
                row+=1

    def delete_param_widgets(self):
        for widget in self.widgets:
            widget.widget.destroy()
        self.container.destroy()
    
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
        # self.source_image_width = 300
        # self.source_image_height = 300

    def getdict(self):
        dict = {}
        dict['source_images'] = [id(source) for source in self.source_image]
        dict['masks'] = [id(mask) for mask in self.mask]
        for source in self.source_image:
            dict[id(source)] = source.getdict()
        for mask in self.mask:
            dict[id(mask)] = mask.getdict()
        return dict

    def setdict(self, dict):
        self.geometry_strategy = dict['geometry_strategy'] = self.geometry_strategy
        self.clips = dict['clips']
        self.layer_visible = dict['layer_visible']
        self.layerID = dict['layerID']
        self.layerIndex = dict['layerIndex']
        self.image_source_strategy = dict['image_source_strategy']    
         
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
        self.nb_point_changed = True
        self.canvas.update()
        self.canvas_w = self.canvas.winfo_width()
        self.canvas_h = self.canvas.winfo_height()   
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.centerx = int(self.canvas.winfo_width()/2)
        self.centery = int(self.canvas.winfo_height()/2)
        self.control_panel = self.parent.geometry_panel

    def update(self):
        self.old_nb_points = len(self.coordinates)
        self.calculatepoints()
        self.calculate_clip_sizes()
        if len(self.coordinates) != self.old_nb_points:
            self.nb_point_changed = True
            self.create_clips()
        else:
            self.nb_point_changed = False
            for c in range(0,len(self.coordinates)):
                self.parent.clips[c].position[0] = self.coordinates[c][0]
                self.parent.clips[c].position[1] = self.coordinates[c][1]
                self.parent.clips[c].refresh_position()


    def create_clips(self):
        self.source_image = self.parent.image_source.get_source_image()
        print ('create ',len(self.coordinates),' image clips using ', len(self.source_image), 'source images - ', 'for generator', self)
        del self.parent.clips[:]
        self.tag = self.parent.layerID
        self.canvas.delete(self.tag)

        for c in range(0,len(self.coordinates)):
            clip_source_image = Image.new("RGBA",(200,200),(127,127,127,20))
            clip_mask =  Image.new("L",(200,200),255)
            self.parent.clips.append(ImageClip(source=clip_source_image,canvas=self.canvas,generator=self, mask=clip_mask))          

            self.parent.clips[c].position[0] = self.coordinates[c][0]
            self.parent.clips[c].position[1] = self.coordinates[c][1]
            self.parent.clips[c].old_position[0] = self.coordinates[c][0]
            self.parent.clips[c].old_position[1] = self.coordinates[c][1]
            self.parent.clips[c].processed_image = self.parent.clips[c].process(mode='display')
            self.parent.clips[c].place()
                 
class grid(geometry):
    def __init__(self, parent):
        super().__init__(parent)
        self.nb_col = 3
        self.nb_lin = 3
        self.parent = parent

        # prepare control panel widgets
        self.param.append('nb_col')
        self.param_label.append('nb col')
        self.param_default.append(self.nb_col)
        self.param.append('nb_lin')
        self.param_label.append('nb lin')
        self.param_default.append(self.nb_lin)
        self.param.append('centerx')
        self.param_label.append('x')
        self.param_default.append(self.centerx)
        self.param.append('centery')
        self.param_label.append('y')
        self.param_default.append(self.centery)
        self.param.append('width')
        self.param_label.append('w')
        self.param_default.append(self.width)
        self.param.append('height')
        self.param_label.append('h')
        self.param_default.append(self.height)
        self.create_param_widgets(2)

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
                        cw,ch = (self.width,self.height)
                        h=int((x+1)/(self.nb_col+1)*cw) + (self.centerx - cw/2)
                        v=int((y+1)/(self.nb_lin+1)*ch) + (self.centery - ch/2)
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
        self.param_label.append('nb lin')
        self.param_default.append(self.nb_lin)
        self.param.append('centerx')
        self.param_label.append('x')
        self.param_default.append(self.centerx)
        self.param.append('centery')
        self.param_label.append('y')
        self.param_default.append(self.centery)
        self.param.append('width')
        self.param_label.append('w')
        self.param_default.append(self.width)
        self.param.append('height')
        self.param_label.append('h')
        self.param_default.append(self.height)
        self.create_param_widgets(2)

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
                        cw,ch = (self.width,self.height)
                        h=int((x+1)/(nb_col+1)*cw) + (self.centerx - cw/2)
                        v=int((y+1)/(self.nb_lin+1)*ch) + (self.centery - ch/2)
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

    def update(self, param=None):
        self.source_image = self.parent.image_source.get_source_image()
        for c in range(0,len(self.clips)):
            if len(self.source_image)>0:
                clip_source_image = self.source_image[random.randint(0,len(self.source_image)-1)].image                
                self.parent.clips[c].source_image=clip_source_image
            else :
                clip_source_image = Image.new("RGBA",(200,200),(127,127,127,20))               
                self.parent.clips[c].source_image=clip_source_image
        print('*****************update clips', self)

    def randomize(self, generator, param):
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
                clip_mask = Image.new("L",(200,200),255) #utile ?               
                self.parent.clips[c].mask=clip_mask
        print('*****************update masks', self)
    
    def randomize(self, generator, param):
        if generator == self:
            print('randomize')

class resize(modulator):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize = 30
        # prepare control panel widgets
        self.param.append('resize')
        self.param_label.append('size')
        self.param_default.append(self.resize)
        self.create_param_widgets(1)
        self.clip_sizes = parent.geometry.get_clip_sizes()

    def update(self, param=None):
        if self.is_int(self.resize):
            self.resize = int(self.resize)
            for clip in self.parent.clips:
                clip.resize_x = self.resize
                clip.resize_y = self.resize
    
    def randomize(self, generator, param):
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
        self.create_param_widgets(1)
    
    def update(self, param=None):
         if self.is_int(self.rotation):
            self.rotation = int(self.rotation)
            for clip in self.parent.clips:
                clip.rotation = self.rotation

    def randomize(self,generator, param):
        if generator == self:
            for clip in self.parent.clips:
                if self.rotation == 90 or self.rotation == 180:
                    clip.rotation = random.randint(0,4)*self.rotation
                else :
                    clip.rotation = random.randint(0,self.rotation)
            Event('generator_change', generator=self)

class hsv(modulator):
    def __init__(self, parent):
        super().__init__(parent)
        self.H_offset = 0
        self.S_offset = 0
        self.V_offset = 0
        self.H_offset_mode = 'value'
        self.S_offset_mode = 'value'
        self.V_offset_mode = 'value'

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
    
    def update(self, param = None):
        if param == 'H_offset':
            self.H_offset = int(self.H_offset)
            self.H_offset_mode = 'value'
            for clip in self.parent.clips:
                clip.H_offset = self.H_offset
        elif param =='S_offset':
            self.S_offset = int(self.S_offset)
            self.S_offset_mode = 'value'
            for clip in self.parent.clips:
                clip.S_offset = self.S_offset
        elif param == 'V_offset':
            self.V_offset = int(self.V_offset)
            self.V_offset_mode = 'value'
            for clip in self.parent.clips:
                clip.V_offset = self.V_offset
        else :
            if self.H_offset_mode == 'value':
                self.H_offset = int(self.H_offset)
                for clip in self.parent.clips:
                    clip.H_offset = self.H_offset
            elif self.H_offset_mode == 'random':
                self.randomize(self,'H_offset')

            if self.S_offset_mode == 'value':
                self.S_offset = int(self.S_offset)
                for clip in self.parent.clips:
                    clip.S_offset = self.S_offset
            elif self.S_offset_mode == 'random':
                self.randomize(self,'S_offset')

            if self.V_offset_mode == 'value':
                self.V_offset = int(self.V_offset)
                for clip in self.parent.clips:
                    clip.V_offset = self.V_offset
            elif self.V_offset_mode == 'random':
                self.randomize(self,'V_offset')

    def randomize(self,generator, param):
        if generator == self:
            if param == 'H_offset':
                self.H_offset = int(self.H_offset)
                self.H_offset_mode = 'random'
                for clip in self.parent.clips:
                    clip.H_offset = int(random.uniform(-self.H_offset,self.H_offset))
            elif param == 'S_offset':     
                self.S_offset = int(self.S_offset)
                self.S_offset_mode = 'random'
                for clip in self.parent.clips:
                    clip.S_offset = int(random.uniform(-self.S_offset,self.S_offset))
            elif param == 'V_offset':    
                self.V_offset = int(self.V_offset)
                self.V_offset_mode = 'random'
                for clip in self.parent.clips:
                    clip.V_offset = int(random.uniform(-self.V_offset,self.V_offset))
            Event('generator_change', generator=self)     

class mask_invert(modulator):
    def __init__(self, parent):
        super().__init__(parent)
        self.mask_invert = False
        self.mask_invert_mode = 'value'
        # prepare control panel widgets
        self.param.append('mask_invert')
        self.param_label.append('msk inv')
        self.param_default.append(self.mask_invert)
        self.create_param_widgets(1)
    
    def update(self, param=None):
        if param == 'mask_invert':
            self.mask_invert_mode = 'value'

        if self.mask_invert_mode == 'value':
            if self.mask_invert == 1:
                self.mask_invert = True
            else:
                self.mask_invert = False
            for clip in self.parent.clips:
                clip.invert_mask = self.mask_invert
        elif self.mask_invert_mode == 'random':
            self.randomize(self)

    def randomize(self,generator, param=None):
        if generator == self:
            self.mask_invert_mode = 'random'
            for clip in self.parent.clips:
                clip.invert_mask = random.choice((False,True))
            Event('generator_change', generator=self)

    
