from tkinter import*
from PIL import Image, ImageDraw
import os, random, glob
from Observer import Observer, Event
from imageClip import ImageClip
from UserInterface import*
from datetime import datetime
from Generator import*
from Strategy import*
import pickle
from tkinter import filedialog

class App(Observer.Observer):
    def __init__(self):
        super().__init__()
        self.canvas_height = 500
        self.canvas_width = 500
        self.display_sizex = 1000
        self.display_sizey = 1000
        self.file_sizex = 10000
        self.file_sizey = 10000
        self.display_to_file_factor = 10
        self.canvas_scalefactor = 0.5

        root=Tk()
        root.title('Maya the best')
        self.appUI = appUI(self, root, self.canvas_height, self.canvas_width)
        self.canvas = self.appUI.output_canvas
        self.control_panel = self.appUI.control_panel
        self.layer_panel = self.appUI.layer_panel
        self.layers = []
        self.selected_layer=None
        self.add_layer()
        self.observe('new_layer',self.add_layer)
        self.observe('select_layer',self.select_layer)
        self.observe('zoom_factor_changed',self.zoom_change_callback)
        # event binding
        root.bind('<Control-s>',self.save_output_image)
        root.bind('<Control-d>', self.dump_state)
        root.bind('<Control-o>', self.load_state)
        
        root.mainloop()
    
    def add_layer(self):
        print('add layer')
        self.newlayer = Layer(parent=self)
        self.layers.append(self.newlayer)
        self.select_layer(self.newlayer)
        
    def select_layer(self, generator):
        self.selected_layer = generator
        for layer in self.layers:
            if layer == self.selected_layer:
                layer.layerUI.control_panel.lift()
                layer.layerUI.layer_widget.selected()
            else:
                layer.layerUI.layer_widget.unselected()
    
    def remove_layer(self):
        print('remove layer')

    def raise_layer(self):
        print('raise layer')
        # a_list = ["a", "b", "c"]
        # index1 = a_list. index("a")
        # index2 = a_list. index("c")
        # a_list[index1], a_list[index2] = a_list[index2], a_list[index1]
    
    def refresh_layer_stacking_order(self):
        for layer in self.layers:
                self.canvas.tag_raise(layer.layerID)
    
    def zoom_change_callback(self, generator, param):
        self.canvas_scalefactor = param
        for layer in self.layers:
            layer.refresh_canvas()

    def save_output_image(self, event):
        print('rendering output image for ',self,' and saving to file')
        self.output_image =Image.new("RGBA",(self.file_sizex,self.file_sizey),(255,255,255,255))
        self.savepath = r'output image'        
        
        for layer in self.layers:
            for c in range(0,len(layer.clips)):
                clip_image = layer.clips[c].process(mode = 'file')
                clip_center_x = layer.clips[c].file_scaled_position[0]
                clip_center_y = layer.clips[c].file_scaled_position[1]
                clip_nw_corner_x = int(layer.clips[c].file_scaled_position[0] - layer.clips[c].resize_x*self.display_to_file_factor /2)
                clip_nw_corner_y = int(layer.clips[c].file_scaled_position[1] - layer.clips[c].resize_y*self.display_to_file_factor /2)
                self.output_image.paste(clip_image,(clip_nw_corner_x,clip_nw_corner_y),clip_image) #last argument is the mask to avoid punching a whole where alpha=0
 
        if not os.path.exists(self.savepath):
            os.makedirs(self.savepath,mode=0o755)

        self.now = datetime.now()
        self.datetime = self.now.strftime("%d_%m_%Y_%H%M%S")
        
        self.filename = self.savepath + '/' + 'output_' + self.datetime + '.png'
        self.output_image.save(self.filename)
    
    def dump_state(self, event):
        print('dumping state to file')
        self.savepath = r'state'
        if not os.path.exists(self.savepath):
            os.makedirs(self.savepath,mode=0o755)

        self.now = datetime.now()
        self.datetime = self.now.strftime("%d_%m_%Y_%H%M%S")
        self.filename = self.savepath + '/' + 'state_' + self.datetime + '.pkl'

        source_images = []
        clips = []

        for layer in self.layers:
            source_images.append(layer.image_source.get_source_image())
            clips.append(layer.clips)

        with open(self.filename,'wb') as f:
            pickle.dump(source_images,f)
            pickle.dump(clips, f)
    
    def load_state(self, event):
        filename = filedialog.askopenfilename()
        clips = []
        with open(filename, 'rb') as f:
            source_images = pickle.load(f)
            clips = pickle.load(f)

        for layer in self.layers:
            for source_image in source_images[0]:
                layer.image_source.get_source_image().append(source_image)
            for clip in clips[0]:
                layer.clips.append(clip)
            layer.refresh_canvas()



class Layer(Observer.Observer):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.canvas = self.parent.canvas
        self.geometry_strategy = 'grid'
        self.clips = []
        self.layer_visible = True

        self.layerID = str(self).replace('.','').replace(' ','_')
        self.layerIndex = len(self.parent.layers)+1
        self.layerUI = layerUI(self, self.parent.control_panel)
        self.control_panel = self.layerUI.control_panel
        self.image_source_panel = self.layerUI.image_source_panel
        self.mask_panel = self.layerUI.mask_panel
        self.geometry_panel = self.layerUI.geometry_panel
        self.modulator_panel = self.layerUI.modulator_panel

        # select image source    
        self.image_source = ImageSource(strategy = imageFromScratchpad, parent=self)

        # mask
        self.masksource = MaskSource(parent = self)

        # select geometry
        geometry_options = ["grid","tree"]
        self.select_geometryUI = geometry_strategy_selectorUI(parent=self, parentUI=self.control_panel,options=geometry_options)
        self.geometry = Geometry(strategy=grid, parent=self)
        
        #select modulators
        self.clip_source = clip_source_image(parent=self)
        self.clip_mask = clip_mask(parent=self)
        self.resize = resize(parent=self)
        self.rotate = rotate(parent=self)
        self.hsv = hsv(parent=self)
        self.mask_invert = mask_invert(parent=self)

        #event binding
        self.observe('param_change',self.update)
        self.observe('generator_change',self.refresh_canvas)
        self.observe('image_source_strategy_change',self.change_image_source_strategy)
        self.observe('geometry_strategy_change',self.change_geometry_strategy)
        self.observe('toggle_layer_visibility',self.toggle_layer_visibility)
        
        self.update(self)
        self.parent.appUI.apply_zoom_factor()
    
    def toggle_layer_visibility(self, generator):
        if generator == self:
            if self.layer_visible == True:
                self.layer_visible = False
                self.canvas.itemconfigure(self.layerID, state='hidden')
            else :
                self.layer_visible = True
                self.canvas.itemconfigure(self.layerID, state='normal')

    def change_image_source_strategy(self, generator):
        if generator == self.layerUI.sel_img_srcUI:
            self.image_source_strategy = generator.option.get()
            if self.image_source_strategy=='scratchpad':
                self.image_source.delete()
                self.image_source = ImageSource(strategy=imageFromScratchpad, parent=self)
            elif self.image_source_strategy=='file':
                self.image_source.delete()
                self.image_source = ImageSource(strategy=imageFromFile, parent=self)
            else:
                print('no change')
            self.update(generator=self)

    def change_geometry_strategy(self, generator):
        if self.geometry_strategy=='grid':
            self.geometry.delete()
            self.geometry = Geometry(strategy=grid, parent=self)
        elif self.geometry_strategy=='tree':
            self.geometry.delete()
            self.geometry = Geometry(strategy=tree, parent=self)
        else:
            print('no change')
        self.update(generator=self)

    def update(self, generator, param = None):
        if generator == self:
            print('update all for layer', self)
            self.geometry.update()
            self.clip_source.update()
            self.clip_mask.update()
            self.resize.update()
            self.rotate.update()
            self.hsv.update(param)
            self.mask_invert.update()
            self.refresh_canvas()

        elif generator == self.geometry.instance:
            print('update', generator, 'for layer', self)
            if generator.nb_point_changed == True :
                self.geometry.update()
                self.clip_source.update()
                self.clip_mask.update()
                self.resize.update()
                self.rotate.update()
                self.hsv.update(param)
                self.mask_invert.update()
                self.refresh_canvas()
            else:
                self.geometry.update()
                self.refresh_position()

        elif generator == self.image_source.instance:
            print('---- update IMAGE source', generator, 'for layer',self)
            self.clip_source.update()
            self.refresh_canvas()
        
        elif generator == self.masksource:
            print('---- update MASK source', generator, 'for layer',self)
            self.clip_mask.update()
            self.refresh_canvas()
        
        elif generator == self.hsv:
            print('Update HSV', generator, 'for layer',self)
            self.hsv.update(param)
            self.refresh_canvas()

        elif generator.parent == self :
            print('------------update modulator', generator, 'for layer',self)
            generator.update(param)
            self.refresh_canvas()
    
    def refresh_canvas(self, generator=all):
        print('refresh canvas for layer', self)
        for clip in self.clips:
            clip.update()
        self.parent.refresh_layer_stacking_order()
     
    def refresh_position(self, generator=all):
        for clip in self.clips:
            clip.refresh_position()
        self.parent.refresh_layer_stacking_order()

    



