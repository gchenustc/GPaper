from PySide6.QtCore import QRunnable, Signal, Slot


class QThreadWorker(QRunnable):
    progressSignal = Signal(int)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    @Slot()
    def run(self):
        self.func(*self.args, **self.kwargs)
