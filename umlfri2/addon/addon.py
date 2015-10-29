class AddOn:
    def __init__(self, identifier, name, version, author, homepage, license, icon, description, config, translations, metamodel):
        self.__identifier = identifier
        self.__name = name
        self.__version = version
        self.__author = author
        self.__homepage = homepage
        self.__license = license
        self.__icon = icon
        self.__description = description
        self.__config_structure = config
        self.__config = config.build_default()
        self.__translations = translations
        self.__metamodel = metamodel
        self.__metamodel._set_addon(self)
    
    @property
    def identifier(self):
        return self.__identifier
    
    @property
    def name(self):
        return self.__name
    
    @property
    def version(self):
        return self.__version
    
    @property
    def author(self):
        return self.__author
    
    @property
    def homepage(self):
        return self.__homepage
    
    @property
    def license(self):
        return self.__license
    
    @property
    def icon(self):
        return self.__icon
    
    @property
    def description(self):
        return self.__description
    
    @property
    def config_structure(self):
        return self.__config_structure
    
    @property
    def config(self):
        return self.__config
    
    @property
    def translations(self):
        return self.__translations
    
    @property
    def metamodel(self):
        return self.__metamodel
    
    def compile(self):
        self.__metamodel.compile()