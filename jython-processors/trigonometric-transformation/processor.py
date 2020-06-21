import math

#Parameters import :
periodical_column_name = params.get('periodical_column')
column_period = params.get('column_period')
compute_cos = params.get('compute_cos')
compute_sin = params.get('compute_sin')
compute_tan = params.get('compute_tan')
output_arg = params.get('output_arg')

L_funcs_available = ['cos', 'sin', 'tan']
L_funcs_choices = [compute_cos, compute_sin, compute_tan]

if compute_cos:
    cos_name = periodical_column_name + "_cos"
if compute_sin:
    sin_name = periodical_column_name + "_sin"
if compute_tan:
    tan_name = periodical_column_name + "_tan"
if output_arg:
    arg_name = periodical_column_name + "_arg"
        
class TrigonometricTransformer():
    
    def __init__(self, L_funcs_available, L_funcs_choices):
        #self.params = params
        self.L_funcs_available = L_funcs_available
        self.L_funcs_choices = L_funcs_choices
        self.trigonometric_transformer = {}
        self.build_trigonometric_transformer(self.L_funcs_available, self.L_funcs_choices)
        pass
    
    def build_trigonometric_transformer(self, L_funcs_available, L_funcs_choices):
        for func_available, choosed in zip(L_funcs_available, L_funcs_choices):
            self.trigonometric_transformer = {'cos': lambda x: math.cos(x) if choosed else None,
                                              'sin': lambda x: math.sin(x) if choosed else None,
                                              'tan': lambda x: math.tan(x) if choosed else None}
        pass
    def compute_trigonometric_transform(self, argument):
        cos_val = self.trigonometric_transformer['cos'](argument)
        sin_val = self.trigonometric_transformer['sin'](argument)
        tan_val = self.trigonometric_transformer['tan'](argument)
        return cos_val, sin_val, tan_val
    
trigonometric_transformer = TrigonometricTransformer(L_funcs_available=L_funcs_available, L_funcs_choices=L_funcs_choices)
#Production code :
def process(row):

    
    periodical_column_value = row[periodical_column_name]    

    try:
        arg_val = math.pi/2.0-(math.pi*int(periodical_column_value))/(column_period/2.0)
        cos_val = math.cos(arg_val)
        sin_val = math.sin(arg_val)
        tan_val = math.tan(arg_val)
        error_message = ""
        
    except Exception as e:
        error_message = str(e)
        arg_val = None
        cos_val = None
        sin_val = None
        tan_val = None
    
    row[arg_name] = arg_val
    row[cos_name] = cos_val
    row[sin_name] = sin_val
    row[tan_name] = tan_val
    
        
    row['error'] = error_message
    
    row[periodical_column_name] = periodical_column_value
    return row
