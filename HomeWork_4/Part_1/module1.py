"""
Часть 1: базовая работа с модулями и пакетами
"""

import time
import json


def matrix_matrix_multiply(matrix_a, matrix_b):
    """
    Умножение матрицы на матрицу.
    
    matrix_a: Матрица M x N
    matrix_b: Матрица N x K
    
    result - Матрица M x K
    """
    m = len(matrix_a)
    n = len(matrix_a[0]) if m > 0 else 0
    k = len(matrix_b[0]) if len(matrix_b) > 0 else 0
    
    result = [[0] * k for _ in range(m)]
    
    for i in range(m):
        for j in range(k):
            for p in range(n):
                result[i][j] += matrix_a[i][p] * matrix_b[p][j]
    
    return result


def matrix_vector_multiply(matrix, vector):
    """
    Умножение матрицы на вектор.
    
    matrix: Матрица M x N
    vector: Вектор N
    
    result - Вектор M
    """
    m = len(matrix)
    n = len(matrix[0]) if m > 0 else 0
    
    if n != len(vector):
        print("Ошибка! кол-во столбцов матрицы должно быть равно длине вектора!")
        return None
    
    result = [0] * m
    
    for i in range(m):
        for j in range(n):
            result[i] += matrix[i][j] * vector[j]
    
    return result


def matrix_trace(matrix):
    """
    Расчет следа матрицы
    matrix: Квадратная матрица N x N
    
    trace - сумма диагональных элементов
    """
    m = len(matrix)
    n = len(matrix[0]) if m > 0 else 0
    
    if m != n:
        print("Ошибка! матрица должна быть квадратной!")
        return None
    
    trace = 0
    for i in range(m):
        trace += matrix[i][i]
    
    return trace


def vector_vector_scalar_multiply(vector_a, vector_b):
    """
    Скалярное произведение двух векторов.
    vector_a: Вектор N
    vector_b: Вектор N
    
    result - Скалярное произведение
    """
    if len(vector_a) != len(vector_b):
        print("Ошибка! векторы должны быть одинаковой размерности!")
        return None
    
    result = 0
    for i in range(len(vector_a)):
        result += vector_a[i] * vector_b[i]
    
    return result


def gistogram(vector, num_bins):
    """
    Расчет гистограммы для вектора с изменяемым количеством квантов.
    vector: Вектор N
    num_bins: Кол-во бинов
    
    histogram_result - Список с кол-вом элементов в каждом бине
    """
    if num_bins <= 0:
        print("Ошибка! кол-во бинов должно быть положительным")
        return None
    
    min_val = min(vector)
    max_val = max(vector)
    if min_val == max_val:
        return [len(vector)] + [0] * (num_bins - 1)
    
    bin_width = (max_val - min_val) / num_bins
    histogram_result = [0] * num_bins
    
    for value in vector:
        bin_index = int((value - min_val) / bin_width)
        if bin_index >= num_bins:
            bin_index = num_bins - 1
        histogram_result[bin_index] += 1
    
    return histogram_result


def vector_filter(vector, filter):
    """
    Фильтрация вектора ядерным фильтром.
    vector: Вектор N
    filter: Вектор K
    
    result - Отфильтрованный веткор
    """
    n = len(vector)
    k = len(filter)
    
    result = []
    
    for i in range(n - k + 1):
        acc = 0
        for j in range(k):
            acc += vector[i + j] * filter[j]
        result.append(acc)
    
    return result


def write_to_file(filename, data):
    """
    Запись в файл JSON.
    filename: Строка имени файла
    data: Данные
    
    Возврат - True если успешно, False иначе
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Данные записаны в файл: {filename}")
        return True
    except Exception as e:
        print(f"Ошибка! {e}")
        return False


def read_from_file(filename):
    """
    Чтение из файла JSON.
    filename: Строка имени файла
    
    Возврат - Данные или None
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        print(f"Данные прочитаны из файла: {filename}")
        return data
    except Exception as e:
        print(f"Ошибка! {e}")
        return None


def measure_time(func, *argv):
    """
    Измерение времени работы функции.
    func: Функция
    *argv - агрументы функции
        
    Возврат - (результат, время выполнения)
    """
    start_time = time.time()
    result = func(*argv)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return result, elapsed_time

