import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout)
from PyQt5.QtGui import QIntValidator
from PyQt5 import QtCore
from PyQt5.uic import loadUi

class AnnotationTool(QMainWindow):
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1" 
    def __init__(self, tool_controller, tool_model, year_panels):
        """Constructor for the main annotation tool window

        Args:
            tool_controller (ToolController): Controller for tool window
            tool_model (ToolModel): Model for tool window
            year_panels (dict[int, YearPanel]): Dictionary of year panels for
            each registration year
        """
        super().__init__()
        self._tool_controller = tool_controller
        self._tool_model = tool_model
        self._year_panels = year_panels
        loadUi('resources/mainapp.ui', self)
        self.setWindowTitle('JPCP Annotation Tool')
        years_layout = QHBoxLayout()
        years_layout.setSpacing(0)
        sorted_year_panels = sorted(year_panels.items())
        for panel in sorted_year_panels:
            years_layout.addWidget(panel[1])
        self.scroll_year_contents.setLayout(years_layout)
        
        # Set up the slab form validator
        slab_form_validator = QIntValidator()
        self.slab_form.setValidator(slab_form_validator)
        # textChanged
        self.slab_form.returnPressed.connect(
            lambda: self._tool_controller.update_slabs_displayed(
                self.slab_form.text(),
                self.slab_form))
        
        # back and next buttons setup
        self.back_btn.clicked.connect(
            lambda: self._tool_controller.update_slabs_displayed(
                str(int(self.slab_form.text()) - 1),
                self.slab_form))
        self.next_btn.clicked.connect(
            lambda: self._tool_controller.update_slabs_displayed(
                str(int(self.slab_form.text()) + 1),
                self.slab_form)
        )

        # menu bar actions
        self.action_range.triggered.connect(
            lambda: self._tool_controller.update_image_type('output_range')
        )
        self.action_intensity.triggered.connect(
            lambda: self._tool_controller.update_image_type('output_intensity')
        )
        self.action_range.setShortcut('Ctrl+R')
        self.action_intensity.setShortcut('Ctrl+I')

        
        
        # set up labels
        self.slab_form.setText(str(self._tool_model.first_BY_index))    
        self.num_lbl.setText("/"+ str(self._tool_model.last_BY_index))
        self.populate_year_buttons()

        # radiate a signal to display the first slabs
        self._tool_controller.update_slabs_displayed(
            str(self._tool_model.first_BY_index),
            self.slab_form)

    
    def populate_year_buttons(self):
        """Populates the text of the year buttons in the main annotation tool
        """
        for year, year_panel in self._year_panels.items():
            year_panel.yr_label.setText(str(year))  

    



