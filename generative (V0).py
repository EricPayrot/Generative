from tkinter import*
from PIL import Image, ImageDraw
import os
#import aggdraw

class app():
    def __init__(self,parent, height, width):
        #define main containers
        self.output_canvas = Canvas(parent,bg='red', width=width, height=height)
        self.control_panel = Frame(parent,height=height,width=100,padx=3)
        
        # layout the main containers
        self.output_canvas.grid(row=1,column=0, sticky ='nw')
        self.control_panel.grid(row=1, column=1,sticky ='ne')
    
class param_widget():
    def __init__(self,parent,value,name,**kwargs):
            
            # define widgets
            self.widget = Frame(parent)
            self.name = name
            self.label = Label(self.widget,text=self.name)            
            self.value = StringVar()
            self.value.set(value)
            self.min = kwargs.get('min',None)
            self.max = kwargs.get('max',None)
            self.validate_cmd = kwargs.get('validatecommand',None)
            self.validate = kwargs.get('validate',False)
            if self.validate:
                self.validate_cmd=validate_value
            self.entry = Entry(self.widget, textvariable=self.value,vcmd=self.validate_cmd)
            
            # layout widgets
            self.widget.grid()            
            self.label.grid(row=0,column=0)
            self.entry.grid(row=0,column=1)
            
            # bindings
            self.entry.bind('<Return>',self.get_value)

    # widget callbacks                
    def get_value(self,event):
        print(self.name,' =  ',self.value.get())
    
    def validate_value(self,event):
        if self.entry.get()>self.min:
            if self.entry.get()<self.max:
                return True
        else:
            return False

class scratchpad():  
    canvas=[]
    def __init__(self,parent):
            self.frame =Frame(parent)

            # palette widgets
            self.palette = Frame(self.frame)
            self.palette_colors = ['red', 'green', 'blue','black',None]

            self.pen_color = StringVar()
            self.pen_color.set(self.palette_colors[1])
            
            for i in range(5):
                self.palet = Radiobutton(self.palette, variable=self.pen_color, value=self.palette_colors[i], bg=self.palette_colors[i])
                self.palet.grid(row=0,column=i,sticky='ew')

            self.stroke = StringVar()
            self.stroke.set(5)
            self.stroke_width = Entry(self.palette, width = 2,textvariable=self.stroke)

            # palette layout
            self.stroke_width.grid(row=0,column=5,sticky='ew')
            
            # scratchpad canvas
            self.scratchpad_frame = Frame(self.frame)
            self.scratch_canvas = Canvas(self.scratchpad_frame,bg='white',borderwidth=1, width=200, height=200)
           
            # PIL image for image save - replicates what's being drawn on canvas
            self.image=Image.new("RGB",(200,200),(255,255,255))
            
            # action bar widgets
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

            # scratchpad layout
            self.frame.grid(pady=10)

            self.palette.grid(row=0, column=0,sticky='we')
            for i in range(6):
                self.palette.columnconfigure(i, weight=1)

            self.scratchpad_frame.grid(row=1,column=0)
            self.scratch_canvas.grid(row=0,column=0)
        
            self.action_bar.grid(row=2,column=0, sticky='we')           
            for i in range(4):
                self.action_bar.columnconfigure(i, weight=1)
            
            # scratchpad bindings
            self.scratch_canvas.bind('<Button-1>',self.new_line)
            self.scratch_canvas.bind('<B1-Motion>',self.draw)
            self.add.bind('<Button-1>',self.add_image)
            self.delete.bind('<Button-1>',self.delete_image)
            self.previous.bind('<Button-1>',self.previous_image)
            self.next.bind('<Button-1>',self.next_image)
    
    # scratchpad callbacks
    def draw(self,event):
        x, y = event.x, event.y

        if self.scratch_canvas.old_coords:
            x1, y1 = self.scratch_canvas.old_coords
            self.pen_size = int(self.stroke.get())
            self.scratch_canvas.create_line(x, y, x1, y1, width=self.pen_size, smooth='true', capstyle=ROUND,fill=self.pen_color.get())
            self.draw=ImageDraw.Draw(self.image)        
            self.draw.line(((x, y), (x1, y1)), self.pen_color.get(), width=self.pen_size)
            self.scratch_canvas.old_coords = x, y
        
    def new_line(self,event):
        self.scratch_canvas.old_coords = event.x,event.y
        print ('pen color : ', self.pen_color.get())  

    def add_image(self,event):
        print('save image')      
        self.savepath = r'scratchpad'
        if not os.path.exists(self.savepath):
            os.makedirs(self.savepath,mode=0o755)
        self.filename = self.savepath + '/' + 'scratch' + str(1) + '.png'
        self.image.save(self.filename)

    def delete_image(self,event):
        print('remove image')

    def next_image(self,event):
        print('next image', self.frame1)

    def previous_image(self,event):
        print('previous image')


#_____ app__________________________________________________________________
root=Tk()
root.title('My application')
myApp = app(root,width=500,height=500)
param1widget = param_widget(parent=myApp.control_panel,value=100,name='param1',min=3,max=10)
param2widget = param_widget(parent=myApp.control_panel,value=10,name='param2')
scratchpad = scratchpad(parent=myApp.control_panel)

root.mainloop()