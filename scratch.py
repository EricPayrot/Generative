import tkinter as tk

root = tk.Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

canvas=tk.Canvas(root, bg="white", height=500, width=500)
canvas.grid()

for i in range(10):
    rectwidth=10+i*10
    rectheight=7+i*50
    rect=canvas.create_rectangle(10*i,10*i,10*i+rectwidth,10*i+rectheight,fill='red',outline='blue')
    #rect.grid(column=0,row=0,)
    


root.mainloop()