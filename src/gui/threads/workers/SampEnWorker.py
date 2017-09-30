from PyQt5.QtCore import QRunnable, pyqtSlot

from src.core.sampen import SampEn
from src.gui.threads.workers.WorkerSignals import WorkerSignals


class SEWorker(QRunnable):
    def __init__(self, *args, **kwargs):
        super(SEWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        res = SampEn.prepare_calculate_window_apen(*self.args)
        self.signals.result.emit(res)