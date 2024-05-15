import sys, os
from PyQt5.QtWidgets import QWidget, QButtonGroup, QAbstractButton, QStyle
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QIcon

class YearPanel(QWidget):
    def __init__(self, year_panel_controller, year_panel_model):    
        super().__init__()
        self._year_panel_controller = year_panel_controller
        self._year_panel_model = year_panel_model
        loadUi('resources/year_panel.ui', self)

        # Set up buttons so slab states can be annotated
        self.state_btn_group = QButtonGroup()   
        self.state_btn_group.setExclusive(False)
        self.state_btn_group.addButton(self.l1_btn)
        self.state_btn_group.addButton(self.l2_btn)
        self.state_btn_group.addButton(self.t1_btn)
        self.state_btn_group.addButton(self.t2_btn)
        self.state_btn_group.addButton(self.cc_btn)
        self.state_btn_group.addButton(self.ss_btn)
        self.state_btn_group.addButton(self.nc_btn)
        self.state_btn_group.addButton(self.error_btn)

        self.vertical_panel_layout.setAlignment(Qt.AlignCenter)
        # listen to updates from model
        self._year_panel_model.image_signal.image_changed.connect(
            self.on_BY_slab_changed
        )
        self._year_panel_model.lock_panel_signal.lock_panel.connect(
            self.on_lock_panel_changed
        )

        self._year_panel_model.next_btn_enable_signal.next_btn_enable.connect(
            self.on_next_btn_enable
        )

        self._year_panel_model.back_btn_enable_signal.back_btn_enable.connect(
            self.on_back_btn_enable
        )


        self.next_btn.clicked.connect(self._year_panel_controller.next_slab)
        self.back_btn.clicked.connect(self._year_panel_controller.prev_slab)
        self.state_btn_group.buttonToggled.connect(
            self.on_state_btn_toggled
        )
        self.yr_label.clicked.connect(
            self._year_panel_controller.popup_original_image
        )

        


    
    @pyqtSlot(str)
    def on_BY_slab_changed(self, slab_dir):
        if slab_dir == "":
            self.slab_img.setText("No slab image for the year")
        elif not os.path.exists(slab_dir):
            self.slab_img.setText("Slab Image Not Found")
        else:
            img = QPixmap(slab_dir).scaled(250, 500, 1, 0)
            self.slab_img.setPixmap(img)

    
    @pyqtSlot(bool)
    def on_lock_panel_changed(self, lock):
        """If the lock is on, the panel is disabled. If the lock is off, the
        panel is enabled.

        Args:
            lock (bool): Whether to lock the panel or unlock it. If True, locks
            the panel.
        """
        self.back_btn.setEnabled(not lock)  
        self.next_btn.setEnabled(not lock)

        for btn in self.state_btn_group.buttons():
            btn.setEnabled(not lock)
    

    @pyqtSlot(bool)
    def on_next_btn_enable(self, enable):
        """Sets the next button to be enabled or disabled

        Args:
            enable (bool): if enable is True, sets the next button to be 
            enabled. Else, sets the next button to be disabled.
        """
        self.next_btn.setEnabled(enable)
    

    @pyqtSlot(bool)
    def on_back_btn_enable(self, enable):
        """Sets the back button to be enabled or disabled

        Args:
            enable (bool): if enable is True, sets the back button to be 
            enabled. Else, sets the back button to be disabled.
        """
        self.back_btn.setEnabled(enable)

    
    @pyqtSlot(QAbstractButton, bool)
    def on_state_btn_toggled(self, btn, checked):
        """Updates the state of the slab based on the button clicked. Ensures
        that only two buttons can be checked at a time. If two buttons are 
        selected, the secondary state is marked accordingly with a circle.

        Args:
            btn (QPushButton): button clicked by the user
            checked (bool): whether the button is checked (True) or unchecked
        """
        checked_btns = [btn for btn in self.state_btn_group.buttons() 
                        if btn.isChecked()]
        
        if len(checked_btns) > 2:
            btn.setChecked(False)
        elif len(checked_btns) == 2 and checked:
            btn.setIcon(self.style().standardIcon(QStyle.SP_DialogYesButton))
        elif len(checked_btns) == 1:
            if not checked:
                btn.setIcon(QIcon())
            checked_btns[0].setIcon(QIcon())
        
        



