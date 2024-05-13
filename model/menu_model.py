from PyQt5.QtCore import QObject, pyqtSignal
import os
class MenuModel(QObject):
    directory_changed = pyqtSignal(str) 
    def __init__(self, slab_inventory):
        super().__init__()
        self._directory = ''
        self._registration = ''
        self._slab_inventory = slab_inventory
        self._registrations = self.construct_registration_list() 


    def construct_registration_list(self):
        """Constructs a list of strings for the dropdown menu for the main menu
        screen when picking which registrations to annotate.

        Returns:
            list[dict]: A list of strings that represent the registrations in the
            slab inventory as the keys, as well as the registration metadata as
            the values
        """
        reg_metadata = self._slab_inventory.all_registration_metadata()
        registrations = {}

        for reg in reg_metadata:
            interstate = reg['segment_id']
            by = reg['base_year']
            years = reg['years']
            year_str = ''

            for year in years:
                if year == by:
                    year_str += f'BY{year}, '
                else:
                    year_str += f'{year}, '
            
            year_str = year_str[:-2]
            reg_str = f'{interstate} [{year_str}]'
            registrations[reg_str] = reg

        return registrations


    def get_subdirectories(self):
        """Gets the subdirectories of the selected directory.

        Returns:
            list[str]: A list of strings that represent the subdirectories of 
            the selected directory
        """
        if self._directory == '':
            return []
        
        entries = os.listdir(self._directory)
        subdirs = [entry for entry in entries if os.path.isdir(
            os.path.join(self._directory, entry))]
        return subdirs

    @property
    def directory(self):
        return self._directory
    

    @directory.setter
    def directory(self, directory):
        self._directory = directory
        self.directory_changed.emit(directory)


    @property
    def registrations(self):
        return self._registrations


    @property
    def registration(self):
        return self._registration


    @registration.setter
    def registration(self, registration):
        self._registration = registration




    




    