import math
import json

def process(row):
    #Parameters import :
    periodical_column_name = params.get('periodical_column')
    column_period = params.get('column_period')
    compute_cos = params.get('compute_cos')
    compute_sin = params.get('compute_sin')
    compute_tan = params.get('compute_tan')
    output_arg = params.get('output_arg')
    
    #Production code :
    periodical_column_value = row[periodical_column_name]
    arg_val = math.pi/2.0-(math.pi*int(periodical_column_value))/(column_period/2.0)
    res = {}
    
    if compute_cos:
        cos_name = periodical_column_name + "_cos"
        res[cos_name] = math.cos(arg_val)   
    if compute_sin:
        sin_name = periodical_column_name + "_sin"
        res[sin_name] = math.sin(arg_val)
    if compute_tan:
        tan_name = periodical_column_name + "_tan"
        res[tan_name] = math.tan(arg_val)
    if output_arg:
        arg_name = periodical_column_name + "_arg"
        res[arg_name] = arg_val
    
    return json.dumps(res)
