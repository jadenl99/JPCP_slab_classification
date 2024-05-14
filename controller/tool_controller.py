from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class ToolController(QObject):
    def __init__(self, tool_model, year_controllers):
        """Constructor for ToolController, containing all the logic for the
        main window of the annotation tool.

        Args:
            tool_model (ToolModel): model containing all the data for the tool
            year_controllers (dict[int, YearPanelController]): mappings from 
            each registration year to its corresponding controller
        """
        super().__init__()
        self._tool_model = tool_model
        self._year_controllers = year_controllers
    

    @pyqtSlot(str)
    def update_slabs_displayed(self, by_slab_id, slab_form):
        """Updates the displayed slabs in the annotation tool main window based
        on the base year slab ID selected by the user. Checks if within bounds
        of the first and last base year slab IDs.   

        Args:
            by_slab_id (str): base year slab ID selected by the user
            slab_form (QLineEdit): QLineEdit object containing the base year 
            slab index
        """
        if by_slab_id == '':
            return
        by_slab_id = int(by_slab_id)

        if by_slab_id < self._tool_model.first_BY_index:
            by_slab_id = self._tool_model.first_BY_index
            slab_form.setText(str(by_slab_id))
        elif by_slab_id > self._tool_model.last_BY_index:
            by_slab_id = self._tool_model.last_BY_index
            slab_form.setText(str(by_slab_id))

        print(str(by_slab_id))

