from umlfri2.types.image import Image
from .componentloader import ComponentLoader
from ..constants import ADDON_NAMESPACE, ADDON_SCHEMA
from .structureloader import UflStructureLoader
from umlfri2.components.text import TextContainerComponent
from umlfri2.metamodel import ElementType, DefaultElementAction


class ElementTypeLoader:
    def __init__(self, storage, xmlroot, definitions):
        self.__storage = storage
        self.__xmlroot = xmlroot
        self.__defintions = definitions
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load element type: {0}".format(ADDON_SCHEMA.error_log.last_error))
    
    def load(self):
        id = self.__xmlroot.attrib["id"]
        icon = None
        ufl_type = None
        display_name = None
        appearance = None
        default_action = DefaultElementAction.properties
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}Icon".format(ADDON_NAMESPACE):
                icon_path = child.attrib["path"]
                if not self.__storage.exists(icon_path):
                    raise Exception("Unknown icon {0}".format(icon_path))
                icon = Image(self.__storage, icon_path)
            elif child.tag == "{{{0}}}Structure".format(ADDON_NAMESPACE):
                ufl_type = UflStructureLoader(child).load()
            elif child.tag == "{{{0}}}DisplayName".format(ADDON_NAMESPACE):
                display_name = TextContainerComponent(ComponentLoader(child, 'text').load())
            elif child.tag == "{{{0}}}Config".format(ADDON_NAMESPACE):
                for childchild in child:
                    if childchild.tag == "{{{0}}}DefaultAction".format(ADDON_NAMESPACE):
                        if childchild.attrib["action"] == 'subdiagram':
                            default_action = DefaultElementAction.subdiagram
                        elif childchild.attrib["action"] == 'properties':
                            default_action = DefaultElementAction.properties
                        else:
                            raise Exception
                    else:
                        raise Exception
            elif child.tag == "{{{0}}}Appearance".format(ADDON_NAMESPACE):
                appearance = ComponentLoader(child, 'visual', self.__defintions).load()[0]
            else:
                raise Exception
        
        return ElementType(id, icon, ufl_type, display_name, appearance, default_action)
