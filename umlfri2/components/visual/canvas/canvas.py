import abc


class Canvas(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def draw_ellipse(self, rectangle, fg=None, bg=None, line_width=None, line_style=None):
        pass
    
    @abc.abstractmethod
    def draw_line(self, start, end, fg, line_width=None, line_style=None):
        pass
    
    @abc.abstractmethod
    def draw_path(self, path, fg=None, bg=None, line_width=None, line_style=None):
        pass
    
    @abc.abstractmethod
    def draw_rectangle(self, rectangle, fg=None, bg=None, line_width=None, line_style=None):
        pass
    
    @abc.abstractmethod
    def draw_text(self, pos, text, font, fg):
        pass
    
    @abc.abstractmethod
    def draw_icon(self, pos, filename):
        pass
    
    @abc.abstractmethod
    def clear(self, color=None):
        pass
    
    @abc.abstractmethod
    def get_ruler(self):
        pass
