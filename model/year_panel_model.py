from PyQt5.QtCore import QObject, pyqtSignal

class ImageSignal(QObject):
    """Signal class for sending changes to the YearPanelView to update the
    image displayed
    """
    image_changed = pyqtSignal(str)


class BackButtonEnableSignal(QObject):
    """Signal class for sending changes to the YearPanelView to enable or
    disable the back button. If True, the back button is enabled. If False, the
    back button is disabled.
    """
    back_btn_enable = pyqtSignal(bool)


class NextButtonEnableSignal(QObject):
    """Signal class for sending changes to the YearPanelView to enable or
    disable the next button. If True, the next button is enabled. If False, the
    next button is disabled.
    """
    next_btn_enable = pyqtSignal(bool)


class LockPanelSignal(QObject):
    """Signal class for sending changes to the YearPanelView to lock or unlock
    the year panel.
    """
    lock_panel = pyqtSignal(bool)

class SlabStateSignal(QObject):
    """Signal class for sending changes to the YearPanelView to update the 
    state of the slab. Will be in the form (primary_state, secondary_state, 
    special_state)
    """
    state_changed = pyqtSignal(tuple)


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
        self.image_signal = ImageSignal()
        self.lock_panel_signal = LockPanelSignal()
        self.next_btn_enable_signal = NextButtonEnableSignal()
        self.back_btn_enable_signal = BackButtonEnableSignal()
        self.state_changed_signal = SlabStateSignal()   
        self._year = year
        self._slab_inventory = slab_inventory
        self._slab_id_list = None
        self._lock_panel = False
        self._slab_id_list_index = None
        self._base_img_directory = None
        self._img_directory = None
        self._primary_states = None
        self._secondary_states = None
        self._special_states = None


    @property
    def img_directory(self):
        return self._img_directory
    

    @img_directory.setter
    def img_directory(self, img_directory):
        self._img_directory = img_directory
        self.image_signal.image_changed.emit(self._img_directory)


    @property
    def lock_panel(self):
        return self._lock_panel 
    

    def update_curr_imgs(self, base_dir, img_type, slab_id_list):
        """Updates the image directory based on the image type selected by the 
        user, as well as any necessary fields. If slab_id_list is empty, the 
        year panel is locked and no images are displayed.

        Args:
            base_dir (str): base directory of the slab data 
            img_type (str): image type selected by the user
            slab_id_list (list[int]): list of slab IDs to display in the 
            YearPanel
        """
        # no slabs belong to this year to prevent user from annotating from 
        # this panel
        if slab_id_list is None or len(slab_id_list) == 0:
            self._img_directory = ""
            self._lock_panel = True
            self.lock_panel_signal.lock_panel.emit(self._lock_panel)
            self.image_signal.image_changed.emit(self._img_directory)
            return
        
        # unlock the panel if it was previously locked
        if self._lock_panel:
            self._lock_panel = False
            self.lock_panel_signal.lock_panel.emit(self._lock_panel)
            
        self._slab_id_list = slab_id_list
        self._slab_id_list_index = 0
        self._base_img_directory = f'{base_dir}/{self._year}/Slabs/{img_type}'
        self._img_directory = (f'{self._base_img_directory}/'
                               f'{slab_id_list[0]}.jpg')
        
        # set states for each CY slab
        self._primary_states = []
        self._secondary_states = []
        self._special_states = []
        for slab_id in self._slab_id_list:
            slab_data = self._slab_inventory.fetch_slab(self._year, slab_id)
            self._primary_states.append(slab_data['primary_state'])
            self._secondary_states.append(slab_data['secondary_state'])
            self._special_states.append(slab_data['special_state'])
        state_tuple = (self._primary_states[0], 
                       self._secondary_states[0],
                       self._special_states[0])
        

        self.image_signal.image_changed.emit(self._img_directory)
        self.state_changed_signal.state_changed.emit(state_tuple)

        # set the enable of the back and next buttons accordingly
        self.back_btn_enable_signal.back_btn_enable.emit(False)
        if len(slab_id_list) == 1:
            self.next_btn_enable_signal.next_btn_enable.emit(False)
        else:
            self.next_btn_enable_signal.next_btn_enable.emit(True)
     

    def change_image_type(self, img_type):
        """Updates base and current directory based off the image type selected

        Args:
            img_type (str): type of images to show
        """
        if self._lock_panel:
            return
        
        last_slash_index = self._base_img_directory.rfind('/')
        self._base_img_directory = (self._base_img_directory[:last_slash_index]
                                   + f'/{img_type}')
        self._img_directory = (f'{self._base_img_directory}/'
                               f'{self._slab_id_list[self._slab_id_list_index]}'
                               f'.jpg')
        self.image_signal.image_changed.emit(self._img_directory)


    def next_slab(self):
        """If the CY has more than one slab associated with the BY slab, goes
        to next CY slab in the list
        """
        self._slab_id_list_index += 1
        self._img_directory = (f'{self._base_img_directory}/'
                               f'{self._slab_id_list[self._slab_id_list_index]}'
                               f'.jpg')
        self.image_signal.image_changed.emit(self._img_directory)

        if self._slab_id_list_index == len(self._slab_id_list) - 1:
            self.next_btn_enable_signal.next_btn_enable.emit(False)
        if self._slab_id_list_index > 0:
            self.back_btn_enable_signal.back_btn_enable.emit(True)

        self.update_state_of_slab(self._slab_id_list_index - 1, 
                                  self._slab_id_list_index)

    def previous_slab(self):
        """If the CY has more than one slab associated with the BY slab, goes
        to previous CY slab in the list
        """
        self._slab_id_list_index -= 1
        self._img_directory = (f'{self._base_img_directory}/'
                               f'{self._slab_id_list[self._slab_id_list_index]}'
                               f'.jpg')
        self.image_signal.image_changed.emit(self._img_directory)

        if self._slab_id_list_index == 0:
            self.back_btn_enable_signal.back_btn_enable.emit(False)
        if self._slab_id_list_index < len(self._slab_id_list) - 1:
            self.next_btn_enable_signal.next_btn_enable.emit(True)
        
        self.update_state_of_slab(self._slab_id_list_index + 1, 
                                  self._slab_id_list_index)
    
    
    def update_state_of_slab(self, curr_slab_list_index, 
                             next_slab_list_index: int=None):
        """Updates state information about the current slab id. 

        Args:
            curr_slab_list_index (int): where in the slab list to index to get
            the CY slab index, so the CY slab can be updated with its annotated
            states
            next_slab_list_index (int, optional): where in the slab list to
            index to get the next CY slab index of interest, so the appropriate
            fields can be set to the next CY slab states. Defaults to None.
        """
        # TODO: logic to store the state of leaving slab

        if next_slab_list_index is not None:
            state_tuple = (self._primary_states[next_slab_list_index], 
                           self._secondary_states[next_slab_list_index],
                           self._special_states[next_slab_list_index])
            self.state_changed_signal.state_changed.emit(state_tuple)
           
