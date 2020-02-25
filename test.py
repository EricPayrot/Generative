from tkinter import*

class test():
    def __init__(self):
        self.frame_list = []      
        self.frame0 = Frame(root)
        self.frame_list.append(self.frame0)
        self.canvas0 = Canvas(self.frame_list[0],bg='red', width=100, height=100)
        self.frame0.grid(row=0,column=0)        
        self.canvas0.grid(row=0,column=0)
        
    def add_canvas(self):
        new_frame=Frame(root)
        self.frame_list.append(new_frame)
        new_canvas=Canvas(new)
        self.ca

    def printvar(self):
        print('canvas : ',self.canvas1)
        print('canvas2 : ',self.canvas2)
        print('canvas list : ',self.canvas_list)
        print('canvas_list element 0 : ', self.canvas_list[0])
        print('canvas_list element 1 : ', self.canvas_list[1])
        print('frame list : ',self.frame_list) 
        self.frame_list[0].lift()
        

root=Tk()
t=test()
t.printvar()
root.mainloop()