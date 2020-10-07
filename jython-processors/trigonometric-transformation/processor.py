#Packages import
import math

#Parameters import :
periodical_column = params.get('periodical_column')
period_min = params.get('period_min')
period_max = params.get('period_max')
feature_period = math.fabs(period_min) + math.fabs(period_max)

#Production code :
def process(row):
    x = row[periodical_column]
    x_orig = x
    try:
        x = int(x)
        if x < 0 :
            x = feature_period + x
        arg_val = math.pi/2.0-(math.pi*x)/(feature_period/2.0)
        cos_val = math.cos(arg_val)
        sin_val = math.sin(arg_val)
        tan_val = math.tan(arg_val)
        
        log_message = None

    except Exception as e:
        log_message = "ERROR : "+str(e)
        arg_val, cos_val, sin_val, tan_val  = None, None, None, None
    row["{0}_arg".format(periodical_column)] = arg_val
    row["{0}_cos".format(periodical_column)] = cos_val
    row["{0}_sin".format(periodical_column)] = sin_val
    row["{0}_tan".format(periodical_column)] = tan_val
    row["log_message"] = log_message

    return row