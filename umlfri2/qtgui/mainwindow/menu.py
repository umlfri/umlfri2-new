import os
import os.path
from functools import partial

from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu, QFileDialog

from umlfri2.application import Application
from umlfri2.application.commands.diagram import HideElementsCommand, PasteSnippetCommand, DuplicateSnippetCommand
from umlfri2.application.events.application.languagechanged import LanguageChangedEvent
from umlfri2.constants.keys import FULL_SCREEN, ZOOM_ORIGINAL, PASTE_DUPLICATE, COPY_IMAGE
from umlfri2.qtgui.fullscreen import FullScreenDiagram
from umlfri2.qtgui.printing import Printing
from umlfri2.qtgui.rendering import ImageExport, ExportDialog
from umlfri2.qtgui.appdialogs.settings import SettingsDialog
from umlfri2.qtgui.appdialogs.about import AboutDialog
from umlfri2.qtgui.appdialogs.addons import AddOnsDialog


class MainWindowMenu(QMenuBar):
    def __init__(self, main_window):
        super().__init__()
        
        self.__main_window = main_window
        
        # FILE MENU
        self.__file, file_menu = self.__add_menu()

        self.__file_new = self.__add_menu_item(file_menu, QKeySequence.New, "document-new", self.__file_new_action)
        self.__file_open = self.__add_menu_item(file_menu, QKeySequence.Open, "document-open", self.__file_open_action)

        self.__file_recent_files, self.__recent_files_menu = self.__add_menu(file_menu)
        self.__recent_files_menu.aboutToShow.connect(self.__recent_files_menu_populate)
        
        self.__file_save = self.__add_menu_item(file_menu, QKeySequence.Save, "document-save", self.__file_save_action)
        self.__file_save_as = self.__add_menu_item(file_menu, QKeySequence.SaveAs, "document-save-as", self.__file_save_as_action)
        
        if Printing().has_printing_support:
            file_menu.addSeparator()
            self.__file_page_setup = self.__add_menu_item(file_menu, None, None, self.__file_page_setup_action)
            self.__file_print_preview = self.__add_menu_item(file_menu, None, "document-print-preview", self.__file_print_preview_action)
            self.__file_print = self.__add_menu_item(file_menu, QKeySequence.Print, "document-print", self.__file_print_action)
        
        file_menu.addSeparator()
        self.__file_exit = self.__add_menu_item(file_menu, QKeySequence.Quit, "application-exit", self.__file_exit_action)
        self.__file_exit.setMenuRole(QAction.QuitRole)
        
        # VIEW MENU
        self.__edit, edit_menu = self.__add_menu()
        self.__edit_undo = self.__add_menu_item(edit_menu, QKeySequence.Undo, "edit-undo", self.__edit_undo_action)
        self.__edit_redo = self.__add_menu_item(edit_menu, QKeySequence.Redo, "edit-redo", self.__edit_redo_action)
        
        edit_menu.addSeparator()
        
        self.__edit_cut = self.__add_menu_item(edit_menu, QKeySequence.Cut, "edit-cut", self.__edit_cut_action)
        self.__edit_copy = self.__add_menu_item(edit_menu, QKeySequence.Copy, "edit-copy", self.__edit_copy_action)
        self.__edit_copy_image = self.__add_menu_item(edit_menu, COPY_IMAGE, None, self.__edit_copy_image_action)
        self.__edit_paste = self.__add_menu_item(edit_menu, QKeySequence.Paste, "edit-paste", self.__edit_paste_action)
        self.__edit_duplicate = self.__add_menu_item(edit_menu, PASTE_DUPLICATE, "edit-paste",
                                                     self.__edit_duplicate_action)
        
        edit_menu.addSeparator()
        
        self.__edit_select_all = self.__add_menu_item(edit_menu, QKeySequence.SelectAll, "edit-select-all",
                                                      self.__edit_select_all_action)
        
        edit_menu.addSeparator()
        
        if os.name != 'nt':
            self.__edit_addons = self.__add_menu_item(edit_menu, None, "preferences-plugin", self.__edit_addons_actions)
            self.__edit_preferences = self.__add_menu_item(edit_menu, QKeySequence.Preferences, "preferences-desktop", self.__edit_preferences_action)
            self.__edit_preferences.setMenuRole(QAction.PreferencesRole)
        
        self.__diagram, diagram_menu = self.__add_menu()
        self.__diagram_export = self.__add_menu_item(diagram_menu, None, None, self.__diagram_export_action)
        self.__diagram_full_screen = self.__add_menu_item(diagram_menu, FULL_SCREEN, "view-fullscreen",
                                                          self.__diagram_full_screen_action)

        if os.name == 'nt':
            self.__tools, tools_menu = self.__add_menu()
            self.__tools_addons = self.__add_menu_item(tools_menu, None, "preferences-plugin", self.__edit_addons_actions)
            self.__tools_options = self.__add_menu_item(tools_menu, QKeySequence.Preferences, "preferences-desktop", self.__edit_preferences_action)
        
        # VIEW MENU
        self.__view, view_menu = self.__add_menu()
        
        self.__view_zoom_in = self.__add_menu_item(view_menu, QKeySequence.ZoomIn, "zoom-in",
                                                   self.__view_zoom_in_action)
        self.__view_zoom_out = self.__add_menu_item(view_menu, QKeySequence.ZoomOut, "zoom-out",
                                                       self.__view_zoom_out_action)
        self.__view_zoom_original = self.__add_menu_item(view_menu, ZOOM_ORIGINAL, "zoom-original",
                                                            self.__view_zoom_original_action)
        
        view_menu.addSeparator()
        
        for action in main_window.get_dock_actions():
            view_menu.addAction(action)
        
        view_menu.addSeparator()
        
        for action in main_window.get_toolbar_actions():
            view_menu.addAction(action)
        
        # HELP MENU
        self.__help, help_menu = self.__add_menu()

        self.__help_about = self.__add_menu_item(help_menu, None, "help-about", self.__help_about_action)
        self.__help_about.setMenuRole(QAction.AboutRole)
        
        Application().event_dispatcher.subscribe(None, self.__event_dispatched)
        Application().event_dispatcher.subscribe(LanguageChangedEvent, self.__language_changed)
        
        self.__reload_texts()
        self.__refresh_enable()
    
    def __event_dispatched(self, event):
        self.__refresh_enable()
    
    def __language_changed(self, event):
        self.__reload_texts()

    def __add_menu(self, parent_menu=None):
        menu_item = QAction(None)
        if parent_menu is None:
            self.addAction(menu_item)
        else:
            parent_menu.addAction(menu_item)
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
        tab = Application().tabs.current_tab
        
        self.__file_save.setEnabled(Application().can_save_solution)
        self.__file_save_as.setEnabled(Application().can_save_solution_as)
        
        self.__file_recent_files.setEnabled(any(Application().recent_files))
        
        if Printing().has_printing_support:
            self.__file_page_setup.setEnabled(Printing().can_print)
            self.__file_print_preview.setEnabled(tab is not None and Printing().can_print)
            self.__file_print.setEnabled(tab is not None and Printing().can_print)
        
        self.__edit_undo.setEnabled(Application().commands.can_undo)
        self.__edit_redo.setEnabled(Application().commands.can_redo)
        self.__edit_select_all.setEnabled(tab is not None)
        
        self.__diagram.setEnabled(tab is not None)
        self.__diagram_export.setEnabled(tab is not None)
        self.__diagram_full_screen.setEnabled(tab is not None)
        
        if tab is None:
            self.__edit_cut.setEnabled(False)
            self.__edit_copy.setEnabled(False)
            self.__edit_copy_image.setEnabled(False)
            self.__edit_paste.setEnabled(False)
            self.__edit_duplicate.setEnabled(False)
            
            self.__view_zoom_in.setEnabled(False)
            self.__view_zoom_out.setEnabled(False)
            self.__view_zoom_original.setEnabled(False)
        else:
            self.__edit_cut.setEnabled(tab.drawing_area.can_copy_snippet)
            self.__edit_copy.setEnabled(tab.drawing_area.can_copy_snippet)
            self.__edit_copy_image.setEnabled(tab.drawing_area.selection.is_element_selected)
            self.__edit_paste.setEnabled(tab.drawing_area.can_paste_snippet)
            self.__edit_duplicate.setEnabled(tab.drawing_area.can_paste_snippet_duplicate)
            
            self.__view_zoom_in.setEnabled(tab.drawing_area.can_zoom_in)
            self.__view_zoom_out.setEnabled(tab.drawing_area.can_zoom_out)
            self.__view_zoom_original.setEnabled(tab.drawing_area.can_zoom_original)
    
    def __file_new_action(self, checked=False):
        self.__main_window.new_project()
    
    def __file_open_action(self, checked=False):
        self.__main_window.open_solution()
    
    def __recent_files_menu_populate(self):
        self.__recent_files_menu.setToolTipsVisible(True)
        self.__recent_files_menu.clear()
        for no, file in enumerate(list(Application().recent_files)):
            action = self.__recent_files_menu.addAction("&{0}. {1}".format(no, file.file_name))
            action.setToolTip(file.path)
            action.triggered.connect(partial(self.__main_window.open_recent_file, file))
    
    def __file_save_action(self, checked=False):
        self.__main_window.save_solution()
    
    def __file_save_as_action(self, checked=False):
        self.__main_window.save_solution_as()
    
    def __file_page_setup_action(self, checked=False):
        Printing().show_page_setup()
    
    def __file_print_preview_action(self, checked=False):
        Printing().for_diagram(Application().tabs.current_tab.drawing_area.diagram).show_preview()
    
    def __file_print_action(self, checked=False):
        Printing().for_diagram(Application().tabs.current_tab.drawing_area.diagram).print()
    
    def __file_exit_action(self, checked=False):
        self.__main_window.close()
    
    def __edit_undo_action(self, checked=False):
        Application().commands.undo()
    
    def __edit_redo_action(self, checked=False):
        Application().commands.redo()
    
    def __edit_copy_action(self, checked=False):
        drawing_area = Application().tabs.current_tab.drawing_area
        
        drawing_area.copy_snippet()
    
    def __edit_copy_image_action(self, checked=False):
        dialog = ExportDialog(self.__main_window)
        
        if dialog.exec_() == ExportDialog.Rejected:
            return
        
        selection = Application().tabs.current_tab.drawing_area.selection
        exp = ImageExport(selection, dialog.zoom, dialog.padding, dialog.transparent)
        exp.export_to_clipboard()
    
    def __edit_cut_action(self, checked=False):
        drawing_area = Application().tabs.current_tab.drawing_area
        
        drawing_area.copy_snippet()
        
        command = HideElementsCommand(drawing_area.diagram, drawing_area.selection.selected_elements)
        Application().commands.execute(command)
    
    def __edit_paste_action(self, checked=False):
        drawing_area = Application().tabs.current_tab.drawing_area
        
        command = PasteSnippetCommand(drawing_area.diagram, Application().clipboard)
        Application().commands.execute(command)
        drawing_area.selection.select(command.element_visuals)
    
    def __edit_duplicate_action(self, checked=False):
        drawing_area = Application().tabs.current_tab.drawing_area
        
        command = DuplicateSnippetCommand(drawing_area.diagram, Application().clipboard)
        Application().commands.execute(command)
        drawing_area.selection.select(command.element_visuals)
    
    def __edit_select_all_action(self, checked=False):
        Application().tabs.current_tab.drawing_area.selection.select_all()
    
    def __edit_addons_actions(self, checked=False):
        AddOnsDialog(self.__main_window).exec_()
    
    def __edit_preferences_action(self, checked=False):
        SettingsDialog(self.__main_window).exec_()
    
    def __diagram_export_action(self, checked=False):
        dialog = ExportDialog(self.__main_window)
        
        if dialog.exec_() == ExportDialog.Rejected:
            return
        
        diagram = Application().tabs.current_tab.drawing_area.diagram
        exp = ImageExport(diagram, dialog.zoom, dialog.padding, dialog.transparent)
        filters = []
        default = exp.default_format
        default_filter = None
        for formats in exp.supported_formats():
            file_names = " ".join("*.{0}".format(i) for i in formats)
            filter_text = _("{0} image").format(formats[0].upper()) + "({0})".format(file_names)
            filters.append((filter_text, formats[0]))
            if default in formats:
                default_filter = filter_text
        
        file_name, filter = QFileDialog.getSaveFileName(
            self,
            caption=_("Export Diagram"),
            filter=";;".join(text for text, format in filters),
            initialFilter=default_filter
        )
        
        if file_name:
            for text, formats in filters:
                if text == filter:
                    break
            else:
                raise Exception
            
            if '.' not in os.path.basename(file_name):
                file_name = file_name + '.' + formats
            
            exp.export(file_name, formats)
    
    def __diagram_full_screen_action(self):
        # needs to keep reference to a window to prevent it to be garbage collected
        self.__window = FullScreenDiagram(self.__main_window, Application().tabs.current_tab.drawing_area)
        self.__window.showFullScreen()
    
    def __view_zoom_in_action(self, checked=False):
        Application().tabs.current_tab.drawing_area.zoom_in()
    
    def __view_zoom_out_action(self, checked=False):
        Application().tabs.current_tab.drawing_area.zoom_out()
    
    def __view_zoom_original_action(self, checked=False):
        Application().tabs.current_tab.drawing_area.zoom_original()
    
    def __help_about_action(self):
        dlg = AboutDialog(self.__main_window)
        dlg.exec_()
    
    def __reload_texts(self):
        self.__file.setText(_("&File"))
        self.__file_new.setText(_("&New"))
        self.__file_open.setText(_("&Open"))
        self.__file_recent_files.setText(_("&Recent Files"))
        self.__file_save.setText(_("&Save"))
        self.__file_save_as.setText(_("Save &as"))
        if Printing().has_printing_support:
            self.__file_page_setup.setText(_("Pa&ge setup"))
            self.__file_print_preview.setText(_("Print pre&view"))
            self.__file_print.setText(_("&Print"))
        self.__file_exit.setText(_("&Quit"))
        
        self.__edit.setText(_("&Edit"))
        self.__edit_undo.setText(_("&Undo"))
        self.__edit_redo.setText(_("&Redo"))
        self.__edit_cut.setText(_("C&ut"))
        self.__edit_copy.setText(_("&Copy"))
        self.__edit_copy_image.setText(_("&Copy as Image"))
        self.__edit_paste.setText(_("&Paste"))
        self.__edit_duplicate.setText(_("Paste &Duplicate"))
        self.__edit_select_all.setText(_("Select &All"))

        if os.name != 'nt':
            self.__edit_addons.setText(_("Add-ons"))
            self.__edit_preferences.setText(_("Preferences"))
        
        self.__diagram.setText(_("&Diagram"))
        self.__diagram_export.setText(_("Export as &Image"))
        self.__diagram_full_screen.setText(_("Show Full &Screen"))

        if os.name == 'nt':
            self.__tools.setText(_("&Tools"))
            self.__tools_addons.setText(_("Add-ons"))
            self.__tools_options.setText(_("Options"))
        
        self.__view.setText(_("&View"))
        self.__view_zoom_in.setText(_("Zoom &In"))
        self.__view_zoom_out.setText(_("Zoom &Out"))
        self.__view_zoom_original.setText(_("O&riginal Zoom"))
        
        self.__help.setText(_("&Help"))
        self.__help_about.setText(_("&About"))
