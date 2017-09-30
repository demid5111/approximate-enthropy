from PyQt5.QtCore import QRunnable, pyqtSlot

from src.core.apen import ApEn
from src.gui.threads.workers.WorkerSignals import WorkerSignals


class AEWorker(QRunnable):
    def __init__(self, *args, **kwargs):
        super(AEWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        res = ApEn.prepare_calculate_window_apen(*self.args)
        self.signals.result.emit(res)