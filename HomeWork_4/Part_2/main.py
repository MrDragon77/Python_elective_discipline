# -*- coding: utf-8 -*-

import sys
import argparse
from pathlib import Path

from utils.reader import image_reader as imread
from utils.reader import wav_reader as audioread
from utils.writer import image_writer as imwrite
from utils.writer import wav_writer as audiowrite
from utils.processor import image_processor, audio_processor, image_hystogram_drawer, audio_hystogram_drawer


def init_parser():
    parser = argparse.ArgumentParser()
    
    #Выбор типа обработки
    parser.add_argument(
        'type',
        choices=['image', 'audio']
    )
    
    #Имя входного файла
    parser.add_argument(
        'filename'
    )
    
    #Гамма для изображений
    parser.add_argument(
        '-g', '--gamma',
        type=float,
        default=1.0
    )
    
    #Бины квантования для аудио
    parser.add_argument(
        '-q', '--quantize',
        type=int,
        default=256
    )
    
    return parser


def main():
    parser = init_parser()
    args = parser.parse_args()
    
    input_dir = Path('input_data')
    output_dir = Path('output_data')
    output_dir.mkdir(exist_ok=True)
    
    if args.type == 'image':
        input_path = input_dir / args.filename
        #Чтение файла
        image = imread.read_data(str(input_path))
            
        if image is None:
            print(f"Ошибка! Не удалось прочитать файл: {input_path}")
            return
        
        #Сохраняем копию в серых тонах
        imwrite.write_data(str(output_dir / "image_gray.jpg"), image)
        print(f"Размер изображения: {image.shape}")
    
        #Гистограмма оригинального изображения
        hist_original = image_processor.compute_histogram(image)
        hystogram_original_image = image_hystogram_drawer.draw_histogram_image(
            hist_original,
            width=1024, 
            height=1024,
            bg_color=(255, 255, 255), #белый
            hist_color=(0, 0, 255) #красный
        )
        imwrite.write_data(str(output_dir / "image_histogram_original.png"), hystogram_original_image)

        #Эквализация гистограммы
        equalized = image_processor.histogram_equalization(image)
        imwrite.write_data(str(output_dir / "image_equalized.jpg"), equalized)

        #Гистограмма эквализированного изображения
        hist_equalized = image_processor.compute_histogram(equalized)
        hystogram_qualized_image = image_hystogram_drawer.draw_histogram_image(
            hist_equalized,
            width=1024,
            height=1024,
            bg_color=(255, 255, 255), #белый
            hist_color=(0, 0, 255) #красный
        )
        imwrite.write_data(str(output_dir / "image_histogram_equalized.png"), hystogram_qualized_image)
        
        #Гамма коррекция
        gamma_image = image_processor.gamma_correction(image, gamma=args.gamma)
        output_filename = f"image_gamma_{args.gamma}.jpg"
        imwrite.write_data(str(output_dir / output_filename), gamma_image)
            
    elif args.type == 'audio':
        input_path = input_dir / args.filename
        #Чтение файла
        audio_arr = audioread.read_wav(str(input_path))
            
        if audio_arr is None:
            print(f"[ERROR] Не удалось прочитать файл: {input_path}")
            return

        #Создание гистограммы оригинального аудио
        histogram = audio_processor.compute_audio_histogram(audio_arr[0], bins=256)
        audio_hystogram_original = audio_hystogram_drawer.draw_audio_histogram(histogram)
        imwrite.write_data(str(output_dir / "audio_histogram_original.png"), audio_hystogram_original)
    
        #Квантование
        audio_quantized = audio_processor.quantize_audio(audio_arr[0], bins=args.quantize)
        hist_after = audio_processor.compute_audio_histogram(audio_quantized)
        audio_arr = audio_arr.copy()
        audio_arr[0] = audio_quantized
        audiowrite.save_wav(str(output_dir / "audio_quantized.wav"), audio_arr)
        audio_hystogram_quantized = audio_hystogram_drawer.draw_audio_histogram(hist_after)
        imwrite.write_data(str(output_dir / "audio_histogram_quantized.png"), audio_hystogram_quantized)
        
    
if __name__ == '__main__':
    main()
