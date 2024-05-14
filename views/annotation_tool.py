import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout)
from PyQt5.QtGui import QPalette, QColor, QIntValidator
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
        self.setWindowTitle('JPCP Annotation Tool')
        loadUi('resources/mainapp.ui', self)
        years_layout = QHBoxLayout()
        sorted_year_panels = sorted(year_panels.items())
        for panel in sorted_year_panels:
            years_layout.addWidget(panel[1])
        self.scroll_year_contents.setLayout(years_layout)
        
        # Set up the slab form validator
        slab_form_validator = QIntValidator()
        self.slab_form.setValidator(slab_form_validator)
        self.slab_form.textChanged.connect(
            lambda: self._tool_controller.update_slabs_displayed(
                self.slab_form.text(),
                self.slab_form))
        
        # set up labels
        self.slab_form.setText(str(self._tool_model.first_BY_index))    
        self.num_lbl.setText(str(self._tool_model.last_BY_index))
        self.populate_year_buttons()

    
    def populate_year_buttons(self):
        """Populates the text of the year buttons in the main annotation tool
        """
        for year, year_panel in self._year_panels.items():
            year_panel.yr_label.setText(str(year))  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnnotationTool()
    window.show()
    app.exec()
