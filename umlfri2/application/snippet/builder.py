from .snippet import Snippet
from umlfri2.ufl.types.structured import UflObjectType, UflListType, UflNullableType
from umlfri2.ufl.types.complex import UflFontType, UflColorType, UflImageType, UflProportionType
from umlfri2.ufl.types.enum import UflFlagsType


class SnippetBuilder:
    def __init__(self, project):
        self.__visuals = []
        self.__project = project
        self.__finished = False
    
    def add_element(self, ruler, visual):
        if self.__finished:
            raise Exception
        
        data = {}
        
        data['kind'] = 'element'
        
        data['id'] = str(visual.object.save_id)
        
        data['type'] = visual.object.type.id
        
        bounds = visual.get_bounds(ruler)
        data['x'] = bounds.x1
        data['y'] = bounds.y1
        data['width'] = bounds.width
        data['height'] = bounds.height
        
        data['data'] = self.__convert_ufl_object(visual.object.data, visual.object.type.ufl_type)
        
        self.__visuals.append(data)
        
        return self
    
    def add_connection(self, ruler, visual):
        if self.__finished:
            raise Exception
        
        data = {}
        
        data['kind'] = 'connection'
        
        data['id'] = str(visual.object.save_id)
        
        data['type'] = visual.object.type.id
        
        data['source'] = str(visual.object.source.save_id)
        data['destination'] = str(visual.object.destination.save_id)
        
        points = []
        for point in visual.get_points(ruler, False, False):
            points.append({'x': point.x, 'y': point.y})
        
        data['points'] = points
        
        labels = {}
        
        for label in visual.get_labels():
            point = label.get_position(ruler)
            labels[label.id] = {'x': point.x, 'y': point.y}
        
        data['labels'] = labels
        
        data['data'] = self.__convert_ufl_object(visual.object.data, visual.object.type.ufl_type)
        
        self.__visuals.append(data)
        
        return self
    
    def __convert_ufl_value(self, ufl_value, ufl_type):
        if isinstance(ufl_type, UflObjectType):
            return self.__convert_ufl_object(ufl_value, ufl_type)
        elif isinstance(ufl_type, UflListType):
            return [self.__convert_ufl_value(item, ufl_type.item_type) for item in ufl_value]
        elif isinstance(ufl_type, UflFlagsType):
            return list(ufl_value)
        elif isinstance(ufl_type, UflNullableType):
            if ufl_value is None:
                return None
            else:
                return self.__convert_ufl_value(ufl_value, ufl_type.inner_type)
        else:
            return self.__convert_ufl_immutable(ufl_value, ufl_type)
    
    def __convert_ufl_object(self, ufl_object, ufl_type):
        ret = {}
        
        for attribute in ufl_type.attributes:
            value = ufl_object.get_value(attribute.name)
            ret[attribute.name] = self.__convert_ufl_value(value, attribute.type)
        
        return ret
    
    def __convert_ufl_immutable(self, ufl_value, ufl_type):
        if isinstance(ufl_type, (UflColorType, UflFontType, UflProportionType)):
            return str(ufl_value)
        elif isinstance(ufl_type, UflImageType):
            raise NotImplementedError("Image type cannot be copied to a snippet yet") # TODO
        else:
            return ufl_value
    
    def build(self):
        ret = {}
        
        ret['project'] = str(self.__project.save_id)
        ret['metamodel'] = self.__project.metamodel.addon.identifier
        ret['objects'] = tuple(self.__visuals)
        
        self.__finished = True
        
        return Snippet(ret)
