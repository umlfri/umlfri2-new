from weakref import ref


class ConnectionType:
    def __init__(self, id, icon, ufl_type, appearance, labels):
        self.__metamodel = None
        self.__id = id
        self.__icon = icon
        self.__ufl_type = ufl_type
        self.__appearance = appearance
        self.__labels = tuple(labels)
    
    def _set_metamodel(self, metamodel):
        self.__metamodel = ref(metamodel)
        
        for label in self.__labels:
            label._set_connection_type(self)
    
    @property
    def metamodel(self):
        return self.__metamodel()
    
    @property
    def id(self):
        return self.__id
    
    @property
    def icon(self):
        return self.__icon
    
    @property
    def ufl_type(self):
        return self.__ufl_type
    
    @property
    def labels(self):
        return self.__labels
    
    def compile(self):
        variables = {'self': self.__ufl_type, 'cfg': self.__metamodel().addon.config_structure}
        
        self.__appearance.compile(variables)
        for label in self.__labels:
            label.compile(variables)
    
    def create_appearance_object(self, context, ruler):
        context.set_config(self.__metamodel().addon.config)
        return self.__appearance.create_connection_object(context)