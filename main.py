# This Python file uses the following encoding: utf-8
import sys
import os

import gui
import process_thread
import PyQt5
import model
import tensorflow as tf
import pandas as pd

app = PyQt5.QtWidgets.QApplication(sys.argv)
window1 = PyQt5.QtWidgets.QMainWindow()
ui = gui.Ui_MainWindow()
ui.setupUi(window1)
threadpool = PyQt5.QtCore.QThreadPool()

current_dir = os.getcwd()
is_predicted = False

# Slot
def get_fileClick():
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
    img_num = all_dataframe['file_path'].count()
    ui.spinBox_imgIndex.setMaximum(max(img_num, 1))
    ui.label_imgImport.setText("{} image imported".format(img_num))
    
def index_changed():
    global img_index
    img_index = ui.spinBox_imgIndex.value()
    set_img()
    img_pathLabel()
    set_indexButton()

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
    if ui.comboBox_modelSelect.currentIndex()==1:
        model_path = current_dir+'/model/model5_76'
    ui.pushButton_modelSet.setEnabled(True)
    
def set_model():
    worker = process_thread.Worker(load_dlModel)
    worker.signal.started.connect(progressBar_loadModel)
    worker.signal.finished.connect(progressBar_loadModelStop)
    threadpool.start(worker)
    ui.pushButton_modelSet.setDisabled(True)

def load_dlModel():
    global dl_model
    dl_model = tf.keras.models.load_model(model_path)

def progressBar_loadModel():
    ui.label_processName.setText("Loading model")
    ui.progressBar.setMaximum(0)
    button_busyState()

def progressBar_loadModelStop():
    ui.label_processName.setText("State : Idle")
    ui.progressBar.setMaximum(1)

def process():
    pred_res = "COBA"
    print(pred_res)
#def predict_res():
#    if(is_predicted):
#        ui.label_res.setText()

# Signal
ui.pushButton_getImg.clicked.connect(get_fileClick)
ui.pushButton_Right.clicked.connect(index_incr)
ui.pushButton_Left.clicked.connect(index_decr)
ui.spinBox_imgIndex.valueChanged.connect(index_changed)
ui.comboBox_modelSelect.currentIndexChanged.connect(model_changed)
ui.pushButton_predict.clicked.connect(process)
ui.pushButton_modelSet.clicked.connect(load_dlModel)

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
    ui.pushButton_modelSet.setEnabled(True)
    ui.pushButton_predict.setEnabled(True)
    ui.pushButton_Right.setEnabled(True)
    ui.pushButton_save.setEnabled(True)
    ui.pushButton_summary.setEnabled(True)
    ui.comboBox_modelSelect.setEnabled(True)

    ui.pushButton_cancelProcess.setDisabled(True)
    
def init():
    ui.pushButton_cancelProcess.setDisabled(True)
    gpu_availability()
    model_changed()

if __name__ == "__main__":

    window1.show()
    init()
    sys.exit(app.exec_())

