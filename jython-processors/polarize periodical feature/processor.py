def process(row):
    import math
    periodical_column_name = params.get('periodical_column')
    periodical_column_value = row[periodical_column_name]
    column_period = params.get('column_period')
    arg = math.pi/2.0-(math.pi*int(periodical_column_value))/(column_period/2.0)
    
    return arg
