import json

def read_data(file_path):
    data = None
    with open(file_path, 'r') as file:
        data = json.load(file)
    data = {data['keys'][i]:data['values'][i] for i in range(len(data['keys']))}

    return data
