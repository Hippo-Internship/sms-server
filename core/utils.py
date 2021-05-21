from uuid import uuid4
import os
from django.contrib.auth import get_user_model

User = get_user_model()

def check_if_user_can_procceed(request_user, school_id, branch_id):
    if request_user.groups.role_id is User.SUPER_ADMIN:
        return True
    if request_user.groups.role_id is User.ADMIN:
        if request_user.school.id is not school_id:
            return False
    else:
        if request_user.branch.id is not branch_id:
            return False
    return True

def check_if_branch_can_procceed(request_user, school_id):
    if request_user.groups.role_id is User.SUPER_ADMIN:
        return True
    if request_user.groups.role_id is User.ADMIN:
        if request_user.school.id is not school_id:
            return False
    else:
            return False
    return True

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

def build_filter_query(query_model, query_params):
    result = {}
    for key in query_params:
        if not key in query_model:
            continue
        query_field = query_model[key]
        query_value = query_params[key]
        if type(query_field).__name__ == "dict":
            if not query_params[key] in query_field:
                continue
            sub_query = query_field[query_params[key]]
            if type(sub_query).__name__ == "list":
                for item in sub_query:
                    query_value = item["value"]
                    query_field = item["name"]
                    result[query_field] = query_value
                continue
            query_value = sub_query["value"]
            query_field = sub_query["name"]
        result[query_field] = query_value
    return result

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        print(instance)
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(path, filename)
    return wrapper
