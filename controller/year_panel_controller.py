from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class YearPanelController(QObject):
    def __init__(self, year_panel_model):
        super().__init__()
        self._year_panel_model = year_panel_model
        