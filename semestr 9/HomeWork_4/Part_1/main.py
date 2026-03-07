"""
Часть 1. Главная программа 
"""

import random
from module1 import *


def gen_random_matrix(rows, cols, min_val=0, max_val=100):
    """Генерирует случайную матрицу."""
    return [[random.randint(min_val, max_val) for _ in range(cols)] for _ in range(rows)]


def gen_random_vector(n, min_val=0, max_val=100):
    """Генерирует случайный вектор."""
    return [random.randint(min_val, max_val) for _ in range(n)]

def print_matrix(matrix):
    for row in matrix:
        for num in row:
            print(num, end = " ")
        print("")

def print_vector(vector):
    for num in vector:
        print(num, end = " ")
    print("")

def main():
    print("Примеры")
    
    
    print("\nПример 1: Умножение матрица-матрица")
    matrix_a = gen_random_matrix(3, 3, 1, 10)
    print("Матрица №1:")
    print_matrix(matrix_a)
    
    matrix_b = gen_random_matrix(3, 3, 1, 10)
    print("Матрица №2:")
    print_matrix(matrix_b)
        
    result, elapsed = measure_time(matrix_matrix_multiply, matrix_a, matrix_b)
    print("Произведение:")
    print_matrix(result)
    print(f"Время: {elapsed*1000} мс")
    

    print("\nПример 2: Умножение матрица-вектор")
    matrix = gen_random_matrix(3, 3, 1, 10)
    print("Матрица:")
    print_matrix(matrix)
    vector = gen_random_vector(3, 1, 10)
    print("Вектор:")
    print_vector(vector)
    
    result, elapsed = measure_time(matrix_vector_multiply, matrix, vector)
    print("Произведение:")
    print_vector(result)
    print(f"Время: {elapsed*1000} мс")
        
    print("\nПример 3: Расчет следа матрицы")
    matrix = gen_random_matrix(3, 3, 1, 10)
    print("Матрица:")
    print_matrix(matrix)
        
    result, elapsed = measure_time(matrix_trace, matrix)
    print(f"след: {result}")
    print(f"Время: {elapsed*1000} мс")
        

    print("\nПример 4: Скалярное произведение двух векторов")
    vector_a = gen_random_vector(3, 1, 10)
    print("Вектор №1:")
    print_vector(vector_a)
    
    vector_b = gen_random_vector(3, 1, 10)
    print("Вектор №2:")
    print_vector(vector_b)
    
    result, elapsed = measure_time(vector_vector_scalar_multiply, vector_a, vector_b)
    print("Произведение:")
    print(result)
    print(f"Время: {elapsed*1000} мс")
        
    
    print("\nПример 5: Расчет гистограммы")    
    vector = gen_random_vector(10, 0, 100)
    print("Вектор:")
    print_vector(vector)
            
    result, elapsed = measure_time(gistogram, vector, 2)
    print("Результат:")
    print_vector(result)
    print(f"Время: {elapsed*1000} мс")
            
    
    print("\nПример 6: Фильтрация вектора ядерным фильтром")
    filter = [-1, 0, 1]
    sizes_filter = [100, 1000, 10000]
    
    vector = gen_random_vector(10, 0, 100)
    print("Вектор:")
    print_vector(vector)
    print("Фильтр:")
    print_vector(filter)
        
    result, elapsed = measure_time(vector_filter, vector, filter)
    print("Результат:")
    print_vector(result)
    print(f"Время: {elapsed*1000} мс")
        
    
    print("\nПример 7: Сохранение в файл")
    matrix = gen_random_matrix(3, 3, 1, 10)
    print("Матрица:")
    print_matrix(matrix)
    write_to_file("test.json", matrix)
    
    # Чтение из файла для проверки
    print("\nПример 8: Чтение из файла")
    loaded_matrix = read_from_file("test.json")
    print("Загруженная матрица:")
    print_matrix(loaded_matrix)


if __name__ == "__main__":
    main()
