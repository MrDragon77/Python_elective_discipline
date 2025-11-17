import json

def write_data(file_path, data):
    reform_data = {'keys':list(data.keys()),
                   'values':list(data.values())}

    with open(file_path, 'w') as file:
        json.dump(reform_data, file)