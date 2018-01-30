from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QTabWidget

from umlfri2.application import Application
from umlfri2.application.commands.model import ApplyPatchCommand
from umlfri2.application.commands.solution import ApplyMetamodelConfigPatchCommand
from umlfri2.qtgui.base.validatingtabbar import ValidatingTabBar
from .listtab import ListPropertyTab
from .objecttab import ObjectPropertyTab
from umlfri2.ufl.dialog import UflDialogListTab, UflDialogObjectTab, UflDialogValueTab


class PropertiesDialog(QDialog):
    def __init__(self, main_window, dialog, mk_apply_patch_command): 
        super().__init__(main_window)
        self.__main_window = main_window
        self.setWindowTitle(_("Properties"))
        self.__dialog = dialog
        self.__mk_apply_patch_command = mk_apply_patch_command
        
        if mk_apply_patch_command:
            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
            button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
            button_box.button(QDialogButtonBox.Cancel).setText(_("Cancel"))
            apply_button = button_box.button(QDialogButtonBox.Apply)
            apply_button.setText(_("Apply"))
            apply_button.clicked.connect(self.__apply_clicked)
        else:
            button_box = QDialogButtonBox(QDialogButtonBox.Ok)
            button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
        
        button_box.accepted.connect(self.__accept_clicked)
        button_box.rejected.connect(self.reject)
        layout = QVBoxLayout()
        
        self.__tabs = []
        tab = dialog.get_lonely_tab()
        if isinstance(tab, UflDialogListTab):
            qt_tab = ListPropertyTab(self, tab, lonely=True)
            layout.addWidget(qt_tab)
            self.__tabs.append(qt_tab)
        elif isinstance(tab, (UflDialogObjectTab, UflDialogValueTab)):
            qt_tab = ObjectPropertyTab(self, tab, lonely=True)
            layout.addWidget(qt_tab)
            self.__tabs.append(qt_tab)
        else:
            tab_bar = ValidatingTabBar()
            
            self.__tab_widget = QTabWidget()
            self.__tab_widget.setTabBar(tab_bar)
            self.__tab_widget.setFocusPolicy(Qt.NoFocus)
            self.__tab_widget.currentChanged.connect(self.__tab_changed)
            tab_bar.validate_tab_change.connect(self.__validate_tab)
            
            for tab in dialog.tabs:
                if isinstance(tab, UflDialogListTab):
                    qt_tab = ListPropertyTab(self, tab)
                elif isinstance(tab, (UflDialogObjectTab, UflDialogValueTab)):
                    qt_tab = ObjectPropertyTab(self, tab)
                self.__tab_widget.addTab(qt_tab, tab.name or _("General"))
                self.__tabs.append(qt_tab)
            layout.addWidget(self.__tab_widget)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def sizeHint(self):
        orig = super().sizeHint()
        return QSize(500, orig.height())
    
    def __apply_clicked(self, checked=False):
        if self.__dialog.should_save_tab:
            if not self.__tabs[self.__dialog.current_tab.tab_index].handle_needed_save():
                return
        
        self.__dialog.finish()
        command = self.__mk_apply_patch_command(self.__dialog.make_patch())
        Application().commands.execute(command)
        self.__dialog.reset()
        
        for tab in self.__tabs:
            tab.refresh()
    
    def __accept_clicked(self):
        if self.__dialog.should_save_tab:
            if not self.__tabs[self.__dialog.current_tab.tab_index].handle_needed_save():
                return

        self.__dialog.finish()
        command = self.__mk_apply_patch_command(self.__dialog.make_patch())
        Application().commands.execute(command)
        
        self.accept()
    
    def __tab_changed(self, tab_index):
        self.__dialog.switch_tab(tab_index)

        for tab in self.__tabs:
            tab.refresh()
    
    def __validate_tab(self, event):
        if self.__dialog.should_save_tab:
            if not self.__tabs[self.__dialog.current_tab.tab_index].handle_needed_save():
                event.invalidate()
                return
    
    @staticmethod
    def open_for(main_window, object):
        dialog = object.create_ufl_dialog()
        dialog.translate(object.type.metamodel.get_translation(Application().language.current_language))
        qt_dialog = PropertiesDialog(main_window, dialog, lambda patch: ApplyPatchCommand(object, patch))
        qt_dialog.setModal(True)
        qt_dialog.exec_()
    
    @staticmethod
    def open_config(main_window, metamodel):
        dialog = metamodel.create_config_dialog()
        dialog.translate(metamodel.get_translation(Application().language.current_language))
        solution = Application().solution
        qt_dialog = PropertiesDialog(main_window, dialog, lambda patch: ApplyMetamodelConfigPatchCommand(solution, metamodel, patch))
        qt_dialog.setModal(True)
        qt_dialog.exec_()
