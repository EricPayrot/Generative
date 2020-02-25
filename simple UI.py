from tkinter import *
rectangle=None
old_coords=[0,0]


def update():
    global rectangle
    if rectangle == None: 
        rectangle = myCanvas.create_rectangle(250-int(x.get())/2,250-int(y.get())/2,250+int(x.get())/2,250+int(y.get())/2)
    myCanvas.coords(rectangle,250-int(x.get())/2,250-int(y.get())/2,250+int(x.get())/2,250+int(y.get())/2)
    labeltext.set('x coord = '+str(x.get()))

def button1(event):
    global value, old_coords
    value = int(x.get())
    old_coords = event.x, event.y
    #print('value on button click ',value)

def motion(event):
    global old_coords, value
    xm1, ym1 = old_coords
    xm = event.x
    ym = event.y
    value = value + (ym1-ym)
    x.set(value)
    old_coords = xm, ym
    #print('ym ',ym,'ym1 ',ym1,'value: ',value)
    update()

root=Tk()
root.geometry("640x500+10+0")
x = StringVar()
y = StringVar()
labeltext = StringVar()

x.set(10)
y.set(10)
labeltext.set('x coord = '+str(x.get()))

myCanvas = Canvas(root, bg="white", height=500, width=500)
UI=Frame(root,height=500, width=100, borderwidth=1, relief='groove')

xcoordlabel = Label(UI,text='x = ',textvariable=labeltext)
xcoord = Entry(UI,textvariable=x)

ycoordlabel = Label(UI,text='y coord',justify='left')
ycoord = Entry(UI,textvariable=y)

mybutton = Button(UI,text='update',command=update)

UI.pack()
myCanvas.pack()
myCanvas.place(relx=0.01,anchor='nw')
xcoordlabel.pack()
xcoord.pack()
ycoordlabel.pack()
ycoord.pack()
mybutton.pack()
UI.pack(fill=None, expand=False)
UI.place(relx=1,rely=0,anchor='ne')

xcoord.bind('<B1-Motion>',motion)
xcoord.bind('<Button-1>',button1)

root.mainloop()


    