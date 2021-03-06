from weakref import ref


class UflDialogWidget:
    def __init__(self, tab, attr, type):
        self.__tab = ref(tab)
        self.__attr = attr
        self.__label = None
        self.__attr = attr
        self.__type = type
    
    @property
    def tab(self):
        return self.__tab()
    
    @property
    def value(self):
        raise NotImplementedError
    
    @property
    def attribute(self):
        return self.__attr
    
    @property
    def type(self):
        return self.__type
    
    @property
    def id(self):
        if self.__attr is None:
            return None
        else:
            return self.__attr.name
    
    @property
    def label(self):
        return self.__label
    
    def associate(self, ufl_object):
        raise NotImplementedError
    
    def associate_default(self):
        raise NotImplementedError
    
    def translate(self, translation):
        if self.__attr is not None:
            self.__label = translation.translate(self.__attr)
    
    @property
    def changed(self):
        raise NotImplementedError
    
    def finish_after_save(self):
        raise NotImplementedError
    
    def discard(self):
        raise NotImplementedError
