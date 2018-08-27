import time
from PyQt5.QtCore import QRunnable, pyqtSlot

from src.gui.threads.workers.WorkerSignals import WorkerSignals


class GeneralWorker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(GeneralWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.fn = fn
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        res = self.fn(*self.args)
        self.signals.result.emit(res)
        time.sleep(0.01)
