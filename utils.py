import re
""""
UUID and Datetime string validators
"""
def is_uuid(uuid_str):
    uuid_pattern = re.compile('^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$')
    return (not uuid_pattern.match(uuid_str) is None)

def is_datetime(datetime_str):
    datetime_pattern = re.compile(
        r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$')
    return (not datetime_pattern.match(datetime_str) is None)

"""
transforms sqlalchemy query object to dictionary
"""
def row_to_dict(row):
    p_dict = row.__dict__
    p_dict.pop('_sa_instance_state')
    p_dict.pop('path')
    p_dict['type'] = p_dict['type'].value
    if 'isupdated' in p_dict.keys():
        p_dict.pop('isupdated')
    if 'rebased' in p_dict.keys():
        p_dict.pop('rebased')
    return p_dict