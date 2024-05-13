from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class ToolController(QObject):
    def __init__(self, tool_model):
        super().__init__()
