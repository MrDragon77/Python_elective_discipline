import struct

def write_data(file_path, data):
    with open(file_path, "wb") as file:
        binary_data = b''.join(struct.pack('f', f) for f in list(data.values()))
        file.write(binary_data)
