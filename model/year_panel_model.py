from PyQt5.QtCore import QObject, pyqtSignal


class YearPanelModel(QObject):
    def __init__(self, year, slab_inventory):
        """Constructor for YearPanelModel, containing all data for a speicific
        image in a given year to display in a YearPanel.

        Args:
            year (int): year the model is responsible
            slab_inventory (SlabInventory): database containing all the slab 
            data
        """
        super().__init__()
        self._year = year
        self._slab_inventory = slab_inventory
        self._primary_state = None
        self._secondary_state = None
        self._special_state = None
           

