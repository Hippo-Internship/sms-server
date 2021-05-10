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
        
    # assert type(data) != "dict"
    # for key in data:
    #     data[key] = data[key][0]
        