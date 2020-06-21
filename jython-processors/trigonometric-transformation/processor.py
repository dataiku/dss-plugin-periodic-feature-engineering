#Packages import 
import math

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
    - 'compute_argument' : is a methiod allowing to convert a numerical value from a 
        periodical feature  into a trigonometric argument. 
    - 'compute_trigonometric_features' : is a method allowing, if 'process_as_time_dimension==True', to 
        pre-process all the possible cos/sin/tan associations of the given preriodical feature. 
        This is a good way to avoid repetitive computations of these values from rows to rows. 
    """
    def __init__(self, L_choosed_functions, period, process_as_time_dimension, range_period):
        self.L_choosed_functions = L_choosed_functions
        self.period = period
        self.process_as_time_dimension = process_as_time_dimension
        self.range_period = range_period
        self.trigonometric_transformer = {}
        self.build_trigonometric_transformer(self.L_choosed_functions)
        self.trigonometric_features = {'cos':{}, 'sin':{}, 'tan':{}}
        if self.process_as_time_dimension:
            self.compute_trigonometric_features()
            
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
    
    def compute_argument(self, value):
        return math.pi/2.0-(math.pi*value)/(self.period/2.0)
    
    def compute_trigonometric_features(self):
        for value in self.range_period:
            value_argument = self.compute_argument(value)
            self.trigonometric_features['cos'][value] = self.trigonometric_transformer['cos'](value_argument)
            self.trigonometric_features['sin'][value] = self.trigonometric_transformer['sin'](value_argument)
            self.trigonometric_features['tan'][value] = self.trigonometric_transformer['tan'](value_argument)
            
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

               
trigonometric_transformer = TrigonometricTransformer(L_choosed_functions=L_choosed_functions,
                                                     period=column_period,
                                                     process_as_time_dimension=process_as_time_dimension,
                                                     range_period=range_period)

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
