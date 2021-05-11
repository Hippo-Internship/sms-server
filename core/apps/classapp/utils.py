def convert_string(data):
    return str(data)

def convert_int(data):
    return int(data)

def convert_data_type(_type, data):
    switch = {
        "str": convert_string,
        "int": convert_int
    }
    return switch[_type](data)

def normalize_data(format, data):
    _data = {}
    for key in format:
        try:
            if key not in data:
                raise ValueError()
            value = data[key][0]
            if type(value).__name__ != format[key]:
                value = convert_data_type(format[key], value)
            _data[key] = value
        except ValueError:
            continue
    return _data
        
def calculate_discount(value, discounts, flag=False):
    temp_value = 0
    for discount in discounts:
        if flag:
            discount.count += 1
            discount.save()
        if discount.percent is None:
            temp_value += discount.value
        else:
            temp_value += value * discount.percent / 100
    return temp_value if temp_value <= value else value

        