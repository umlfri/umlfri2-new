from .point import SnappedPoint
from .rectangle import SnappedRectangle
from umlfri2.types.geometry import Point, Vector


class InitializedSnapping:
    MAXIMAL_DISTANCE = 10
    
    def __init__(self, rectangles, points):
        self.__center_guidelines = []
        self.__vertical_guidelines = []
        self.__horizontal_guidelines = []
        
        self.__center_guidelines.extend(points)
        
        for rectangle in rectangles:
            self.__center_guidelines.append(rectangle.center)
            self.__vertical_guidelines.append(rectangle.top_center)
            self.__vertical_guidelines.append(rectangle.bottom_center)
            self.__horizontal_guidelines.append(rectangle.left_center)
            self.__horizontal_guidelines.append(rectangle.right_center)
    
    def add_point(self, point):
        self.__center_guidelines.append(point)
    
    def snap_point(self, point):
        best_horizontal = None
        best_horizontal_distance = self.MAXIMAL_DISTANCE
        best_vertical = None
        best_vertical_distance = self.MAXIMAL_DISTANCE
        
        for guideline in self.__center_guidelines:
            horizontal_distance = abs(guideline.x - point.x)
            vertical_distance = abs(guideline.y - point.y)
            if horizontal_distance < best_horizontal_distance:
                best_horizontal_distance = horizontal_distance
                best_horizontal = guideline
            if vertical_distance < best_vertical_distance:
                best_vertical_distance = vertical_distance
                best_vertical = guideline
        
        horizontal_indicators = set()
        vertical_indicators = set()
        
        if best_horizontal is not None and best_vertical is not None:
            point = Point(best_horizontal.x, best_vertical.y)
        elif best_horizontal is not None:
            point = Point(best_horizontal.x, point.y)
        elif best_vertical is not None:
            point = Point(point.x, best_vertical.y)
        
        if best_horizontal is not None:
            for guideline in self.__center_guidelines:
                if best_horizontal.x == guideline.x:
                    horizontal_indicators.add(guideline)
            horizontal_indicators.add(point)
        
        if best_vertical is not None:
            for guideline in self.__center_guidelines:
                if best_vertical.y == guideline.y:
                    vertical_indicators.add(guideline)
            vertical_indicators.add(point)
        
        return SnappedPoint(point, horizontal_indicators, vertical_indicators)
    
    def __snap_point_horizontally(self, point):
        best = None
        best_distance = self.MAXIMAL_DISTANCE
        
        for guideline in self.__horizontal_guidelines:
            horizontal_distance = abs(guideline.x - point.x)
            if horizontal_distance < best_distance:
                best_distance = horizontal_distance
                best = guideline
        
        indicators = set()
        
        if best is not None:
            point = Point(best.x, point.y)
            for guideline in self.__horizontal_guidelines:
                if best.x == guideline.x:
                    indicators.add(guideline)
            indicators.add(point)
            
            return SnappedPoint(point, horizontal_indicators=indicators)
        
        return SnappedPoint(point)
    
    def __snap_point_vertically(self, point):
        best_vertical = None
        best_vertical_distance = self.MAXIMAL_DISTANCE
        
        for guideline in self.__vertical_guidelines:
            vertical_distance = abs(guideline.y - point.y)
            if vertical_distance < best_vertical_distance:
                best_vertical_distance = vertical_distance
                best_vertical = guideline
        
        vertical_indicators = set()
        
        if best_vertical is not None:
            point = Point(point.x, best_vertical.y)
            for guideline in self.__vertical_guidelines:
                if best_vertical.y == guideline.y:
                    vertical_indicators.add(guideline)
            vertical_indicators.add(point)
            
            return SnappedPoint(point, vertical_indicators=vertical_indicators)
        
        return SnappedPoint(point)
    
    def snap_rectangle(self, rectangle):
        snapped_vertically = []
        snapped_horizontally = []
        
        center = rectangle.center
        snapped_center = self.snap_point(center)
        if snapped_center.snapped_horizontally:
            snapped_horizontally.append((snapped_center, (snapped_center.point - center)))
        if snapped_center.snapped_vertically:
            snapped_vertically.append((snapped_center, (snapped_center.point - center)))
        
        for point in rectangle.left_center, rectangle.right_center:
            snapped_point = self.__snap_point_horizontally(point)
            if snapped_point.snapped_horizontally:
                snapped_horizontally.append((snapped_point, (snapped_point.point - point)))
        
        for point in rectangle.top_center, rectangle.bottom_center:
            snapped_point = self.__snap_point_vertically(point)
            if snapped_point.snapped_vertically:
                snapped_vertically.append((snapped_point, (snapped_point.point - point)))
        
        best_vertical_indicators = None
        best_vertical_delta = float('inf')
        best_horizontal_indicators = None
        best_horizontal_delta = float('inf')
        
        for snapping, vector in snapped_vertically:
            if abs(vector.y) < abs(best_vertical_delta):
                best_vertical_delta = vector.y
                best_vertical_indicators = snapping.vertical_indicators
        
        for snapping, vector in snapped_horizontally:
            if abs(vector.x) < abs(best_horizontal_delta):
                best_horizontal_delta = vector.x
                best_horizontal_indicators = snapping.horizontal_indicators
        
        if best_horizontal_indicators is not None and best_vertical_indicators is not None:
            return SnappedRectangle(
                rectangle + Vector(best_horizontal_delta, best_vertical_delta),
                best_horizontal_indicators,
                best_vertical_indicators
            )
        elif best_horizontal_indicators is not None:
            return SnappedRectangle(
                rectangle + Vector(best_horizontal_delta, 0),
                horizontal_indicators=best_horizontal_indicators
            )
        elif best_vertical_indicators is not None:
            return SnappedRectangle(
                rectangle + Vector(0, best_vertical_delta),
                vertical_indicators=best_vertical_indicators
            )
        else:
            return SnappedRectangle(rectangle)
