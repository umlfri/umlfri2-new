import os.path
from functools import partial

from PySide.QtGui import QMenuBar, QAction, QMenu, QKeySequence, QIcon, QFileDialog
from umlfri2.application import Application
from umlfri2.application.events.application.languagechanged import LanguageChangedEvent
from umlfri2.constants.languages import AVAILABLE_LANGUAGES
from umlfri2.qtgui.rendering import ImageExport
from .newproject import NewProjectDialog


class MainWindowMenu(QMenuBar):
    def __init__(self, main_window): 
        super().__init__()
        
        self.__main_window = main_window
        
        # FILE MENU
        self.__file, file_menu = self.__add_menu()

        self.__file_new = self.__add_menu_item(file_menu, QKeySequence.New, "document-new", self.__file_new_action)
        self.__file_open = self.__add_menu_item(file_menu, QKeySequence.Open, "document-open", self.__file_open_action)
        self.__file_save = self.__add_menu_item(file_menu, QKeySequence.Save, "document-save", self.__file_save_action)
        self.__file_save_as = self.__add_menu_item(file_menu, QKeySequence.SaveAs, "document-save-as", self.__file_save_as_action)
        file_menu.addSeparator()
        self.__file_exit = self.__add_menu_item(file_menu, QKeySequence.Quit, "application-exit", self.__file_exit_action)
        
        # VIEW MENU
        self.__edit, edit_menu = self.__add_menu()
        self.__edit_undo = self.__add_menu_item(edit_menu, QKeySequence.Undo, "edit-undo", self.__edit_undo_action)
        self.__edit_redo = self.__add_menu_item(edit_menu, QKeySequence.Redo, "edit-redo", self.__edit_redo_action)
        edit_menu.addSeparator()
        self.__edit_select_all = self.__add_menu_item(edit_menu, QKeySequence.SelectAll, "edit-select-all",
                                                      self.__edit_select_all_action)
        
        self.__diagram, diagram_menu = self.__add_menu()
        self.__diagram_export = self.__add_menu_item(diagram_menu, None, None, self.__diagram_export_action)
        
        self.__tools, tools_menu = self.__add_menu()
        self.__tools_languages_menu = QMenu()
        self.__tools_languages_menu.aboutToShow.connect(self.__tools_languages_menu_populate)
        self.__tools_languages = self.__add_submenu_item(tools_menu, None, None, self.__tools_languages_menu)
        
        # VIEW MENU
        self.__view, view_menu = self.__add_menu()
        
        for action in main_window.get_dock_actions():
            view_menu.addAction(action)
        
        view_menu.addSeparator()
            
        for action in main_window.get_toolbar_actions():
            view_menu.addAction(action)
        
        Application().event_dispatcher.subscribe(None, lambda event: self.__refresh_enable())
        Application().event_dispatcher.subscribe(LanguageChangedEvent, lambda event: self.__reload_texts())
        
        self.__reload_texts()
        self.__refresh_enable()

    def __add_menu(self):
        menu_item = QAction(None)
        self.addAction(menu_item)
        menu = QMenu()
        menu_item.setMenu(menu)
        return menu_item, menu

    def __add_menu_item(self, menu, shortcut, icon, action=None):
        ret = QAction(None)
        if shortcut is not None:
            ret.setShortcut(QKeySequence(shortcut))
        if icon is not None:
            ret.setIcon(QIcon.fromTheme(icon))
        if action is not None:
            ret.triggered.connect(action)
        menu.addAction(ret)
        return ret
    
    def __add_submenu_item(self, menu, shortcut, icon, submenu):
        ret = QAction(None)
        if shortcut is not None:
            ret.setShortcut(QKeySequence(shortcut))
        if icon is not None:
            ret.setIcon(QIcon.fromTheme(icon))
        ret.setMenu(submenu)
        menu.addAction(ret)
        return ret
    
    def __refresh_enable(self):
        self.__file_save.setEnabled(Application().can_save_solution)
        self.__file_save_as.setEnabled(Application().can_save_solution_as)
        
        self.__edit_undo.setEnabled(Application().commands.can_undo)
        self.__edit_redo.setEnabled(Application().commands.can_redo)
        self.__edit_select_all.setEnabled(Application().tabs.current_tab is not None)
        
        self.__diagram.setEnabled(Application().tabs.current_tab is not None)
    
    def __file_new_action(self, checked=False):
        self.__main_window.new_project()
    
    def __file_open_action(self, checked=False):
        self.__main_window.open_solution()
    
    def __file_save_action(self, checked=False):
        self.__main_window.save_solution()
    
    def __file_save_as_action(self, checked=False):
        self.__main_window.save_solution_as()
    
    def __file_exit_action(self, checked=False):
        self.__main_window.close()
    
    def __edit_undo_action(self, checked=False):
        Application().commands.undo()
    
    def __edit_redo_action(self, checked=False):
        Application().commands.redo()
    
    def __edit_select_all_action(self, checked=False):
        Application().tabs.current_tab.drawing_area.selection.select_all()
    
    def __diagram_export_action(self, checked=False):
        exp = ImageExport(Application().tabs.current_tab.drawing_area.diagram)
        formats = []
        for format in exp.supported_formats():
            file_names = " ".join("*.{0}".format(i) for i in format)
            filter_text = _("{0} image").format(format[0].upper()) + "({0})".format(file_names)
            formats.append((filter_text, format[0]))
        
        file_name, filter = QFileDialog.getSaveFileName(
            self,
            caption=_("Export diagram"),
            filter=";;".join(text for text, format in formats)
        )
        
        if file_name:
            for text, format in formats:
                if text == filter:
                    break
            else:
                raise Exception
            
            if '.' not in os.path.basename(file_name):
                file_name = file_name + '.' + format
            
            # TODO: export to python file?
            exp.export(file_name, format)
    
    def __tools_languages_menu_populate(self):
        selected_language = Application().selected_language
        
        self.__tools_languages_menu.clear()
        system_lang = self.__tools_languages_menu.addAction(_("System language"))
        system_lang.triggered.connect(partial(self.__tools_languages_menu_activate, None))
        system_lang.setCheckable(True)
        system_lang.setChecked(selected_language is None)
        
        self.__tools_languages_menu.addSeparator()
        
        for lang_id, label in AVAILABLE_LANGUAGES:
            language = self.__tools_languages_menu.addAction(label)
            language.triggered.connect(partial(self.__tools_languages_menu_activate, lang_id))
            language.setCheckable(True)
            language.setChecked(selected_language == lang_id)
    
    def __tools_languages_menu_activate(self, lang_id, checked=False):
        Application().change_language(lang_id)
    
    def __reload_texts(self):
        self.__file.setText(_("&File"))
        self.__file_new.setText(_("&New"))
        self.__file_open.setText(_("&Open"))
        self.__file_save.setText(_("&Save"))
        self.__file_save_as.setText(_("Save &as"))
        self.__file_exit.setText(_("&Quit"))
        
        self.__edit.setText(_("&Edit"))
        self.__edit_undo.setText(_("&Undo"))
        self.__edit_redo.setText(_("&Redo"))
        self.__edit_select_all.setText(_("Select &all"))
        
        self.__diagram.setText(_("&Diagram"))
        self.__diagram_export.setText(_("Export as &image"))
        
        self.__tools.setText(_("&Tools"))
        self.__tools_languages.setText(_("Change &language"))
        
        self.__view.setText(_("&View"))
