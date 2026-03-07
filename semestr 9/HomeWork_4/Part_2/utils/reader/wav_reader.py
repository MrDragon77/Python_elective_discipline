import wave
import struct
import numpy as np
import cv2

def read_wav(filepath):
    """
    Чтение WAV файла
    """
    with wave.open(filepath, 'rb') as wav_file:
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        n_frames = wav_file.getnframes()

        audio_bytes = wav_file.readframes(n_frames)
        
        if sample_width == 1:
            audio_data = np.frombuffer(audio_bytes, dtype=np.uint8)
        elif sample_width == 2:
            audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
        elif sample_width == 4:
            audio_data = np.frombuffer(audio_bytes, dtype=np.int32)
        else:
            print("Ошибка! Невозможно прочиать файл!")
            return 

        return [audio_data, n_channels, sample_width, sample_rate]