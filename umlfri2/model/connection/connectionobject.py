from _weakrefset import WeakSet
from uuid import uuid4
from weakref import ref
from umlfri2.components.base.context import Context
from umlfri2.model.cache import ModelTemporaryDataCache
from umlfri2.ufl.dialog import UflDialog, UflDialogOptions


class ConnectionObject:
    def __init__(self, type, source, destination, save_id=None):
        self.__type = type
        self.__data = type.ufl_type.build_default(None)
        self.__source = ref(source)
        self.__destination = ref(destination)
        self.__visuals = WeakSet()
        self.__cache = ModelTemporaryDataCache(None)
        if save_id is None:
            self.__save_id = uuid4()
        else:
            self.__save_id = save_id
    
    def add_visual(self, visual):
        if visual.object is not self:
            raise Exception
        self.__visuals.add(visual)
    
    def remove_visual(self, visual):
        self.__visuals.remove(visual)
    
    @property
    def visuals(self):
        yield from self.__visuals
    
    @property
    def cache(self):
        return self.__cache
    
    @property
    def type(self):
        return self.__type
    
    @property
    def data(self):
        return self.__data
    
    @property
    def source(self):
        return self.__source()
    
    @property
    def destination(self):
        return self.__destination()
    
    def get_other_end(self, element):
        if self.__source() is element:
            return self.__destination
        elif self.__destination() is element:
            return self.__source
        else:
            return None
    
    def is_connected_with(self, element):
        return self.__source() is element or self.__destination() is element
    
    @property
    def save_id(self):
        return self.__save_id
    
    def create_appearance_object(self, ruler):
        context = Context().extend(self.__data, 'self')
        return self.__type.create_appearance_object(context, ruler)
    
    def create_label_object(self, id, ruler):
        context = Context().extend(self.__data, 'self')
        return self.__type.get_label(id).create_appearance_object(context, ruler)
    
    def apply_ufl_patch(self, patch):
        self.__data.apply_patch(patch)
        self.__cache.refresh()
    
    @property
    def has_ufl_dialog(self):
        return self.__type.ufl_type.has_attributes
    
    def create_ufl_dialog(self, language, options=UflDialogOptions.standard):
        if not self.__type.ufl_type.has_attributes:
            raise Exception
        translation = self.__type.metamodel.addon.get_translation(language)
        dialog = UflDialog(self.__type.ufl_type, translation, options)
        dialog.associate(self.__data)
        return dialog
