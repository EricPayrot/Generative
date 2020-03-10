
from __future__ import division  # we need floating division
from svgpathtools import*
from tkinter import*
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk
import itertools
import numpy as np
import math
import os

# svgpath = """m 76,232.24998 c 81.57846,-49.53502 158.19366,-20.30271 216,27 61.26714,
# 59.36905 79.86223,123.38417 9,156 
# -80.84947,31.72743 -125.19991,-53.11474 -118,-91 v 0 """

svgpath = "M7,196,144,74l122,80L394,48,501,166" #multiline
#svgpath = "M27,161c35.08-47.72,88-106.9,137-97,39.74,8,46.43,55.33,92,80,34.17,18.5,93.78,26.2,204-33" #curves
#svgpath = "M394,368H97V71h297V368z" #square
#svgpath = "M412,242c0,89.47-72.53,162-162,162S88,331.47,88,242S160.53,80,250,80S412,152.53,412,242z" #circle

# circle path
# top_half = Arc(start=-1, radius=1+2j, rotation=0, large_arc=1, sweep=1, end=1)
# bottom_half = top_half.rotated(180)
# circle = Path(top_half, bottom_half)

svgpaths = []
svgpaths.append("M44,114c21.39-25.04,53.62-54.11,92-53c38.12,1.1,54.87,31.17,91,46c34.61,14.2,90.46,15.84,183-42")
svgpaths.append("M55,200c47.31-45.39,85.75-54.23,112-54c59.15,0.51,85.04,47.32,149,52c46.99,3.44,86.97-17.89,113-36")
svgpaths.append("M65,277c26.06-23.29,64.9-49.78,113-51c54.59-1.39,79.44,30.82,132,30c30.43-0.48,73.03-12.07,124-63")

paths = []

for svgpath in svgpaths :
    path = parse_path(svgpath)
    paths.append(path)

root = Tk()
canvas = Canvas(root,width=500,height=500,bg = 'white')
canvas.pack()

#draw path
n = 1000  # number of line segments to draw
image = Image.new('RGB',(500, 500), 'white')
d=ImageDraw.Draw(image)

for path in paths:
    pts = [ (p.real,p.imag) for p in (path.point(i/n) for i in range(0, n+1))]
    d.line(pts, 'black', width=5)

# find clip points
image_path = filedialog.askopenfilename()
#image_path = r"C:\Users\100004614\Pictures\source images\test"
m = 10
r = 3
s = 40

picture = Image.open(image_path).convert('RGBA').resize((s,s), resample=3)

for path in paths:
    clip_pts =  [ (int(p.real),int(p.imag)) for p in (path.point(i/m) for i in range(0, m+1))]
    clip_normals = [(n.real, n.imag) for n in (path.normal (i/m) for i in range(0,m+1))]

    for clip_pt in clip_pts:
        x1 = clip_pt[0]-r
        y1  = clip_pt[1]-r
        x2 = clip_pt[0]+r
        y2  = clip_pt[1]+r
        box = (x1,y1,x2,y2)
        #d.ellipse(box, fill='red', outline=None)

    for (clip_pt,clip_normal) in zip(clip_pts,clip_normals):
        normal = (clip_pt[0]+30*clip_normal[0],clip_pt[1]+30*clip_normal[1])
        #d.line((clip_pt,normal), 'black', width=1)

    # define rotation angle for clip
    vertical_vector = [0, 100]
    unit_vector_1 = vertical_vector / np.linalg.norm(vertical_vector)
    clip_angles = []

    for clip_normal in clip_normals:
        normal = np.complex(clip_normal[0],clip_normal[1])
        vertical = np.complex(vertical_vector[0],vertical_vector[1])
        angle = np.angle((normal,vertical), deg = True)
        clip_angles.append(angle[0])  #vs vertical axis

    # draw an angled square for each point
    for (pt,angle) in zip(clip_pts,clip_angles):
        clip_image = Image.new('RGBA',(s, s), (0,0,0,0))
        d1=ImageDraw.Draw(clip_image)
        d1.line((s/2,0,s/2,s-5), 'white', width=1)
        clip_image.paste(picture,(0,0), picture)
        clip_image = clip_image.rotate(270-angle, expand=True)

        # calculate the new size of rotated image
        a = int(abs(s * math.sin(-angle)) + abs(s * math.cos(-angle)))
        b = int(abs(s * math.cos(-angle)) + abs(s * math.sin(-angle)))
        clip_image.resize((a,b),resample=3)

        nwcorner = (int(pt[0]-a/2),int(pt[1]-b/2))
        image.paste(clip_image,nwcorner, clip_image)

#display image
TKImage = ImageTk.PhotoImage(image)
canvas.create_image((250,250),image=TKImage,anchor='center')

root.mainloop()


