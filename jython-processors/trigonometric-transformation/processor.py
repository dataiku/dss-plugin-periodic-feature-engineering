# Packages import
import math


class PeriodicalFeaturesTransformer:
    """
    Set up all the functions that will be called by the recipe's processor.
    These functions are defined as lambdas functions contextualized by the end user's selection.
    This way the condition in order to compute the asked functions is checked only once.
    """

    def __init__(self, choosed_functions, period, process_as_time_dimension):
        """
        Initialization method for the PeriodicalFeaturesTransformer class

        Args:

            - choosed_functions (list, mandatory) : a list containing boolean values.
                It allows to choose the trigonometric functions to apply on the data.
                It is a sorted mapping between the :
                    the boolean conditions [bool_1, bool_2, bool_3]
                    and the will to use the  trigonometric functions [cos, sin, tan].

            - period (float, mandatory) : The period of the periodical feature to transform.

            - process_as_time_dimension (boolean, mandatory) :
                Allows to pre-compute all the possible cos/sin/tan associations
                of the given preriodical feature.
        """
        self.choosed_functions = choosed_functions
        self.period = period
        self.process_as_time_dimension = process_as_time_dimension
        self.range_period = range(int(self.period + 2))
        self.trigonometric_transformer = {}
        self.build_trigonometric_transformer(self.choosed_functions)
        self.trigonometric_features = {"cos": {}, "sin": {}, "tan": {}}
        if self.process_as_time_dimension:
            self.compute_trigonometric_features()

        pass

    def build_trigonometric_transformer(self, choosed_functions):
        """
        Method of PeriodicalFeaturesTransformer class.
        Setup the lambdas functions called by the class.
        """
        cos_choosed = choosed_functions[0]
        sin_choosed = choosed_functions[1]
        tan_choosed = choosed_functions[2]
        self.trigonometric_transformer = {
            "cos": lambda x: math.cos(x) if cos_choosed else None,
            "sin": lambda x: math.sin(x) if sin_choosed else None,
            "tan": lambda x: math.tan(x) if tan_choosed else None,
        }
        pass

    def compute_trigonometric_transform(self, argument):
        """
        Method of PeriodicalFeaturesTransformer class.
        Maps a variable argument to the trigonometric functions set by the build_trigonometric_transformer() method.

        Args:
            - argument (float, mandatory) : A trigonometric argument.
        """
        cos_val = self.trigonometric_transformer["cos"](argument)
        sin_val = self.trigonometric_transformer["sin"](argument)
        tan_val = self.trigonometric_transformer["tan"](argument)
        return cos_val, sin_val, tan_val

    def compute_argument(self, value):
        """
        Method of PeriodicalFeaturesTransformer class.
        Converts a numerical value from a periodical feature into a trigonometric argument.

        IMPORTANT : The trigonometric argument is made so that, when projected over a trigonometric circle,
        we can follow the periodical variable as if we read a clock.

        Args:
            - value (float, mandatory) : The periodical feature's value.
        """
        return math.pi / 2.0 - (math.pi * value) / (self.period / 2.0)

    def compute_trigonometric_features(self):
        """
        Method of PeriodicalFeaturesTransformer class.
        Allows, if 'process_as_time_dimension==True', to pre-compute all the possible cos/sin/tan associations
        of the given preriodical feature.
        This is a good way to avoid repetitive computations of these values from rows to rows;
        Instead we do some lookups from the periodical feature values to the pre-computed values
        of its cos/sin/tan.
        """
        for value in self.range_period:
            value_argument = self.compute_argument(value)
            self.trigonometric_features["cos"][value] = self.trigonometric_transformer["cos"](value_argument)
            self.trigonometric_features["sin"][value] = self.trigonometric_transformer["sin"](value_argument)
            self.trigonometric_features["tan"][value] = self.trigonometric_transformer["tan"](value_argument)
            pass


def compute_trigonometric_labels(col_name, output_arg, choosed_functions, available_functions):
    """
        Function allowing to compute the labels of a column created by the recipe

        Args:

            - col_name (string, mandatory) : The name of the original column.

            - output_arg (bool, mandatory) : Boolean condition.
                Specifies if we want to output the trigonometric argument
                associated to the column.

            - choosed_functions (list, mandatory) : A list containing boolean values.
                It allows to choose the trigonometric functions to apply on the data.
                It is a sorted mapping between the :
                    the boolean conditions [bool_1, bool_2, bool_3]
                    and the will to use the  trigonometric functions [cos, sin, tan].

            - available_functions (list, mandatory) : A list containing the available
                Trigonometric functions.
    """
    trigonometric_labels = []
    if output_arg:
        trigonometric_labels.append(col_name + "_arg")

    for choosed_function, function in zip(choosed_functions, available_functions):
        if choosed_function:
            trigonometric_labels.append(col_name + "_" + function)
    return trigonometric_labels


def apply_trigonometric_transform(x, choosed_functions, output_arg):
    """
        Function allowing to compute the labels of a column created by the recipe

        Args:

            - x (string, float) : The feature's value on which we want to compute
                trigonometric transformations.

            - choosed_functions (list, mandatory) : A list containing boolean values.
                It allows to choose the trigonometric functions to apply on the data.
                It is a sorted mapping between the :
                    the boolean conditions [bool_1, bool_2, bool_3]
                    and the will to use the  trigonometric functions [cos, sin, tan].

            - output_arg (bool, mandatory) : Boolean condition.
                Specifies if we want to output the trigonometric argument
                associated to the column.
    """
    periodic_features = []
    try:
        x = int(x)
        arg_val = trigonometric_transformer.compute_argument(x)
        if process_as_time_dimension:
            cos_val = trigonometric_features["cos"][x]
            sin_val = trigonometric_features["sin"][x]
            tan_val = trigonometric_features["tan"][x]
        else:
            cos_val, sin_val, tan_val = trigonometric_transformer.compute_trigonometric_transform(arg_val)
        log_message = None

    except Exception as e:
        log_message = "ERROR : " + str(e)
        arg_val, cos_val, sin_val, tan_val = None, None, None, None
    trig_results = [cos_val, sin_val, tan_val]

    if output_arg:
        periodic_features.append(arg_val)
    for choice, trig_result in zip(choosed_functions, trig_results):
        if choice:
            periodic_features.append(trig_result)

    return periodic_features, log_message


# Parameters import :
periodical_cols = params.get("periodical_columns")
process_as_time_dimension = params.get("process_as_time_dimension")
column_period = params.get("column_period")
compute_cos = params.get("compute_cos")
compute_sin = params.get("compute_sin")
compute_tan = params.get("compute_tan")
output_arg = params.get("output_arg")

# A variable allowing the boolean mapping to the functions to use :
choosed_functions = [compute_cos, compute_sin, compute_tan]
# Constant:
AVAILABLE_FUNCTIONS = ["cos", "sin", "tan"]

# Variable allowing to label the created columns :
trigonometric_mapping = {}
for col_name in periodical_cols:
    trigonometric_mapping[col_name] = compute_trigonometric_labels(
        col_name, output_arg, choosed_functions, AVAILABLE_FUNCTIONS
    )

# Trigonometric transformer class instantiation :
trigonometric_transformer = PeriodicalFeaturesTransformer(
    choosed_functions=choosed_functions, period=column_period, process_as_time_dimension=process_as_time_dimension
)

trigonometric_features = trigonometric_transformer.trigonometric_features


# Production code :
def process(row):
    for col_name in periodical_cols:
        trigonometric_labels = trigonometric_mapping[col_name]
        raw_value = row[col_name]
        periodic_features, log_message = apply_trigonometric_transform(raw_value, choosed_functions, output_arg)
        row["trigonometric_log_%s" % col_name] = log_message
        for label, feature in zip(trigonometric_labels, periodic_features):
            row[label] = feature
    return row
