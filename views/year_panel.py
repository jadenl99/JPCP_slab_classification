import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QAction, 
                             QMenu, QFileDialog, QPushButton, QWidget, QLabel,
                             QWidget)
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtCore
from PyQt5.uic import loadUi

class YearPanel(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('resources/year_panel.ui', self)