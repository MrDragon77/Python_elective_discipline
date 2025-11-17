import sys
import struct

def read_data(file_path):
    data = []
    with open(file_path, 'rb') as file:
        data = struct.unpack('f'*256, file.read(sys.getsizeof(0.0)*256))

    data ={i: data[i] for i in range(len(data))}

    return data