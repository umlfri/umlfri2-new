import math

from umlfri2.ufl.components.visual.rectangle import CornerDefinition, SideDefinition
from ....constants import ADDON_NAMESPACE, ADDON_SCHEMA
from umlfri2.ufl.components.connectionvisual.arrow import ArrowDefinition
from umlfri2.types.geometry import PathBuilder, Point, Size


class DefinitionsLoader:
    def __init__(self, xmlroot):
        self.__xmlroot = xmlroot
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load definitions: {0}".format(ADDON_SCHEMA.error_log.last_error))
    
    def load(self):
        definitions = {
            "ArrowDefinition": {},
            "CornerDefinition": {},
            "SideDefinition": {},
        }
        
        for child in self.__xmlroot:
            if child.tag == "{{{0}}}ArrowDefinition".format(ADDON_NAMESPACE):
                definition = ArrowDefinition(
                    child.attrib["id"],
                    PathBuilder().from_string(child.attrib["path"]).build(),
                    Point.parse(child.attrib["center"]),
                    self.__parse_rotation(child.attrib["rotation"])
                )
                definitions["ArrowDefinition"][definition.id] = definition
            elif child.tag == "{{{0}}}CornerDefinition".format(ADDON_NAMESPACE):
                ornament = None
                if "ornament" in child.attrib:
                    ornament = PathBuilder().from_string(child.attrib["ornament"]).build()
                
                definition = CornerDefinition(
                    child.attrib["id"],
                    PathBuilder().from_string(child.attrib["path"]).build(),
                    ornament,
                    Point.parse(child.attrib["center"]),
                    child.attrib["corner"]
                )
                definitions["CornerDefinition"][definition.id] = definition
            elif child.tag == "{{{0}}}SideDefinition".format(ADDON_NAMESPACE):
                ornament = None
                if "ornament" in child.attrib:
                    ornament = PathBuilder().from_string(child.attrib["ornament"]).build()
                
                definition = SideDefinition(
                    child.attrib["id"],
                    PathBuilder().from_string(child.attrib["path"]).build(),
                    ornament,
                    Point.parse(child.attrib["center"]),
                    Size(int(child.attrib["width"]), int(child.attrib["height"])),
                    child.attrib["side"]
                )
                definitions["SideDefinition"][definition.id] = definition
        
        return definitions

    def __parse_rotation(self, value):
        if value.endswith("°"):
            return int(value[:-1]) * math.pi / 180
        else:
            return float(value)
