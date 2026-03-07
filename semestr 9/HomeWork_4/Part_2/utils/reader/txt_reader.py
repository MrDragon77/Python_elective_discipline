
def read_data(file_path):
    data = None
    with open(file_path, "r") as file:
        source = file.read().split()
        data = { int(i): float(source[2*i+1]) for i in range(len(source) // 2)}
    return data