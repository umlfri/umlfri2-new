from PySide.QtCore import QSize, Qt
from PySide.QtGui import QDialog, QDialogButtonBox, QVBoxLayout, QTableWidget, QHBoxLayout, QLabel, QWidget, \
    QTableWidgetItem, QFont, QStyledItemDelegate, QStyle
from umlfri2.application import Application
from ..base import image_loader


class AddOnsDialog(QDialog):
    class __NoSelectionItemDelegate(QStyledItemDelegate):
        def initStyleOption(self, option, index):
            super().initStyleOption(option, index)
            
            option.state = option.state & ~QStyle.State_HasFocus
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setWindowTitle(_("Add-ons"))
        
        self.__main_window = main_window
        
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.button(QDialogButtonBox.Close).setText(_("Close"))
        
        button_box.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        
        self.__table = QTableWidget()
        self.__table.setItemDelegate(self.__NoSelectionItemDelegate())
        self.__table.verticalHeader().hide()
        self.__table.horizontalHeader().hide()
        self.__table.setColumnCount(2)
        self.__table.setSelectionBehavior(QTableWidget.SelectRows)
        self.__table.setSelectionMode(QTableWidget.SingleSelection)
        self.__table.horizontalHeader().setStretchLastSection(True)
        self.__table.setAlternatingRowColors(True)
        self.__table.setShowGrid(False)
        self.__table.setIconSize(QSize(32, 32))
        layout.addWidget(self.__table)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
        
        self.__refresh()
    
    def sizeHint(self):
        return QSize(600, 300)
    
    def __refresh(self):
        addons = list(Application().addons)
        
        self.__table.setRowCount(len(addons))
        
        for no, addon in enumerate(addons):
            if addon.icon:
                icon_item = QTableWidgetItem()
                icon_item.setIcon(image_loader.load(addon.icon))
                self.__table.setItem(no, 0, icon_item)
            
            layout = QVBoxLayout()
            layout.setSpacing(0)
            
            name_layout = QHBoxLayout()
            name_layout.setSpacing(20)
            name_layout.setAlignment(Qt.AlignLeft)
            
            name_label = QLabel(addon.name)
            name_label.setTextFormat(Qt.PlainText)
            font = name_label.font()
            font.setWeight(QFont.Bold)
            name_label.setFont(font)
            name_layout.addWidget(name_label)
            
            version_label = QLabel(str(addon.version))
            version_label.setTextFormat(Qt.PlainText)
            name_layout.addWidget(version_label)
            
            layout.addLayout(name_layout)
            
            if addon.description:
                description_label = QLabel(addon.description)
                description_label.setTextFormat(Qt.PlainText)
                description_label.setWordWrap(True)
                layout.addWidget(description_label)
            
            widget = QWidget()
            widget.setLayout(layout)
            self.__table.setCellWidget(no, 1, widget)
        
        self.__table.resizeColumnsToContents()
        self.__table.resizeRowsToContents()