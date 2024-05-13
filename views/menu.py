import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QAction, 
                             QMenu, QFileDialog, QPushButton, QWidget, QLabel,
                             QWidget, QComboBox)
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot


class MainMenu(QMainWindow):
    def __init__(self, menu_controller, menu_model):
        super().__init__()
        self._menu_controller = menu_controller
        self._menu_model = menu_model
        self.setWindowTitle('Main Menu')
        layout = QVBoxLayout()  
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.dir_select_btn = QPushButton('Select Directory')

        self.dir_select_lbl = QLabel('Please select the directory containing '
                                     'all the segment data files.')
        self.dir_label = QLabel('Directory: ')
        self.reg_label = QLabel('Select Registration: ')    
        self.reg_selector = QComboBox()
        self.submit_button = QPushButton('Submit')
        layout.addWidget(self.dir_select_lbl)        
        layout.addWidget(self.dir_select_btn)
        layout.addWidget(self.dir_label)
        layout.addWidget(self.reg_label)
        layout.addWidget(self.reg_selector)
        layout.addWidget(self.submit_button)
        self.populate_reg_selector()

        widget = QWidget()
        widget.setLayout(layout)    
        self.setCentralWidget(widget)

        # connection to controller
        self.dir_select_btn.clicked.connect(
            lambda: self._menu_controller.select_directory(self)
            )
        self.submit_button.clicked.connect(
            lambda: self._menu_controller.submit(self)  
        )

        # listen to updates from model
        self._menu_model.directory_changed.connect(self.on_directory_changed)

        # detect when views update
        self.reg_selector.currentIndexChanged.connect(self.on_reg_changed)
    

    def populate_reg_selector(self):
        """Populates the registration selector with the registrations from the
        database.
        """
        self.reg_selector.addItem('')
        reg_list = list(self._menu_model.registrations.keys())
        reg_list.sort()
        for reg in reg_list:
            self.reg_selector.addItem(reg)
    

    @pyqtSlot(str)
    def on_directory_changed(self, directory):
        self.dir_label.setText(f'Directory: {directory}')   
    

    @pyqtSlot(int)
    def on_reg_changed(self, index):
        self._menu_controller.update_registration(
            self.reg_selector.currentText()
        )   



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    app.exec()


