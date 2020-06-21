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
               
trigonometric_transformer = TrigonometricTransformer(L_choosed_functions=L_choosed_functions,
                                                     period=column_period,
                                                     process_as_time_dimension=process_as_time_dimension,
                                                     range_period=range_period)