"""
Helper used to change format of the data to retrieve to the front-end (JavaScript/AngularJS)
"""

def count_to_d3_json(list, key, value):
    data = []
    for item in list:
        if not item[key]:
            continue
        data.append({
            'label': item[key],
            'value': item[value]
        })
    return data

def list_to_json_array(list, key):
    data = []
    for item in list:
        data.append(item[key])
    return data
