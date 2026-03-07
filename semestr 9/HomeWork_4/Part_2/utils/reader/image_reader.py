import cv2

def read_data(file_path):
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    return image