from tkinter import*
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk
from Observer import*
import os, Observer
from imageClip import SourceImage, Mask

class appUI():
    def __init__(self,parent, parentUI, height, width):
        # define main containers
        self.parent = parent
        self.canvas_frame = Frame(parentUI)
        self.xscrollbar = Scrollbar(self.canvas_frame, orient=HORIZONTAL)
        self.yscrollbar = Scrollbar(self.canvas_frame)
        self.output_canvas = Canvas(self.canvas_frame,bg='white', width=width, height=height,xscrollcommand=self.xscrollbar.set,yscrollcommand=self.yscrollbar.set)
        self.output_canvas['scrollregion'] = (0, 0, self.parent.display_sizex, self.parent.display_sizey)
        self.xscrollbar.config(command=self.output_canvas.xview)
        self.yscrollbar.config(command=self.output_canvas.yview)
        self.old_scale_ratio = 0.5
        self.canvas_zoom = StringVar()
        self.canvas_zoom.set(50)
        self.zoom_entry = Entry(self.canvas_frame, textvariable=self.canvas_zoom, width=4)

        self.control_panel = Frame(parentUI,height=height,width=250,padx=3)
        self.layer_panel = Frame(parentUI,height=height,width=50,bg='white')
              
        # layout the main containers
        self.canvas_frame.grid(row=1,column=0)
        self.output_canvas.grid(row=1,column=0, sticky ='nw', columnspan=2)
        self.xscrollbar.grid(row=2, column=1, sticky=E+W)
        self.yscrollbar.grid(row=1, column=2, sticky=N+S)
        self.zoom_entry.grid(row=2, column=0, sticky=W)
        self.canvas_frame.grid_columnconfigure(0, weight=0)
        self.canvas_frame.grid_columnconfigure(1, weight=1)
        self.control_panel.grid(row=1, column=2,sticky ='ne')
        self.layer_panel.grid(row=1, column=3,sticky ='ne')
        self.layer_panel.grid_propagate(0)
    
        # App widgets
        new_layer_widget(self.layer_panel)

        # Bindings
        self.zoom_entry.bind('<Return>',self.apply_zoom_factor)

    def apply_zoom_factor(self, event=None):
        if float(self.canvas_zoom.get()) > 0:
            self.new_scale_ratio = float(self.canvas_zoom.get()) / 100
            Event('zoom_factor_changed',generator = self, param=self.new_scale_ratio)
            self.center_x = self.output_canvas.winfo_width()/2
            self.center_y = self.output_canvas.winfo_height()/2
            # self.output_canvas.scale(ALL,self.center_x,self.center_y,1/self.old_scale_ratio,1/self.old_scale_ratio) #undo previous zoom
            # self.output_canvas.scale(ALL,self.center_x,self.center_y,self.new_scale_ratio,self.new_scale_ratio)
            self.scroll_region_x1 = 0
            self.scroll_region_x2 = self.new_scale_ratio * self.parent.display_sizex
            self.scroll_region_y1 = 0
            self.scroll_region_y2 = self.new_scale_ratio * self.parent.display_sizey
            bbox = (self.scroll_region_x1, self.scroll_region_y1, self.scroll_region_x2, self.scroll_region_y2)
            self.output_canvas['scrollregion'] = bbox
            self.old_scale_ratio = self.new_scale_ratio


    
    def reorder_layer_panels():
        print('***********************reorder layers')

class layerUI():
    def __init__(self, parent, parentUI):
        self.parentUI = parentUI
        self.control_panel = Frame(self.parentUI, height=500, width=250)
        #self.control_panel.grid_propagate(0)
        self.control_panel.grid(row=0,column=0)
        self.control_panel.grid_columnconfigure(0, weight=1)
        self.layer_widget = layer_widget(parent.parent.layer_panel,parent)
        self.image_source_selector_panel = Frame(self.control_panel)
        self.image_source_selector_panel.grid(row=0, in_=self.control_panel,sticky='ew')
        self.image_source_selector_panel.grid_columnconfigure(0, weight=1)
        self.image_source_panel = Frame(self.control_panel)
        self.image_source_panel.grid(row=1, in_=self.control_panel, sticky='')
        self.image_source_panel.grid_columnconfigure(0, weight=1)
        image_source_options = ["scratchpad", "file"]
        self.sel_img_srcUI = image_source_strategy_selectorUI(parentUI=self.image_source_selector_panel,options=image_source_options)
        self.mask_panel = Frame(self.control_panel)
        self.mask_panel.grid(row=1, in_=self.control_panel, sticky='')
        self.src_msk_sel = source_mask_selector_widget(parentUI=self)
        self.geometry_panel = Frame(self.control_panel, borderwidth=5)
        self.geometry_panel.grid(row=2, sticky='ew')
        self.geometry_panel.grid_columnconfigure(0, weight=1)
        self.modulator_panel = Frame(self.control_panel, borderwidth=5)
        self.modulator_panel.grid(row=3, sticky='ew')
        self.modulator_panel.grid_columnconfigure(0, weight=1)

class new_layer_widget():
    def __init__(self,parentUI):
        self.widget = Frame(parentUI)
        self.plus_button = Button(self.widget,text='+', anchor='center', width=5, command=self.callback, relief=FLAT,bg='white')  
        self.plus_button.grid()
        self.widget.grid()

    def callback(self):
        Event('new_layer')

class layer_widget():
    def __init__(self,parentUI, layer):
        self.parentUI = parentUI
        self.layer = layer
        self.label = self.layer.layerIndex
        self.widget = Frame(parentUI, background='red')
        self.layer_button = Button(self.widget,text=self.label, anchor='center',relief=FLAT, width=5, command=self.B1callback)  
        self.layer_button.grid()
        self.widget.grid()
        self.layer_button.bind("<Control-Button-1>", self.CtlB1callback)
    
    def B1callback(self):
        Event('select_layer', generator=self.layer)
    
    def CtlB1callback(self, event):
        Event('toggle_layer_visibility', generator=self.layer)
        if self.layer.layer_visible == True:
            self.layer_button.config(fg='black')
        else :
            self.layer_button.config(fg='red')
    
    def selected(self):
        self.layer_button.configure(background='SystemButtonFace')
    
    def unselected(self):
        self.layer_button.configure(background='white')

class source_mask_selector_widget():
    def __init__(self,parentUI):
        self.parentUI = parentUI.image_source_selector_panel
        self.image_source_panel = parentUI.image_source_panel
        self.mask_panel = parentUI.mask_panel
        self.widget = Frame(self.parentUI, background='red')
        self.label1 = 'source'
        self.label2 = 'mask'
        self.source_button = Button(self.widget,text=self.label1, anchor='center',relief=FLAT, width=5, command=self.show_source)  
        self.mask_button = Button(self.widget,text=self.label2, anchor='center',relief=FLAT, width=5, command=self.show_mask)
        self.source_button.grid(row=0, column=0, sticky='ew')
        self.mask_button.grid(row=0, column=1, sticky='ew')
        self.widget.grid(row=0,column=1, sticky='ew')
        self.widget.columnconfigure(1, weight=1)
        self.show_source()
    
    def show_source(self):
        self.image_source_panel.lift()
        self.source_button.configure(background='white')
        self.mask_button.configure(background='SystemButtonFace')
    
    def show_mask(self):
        self.mask_panel.lift()
        self.mask_button.configure(background='white')
        self.source_button.configure(background='SystemButtonFace')


class param_widget():
    def __init__(self,generator,parentUI,param,label,value):
        # define widgets
        self.widget = Frame(parentUI)
        self.param = param
        self.name = label
        self.generator = generator
        self.label = Label(self.widget,text=self.name, width=5)            
        self.value = StringVar()
        self.value.set(value)
        self.entry = Entry(self.widget, textvariable=self.value, width=4)
        self.old_coords = None
        
        # layout widgets
        self.widget.grid()            
        #self.widget.columnconfigure(0,minsize=120)
        self.label.grid(row=0,column=0, sticky='e')
        self.entry.grid(row=0,column=1, sticky='e')

        # bindings
        self.entry.bind('<Return>',self.get_value)
        self.entry.bind('<B1-Motion>',self.motion)
        self.entry.bind('<Button-1>',self.button1)
        self.entry.bind('<Up>',self.up)
        self.entry.bind('<Down>',self.down)
        self.label.bind('<Button-1>',self.param_label_clicked)

    # widget callbacks                
    def get_value(self,event):
        setattr(self.generator,self.param,int(self.value.get()))
        Event('param_change',generator=self.generator, param=self.param)

    def param_label_clicked(self,event):
        Event('param_label_clicked',generator=self.generator,param=self.param)

    def button1(self,event):
        self.v=int(self.value.get())
        self.old_coords = event.x, event.y

    def motion(self,event):
        xm1, ym1 = self.old_coords
        xm = event.x
        ym = event.y
        if abs(ym1-ym) >=20:
            self.v = int(self.v + (ym1-ym)/20)
            self.value.set(self.v)
            old_coords = xm, ym
            setattr(self.generator,self.param,self.v)
            Event('param_change', generator=self.generator, param=self.param)
    
    def up(self,event):
        self.v=int(self.value.get())
        self.v +=1
        self.value.set(self.v)
        setattr(self.generator,self.param,self.v)
        Event('param_change', generator=self.generator, param=self.param)

    def down(self,event):
        self.v=int(self.value.get())
        self.v -=1
        self.value.set(self.v)
        setattr(self.generator,self.param,self.v)
        Event('param_change', generator=self.generator, param=self.param)


class image_sourceUI():
    def __init__(self,parent, parentUI):
        self.parent = parent
        self.parentUI = parentUI
        self.frame =Frame(self.parentUI)
        self.frame.grid(row=1,pady=10, sticky='w')
        self.source_image = self.parent.source_image
        self.originals = parent.originals
        self.scratchpad_image_index = 0
        self.scratchmode = True
        self.zoom = StringVar()
        self.zoom.set(100)
     
    def canvas(self):
        self.scratchpad_frame = Frame(self.frame)
        self.scratchpad_frame.grid(row=1,column=0)
        self.scratch_canvas = Canvas(self.scratchpad_frame,bg='white',borderwidth=1, width=200, height=200)
        self.scratch_canvas.grid(row=0,column=0)
        # PIL image for image save - replicates what's being drawn on canvas
        self.image=Image.new("RGBA",(200,200),(255,255,255,0))
        
        #bindings
        self.scratch_canvas.bind('<Button-1>',self.button1_callback)
        self.scratch_canvas.bind('<B1-Motion>',self.B1_motion_callback)
        self.scratch_canvas.bind('<B1-ButtonRelease>', self.B1_release_callback)

    def action_bar(self):
        self.action_bar =Frame(self.frame)
        self.next=Button(self.action_bar,text='>',)
        self.previous=Button(self.action_bar,text='<')
        self.add=Button(self.action_bar,text='+')
        self.delete=Button(self.action_bar,text='-')
        self.name = 'scratchpad'   
    
        # action bar layout
        self.previous.grid(row=0,column=0, sticky='ew')   
        self.add.grid(row=0,column=1, sticky='ew')
        self.delete.grid(row=0,column=2, sticky='ew')
        self.next.grid(row=0,column=3, sticky='ew')
        self.action_bar.grid(row=2,column=0, sticky='we')           
        for i in range(4):
            self.action_bar.columnconfigure(i, weight=1)
        
        #bindings
        self.add.bind('<Button-1>',self.add_image)
        self.delete.bind('<Button-1>',self.delete_image)
        self.previous.bind('<Button-1>',self.previous_image)
        self.next.bind('<Button-1>',self.next_image)
       
    # scratchpad callbacks
    def get_mouse_coords(self,event):
        self.scratch_canvas.old_coords = event.x,event.y

    def display_in_scratchpad(self):
            self.clear_scratchpad()
            if self.scratchmode:
                self.TKImage = ImageTk.PhotoImage(self.image) 
            else:
                self.TKImage = ImageTk.PhotoImage(self.source_image[self.scratchpad_image_index].image.resize((200,200),resample=0))
                self.zoom.set(self.source_image[self.scratchpad_image_index].zoom_factor)
            self.scratch_canvas.create_image((100,100),image=self.TKImage,anchor='center')
            
    def delete_image(self,event):
        if len(self.source_image) > 1:
            del(self.source_image[self.scratchpad_image_index])
            self.previous_image(event)
        elif len(self.source_image) == 1:
            del(self.source_image[self.scratchpad_image_index])
            self.add_image(event)
            self.scratchmode == True
            self.scratchpad_image_index=0
        Event('param_change', generator=self.parent)

    def next_image(self,event):    
        if len(self.source_image) > 1:
            if self.scratchpad_image_index < len(self.source_image) - 1:
                self.scratchpad_image_index +=1 
            else:
                self.scratchpad_image_index=len(self.source_image) - 1
        else: 
            self.scratchpad_image_index = 0

        print('next image', self.scratchpad_image_index)
        self.scratchmode = False
        self.display_in_scratchpad()



    def previous_image(self,event):    
        if len(self.source_image) > 1:    
            if self.scratchpad_image_index > 0:
                self.scratchpad_image_index -=1
            else:
                self.scratchpad_image_index=0
        else: 
            self.scratchpad_image_index = 0

        print('previous image', self.scratchpad_image_index)
        self.scratchmode = False
        self.display_in_scratchpad()


        print('index : ',self.scratchpad_image_index)

    def clear_scratchpad(self):
        self.scratch_canvas.delete('all')
    
    def move_crop_zone(self,event):
        x, y = event.x, event.y
        if self.scratch_canvas.old_coords:
            x1, y1 = self.scratch_canvas.old_coords
            self.center_x = self.source_image[self.scratchpad_image_index].center_x
            self.center_y = self.source_image[self.scratchpad_image_index].center_y
            self.source_image[self.scratchpad_image_index].center_x = self.center_x + (x1-x)/10
            self.source_image[self.scratchpad_image_index].center_y = self.center_y + (y1-y)/10
            self.source_image[self.scratchpad_image_index].crop_original_image()
            self.display_in_scratchpad()
    
    # zoom methods to be renamed zoom_
    def zoom_get_value(self,event):
        self.source_image[self.scratchpad_image_index].zoom_factor = int(self.zoom.get())
        self.source_image[self.scratchpad_image_index].crop_original_image()
        self.display_in_scratchpad()
        Event('param_change', generator=self.parent)

    def zoom_button1(self,event):
        self.v=int(self.zoom.get())
        self.old_coords = event.x, event.y

    def zoom_motion(self,event):
        xm1, ym1 = self.old_coords
        xm = event.x
        ym = event.y
        if abs(ym1-ym) >=20:
            self.v = int(self.v + (ym1-ym)/20)
            self.zoom.set(self.v)
            self.zoom_get_value(event)
            Event('param_change', generator=self.parent)
        old_coords = xm, ym
    def zoom_up(self,event):
        self.v=int(self.zoom.get())
        self.v +=1
        self.zoom.set(self.v)
        self.source_image[self.scratchpad_image_index].zoom_factor = int(self.zoom.get())
        self.source_image[self.scratchpad_image_index].crop_original_image()
        self.display_in_scratchpad()
        Event('param_change', generator=self.parent)

    def zoom_down(self,event):
        self.v=int(self.zoom.get())
        self.v -=1
        self.zoom.set(self.v)
        self.source_image[self.scratchpad_image_index].zoom_factor = int(self.zoom.get())
        self.source_image[self.scratchpad_image_index].crop_original_image()
        self.display_in_scratchpad()
        Event('param_change', generator=self.parent)

class scratchpad(image_sourceUI):  

    def __init__(self, parent, parentUI):
        super().__init__(parent, parentUI)
        self.drawing_palette()
        self.canvas()
        self.action_bar()

    def drawing_palette(self):
        self.palette = Frame(self.frame)
        self.palette_colors = ['red', 'green', 'blue','black','white']
        self.pen_color = StringVar()
        self.pen_color.set(self.palette_colors[1])
     
        for i in range(5):
            self.palet = Radiobutton(self.palette, variable=self.pen_color, value=self.palette_colors[i], bg=self.palette_colors[i])
            self.palet.grid(row=0,column=i,sticky='ew')

        self.stroke = StringVar()
        self.stroke.set(50)
        self.stroke_width = Entry(self.palette, width = 2,textvariable=self.stroke)

        # palette layout
        self.stroke_width.grid(row=0,column=5,sticky='ew')
        self.palette.grid(row=0, column=0,sticky='we')
        for i in range(6):
            self.palette.columnconfigure(i, weight=1)

    def button1_callback(self,event):
        self.get_mouse_coords(event)
    
    def B1_motion_callback(self,event):
        self.draw(event)
    
    def B1_release_callback(self,event):
        pass
        #Event('param_change', generator=self.parent)

    def draw(self,event):
        x, y = event.x, event.y

        if self.scratch_canvas.old_coords:
            x1, y1 = self.scratch_canvas.old_coords
            self.pen_size = int(self.stroke.get())

            if self.scratchmode:
                self.d = ImageDraw.Draw(self.image) 

            else:
                self.d = ImageDraw.Draw(self.source_image[self.scratchpad_image_index].image)

            self.d.line(((x, y), (x1, y1)), self.pen_color.get(), width=self.pen_size)
            
            if self.scratchmode:
                self.TKImage = ImageTk.PhotoImage(self.image)
            else :
                self.TKImage = ImageTk.PhotoImage(self.source_image[self.scratchpad_image_index].image)

            self.scratch_canvas.create_image((100,100),image=self.TKImage,anchor='center')
            self.scratch_canvas.old_coords = x, y
            #self.scratchmode = True
        
    def add_image(self,event):   
        if self.scratchmode:
            source = SourceImage(original= self.image)
            self.source_image.append(source)
            self.scratchpad_image_index = len(self.source_image)
        self.clear_scratchpad()
        self.image=Image.new("RGBA",(200,200),(255,255,255,0))
        self.scratchmode = True
        Event('param_change', generator=self.parent)
        print('scratch pad index', self.scratchpad_image_index)

class image_from_fileUI(image_sourceUI):
    def __init__(self, parent, parentUI):
        super().__init__(parent, parentUI)
        self.generator = parent
        self.image_from_file_palette()
        self.canvas()
        self.action_bar()

    def image_from_file_palette(self):
        self.palette = Frame(self.frame)
        self.palette.grid(row=0, column=0,sticky='we')

        self.load_button = Button(self.palette, text='Load', relief=FLAT, command=self.load_image)
        self.load_button.grid(row=0,column=0,sticky='ew')


        self.zoom_entry = Entry(self.palette, width = 4,textvariable=self.zoom)
        self.zoom_entry.grid(row=0,column=2,sticky='ew')

        #self.load_button.bind('<Button-1>',self.load_image)
        for i in range(2):
            self.palette.columnconfigure(i, weight=1)
        
        # bindings
        self.zoom_entry.bind('<Return>',self.zoom_get_value)
        self.zoom_entry.bind('<B1-Motion>',self.zoom_motion)
        self.zoom_entry.bind('<Button-1>',self.zoom_button1)
        self.zoom_entry.bind('<Up>',self.zoom_up)
        self.zoom_entry.bind('<Down>',self.zoom_down)

    # widget callbacks                

    def load_image(self):
        self.fileNames = filedialog.askopenfilename(multiple=True)
        for filename in self.fileNames:
            self.original = Image.open(filename).convert('RGBA')
            source = SourceImage(original= self.original)
            self.source_image.append(source)
            self.display_in_scratchpad()
        Event('param_change', generator=self.parent)

    def button1_callback(self,event):
        self.get_mouse_coords(event)
    
    def B1_motion_callback(self,event):
            self.move_crop_zone(event)
    
    def B1_release_callback(self,event):
        Event('param_change', generator=self.parent)

    def add_image(self,event):   
        self.load_image
    


class MaskUI(image_sourceUI):  

    def __init__(self, parent, parentUI):
        super().__init__(parent, parentUI)
        self.drawing_palette()
        self.canvas()
        self.action_bar()
        self.source_image = self.parent.mask
        self.image=Image.new("L",(200,200),0)
        self.display_in_scratchpad()

    def drawing_palette(self):
        self.palette = Frame(self.frame)
        self.load_button = Button(self.palette, text='Load', relief=FLAT, command=self.load_image)
        self.load_button.grid(row=0,column=0,sticky='ew')
        self.zoom_entry = Entry(self.palette, width = 4,textvariable=self.zoom)
        self.zoom_entry.grid(row=0,column=1,sticky='ew')
        self.palette_colors = ['black','white']
        self.pen_color = StringVar()
        self.pen_color.set(self.palette_colors[1])

        #bindings
        self.zoom_entry.bind('<Return>',self.zoom_get_value)
        self.zoom_entry.bind('<B1-Motion>',self.zoom_motion)
        self.zoom_entry.bind('<Button-1>',self.zoom_button1)
        self.zoom_entry.bind('<Up>',self.zoom_up)
        self.zoom_entry.bind('<Down>',self.zoom_down)
     
        for i in range(2):
            self.palet = Radiobutton(self.palette, variable=self.pen_color, value=self.palette_colors[i], bg=self.palette_colors[i])
            self.palet.grid(row=0,column=i+2,sticky='ew')

        self.stroke = StringVar()
        self.stroke.set(50)
        self.stroke_width = Entry(self.palette, width = 2,textvariable=self.stroke)

        # palette layout
        self.stroke_width.grid(row=0,column=5,sticky='ew')
        self.palette.grid(row=0, column=0,sticky='we')
        for i in range(6):
            self.palette.columnconfigure(i, weight=1)

    def button1_callback(self,event):
        self.get_mouse_coords(event)
    
    def B1_motion_callback(self,event):
        if len(self.source_image)>0:
            if self.source_image[self.scratchpad_image_index].mode == 'file':
                self.move_crop_zone(event)
            else :
                self.draw(event)
        else:
            self.draw(event)

    def B1_release_callback(self,event):
        Event('param_change', generator=self.parent)

    def draw(self,event):
        x, y = event.x, event.y

        if self.scratch_canvas.old_coords:
            x1, y1 = self.scratch_canvas.old_coords
            self.pen_size = int(self.stroke.get())

            if self.scratchmode:
                self.d = ImageDraw.Draw(self.image) 

            else:
                self.d = ImageDraw.Draw(self.source_image[self.scratchpad_image_index].image)

            self.brush_color = self.pen_color.get()
            if self.brush_color == 'white':
                self.brush_color = (255)
            elif self.brush_color == 'black':
                self.brush_color = (0)
            self.d.line(((x, y), (x1, y1)), self.brush_color, width=self.pen_size)

            self.display_in_scratchpad()            
            # if self.scratchmode:
            #     self.TKImage = ImageTk.PhotoImage(self.image)
            # else :
            #     self.TKImage = ImageTk.PhotoImage(self.source_image[self.scratchpad_image_index].image)

            # self.scratch_canvas.create_image((100,100),image=self.TKImage,anchor='center')
            self.scratch_canvas.old_coords = x, y
            #self.scratchmode = True
        
    def add_image(self,event):  
        if self.scratchmode:
            source = Mask(original= self.image, mode = 'draw')
            self.source_image.append(source)
            self.clear_scratchpad()
            self.image=Image.new("L",(200,200),0)
        self.scratchmode = True
        self.scratchpad_image_index = len(self.source_image)-1
        self.display_in_scratchpad()
        Event('param_change', generator=self.parent)
        print('scratch pad index', self.scratchpad_image_index) 
    
    def load_image(self):
        self.fileNames = filedialog.askopenfilename(multiple=True)
        for filename in self.fileNames:
            self.original = Image.open(filename).convert('RGBA')
            source = Mask(original= self.original, mode = 'file')
            self.source_image.append(source)
            self.display_in_scratchpad()
        Event('param_change', generator=self.parent)


class geometry_strategy_selectorUI():
    def __init__(self, parent, parentUI, options):
        super().__init__()
        self.parent = parent
        self.option = StringVar(parentUI)
        self.option.set(options[0]) # default value
        self.control_panel = self.parent.geometry_panel
        w = OptionMenu(self.control_panel, self.option, *options, command=self.callback)
        w.grid(row=0, sticky='ew')
    
    def callback(self, selected_strategy):
        setattr(self.parent,'geometry_strategy',selected_strategy)
        Event('geometry_strategy_change',generator=self.parent)

class image_source_strategy_selectorUI():
    def __init__(self, parentUI, options):
        super().__init__()
        self.control_panel = parentUI
        self.option = StringVar()
        self.option.set(options[0]) # default value
        w = OptionMenu(self.control_panel, self.option, *options, command=self.callback)
        w.grid(row=0, column= 0, sticky='ew')
        #self.control_panel.columnconfigure(0,minsize=120)
    
    def callback(self, selected_strategy):
        #setattr(self.parent,'image_source_strategy',selected_strategy)
        Event('image_source_strategy_change',generator=self)
