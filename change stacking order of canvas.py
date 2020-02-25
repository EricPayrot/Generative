from tkinter import*

class test():
    def __init__(self):
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.frame_list = []
        self.frame_list.append(self.frame1)
        self.frame_list.append(self.frame2)

        self.canvas1 = Canvas(self.frame_list[0],bg='red', width=100, height=100)
        self.canvas2 = Canvas(self.frame_list[1],bg='yellow', width=100, height=100)

        self.frame1.grid(row=0,column=0)
        self.frame2.grid(row=0,column=0)
        self.canvas1.grid(row=0,column=0)
        self.canvas2.grid(row=0,column=0)
        

        self.canvas_list=[]
        self.canvas_list.append(self.canvas1)
        self.canvas_list.append(self.canvas2)


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