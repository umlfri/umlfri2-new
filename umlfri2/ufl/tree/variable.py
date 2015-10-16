from .node import UflNode

class UflVariable(UflNode):
    def __init__(self, name):
        self.__name = name
    
    @property
    def name(self):
        return self.__name
    
    def _get_params(self):
        return self.__name,

    def accept(self, visitor):
        return visitor.visit_variable(self)
