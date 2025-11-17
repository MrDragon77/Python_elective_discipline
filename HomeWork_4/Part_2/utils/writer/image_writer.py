import numpy as np
import cv2

def write_data(file_path, data):
    cv2.imwrite(file_path, data)