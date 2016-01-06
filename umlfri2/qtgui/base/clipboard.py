from PySide.QtCore import QMimeData
from PySide.QtGui import QApplication, QClipboard

from umlfri2.application import Application
from umlfri2.application.events.application import ClipboardSnippetChangedEvent
from umlfri2.application.snippet import Snippet


class QtClipboardAdatper:
    UMLFRI_CLIPBOARD_FORMAT = 'application/umlfri-snippet'
    
    def __init__(self):
        self.__clipboard = QApplication.clipboard()
        self.__last_snippet = Application().clipboard
        self.__serialized = None
        
        self.__clipboard.changed.connect(self.__qt_clipboard_changed)
        Application().event_dispatcher.subscribe(ClipboardSnippetChangedEvent, self.__umlfri_clipboard_changed)
    
    def __qt_clipboard_changed(self, mode):
        if mode != QClipboard.Clipboard:
            return
        
        mime_data = self.__clipboard.mimeData()
        if mime_data.hasFormat(self.UMLFRI_CLIPBOARD_FORMAT):
            serialized = mime_data.data(self.UMLFRI_CLIPBOARD_FORMAT).data()
            if serialized == self.__serialized:
                return False
            self.__serialized = serialized
            self.__last_snippet = Snippet.deserialize(serialized.decode('utf8'))
            
            Application().clipboard = self.__last_snippet
        else:
            Application().clipboard = None
    
    def __umlfri_clipboard_changed(self, event):
        if event.new_snippet is None:
            return
        
        if event.new_snippet is not self.__last_snippet:
            self.__last_snippet = event.new_snippet
            
            self.__mime_data = QMimeData() # keep reference
            self.__serialized = event.new_snippet.serialize().encode('utf8')
            self.__mime_data.setData(self.UMLFRI_CLIPBOARD_FORMAT, self.__serialized)
            self.__clipboard.setMimeData(self.__mime_data, QClipboard.Clipboard)