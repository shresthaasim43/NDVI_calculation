from tkinter import *
from tkinter.ttk import * 
from tkinter.filedialog import askopenfilename, asksaveasfilename

from functools import partial
import matplotlib
import matplotlib.pyplot as plt

import fiona
import rasterio
import rasterio.mask
from rasterio.plot import show

import numpy as np

W,H = 500,700

TIFF_NAMES = ['Choose Band']
TIFF_FILES = [None]
TIFF_IMAGES = [None]
CANVAS_LIST = [None]

WINDOW = Tk()
WINDOW.geometry('+10+10') #window starting from 10,10
WINDOW.geometry('{}x{}'.format(W,H)) #set the geomentry of WINDOW
WINDOW.title("Normalization Difference Vegetation Index") 


style = Style()  
style.configure('W.TButton', font =('calibri', 12, 'bold', 'underline'), 
               foreground = 'blue', borderwidth = '4', height=5, width=10) 

def calculation(buttonType,selection1,selection2):
    in1 = TIFF_NAMES.index(str(selection1.get()))
    in2 = TIFF_NAMES.index(str(selection2.get()))

    tif1_value = TIFF_FILES[in1] #red tif
    tif2_value = TIFF_FILES[in2]   #nir tif
    tif_Im = TIFF_IMAGES[in2]

    saveFileName = asksaveasfilename()
    if '.tif' not in saveFileName:
        saveFileName += '.tif'

    '''Calculate NDVI from integer arrays '''
    if buttonType == 'calculate':
        nir , red = tif2_value, tif1_value
        nir = nir.astype('f4')
        red = red.astype('f4')
        ndvi = (nir - red) / (nir + red)
        result = ndvi
    else:
        result = tif2_value - tif1_value

    with rasterio.open(
        saveFileName,
        'w',
        driver='GTiff',
        height=tif_Im.shape[0],
        width=tif_Im.shape[1],
        count=1,
        dtype='float32',
        crs='+proj=latlong',
        transform=tif_Im.transform,
    ) as resulted_TIF:
        resulted_TIF.write(result, 1)
    
    fileNameOnly = saveFileName.split('/')[-1]
    name = fileNameOnly.split('.')[0] 

    TIFF_FILES.append(result)
    TIFF_NAMES.append(name)
    TIFF_IMAGES.append(resulted_TIF)
    addToCanvas(name)
    Window2.destroy()

def showImageFromCanvas(index,event):
    plt.imshow(TIFF_FILES[index], cmap='RdYlGn')
    plt.colorbar(shrink=0.5)
    plt.title(TIFF_NAMES[index])
    plt.show()

def func(*arg):
    pass

def openWindow2(buttonType):
    global Window2
    Window2 = Tk()
    
    canvas = Canvas(Window2,width=350,height=250)
    canvas.place(x=1,y=1, anchor=NW)

    Window2.geometry('350x250+250+250')  
    
    variable1 = StringVar(Window2)
    variable1.set(TIFF_NAMES[0]) # default value
    w1 = OptionMenu(Window2, variable1, *TIFF_NAMES)
    w1.config(width=20)
    dropdown1 = canvas.create_window(5,35,window=w1,anchor=NW)
    variable1.trace('w',func)

    variable2 = StringVar(Window2)
    variable2.set(TIFF_NAMES[0]) # default value
    w2 = OptionMenu(Window2, variable2, *TIFF_NAMES)
    w2.config(width=20)
    dropdown2 = canvas.create_window(5,85,window=w2,anchor=NW)
    variable2.trace('w',func)
    

    if buttonType == 'compare':
        Window2.title('Compare NDVI')
        label1 = canvas.create_text((5,5), text="NDVI Image 1", font="MSGothic 15 ", fill='#000000',anchor=NW)
        label2 = canvas.create_text((5,60), text="NDVI Image 2", font="MSGothic 15 ", fill='#000000',anchor=NW)
        saveAs_btn = Button(Window2, text='Compare and Save As',command=partial(calculation, 'compare',variable1,variable2) )
    elif buttonType == 'calculate':
        Window2.title('Calculate NDVI')
        label1 = canvas.create_text((5,5), text="Input Red Band", font="MSGothic 15 ", fill='#000000',anchor=NW)
        label2 = canvas.create_text((5,60), text="Input NIR Band", font="MSGothic 15 ", fill='#000000',anchor=NW)
        saveAs_btn = Button(Window2,text='Calculate and Save As',command=partial(calculation, 'calculate',variable1,variable2) )
    else:
        Window2.title('Show Sub Plot')
        label1 = canvas.create_text((5,5), text="Figure 1", font="MSGothic 15 ", fill='#000000',anchor=NW)
        label2 = canvas.create_text((5,60), text="Figure 2", font="MSGothic 15 ", fill='#000000',anchor=NW)
        label3 = canvas.create_text((5,115), text="Figure 3", font="MSGothic 15 ", fill='#000000',anchor=NW)

        variable3 = StringVar(Window2)
        variable3.set(TIFF_NAMES[0]) # default value
        w3 = OptionMenu(Window2, variable3, *TIFF_NAMES)
        w3.config(width=20)
        dropdown2 = canvas.create_window(5,140,window=w3,anchor=NW)
        variable3.trace('w',func)
        saveAs_btn = Button(Window2, text='Show Sub plot',command=partial(showSubPlot,variable1,variable2,variable3) )

    SaveAs_btn = canvas.create_window(200,75,window=saveAs_btn,anchor=NW)
    Window2.mainloop()

def openTif_File():
    global tif_filePath, tif_fileName
    tif_filePath = askopenfilename(initialdir = "/",title = "Select file",
                        filetypes = (("tif images","*.tif"),("all files","*.*")))
    temp2 = tif_filePath.split('/')[-1]
    tif_fileName = temp2.split('.')[0]

def openShapeFile():
    global shapeFilepath, shapeFileName
    shapeFilepath =  askopenfilename(initialdir = "",title = "Select file",
                        filetypes = (("all files","*.*"),("tif images","*.tif")))
    temp = shapeFilepath.split('/')[-1]
    shapeFileName = temp.split('.')[0]

def maskWindow():
    global Window3
    Window3 = Tk()
    
    canvas = Canvas(Window3,width=350,height=250)
    canvas.place(x=1,y=1, anchor=NW)
    Window3.title('Mask Image')
    Window3.geometry('350x250+250+250')

    label1 = canvas.create_text((5,5), text=" ", font="MSGothic 15 ", fill='#000000',anchor=NW)
    shapeFile_btn = Button(Window3, text='Open Shape File',command=openShapeFile)
    ShapeFIle_btn = canvas.create_window(100,5,window=shapeFile_btn,anchor=NW)
# comments 123
    label2 = canvas.create_text((5,60), text=" ", font="MSGothic 15 ", fill='#000000',anchor=NW)
    tif_file_btn = Button(Window3, text='Open Tif File',command=openTif_File)
    Tif_file_btn = canvas.create_window(100,75,window=tif_file_btn,anchor=NW)

    saveAs_btn = Button(Window3, text='Mask and Save as',command=maskImage)
    SaveAs_btn = canvas.create_window(100,150,window=saveAs_btn,anchor=NW)
    Window3.mainloop()

def maskImage():
    saveFileName = asksaveasfilename()
    if '.tif' not in saveFileName:
        saveFileName += '.tif'

    with fiona.open(shapeFilepath)as shapefile:
        shapes=[feature["geometry"] for feature in shapefile]

    with rasterio.open(tif_filePath) as src:
        out_image,out_transform=rasterio.mask.mask(src,shapes,crop=True)
        out_meta=src.meta
        
    out_meta.update({"driver": "GTiff","height": out_image.shape[1],"width": out_image.shape[2],"transform": out_transform})
    with rasterio.open(saveFileName, "w", **out_meta) as dest:
        dest.write(out_image)

def showSubPlot(selection1,selection2,selection3):
    in1 = TIFF_NAMES.index(str(selection1.get()))
    in2 = TIFF_NAMES.index(str(selection2.get()))
    in3 = TIFF_NAMES.index(str(selection3.get()))

    result1 = TIFF_FILES[in1]
    result2 = TIFF_FILES[in2]
    result3 = TIFF_FILES[in3]

    fig, axes = plt.subplots(1,3, figsize=(14,6), sharex=True, sharey=True)
    plt.sca(axes[0])
    plt.imshow(result1, cmap='RdYlGn', vmin=-1, vmax=1)
    plt.colorbar(shrink=0.5)
    plt.title(TIFF_NAMES[in1])
    plt.xlabel('Column #')
    plt.ylabel('Row #')

    plt.sca(axes[1])
    plt.imshow(result2, cmap='RdYlGn', vmin=-1, vmax=1)
    plt.colorbar(shrink=0.5)
    plt.title(TIFF_NAMES[in2])

    plt.sca(axes[2])
    plt.imshow(result3, cmap='bwr', vmin=-1, vmax=1)
    plt.colorbar(shrink=0.5)
    plt.title(TIFF_NAMES[in3])
    plt.show()

def removeCanvas(name):
    idx = TIFF_NAMES.index(name)
    canvas = CANVAS_LIST[idx]
    tif_name = TIFF_NAMES[idx]
    tif_file = TIFF_FILES[idx]
    canvas.delete('all')
    CANVAS_LIST.pop(idx)
    TIFF_FILES.pop(idx)
    TIFF_NAMES.pop(idx)
    MAIN_CANVAS.delete('all')
    rect = MAIN_CANVAS.create_rectangle(5,5,W-10, H*.91-10)
    for i, canvas in enumerate(CANVAS_LIST[1:]):
        canvas.place(x=10,y = 10+i*75, anchor=NW)

def openImage():
    filename = askopenfilename(initialdir = "",title = "Select file",
                        filetypes = (("tif images","*.tif"),("all files","*.*")))
    
    if filename == '':
        return
    
    with rasterio.open(filename) as src:
        tiff = src.read(1)

    TIFF_FILES.append(tiff)
    TIFF_IMAGES.append(src)
    #TIFF_NAMES.append(tiff) #for later use and calculation

    
    fileNameOnly = filename.split('/')[-1]
    name = fileNameOnly.split('.')[0] 

    TIFF_NAMES.append(name)
    addToCanvas(name)

def addToCanvas(name):
    #add details to the left canvas
    height = 10 + (len(CANVAS_LIST)-1)*(H*.07)
    canvas= Canvas(MAIN_CANVAS, width=W*.95 ,height=H*.06)
    CANVAS_LIST.append(canvas)
    canvas.bind("<Button-1>", partial(showImageFromCanvas,len(CANVAS_LIST)-1))
    canvas.place(x=10,y = height, anchor=NW)

    btn_rect = canvas.create_rectangle(3,3,W*.95-1,H*.06)
    label = canvas.create_text((10,10), text= name, font="MSGothic 12 bold", fill="#000000",anchor=NW)
    remove_btn = Button(canvas,text='X',width=2,command=partial(removeCanvas,name))
    Remove_btn = canvas.create_window(W*.95-30,8,window=remove_btn,anchor=NW)

#canvas for buttons
BUTTON_CANVAS = Canvas(WINDOW,width=W,height=H*.08)
BUTTON_CANVAS.place(x=1,y=1, anchor=NW)
btn_rect = BUTTON_CANVAS.create_rectangle(5,5,W-10,H*.08-5)

#main canvas with checkbox and file name
MAIN_CANVAS = Canvas(WINDOW,width=W,height=H*.91)
MAIN_CANVAS.place(x=1,y=H*.08, anchor=NW)
left_rect = MAIN_CANVAS.create_rectangle(5,5,W-10, H*.91-10)

add_btn = Button(WINDOW,text='Add',style='W.TButton',command=openImage)
Place_Add_btn = BUTTON_CANVAS.create_window(10,13,window=add_btn,anchor=NW)

calculate_btn = Button(WINDOW,text='Calculate',style='W.TButton',command=partial(openWindow2,'calculate'))
Place_Calculate_btn = BUTTON_CANVAS.create_window(105,13,window=calculate_btn,anchor=NW)

compare_btn = Button(WINDOW,text='Compare',style='W.TButton',command=partial(openWindow2,'compare'))
Place_Compare_btn = BUTTON_CANVAS.create_window(200,13,window=compare_btn,anchor=NW)

showSubplot_btn = Button(WINDOW,text='Sub Plot',style='W.TButton',command=partial(openWindow2,'showSubPlot'))
Place_ShowSubplot_btn = BUTTON_CANVAS.create_window(295,13,window=showSubplot_btn,anchor=NW)

mask_btn = Button(WINDOW,text='Mask Image',style='W.TButton',command=maskWindow)
Place_Mask_btn = BUTTON_CANVAS.create_window(390,13,window=mask_btn,anchor=NW)

WINDOW.mainloop()


