# This Python file uses the following encoding: utf-8
import sys
import os

import gui
import process_thread
import PyQt5
import model
import tensorflow as tf
import cv2
import numpy as np
import pandas as pd
from PIL import Image

app = PyQt5.QtWidgets.QApplication(sys.argv)
window1 = PyQt5.QtWidgets.QMainWindow()
ui = gui.Ui_MainWindow()
ui.setupUi(window1)
threadpool = PyQt5.QtCore.QThreadPool()
class_label = ['meningioma', 'glioma', 'no tumor', 'pituitary']

current_dir = os.getcwd()
is_predicted = False
current_modelSelect=-1
img_num = 0

# Slot
def get_fileClick():
    ui.label_res.setText("...")
    ui.label_res_2.setText("...")
    browse_img()
    index_changed()

def browse_img():
    global img_num
    global file_temp
    global filename
    global all_dataframe
    file_temp = PyQt5.QtWidgets.QFileDialog.getOpenFileNames(window1, 'Open img', current_dir, "Image files (*.jpg *.gif *.png)")
    filename = file_temp[0]
    all_dataframe = pd.DataFrame()
    all_dataframe['file_path'] = filename
    all_dataframe['validation_res'] = "No Data"
    all_dataframe['prediction_res'] = "No Data"
    all_dataframe['prediction_belief'] = np.NaN
    all_dataframe['isTrue'] = False
    img_num = all_dataframe['file_path'].count()
    ui.spinBox_imgIndex.setMaximum(max(img_num, 1))
    ui.label_imgImport.setText("{} image imported".format(img_num))
    get_valid_val()
    process_button_state()
    
def index_changed():
    global img_index
    img_index = ui.spinBox_imgIndex.value()
    set_img()
    img_pathLabel()
    set_indexButton()
    img_validRes()
    img_predictRes()

def set_img():
    if img_num>=1:
        img = PyQt5.QtGui.QPixmap(all_dataframe['file_path'].values[img_index-1])
        scene = PyQt5.QtWidgets.QGraphicsScene()
        scene.clear()
        scene.addItem(PyQt5.QtWidgets.QGraphicsPixmapItem(img))
        ui.graphicsView_mainImg.setScene(scene)

def img_pathLabel():
    if img_num>=1:
        ui.lineEdit_filePath.setText(all_dataframe['file_path'].values[img_index-1])

def img_predictRes():
    if img_num>=1:
        ui.label_res.setText(all_dataframe['prediction_res'].values[img_index-1])
        
def img_validRes():
    if img_num>=1:
        ui.label_res_2.setText(all_dataframe['validation_res'].values[img_index-1])

def index_incr():
    ui.spinBox_imgIndex.setValue(max(1, min(img_index + 1, img_num)))

def index_decr():
    ui.spinBox_imgIndex.setValue(max(1, min(img_index - 1, img_num)))

def set_indexButton():
    if img_index <= 1:
        ui.pushButton_Left.setDisabled(True)
    else :
        ui.pushButton_Left.setEnabled(True)

    if img_index >= img_num:
        ui.pushButton_Right.setDisabled(True)
    else :
        ui.pushButton_Right.setEnabled(True)

def model_changed():
    global model_path
    if ui.comboBox_modelSelect.currentIndex()==0:
        model_path = current_dir+'/model/model8_92'
        if current_modelSelect == 0:
            ui.pushButton_modelSet.setDisabled(True)
        else :
            ui.pushButton_modelSet.setEnabled(True)
            
    if ui.comboBox_modelSelect.currentIndex()==1:
        model_path = current_dir+'/model/model5_76'
        if current_modelSelect == 1:
            ui.pushButton_modelSet.setDisabled(True)
        else :
            ui.pushButton_modelSet.setEnabled(True)

def set_model():
    worker = process_thread.Worker(load_dlModel)
    worker.signal.started.connect(progressBar_loadModel)
    worker.signal.finished.connect(progressBar_stop)
    worker.signal.error.connect(error_handle)
    ui.pushButton_cancelProcess.clicked.connect(worker.stop)
    threadpool.start(worker)

def error_boxShow():
    box = PyQt5.QtWidgets.QMessageBox()
    box.setText("Error")
    box.setInformativeText(error_msg)
    box.setWindowTitle("Error")
    box.exec_()

def error_handle(errorMessage):
    global current_modelSelect
    global error_msg
    error_msg = errorMessage
    error_boxShow()
    current_modelSelect = -1  
    ui.label_selectedModel.setText("Selected Model : None")
    process_button_state()

def load_dlModel():
    global dl_model, model1, model2
    global current_modelSelect
    if ui.comboBox_modelSelect.currentIndex()==0:
        try :
            type(model1)
        except :
            model1 = tf.keras.models.load_model(model_path)                
        dl_model = model1
        current_modelSelect = 0
        ui.label_selectedModel.setText("Selected Model : Improved Resnet50")
        

    if ui.comboBox_modelSelect.currentIndex()==1:
        try :
            type(model2)
        except :
            model2 = tf.keras.models.load_model(model_path)
        dl_model = model2
        current_modelSelect = 1
        ui.label_selectedModel.setText("Selected Model : Lu-Net")

def progressBar_loadModel():
    ui.label_processName.setText("Loading model")
    ui.progressBar.setMaximum(0)
    button_busyState()

def progressBar_stop():
    ui.label_processName.setText("State : Idle")
    ui.progressBar.setMaximum(1)
    button_idleState()
    process_button_state()

def process_button_state():
    if current_modelSelect == -1 or img_num == 0:
        ui.pushButton_predict.setDisabled(True)
    else :
        ui.pushButton_predict.setEnabled(True)

def process_call():
    worker = process_thread.Worker(process)
    worker.signal.started.connect(progressBar_process)
    worker.signal.finished.connect(progressBar_stop)
    worker.signal.error.connect(error_handleProcess)
    ui.pushButton_cancelProcess.clicked.connect(worker.stop)
    threadpool.start(worker)
    index_changed()

def error_handleProcess(errorMessage):
    global current_modelSelect
    global error_msg
    error_msg = errorMessage
    error_boxShow()
    process_button_state()

def progressBar_process():
    ui.label_processName.setText("Loading model")
    ui.progressBar.setMaximum(0)
    button_busyState()

def process():
    global all_dataframe
    predict_label = []
    predict_label_belief = []
    for dir in all_dataframe['file_path'] :
        img = Image.open(dir).convert('L').resize((512, 512), resample=0)
        img_arr = (np.array(img))/255.0
        img_arr = np.stack([img_arr], axis=0)
        res_array = dl_model.predict(img_arr)
        predict_label.append(class_label[np.argmax(res_array)])
        predict_label_belief.append(np.max(res_array))
    all_dataframe.prediction_res= predict_label

    all_dataframe.isTrue = np.where(all_dataframe['prediction_res']==all_dataframe['validation_res'], True, False)

def save():
    all_dataframe.to_excel(current_dir+'/save.xlsx')

# Signal
ui.pushButton_getImg.clicked.connect(get_fileClick)
ui.pushButton_Right.clicked.connect(index_incr)
ui.pushButton_Left.clicked.connect(index_decr)
ui.spinBox_imgIndex.valueChanged.connect(index_changed)
ui.comboBox_modelSelect.currentIndexChanged.connect(model_changed)
ui.pushButton_predict.clicked.connect(process_call)
ui.pushButton_modelSet.clicked.connect(set_model)
ui.pushButton_save.clicked.connect(save)


def gpu_availability():
    if(tf.test.is_gpu_available()):
        ui.label_GPU.setText("GPU is available")
        ui.label_GPU.setStyleSheet("background : rgb(77, 255, 57)")
    else:
        ui.label_GPU.setText("GPU is unavailable")
        ui.label_GPU.setStyleSheet("background : rgb(255, 0, 0)")

def button_busyState():
    ui.pushButton_getDir.setDisabled(True)
    ui.pushButton_getImg.setDisabled(True)    
    ui.pushButton_help.setDisabled(True)
    ui.pushButton_Left.setDisabled(True)
    ui.pushButton_modelSet.setDisabled(True)
    ui.pushButton_predict.setDisabled(True)
    ui.pushButton_Right.setDisabled(True)
    ui.pushButton_save.setDisabled(True)
    ui.pushButton_summary.setDisabled(True)
    ui.comboBox_modelSelect.setDisabled(True)

    ui.pushButton_cancelProcess.setEnabled(True)

def button_idleState():
    ui.pushButton_getDir.setEnabled(True)
    ui.pushButton_getImg.setEnabled(True)    
    ui.pushButton_help.setEnabled(True)
    ui.pushButton_Left.setEnabled(True)
    ui.pushButton_predict.setEnabled(True)
    ui.pushButton_Right.setEnabled(True)
    ui.pushButton_save.setEnabled(True)
    ui.pushButton_summary.setEnabled(True)
    ui.comboBox_modelSelect.setEnabled(True)

    ui.pushButton_cancelProcess.setDisabled(True)
    
def get_valid_val():
    if img_num>=1:   
        last2path = all_dataframe['file_path'].str.split().str[-2:]
        valid_label = []
        for file_dir in last2path:
            file_dir = "".join(file_dir)
            if "meningioma" in file_dir:
                valid_label.append("meningioma")
            elif "glioma" in file_dir:
                valid_label.append("glioma")
            elif "no_tumor" in file_dir:
                valid_label.append("no_tumor")
            elif "pituitary" in file_dir:
                valid_label.append("pituitary")
            else :
                valid_label.append("no validation")
        all_dataframe.validation_res = valid_label


def init():
    ui.pushButton_cancelProcess.setDisabled(True)
    gpu_availability()
    model_changed()
    process_button_state()

if __name__ == "__main__":
    window1.show()
    init()
    sys.exit(app.exec_())

