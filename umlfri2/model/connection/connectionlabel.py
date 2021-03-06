import math
from weakref import ref

from ..cache import ModelTemporaryDataCache
from umlfri2.types.geometry import Vector, Rectangle, Line, Point


class ConnectionLabel:
    def __init__(self, connection, id):
        self.__cache = ModelTemporaryDataCache(self.__create_appearance_object)
        self.__cache.depend_on(connection.cache)
        
        self.__connection = ref(connection)
        self.__id = id
        self.__cached_appearance = None
        self.__line_index = 0
        self.__line_position = connection.object.type.get_label(id).position.value
        self.__angle = math.pi/2
        self.__distance = 0
    
    @property
    def cache(self):
        return self.__cache
    
    @property
    def connection(self):
        return self.__connection()
    
    @property
    def id(self):
        return self.__id
    
    @property
    def line_index(self):
        return self.__line_index
    
    def get_position(self, ruler):
        self.__cache.ensure_valid(ruler=ruler)
        
        return self.__cached_appearance.position
    
    def move(self, ruler, new_position):
        self.__cache.ensure_valid(ruler=ruler)
        
        new_center = Rectangle.from_point_size(new_position, self.__cached_appearance.get_minimal_size()).center
        
        new_index = None
        new_distance = float('inf')
        new_position = None
        new_angle = None
        
        points = list(self.__connection().get_points(ruler))
        
        old_point = points.pop(0)
        for idx, point in enumerate(points):
            line = Line.from_point_point(old_point, point)
            
            point_on_line = line.get_nearest_point_to(new_center)
            
            cur_distance = (new_center - point_on_line).length
            
            if new_distance > cur_distance:
                new_distance = cur_distance
                new_index = idx
                if point.x == old_point.x:
                    if point.y == old_point.y:
                        new_position = 0
                    else:
                        new_position = (point_on_line.y - old_point.y) / (point.y - old_point.y)
                else:
                    new_position = (point_on_line.x - old_point.x) / (point.x - old_point.x)
                
                first_angle = math.atan2(new_center.y - point_on_line.y, new_center.x - point_on_line.x)
                second_angle = math.atan2(point.y - old_point.y, point.x - old_point.x)
                new_angle = first_angle - second_angle
            
            old_point = point
        
        self.__distance = new_distance
        self.__line_index = new_index
        self.__line_position = new_position
        self.__angle = new_angle
        
        self.__cache.invalidate()
    
    def _adding_point(self, line_index, line1_length, line2_length):
        if line_index < self.__line_index:
            self.__line_index += 1
            self.__cache.invalidate()
        elif line_index == self.__line_index:
            if line1_length == 0:
                self.__line_index += 1
            elif line2_length > 0:
                proportions = line1_length / (line1_length + line2_length)
                if self.__line_position < proportions:
                    self.__line_position = self.__line_position / proportions
                else:
                    self.__line_position = (self.__line_position - proportions) / (1 - proportions)
                    self.__line_index += 1
                self.__cache.invalidate()
    
    def _removing_point(self, line_index, line1_length, line2_length):
        if line_index + 1 < self.__line_index:
            self.__line_index -= 1
            self.__cache.invalidate()
        else:
            proportions = line1_length / (line1_length + line2_length)
            
            if line_index + 1 == self.__line_index:
                self.__line_position = self.__line_position * (1 - proportions) + proportions
                self.__line_index -= 1
                self.__cache.invalidate()
            elif line_index == self.__line_index:
                self.__line_position = self.__line_position * proportions
                self.__cache.invalidate()
    
    def get_bounds(self, ruler):
        self.__cache.ensure_valid(ruler=ruler)
        
        return Rectangle.from_point_size(self.__cached_appearance.position, self.__cached_appearance.size)
    
    def is_at_position(self, ruler, position):
        return self.get_bounds(ruler).contains(position)
    
    def get_nearest_point(self, ruler):
        first_point = self.__connection().get_point(ruler, self.__line_index)
        second_point = self.__connection().get_point(ruler, self.__line_index + 1)
        
        return first_point + (second_point - first_point) * self.__line_position
    
    def draw(self, canvas):
        self.__cache.ensure_valid(ruler=canvas.get_ruler())
        
        self.__cached_appearance.draw(canvas)

    def __create_appearance_object(self, ruler):
        self.__cached_appearance = self.__connection().object.create_label_object(self.__id, ruler)
        first_point = self.__connection().get_point(ruler, self.__line_index)
        second_point = self.__connection().get_point(ruler, self.__line_index + 1)
        
        line_vector = second_point - first_point
        
        vector_to_label = Vector.from_angle_length(line_vector.angle + self.__angle, self.__distance)
        
        position = first_point\
                   + line_vector * self.__line_position\
                   + vector_to_label\
                   - self.__cached_appearance.size.as_vector() / 2
        
        x, y = round(position.x), round(position.y)
        
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        
        self.__cached_appearance.move(Point(x, y))
