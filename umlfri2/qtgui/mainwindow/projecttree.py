from PySide.QtGui import QTreeWidget, QTreeWidgetItem

from umlfri2.application import Application
from ..base import image_loader


class ProjectTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.header().close()
    
    def reload(self):
        for project in Application().solution.children:
            item = QTreeWidgetItem(self, [project.name])
            item.setIcon(0, image_loader.load_icon(project.metamodel.addon.icon))
            
            for element in project.children:
                self.__reload_element(item, element)
            item.setExpanded(True)
            self.addTopLevelItem(item)
    
    def __reload_element(self, parent, element):
        item = QTreeWidgetItem(parent, [element.get_display_name()])
        item.setIcon(0, image_loader.load_icon(element.type.icon))
        
        for child_diagram in element.diagrams:
            child = QTreeWidgetItem(item, [child_diagram.get_display_name()])
            child.setIcon(0, image_loader.load_icon(child_diagram.type.icon))
            item.addChild(child)
        
        for child_element in element.children:
            self.__reload_element(item, child_element)
        parent.addChild(item)