# NDVI_calculation
This is the first python project which was initially programmed to calculated the ndvi values from landsat imageries. It was futher improved to crop the imagery to study area extent and also to display the imageries in the screen. So, this program can be used to:
1. Crop imagery to the study area extent
2. Calculate NDVI values from landsat imagery
3. Compare the ndvi values of different ties using subplotting

The initial user interface of this program looks as shown below. There are two canvas in this ui whose task are described:
## Button canvas
Button canvas holds five buttons whose tasks are as follows:
1.Add: This button is used to add the files from the local directories. After we choose a file, the file name is displated with a clickable button. If we press the               button, the image is viewed in next interface.
2.Calculate: This button is used to calculate the image from the files added in the screen. 
3.Compare: This button is used to compared the NDVI values of different periods, which is calculated using calculate button
4.sub plot: This image is used to sub-plot the three images on the same interface
5.Mask image: This area is used to mask the resulted or raw image by the study area of the project.

## Main canvas
The main canvas is for holding the input image and outputs from the program and the image files can be clicked to view the image on next interface.

