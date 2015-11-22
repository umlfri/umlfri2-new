from PySide.QtCore import QSize, Qt
from PySide.QtGui import QDialog, QDialogButtonBox, QVBoxLayout, QTabWidget

from umlfri2.application import Application
from umlfri2.application.commands.model import ApplyPatchCommand
from .listtab import ListPropertyTab
from .objecttab import ObjectPropertyTab
from umlfri2.ufl.dialog import UflDialogListTab, UflDialogObjectTab


class PropertiesDialog(QDialog):
    def __init__(self, main_window, dialog): 
        super().__init__(main_window)
        self.__main_window = main_window
        self.setWindowTitle(_("Properties"))
        self.__dialog = dialog
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.button(QDialogButtonBox.Ok).setText(_("Ok"))
        buttonBox.button(QDialogButtonBox.Cancel).setText(_("Cancel"))
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout = QVBoxLayout()
        
        tab = dialog.get_lonely_tab()
        if isinstance(tab, UflDialogListTab):
            layout.addWidget(ListPropertyTab(self, tab))
        elif isinstance(tab, UflDialogObjectTab):
            layout.addWidget(ObjectPropertyTab(self, tab))
        else:
            tabs = QTabWidget()
            tabs.setFocusPolicy(Qt.NoFocus)
            
            for tab in dialog.tabs:
                if isinstance(tab, UflDialogListTab):
                    tabs.addTab(ListPropertyTab(self, tab), tab.name or _("General"))
                elif isinstance(tab, UflDialogObjectTab):
                    tabs.addTab(ObjectPropertyTab(self, tab), tab.name or _("General"))
            layout.addWidget(tabs)
        
        layout.addWidget(buttonBox)
        self.setLayout(layout)
    
    def sizeHint(self):
        orig = super().sizeHint()
        return QSize(500, orig.height())
    
    @staticmethod
    def open_for(main_window, object):
        dialog = object.create_ufl_dialog()
        qt_dialog = PropertiesDialog(main_window, dialog)
        qt_dialog.setModal(True)
        if qt_dialog.exec_() == PropertiesDialog.Accepted:
            dialog.finish()
            command = ApplyPatchCommand(object, dialog.make_patch())
            Application().commands.execute(command)
