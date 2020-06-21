import math
import json


class TrigonometricTransformer():
    
    def __init__(self, params):
        self.compute_cos = params.get('compute_cos')
        pass
    

trigonometric_transformer = TrigonometricTransformer(params=params)

def compute_trigonometric_features(L_computation, arg):
    compute_cos = L_computation[0]
    compute_sin = L_computation[1]
    compute_tan = L_computation[2]
    if compute_cos:
        cos_val = math.cos(arg_val)
    else
    

def process(row):
    #Parameters import :
    periodical_column_name = params.get('periodical_column')
    column_period = params.get('column_period')
    compute_cos = trigonometric_transformer.compute_cos
    compute_sin = params.get('compute_sin')
    compute_tan = params.get('compute_tan')
    output_arg = params.get('output_arg')
    
    #Production code :
    periodical_column_value = row[periodical_column_name]
    orig_value = periodical_column_value
    
    #L_computables = ['cos', 'sin', 'tan']
    L_computation = [compute_cos, compute_sin, compute_tan]
    
    if compute_cos:
        cos_name = periodical_column_name + "_cos"
    if compute_sin:
        sin_name = periodical_column_name + "_sin"
    if compute_tan:
        tan_name = periodical_column_name + "_tan"
    if output_arg:
        arg_name = periodical_column_name + "_arg
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
