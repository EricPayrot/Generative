from tkinter import*
from PIL import Image, ImageDraw
import os, random, glob
#from Observer import Observer, Event
from imageClip import ImageClip
from UserInterface import*
from Generator import*


class ImageSource():
    def __init__(self, parent, strategy=None):
        super().__init__()
        self.parent=parent
        self.strategy = strategy
        self.instance = self.strategy(parent = self.parent)
        # UI

    def get_source_image(self):
        return self.instance.source_image
    
    def delete(self):
        print('delete', self.instance)
        self.instance.destroyUI()
        self.instance.source_image.clear()
        del self.instance

class Geometry():
    def __init__(self, parent, strategy=None):
        super().__init__()
        self.parent=parent
        self.strategy = strategy
        self.instance = self.strategy(parent = self.parent)
        # UI
    def update(self):
        self.instance.update()

    def get_coordinates(self):
        return self.instance.coordinates
    
    def get_clip_sizes(self):
        return self.instance.clip_sizes
    
    def delete(self):
        print('delete', self.instance)
        self.instance.delete_param_widgets()
        del self.instance



