from PyQt5.QtCore import QObject, pyqtSignal


class WorkerSignals(QObject):
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
