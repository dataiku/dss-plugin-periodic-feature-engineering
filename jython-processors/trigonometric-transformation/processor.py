#Packages import
import math

#Parameters import :
periodic_column = params.get('periodic_column')
min_value = float(params.get('min_value'))
max_value = float(params.get('max_value'))

# min_adjusted and max_adjusted allows to adjust all the values (translation of "- min_adjusted")
max_adjusted = max_value - min_value
min_adjusted = 0 # = (min_value - min_value)

#Production code :
def process(row):
    
    x = row[periodic_column]
    
    try:
        x_adjusted = float(x) - min_value
        x_scaled = (x_adjusted - min_adjusted)/(max_adjusted - min_adjusted )# = (x_adjusted / max_adjusted)
        feature_period = 1
        arg_val = math.pi/2.0-(math.pi*x_scaled)/(feature_period/2.0) 
        cos_val = math.cos(arg_val)
        sin_val = math.sin(arg_val)
        tan_val = math.tan(arg_val)
        log_message = None
        
    except TypeError as t:
        log_message = "TypeError : {0}".format(str(t.args))
        arg_val, cos_val, sin_val, tan_val  = None, None, None, None
    
    except ValueError as v:
        log_message = "ValueError : {0}".format(str(v.args))
        arg_val, cos_val, sin_val, tan_val  = None, None, None, None
    
    except Exception as e:
        if min_value == max_value : 
            log_message = "ERROR : Minimum and Maximum values must be different."
        else:
            log_message = "ERROR : "+str(e)
        arg_val, cos_val, sin_val, tan_val  = None, None, None, None
        
    row["{0}_arg".format(periodic_column)] = arg_val
    row["{0}_cos".format(periodic_column)] = cos_val
    row["{0}_sin".format(periodic_column)] = sin_val
    row["{0}_tan".format(periodic_column)] = tan_val
    row["{0}_transformation_log".format(periodic_column)] = log_message
    
    return row