import wave
import struct
import numpy as np
import cv2

def save_wav(filepath, audio_arr):
    """
    Сохранение аудио в .wav
    """
    with wave.open(filepath, 'wb') as wav_file:
        wav_file.setnchannels(audio_arr[1])
        wav_file.setsampwidth(audio_arr[2])
        wav_file.setframerate(audio_arr[3])
        

        if audio_arr[2] == 1:
            audio_bytes = audio_arr[0].astype(np.uint8).tobytes()
        elif audio_arr[2] == 2:
            audio_bytes = audio_arr[0].astype(np.int16).tobytes()
        elif audio_arr[2] == 4:
            audio_bytes = audio_arr[0].astype(np.int32).tobytes()

        wav_file.writeframes(audio_bytes)