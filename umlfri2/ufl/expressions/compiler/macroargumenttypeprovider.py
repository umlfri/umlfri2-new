from ..tree import UflUnpackNode, UflLambdaExpressionNode
from ...types.structured import UflVariableWithMetadataType
from ...types.executable import UflLambdaType
from ...macro.argumenttypechecker import ArgumentTypeChecker


class MacroArgumentTypeProvider(ArgumentTypeChecker):
    def __init__(self, target_type, expressions, typing_visitor):
        self.__target_type = target_type
        
        self.__expressions = tuple(expressions)
        self.__typing_visitor = typing_visitor
        
        self.__typed_expressions = {}
    
    def check_arguments(self, self_type, expected_types):
        generic_cache = {}
        
        resolved_self_type = self_type.resolve_generic(self.__target_type, generic_cache)
        if resolved_self_type is None:
            return False
        
        expected_types = tuple(expected_types)
        
        if len(expected_types) != len(self.__expressions):
            return False
        
        typed_node_list = []
        for no, macro_parameter_type in enumerate(expected_types):
            typed_node = self.__resolve_argument(no, macro_parameter_type, generic_cache)
            if typed_node is None:
                return False
            typed_node_list.append(typed_node)
        
        self.__typed_expressions[expected_types] = typed_node_list
        
        return True
    
    def __resolve_argument(self, no, expected_type, generic_cache):
        expression = self.__expressions[no]
        
        if isinstance(expression, UflLambdaExpressionNode):
            if not isinstance(expected_type, UflLambdaType):
                return None
            
            if expected_type.parameter_count != expression.parameter_count:
                return None
            
            typed_arguments = {}
            resolved_param_types = []
            for name, type in zip(expression.parameters, expected_type.parameter_types):
                resolved_type = type.resolve_unknown_generic(generic_cache)
                if resolved_type is None:
                    return None
                typed_arguments[name] = resolved_type
                resolved_param_types.append(resolved_type)
            
            lambda_typing_visitor = self.__typing_visitor.create_for_lambda(typed_arguments)
            typed_body = expression.body.accept(lambda_typing_visitor)
            
            return_type = expected_type.return_type.resolve_generic(typed_body.type, generic_cache)
            if return_type is None:
                return None
            return UflLambdaExpressionNode(typed_body, expression.parameters, UflLambdaType(resolved_param_types, return_type))
        else:
            node = expression.accept(self.__typing_visitor)
            
            while isinstance(node.type, UflVariableWithMetadataType):
                node = UflUnpackNode(node, node.type.underlying_type)
                
            resolved_type = expected_type.resolve_generic(node.type, generic_cache)
            if resolved_type is None:
                return None
            return node
    
    def resolve_for(self, found_signature):
        yield from self.__typed_expressions[found_signature.parameter_types]
