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

    
    @pyqtSlot(list)
    def change_slab_state_info(self, buttons_pressed):
        """Changes the state of the slab based on the button pressed by the user
        in the model

        Args:
            buttons_pressed (list[QPushButton]): list of buttons pressed by the
            user, denoting the primary and secondary states of the slab
        """
        primary_state_list = self._year_panel_model.primary_states
        secondary_state_list = self._year_panel_model.secondary_states
        slab_index = self._year_panel_model.slab_id_list_index

        try:
            btn = buttons_pressed[0]
            primary_state_list[slab_index] = btn.text()
        except:
            primary_state_list[slab_index] = None
        try:
            btn = buttons_pressed[1]
            secondary_state_list[slab_index] = btn.text()
        except:
            secondary_state_list[slab_index] = None
        
        self._year_panel_model.panel_updated = True
        



    
        