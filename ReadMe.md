Medical Image Analysis Application

About :
This is an application interface for analyzing medical image data. Currently used for tumor classification from MRI image. Created using Python3.8

Created by : Izzun Nafis Ibadik and Dimas Sofyan Ashari from Universitas Gadjah Mada  

Installation :
- Make sure that you already install python along with the pip package manager
- Please check the requirements.txt and install its dependency manually or
- go to this program directory in terminal and type 'pip install -r requirements.txt'

Preparation :
Please set your folder into the following format :
(Working directory)
├───main.py
├───process_thread.py
├───gui.py
├───summary.py
├───information.py
├───requirements.txt
├───Dataset
│   └───Dataset folder 1
│   └───Dataset folder 2
│   └───Dataset folder ...
├───model
│   ├───model_LU_Net
│   └───model_Improved_Resnet50
└───Result
      ├───Classification Result folder1
      ├───Classification Result folder2
      └───Classification Result ...

Run :
- go to the program directory in terminal
- type 'python main.py'

Feature :
- Loading multiple images
- Navigate to all loaded images
- Choose from two inserted model: Improved Resnet50 or LU-Net
- Classify all the image
- Compare the classification result with validation value from the image*
- Show the summary of the classification result, include with confusion matrix and performance measurement
- Save the image data into some separate folder corresponding to the classification result
- Save the summary result into some CSV file
- Information page 

*It only appears when your image file or your image folder contains the tumor name, else it will show "No Data"


Credit :
In this application we use the deep learning model from the following paper :

Improved Resnet50 :
Çinar, Ahmet, Yildirim, Muhammed. Detection of tumors on brain MRI images using the hybrid convolutional neural network architecture. Medical Hypotheses. 139, 2020, 109684.

LU-Net :
 Hari Mohan Rai, Kalyan Chatterjee.Detection of brain abnormality by a novel Lu-Net deep neural CNN model from MR images. 2020. https://www.sciencedirect.com/science/article/pii/S2666827020300049