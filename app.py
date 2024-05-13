import sys 
from PyQt5.QtWidgets import QApplication    
from views.menu import MainMenu
from model.menu_model import MenuModel
from model.tool_model import ToolModel
from controller.menu_controller import MenuController
from controller.tool_controller import ToolController
from views.annotation_tool import AnnotationTool
from views.year_panel import YearPanel
from database.db import SlabInventory
class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.slab_inventory = SlabInventory()
        self.menu_model = MenuModel(self.slab_inventory)
        self.menu_controller = MenuController(self.menu_model, self)
        self.menu = MainMenu(self.menu_controller, self.menu_model)
        self.menu.show()
    
    def run_annotation_tool(self):
        self.menu.close()

        reg_data = self.menu_model.registrations[self.menu_model.registration]
        self.year_panels = {}
        for year in reg_data['years']:
            self.year_panels[year] = YearPanel()

        self.tool_model = ToolModel()
        self.tool_controller = ToolController(self.tool_model)  
        self.annotation_tool = AnnotationTool(self.tool_controller, 
                                              self.tool_model, 
                                              self.year_panels)
        self.annotation_tool.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())    