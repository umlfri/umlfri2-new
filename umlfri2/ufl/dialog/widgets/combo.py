from .valued import UflDialogValuedWidget


class UflDialogComboWidget(UflDialogValuedWidget):
    def __init__(self, tab, id, label, possibilities): 
        super().__init__(tab, id, label)
        self.__possibilities = possibilities
    
    @property
    def possibilities(self):
        yield from self.__possibilities