import PyQt5
import tensorflow as tf

class WorkerSignals(PyQt5.QtCore.QObject):
    finished = PyQt5.QtCore.pyqtSignal()
    started = PyQt5.QtCore.pyqtSignal()
    error = PyQt5.QtCore.pyqtSignal(tuple)
    
class Worker(PyQt5.QtCore.QRunnable):

    def __init__(self, func):
        super(Worker, self).__init__()
        self.func = func
        self.signal = WorkerSignals()

    def run(self):
        self.signal.started.emit()
        try :
            self.func()
        except Exception as e:
            self.signal.error.emit(e)
        finally :
            self.signal.finished.emit()