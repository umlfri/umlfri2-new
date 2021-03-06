from umlfri2.metamodel.projecttemplate import ProjectTemplate, ElementTemplate, DiagramTemplate, ConnectionTemplate, \
    ElementVisualTemplate, ConnectionVisualTemplate, DiagramTemplateState
from umlfri2.types.geometry import Point, Size
from ....constants import ADDON_NAMESPACE, ADDON_SCHEMA


class TemplateLoader:
    def __init__(self, xmlroot):
        self.__last_id = 0
        self.__xmlroot = xmlroot
        if not ADDON_SCHEMA.validate(xmlroot):
            raise Exception("Cannot load project: {0}".format(ADDON_SCHEMA.error_log.last_error))
    
    def load(self):
        id = self.__xmlroot.attrib["id"]
        elements = []
        self.__all_diagrams = []
        self.__all_connections = []
        self.__provided_ids = {}
        self.__required_ids = {}
        
        for node in self.__xmlroot:
            if node.tag == "{{{0}}}Element".format(ADDON_NAMESPACE):
                elements.append(self.__load_element(node))

        self.__check_ids()
        
        return ProjectTemplate(id, elements, self.__all_connections, self.__all_diagrams)

    def __load_element(self, node):
        type = node.attrib["type"]
        id = node.attrib.get("id") or self.__new_id()
        
        self.__provide_id(id, 'element')
        
        children = []
        data = {}
        
        for child in node:
            if child.tag == "{{{0}}}Element".format(ADDON_NAMESPACE):
                children.append(self.__load_element(child))
            elif child.tag == "{{{0}}}Connection".format(ADDON_NAMESPACE):
                self.__all_connections.append(self.__load_connection(child, id))
            elif child.tag == "{{{0}}}Diagram".format(ADDON_NAMESPACE):
                self.__all_diagrams.append(self.__load_diagram(child, id))
            elif child.tag == "{{{0}}}Attribute".format(ADDON_NAMESPACE):
                self.__load_attribute(child, data)

        return ElementTemplate(type, data, children, id)
    
    def __load_data(self, node):
        if "value" in node.attrib:
            return node.attrib["value"]
        
        data_attribs = {}
        data_values  = []
        
        for child in node:
            if child.tag == "{{{0}}}Attribute".format(ADDON_NAMESPACE):
                self.__load_attribute(child, data_attribs)
            elif child.tag == "{{{0}}}Item".format(ADDON_NAMESPACE):
                self.__load_item(child, data_values)
        
        return data_attribs or data_values
    
    def __load_attribute(self, node, attributes):
        attributes[node.attrib["id"]] = self.__load_data(node)
    
    def __load_item(self, node, items):
        items.append(self.__load_data(node))

    def __load_connection(self, node, source_id):
        type = node.attrib["type"]
        destination_id = node.attrib["to"]
        id = node.attrib.get("id") or self.__new_id()
        
        self.__require_id(source_id, 'element')
        self.__require_id(destination_id, 'element')
        self.__provide_id(id, 'connection')
        
        data = {}

        for child in node:
            if child.tag == "{{{0}}}Attribute".format(ADDON_NAMESPACE):
                self.__load_attribute(child, data)
        
        return ConnectionTemplate(type, data, source_id, destination_id, id)
    
    def __load_diagram(self, node, parent_id):
        type = node.attrib["type"]
        
        self.__require_id(parent_id, 'element')
        
        data = {}
        elements = []
        connections = []
        
        for child in node:
            if child.tag == "{{{0}}}Attribute".format(ADDON_NAMESPACE):
                self.__load_attribute(child, data)
            elif child.tag == "{{{0}}}Element".format(ADDON_NAMESPACE):
                elements.append(self.__load_element_visual(child))
            elif child.tag == "{{{0}}}Connection".format(ADDON_NAMESPACE):
                connections.append(self.__load_connection_visual(child))
        
        state = DiagramTemplateState[node.attrib.get("state", "closed")]
        
        return DiagramTemplate(type, data, elements, connections, parent_id, state=state)
    
    def __load_element_visual(self, node):
        id = node.attrib["id"]
        
        self.__require_id(id, 'element')
        
        position = None
        if "x" in node.attrib or "y" in node.attrib:
            position = self.__get_position(node)
        
        size = None
        if "width" in node.attrib or "height" in node.attrib:
            size = self.__get_size(node)

        return ElementVisualTemplate(id, position, size)

    def __load_connection_visual(self, node):
        id = node.attrib["id"]
        
        self.__require_id(id, 'connection')
        
        points = []
        
        for child in node:
            if child.tag == "{{{0}}}Point".format(ADDON_NAMESPACE):
                points.append(self.__get_position(child))
        
        return ConnectionVisualTemplate(id, points)
    
    def __get_position(self, node):
        return Point(int(node.attrib.get("x", 0)), int(node.attrib.get("y", 0)))
    
    def __get_size(self, node):
        return Size(int(node.attrib.get("width", 0)), int(node.attrib.get("height", 0)))
    
    def __provide_id(self, id, type):
        if id in self.__provided_ids:
            raise Exception("Duplicated id in a template: {0}".format(id))
        
        self.__provided_ids[id] = type
    
    def __require_id(self, id, type):
        if id in self.__required_ids:
            if type != self.__required_ids[id]:
                raise Exception("Invalid references in the template")

        self.__required_ids[id] = type
    
    def __new_id(self):
        self.__last_id += 1
        return self.__last_id

    def __check_ids(self):
        for id, type in self.__required_ids.items():
            if id not in self.__provided_ids or self.__provided_ids[id] != type:
                raise Exception("Invalid references in the template")
