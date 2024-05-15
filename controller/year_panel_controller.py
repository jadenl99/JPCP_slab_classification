from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PIL import Image
class YearPanelController(QObject):
    def __init__(self, year_panel_model):
        super().__init__()
        self._year_panel_model = year_panel_model

    
    @pyqtSlot(bool)
    def next_slab(self):
        """Updates the displayed slab image to the next slab in the slab ID list
        """
        print("Next Slab")
        self._year_panel_model.next_slab()
    

    @pyqtSlot(bool)
    def prev_slab(self):
        """Updates the displayed slab image to the previous slab in the slab ID list
        """
        self._year_panel_model.previous_slab()  

    @pyqtSlot(bool)
    def popup_original_image(self):
        """Opens a dialog box to display the original image of the slab
        """
        try:
            image = Image.open(self._year_panel_model.img_directory)
            image.show()   
        except:
            pass




    
        