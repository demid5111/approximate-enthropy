from PyQt5.QtCore import QRunnable, pyqtSlot

from src.core.cordim import CorDim
from src.gui.threads.workers.WorkerSignals import WorkerSignals


class CDWorker(QRunnable):
    def __init__(self, *args, **kwargs):
        super(CDWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        res = CorDim.prepare_calculate_window_cor_dim(*self.args)
        self.signals.result.emit(res)