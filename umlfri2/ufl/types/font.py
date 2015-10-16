from .type import UflType
from .integer import UflIntegerType
from .string import UflStringType
from .typedenum import UflTypedEnumType
from umlfri2.types.font import FontStyle


class UflFontType(UflType):
    def __init__(self, default=None):
        self.__default = default
    
    @property
    def default(self):
        return self.__default

UflFontType.ALLOWED_DIRECT_ATTRIBUTES = {
    'size': ('size', UflIntegerType),
    'style': ('style', UflTypedEnumType(FontStyle)),
    'family': ('family', UflStringType),
}

UflFontType.ALLOWED_DIRECT_METHODS = {
    'change': ('change', (UflStringType, UflTypedEnumType(FontStyle)), UflFontType)
}
