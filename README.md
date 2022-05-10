# NDVI_calculation
## Introduction
Normalized Difference Vegetation Index (NDVI) quantifies vegetation by measuring the difference between near-infrared (which vegetation strongly reflects) and red light (which vegetation absorbs). Its value ranges from -1 to 1. The formula for calculation of NDVI is:<br>
            ![NDVI equation](https://github.com/shresthaasim43/NDVI_calculation/raw/newBranch/Assets/NDVI_equation.JPG)

This program can be used to:
1. Crop imagery to the study area extent
2. Calculate NDVI values from landsat imagery
3. Compare the ndvi values of different periods 
4. Visualise the difference of different time periods using subplotting.

The initial user interface of this program looks as shown below:<br>
![initial UI](https://github.com/shresthaasim43/NDVI_calculation/raw/newBranch/Assets/First_Interface.JPG)

There are two canvas in this UI namely: Button canvas and Main Canvas which are described below:<br>
## Button canvas
Button canvas holds five buttons whose tasks are as follows:
1. Add: This button is used to add the files from the local directories. After we choose a file, the file name is displayed on main canvas, which can be clicked to view the image and closed using close button.<br>

2. Calculate: This button is used to calculate the image from the files added in the main canvas. <br>
![initial UI](https://github.com/shresthaasim43/NDVI_calculation/raw/newBranch/Assets/Calculate_Button.JPG)<br>

3. Compare: This button is used to compare the NDVI values of different periods, which is calculated using calculate button<br>
![compare window](https://github.com/shresthaasim43/NDVI_calculation/raw/newBranch/Assets/Compare_Button.JPG)

4. Subplot: This button is used to sub-plot the three images on the same interface. For example; 2 images of different times and their comaparison.<br>
![subplot window](https://github.com/shresthaasim43/NDVI_calculation/raw/newBranch/Assets/Subplot_Button.JPG)
5. Mask image: This area is used to mask the resulted or raw image by the study area of the project.<br>
![mask window]{ width : 200px; }(https://github.com/shresthaasim43/NDVI_calculation/raw/newBranch/Assets/Mask_Image_Button.JPG )

## Main canvas
The main canvas is for holding the input image and outputs from the program. A user can click on the files to view the imagery on another window. 


