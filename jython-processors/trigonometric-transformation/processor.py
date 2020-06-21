import math
#Parameters import :
periodical_column_name = params.get('periodical_column')
process_as_time_dimension = params.get('process_as_time_dimension')
column_period = params.get('column_period')
range_period = range(int(column_period+2))
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

trigonometric_features = trigonometric_transformer.trigonometric_features
#Production code :
def process(row):
    periodical_column_value = row[periodical_column_name]    
    try:
        periodical_column_value = int(periodical_column_value)
        arg_val = trigonometric_transformer.compute_argument(periodical_column_value)
        if process_as_time_dimension:
            cos_val = trigonometric_features['cos'][periodical_column_value]
            sin_val = trigonometric_features['sin'][periodical_column_value]
            tan_val = trigonometric_features['tan'][periodical_column_value]
        else:
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
