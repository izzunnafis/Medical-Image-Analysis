# Medical Image Analysis Application

### About : <br/>
This is an application interface for analyzing medical image data. Currently used for tumor classification from MRI image. Created using Python3.8

Created by : Izzun Nafis Ibadik and Dimas Sofyan Ashari from Universitas Gadjah Mada  

### Installation :<br/>
- Make sure that you already install python along with the pip package manager
- Please check the requirements.txt and install its dependency manually or
- go to this program directory in terminal and type 'pip install -r requirements.txt'

### Preparation :<br/>
Please set your folder into the following format :<br/>
(Working directory)<br/>
├───main.py<br/>
├───process_thread.py<br/>
├───gui.py<br/>
├───summary.py<br/>
├───information.py<br/>
├───requirements.txt<br/>
├───Dataset<br/>
│   └───Dataset folder 1<br/>
│   └───Dataset folder 2<br/>
│   └───Dataset folder ...<br/>
├───model<br/>
│   ├───model_LU_Net<br/>
│   └───model_Improved_Resnet50<br/>
└───Result<br/>
      ├───Classification Result folder1<br/>
      ├───Classification Result folder2<br/>
      └───Classification Result ...<br/>

### Run :<br/>
- go to the program directory in terminal
- type 'python main.py'

### Feature :
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


### Credit :
In this application we use the deep learning model from the following paper :

- Improved Resnet50 :<br/>
Çinar, Ahmet, Yildirim, Muhammed. Detection of tumors on brain MRI images using the hybrid convolutional neural network architecture. Medical Hypotheses. 139, 2020, 109684.

- LU-Net :<br/>
 Hari Mohan Rai, Kalyan Chatterjee.Detection of brain abnormality by a novel Lu-Net deep neural CNN model from MR images. 2020. https://www.sciencedirect.com/science/article/pii/S2666827020300049