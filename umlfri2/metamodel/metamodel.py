from collections import OrderedDict
from weakref import ref

from .translation import TranslationList


class Metamodel:
    def __init__(self, diagrams, elements, connections, templates, translations, config):
        self.__diagrams = OrderedDict(item for item in sorted(diagrams.items()))
        self.__elements = OrderedDict(item for item in sorted(elements.items()))
        self.__connections = OrderedDict(item for item in sorted(connections.items()))
        self.__templates = list(templates)
        self.__templates.sort(key=lambda item: item.file_name)
        self.__translations = TranslationList(translations)
        
        if config is None:
            self.__config_structure = UflObjectType({})
            self.__has_config = False
        else:
            self.__config_structure = config
            self.__has_config = True
        self.__config_structure.set_parent(None)
        self.__config = self.__config_structure.build_default(None)
        
        self.__addon = None
    
    def _set_addon(self, addon):
        self.__addon = ref(addon)
        
        for diagram in self.__diagrams.values():
            diagram._set_metamodel(self)
        
        for element in self.__elements.values():
            element._set_metamodel(self)
        
        for connection in self.__connections.values():
            connection._set_metamodel(self)
        
        for template in self.__templates:
            template._set_metamodel(self)
    
    @property
    def addon(self):
        return self.__addon()
    
    @property
    def diagram_types(self):
        yield from self.__diagrams.values()
    
    @property
    def element_types(self):
        yield from self.__elements.values()
    
    @property
    def connection_types(self):
        yield from self.__connections.values()
    
    @property
    def templates(self):
        yield from self.__templates
    
    def get_element_type(self, name):
        return self.__elements[name]
    
    def get_diagram_type(self, name):
        return self.__diagrams[name]
    
    def get_connection_type(self, name):
        return self.__connections[name]

    def get_translation(self, language):
        return self.__translations.get_translation(language)
    
    @property
    def config_structure(self):
        return self.__config_structure
    
    @property
    def config(self):
        return self.__config
    
    @property
    def has_config(self):
        return self.__has_config
    
    def compile(self):
        for diagram in self.__diagrams.values():
            diagram.compile()
        
        for element in self.__elements.values():
            element.compile()
        
        for connection in self.__connections.values():
            connection.compile()
