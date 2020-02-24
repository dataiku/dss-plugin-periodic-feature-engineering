def process(row):
    import math
    import json
    periodical_column_name = params.get('periodical_column')
    periodical_column_value = row[periodical_column_name]
    column_period = params.get('column_period')
    arg_val = math.pi/2.0-(math.pi*int(periodical_column_value))/(column_period/2.0)
    
    arg_name = periodical_column_name + "_arg"
    
    cos_name = periodical_column_name + "_cos"
    sin_name = periodical_column_name + "_sin"
    tan_name = periodical_column_name + "_tan"
    cos_val = math.cos(arg_val)
    sin_val = math.sin(arg_val)
    tan_val = math.tan(arg_val)
    
    res = {arg_name:arg_val, cos_name:cos_val, sin_name:sin_val, tan_name:tan_val}
    
    return json.dumps(res)
