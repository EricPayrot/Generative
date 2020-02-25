from tkinter import*
from PIL import Image, ImageDraw
import os, random, glob
from Observer import Observer, Event
from imageClip import ImageClip
from UserInterface import*
from datetime import datetime

class Application(Observer.Observer):
    def __init__(self):
        super().__init__()
        self.root=Tk()
        self.root.title('Maya the best')
        self.myApp = appUI(root,width=500,height=500)
        self.output_canvas = self.myApp.output_canvas
        self.control_panel = self.myApp.control_panel

class Layer(Observer.Observer):
    def __init__(self, parent):
        super().__init__()
        self.layerID = None
        self.layer_name = None
        self.layer_stack_position = 0
        self.parent = parent
        self.canvas = self.parent.canvas
        self.layer_panel = Frame(self.parent)




    def add_layer(self):
        print('add layer')

    def remove_layer(self):
        print('remove layer')

    def move_layer_up(self):
        print('move layer up')

    def move_layer_down(self):
        print('move layer down')
    
    def show_layer(self):
        print('show layer')

    def hide_layer(self):
        print('hide down')

