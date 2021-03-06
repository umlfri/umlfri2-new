from umlfri2.ufl.types.enum import UflDefinedEnumType
from umlfri2.ufl.types.structured import UflNullableType


class TypeContext:
    def __init__(self, definitions):
        self.__definitions = definitions
        self.__local_types = {}
    
    def get_variable_type(self, name):
        return self.__local_types[name]
    
    def as_dict(self, prefix=None):
        if prefix is None:
            return self.__local_types.copy()
        else:
            return {prefix + k: v for k, v in self.__local_types.items()}
    
    def resolve_defined_enum(self, type):
        if isinstance(type, UflDefinedEnumType):
            return UflDefinedEnumType(type.type, self.__definitions.get(type.type.__name__, {}))
        elif isinstance(type, UflNullableType) and isinstance(type.inner_type, UflDefinedEnumType):
            return UflNullableType(self.resolve_defined_enum(type.inner_type))
        else:
            return type
    
    def set_variable_type(self, name, type):
        ret = TypeContext(self.__definitions)
        ret.__local_types = self.__local_types.copy()
        ret.__local_types[name] = type
        return ret
