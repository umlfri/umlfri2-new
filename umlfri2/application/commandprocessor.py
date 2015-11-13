MAX_STACK_SIZE = 100


class CommandProcessor:
    def __init__(self, dispatcher):
        self.__undo_stack = []
        self.__redo_stack = []
        self.__dispatcher = dispatcher
    
    def execute(self, command):
        command.execute()
        
        if not command.is_error:
            self.__redo_stack = []
            
            self.__undo_stack.append(command)
            del self.__undo_stack[:-MAX_STACK_SIZE]
            
            self.__dispatcher.dispatch_all(command.get_updates())
            self.__dispatcher.dispatch_all(command.get_actions())
    
    def undo(self, count=1):
        for i in range(count):
            command = self.__undo_stack.pop()
            command.undo()
            self.__redo_stack.append(command)
            for event in command.get_updates():
                opposite = event.get_opposite()
                if opposite is not None:
                    self.__dispatcher.dispatch(opposite)
            
    def redo(self, count=1):
        for i in range(count):
            command = self.__redo_stack.pop()
            command.redo()
            self.__undo_stack.append(command)
            self.__dispatcher.dispatch_all(command.get_updates())
    
    def clear_buffers(self):
        self.__undo_stack = []
        self.__redo_stack = []
    
    @property
    def undo_stack(self):
        yield from self.__undo_stack
    
    @property
    def redo_stack(self):
        yield from self.__redo_stack
    
    @property
    def can_undo(self):
        if self.__undo_stack:
            return True
        else:
            return False
    
    @property
    def can_redo(self):
        if self.__redo_stack:
            return True
        else:
            return False