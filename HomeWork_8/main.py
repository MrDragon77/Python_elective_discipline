import numpy as np
import cv2


def linear_generator(image):
    height, width = image.shape
    for i in range(height):
        for j in range(width):
            yield (i, j)


def spiral_generator(image):
    height, width = image.shape
    center_y, center_x = height // 2, width // 2
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  #вправо, вниз, влево, вверх
    dir_i = 0
    y, x = center_y, center_x
    steps_in_direction = 1
    step_count = 0
    direction_changes = 0
    counter = 0
    
    while counter < height * width:
        if 0 <= y < height and 0 <= x < width:
            yield (y, x)
            counter += 1
        
        dy, dx = directions[dir_i]
        y += dy
        x += dx
        step_count += 1
        
        if step_count == steps_in_direction:
            step_count = 0
            dir_i = (dir_i + 1) % 4
            direction_changes += 1
            
            if direction_changes % 2 == 0:
                steps_in_direction += 1


def zigzag_generator(image):
    height, width = image.shape
    
    for diagonal in range(height + width - 1):
        if diagonal < width:
            x_start = 0
            y_start = diagonal
        else:
            x_start = diagonal - width + 1
            y_start = width - 1
        
        if diagonal % 2 == 0:
            #прямая диагональ
            x, y = x_start, y_start
            while y >= 0 and x < height:
                yield (x, y)
                x += 1
                y -= 1
        else:
            x, y = x_start, y_start
            while y >= 0 and x < height:
                x += 1
                y -= 1
            
            #обратная диагональ
            x -= 1
            y += 1
            while y < y_start + 1 and x >= x_start:
                yield (x, y)
                x -= 1
                y += 1
                

def peano_generator_rec(order, x=0, y=0, width=1):
    if order == 0:
        yield (x, y)
    else:
        s = width // 2
        yield from peano_generator_rec(order - 1, x, y, s) #верхний левый
        yield from peano_generator_rec(order - 1, x + s, y, s) #верхний правый
        yield from peano_generator_rec(order - 1, x + s, y + s, s) #нижний правый
        yield from peano_generator_rec(order - 1, x, y + s, s) #нижний левый

def peano_generator(image):
    height, width = image.shape
    #Находим ближайшую степень 2, которая больше размера image
    order = max(1, int(np.ceil(np.log2(max(height, width)))))
    size = 2 ** order
    
    peano_coords = list(peano_generator_rec(order, 0, 0, size))
    
    for x, y in peano_coords:
        if 0 <= x < height and 0 <= y < width:
            yield (x, y)


def average_filter_kernel(kernel_size):
    return np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)


def gaussian_filter_kernel(kernel_size, sigma=1.0):
    kernel = np.zeros((kernel_size, kernel_size))
    center = kernel_size // 2
    
    for i in range(kernel_size):
        for j in range(kernel_size):
            x = i - center
            y = j - center
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    
    return kernel / np.sum(kernel)


def mse(image1, image2):
    return np.mean((image1.astype(np.float32) - image2.astype(np.float32)) ** 2)


def apply_filter(image, kernel, generator):
    height, width = image.shape
    kernel_size = kernel.shape[0]
    offset = kernel_size // 2
    result_height = height - kernel_size + 1
    result_width = width - kernel_size + 1
    result = np.zeros((result_height, result_width), dtype=np.float32)
    
    valid_coords = list(filter(lambda coord: offset <= coord[0] < height - offset and offset <= coord[1] < width - offset, generator(image)))
    
    for i, j in valid_coords:
        patch = image[i - offset:i + offset + 1, j - offset:j + offset + 1]
        filtered_value = np.sum(patch * kernel)
        result[i - offset, j - offset] = filtered_value
    
    return result


if __name__ == "__main__":
    image = cv2.imread("image.jpg", cv2.IMREAD_COLOR)
    
    image_gray = (lambda image: cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))(image)
    
    avg_kernel = average_filter_kernel(3)
    gauss_kernel = gaussian_filter_kernel(5, sigma=1.0)
    
    # result_linear = apply_filter(image_gray, avg_kernel, linear_generator)
    # result_spiral = apply_filter(image_gray, avg_kernel, spiral_generator)
    # result_zigzag = apply_filter(image_gray, avg_kernel, zigzag_generator)
    # result_peano = apply_filter(image_gray, avg_kernel, peano_generator)
    
    result_linear = apply_filter(image_gray, gauss_kernel, linear_generator)
    result_spiral = apply_filter(image_gray, gauss_kernel, spiral_generator)
    result_zigzag = apply_filter(image_gray, gauss_kernel, zigzag_generator)
    result_peano = apply_filter(image_gray, gauss_kernel, peano_generator)
    
    print("Testing:")
    print(f"MSE (Linear vs Spiral): {mse(result_linear, result_spiral)}")
    print(f"MSE (Linear vs Zigzag): {mse(result_linear, result_zigzag)}")
    print(f"MSE (Linear vs Peano): {mse(result_linear, result_peano)}")
    print(f"MSE (Spiral vs Zigzag): {mse(result_spiral, result_zigzag)}")
    print(f"MSE (Spiral vs Peano): {mse(result_spiral, result_peano)}")
    print(f"MSE (Zigzag vs Peano): {mse(result_zigzag, result_peano)}")

