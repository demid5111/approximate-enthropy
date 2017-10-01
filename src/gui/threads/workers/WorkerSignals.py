from PyQt5.QtCore import QObject, pyqtSignal

from src.core.report import IReport


class WorkerSignals(QObject):
    error = pyqtSignal(tuple)
    result = pyqtSignal(IReport)
