from .enum import UflEnumType
from .enumpossibility import UflEnumPossibility


class UflTypedEnumType(UflEnumType):
    def __init__(self, type, default=None):
        self.__type = type
        
        items = tuple(i for i in dir(type) if not i.startswith('_'))
        super().__init__((UflEnumPossibility(self, item, getattr(type, item)) for item in items), default)
    
    @property
    def name(self):
        return self.__type.__name__
    
    @property
    def type(self):
        return self.__type
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        return self.__type == other.__type
    
    def __str__(self):
        return 'TypedEnum[{0}]'.format(self.name)
