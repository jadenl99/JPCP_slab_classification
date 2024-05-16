from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class MenuController(QObject):
    def __init__(self, menu_model, app):
        """Constructor for MenuController

        Args:
            menu_model (MenuModel): Model for main menu
            app (App): Main application
        """
        super().__init__()
        self._menu_model = menu_model
        self._app = app

    @pyqtSlot(bool)
    def select_directory(self, menu_view):
        dir = QFileDialog.getExistingDirectory(menu_view, 'Select Directory')
        self._menu_model.directory = dir
    

    @pyqtSlot(bool)
    def submit(self, menu_view):
        """Submit the form and check if the registration and directory are
        filled out correctly. If not, display an error message. If everything 
        works, then the menu window is closed and the annotation tool is 
        started.

        Args:
            menu_view (MainMenu): The main menu window/view
        """
        dir = self._menu_model.directory
        reg = self._menu_model.registration
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Critical)
        popup.setWindowTitle('Error')
        if dir == '':
            popup.setText('Please select a directory.')
            popup.exec_()
            return

        if reg == '':   
            popup.setText('Please select a registration.')
            popup.exec_()
            return
        
        years = self._menu_model.registrations[reg]['years']
        dir_years = set(self._menu_model.get_subdirectories())
        years_set = {str(year) for year in years}   
        if not years_set.issubset(dir_years):
            popup.setText('Not all years for the registration are present in '
                          'the directory.')
            popup.exec_()
            return

        self._app.run_annotation_tool()   
    
    
    @pyqtSlot(str)
    def update_registration(self, reg):
        self._menu_model.registration = reg