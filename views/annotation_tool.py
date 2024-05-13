import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout)
from PyQt5.QtGui import QPalette, QColor
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
        self.setWindowTitle('JPCP Annotation Tool')
        loadUi('resources/mainapp.ui', self)
        years_layout = QHBoxLayout()
        sorted_year_panels = sorted(year_panels.items())
        for panel in sorted_year_panels:
            years_layout.addWidget(panel[1])
        self.scroll_year_contents.setLayout(years_layout)
        # self.horizontal_year_panels_layout.addWidget(YearPanel())   
        # self.yr_panel = YearPanel()
        # self.yr_panel2 = YearPanel()
        # self.yr_panel3 = YearPanel()
        # self.yr_panel4 = YearPanel()
        # self.yr_panel5 = YearPanel()
        # self.yr_panel6 = YearPanel()
        
    
        # central_widget = QWidget()
        # outer_layout = QVBoxLayout()
        # year_panel_layout = QHBoxLayout()
        # year_panel_layout.addWidget(self.yr_panel)
        # year_panel_layout.addWidget(self.yr_panel2)
        # year_scroll_area = QScrollArea()
        # year_scroll_area.setWidgetResizable(True)   


        # outer_layout.addLayout(year_panel_layout)
        # central_widget.setLayout(outer_layout)
        # self.setCentralWidget(central_widget)  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnnotationTool()
    window.show()
    app.exec()
