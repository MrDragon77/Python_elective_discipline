import sys
import struct
import csv
import json
import cv2
import numpy as np

"""
Стратегия (Strategy) - Encoders
"""

class HistEncoder:
    @staticmethod
    def encode(file_path, data):
        raise NotImplementedError()


class BinHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        values = [data.get(i, 0.0) for i in range(256)]
        with open(file_path, 'wb') as file:
            packed_data = struct.pack('f' * 256, *values)
            file.write(packed_data)



class CsvHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        items = sorted(data.items())
        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['bin', 'value'])
            for bin_idx, value in items:
                writer.writerow([bin_idx, value])


class TxtHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        items = sorted(data.items())
        with open(file_path, 'w') as file:
            for bin_idx, value in items:
                file.write(f"{bin_idx} {value}\n")


class JsonHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        items = sorted(data.items())
        json_data = {
            'keys': [item[0] for item in items],
            'values': [item[1] for item in items],
        }
        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=2)


class ImageHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        values = [data.get(i, 0.0) for i in range(256)]
        values = np.array(values, dtype=np.float32)
        if values.max() > 0:
            values = (values / values.max()) * 255

        hist_image = np.zeros((256, 256), dtype=np.uint8)
        for i, val in enumerate(values):
            height = int(val)
            hist_image[256 - height:256, i] = 255

        cv2.imwrite(file_path, hist_image)
