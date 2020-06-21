import math

#Parameters import :
periodical_column_name = params.get('periodical_column')
is_time_dimension = params.get('process_as_time_dimension')
column_period = params.get('column_period')
compute_cos = params.get('compute_cos')
compute_sin = params.get('compute_sin')
compute_tan = params.get('compute_tan')
output_arg = params.get('output_arg')
L_choosed_functions = [compute_cos, compute_sin, compute_tan]
L_functions = ['cos', 'sin', 'tan']
L_trigonometric_cols = []

if output_arg:
    L_trigonometric_cols.append(periodical_column_name + "_arg")
    
for choosed_function, function in zip(L_choosed_functions, L_functions):
    if choosed_function :
        L_trigonometric_cols.append(periodical_column_name+"_"+function)

#Class definition :
class TrigonometricTransformer():
    """
    The TrigonometricTransformer's goal is to set up all the functions
    that will be called by the recipe's processor. 
    These functions are defined as lambdas functions contextualized by the end user's selection. 
    This way the condition in order to compute the asked functions is checked only once.
    
    - 'build_trigonometric_transformer' : is a method allowing to setup the lambdas functions 
        called by the TrigonometricTransformer() class.
    - 'compute_trigonometric_transform' : is a method allowing to map the dataset variable 
        to the functions set by the build_trigonometric_transformer() method.
    """
    def __init__(self, L_choosed_functions):
        self.L_choosed_functions = L_choosed_functions
        self.trigonometric_transformer = {}
        self.build_trigonometric_transformer(self.L_choosed_functions)
        pass
    
    def build_trigonometric_transformer(self, L_choosed_functions):
        cos_choosed = L_choosed_functions[0]
        sin_choosed = L_choosed_functions[1]
        tan_choosed = L_choosed_functions[2]
        self.trigonometric_transformer = {'cos': lambda x: math.cos(x) if cos_choosed else None,
                                          'sin': lambda x: math.sin(x) if sin_choosed else None,
                                          'tan': lambda x: math.tan(x) if tan_choosed else None}
        pass
    
    def compute_trigonometric_transform(self, argument):
        cos_val = self.trigonometric_transformer['cos'](argument)
        sin_val = self.trigonometric_transformer['sin'](argument)
        tan_val = self.trigonometric_transformer['tan'](argument)
        return cos_val, sin_val, tan_val
    
trigonometric_transformer = TrigonometricTransformer(L_choosed_functions=L_choosed_functions)

#Production code :
def process(row):
    periodical_column_value = row[periodical_column_name]    
    try:
        arg_val = math.pi/2.0-(math.pi*int(periodical_column_value))/(column_period/2.0)
        cos_val, sin_val, tan_val = trigonometric_transformer.compute_trigonometric_transform(arg_val)
        log_message = None
        
    except Exception as e:
        log_message = "ERROR : "+str(e)
        arg_val, cos_val, sin_val, tan_val  = None, None, None, None
    
    L_values = [arg_val, cos_val, sin_val, tan_val]
    
    for column, value in zip(L_trigonometric_cols, L_values):
        if value is not None:
            row[column] = value
        
    row['trigonometric_log'] = log_message
    
    row[periodical_column_name] = periodical_column_value
    return row
