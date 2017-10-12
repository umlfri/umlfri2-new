class Expression:
    def compile(self, type_context, expected_type):
        raise NotImplementedError
    
    def get_type(self):
        raise NotImplementedError
    
    def __call__(self, context):
        raise NotImplementedError
