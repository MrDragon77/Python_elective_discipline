import json
import os
from morse_converter_eng import MorseConverterEng

#MorseCalcConverter : наследник MorseConverterEng для цифр и операторов
class MorseCalcConverter(MorseConverterEng):
    def __init__(self, file_path):
        self._MorseConverterEng__cur_idx = 0
        if file_path is None or not os.path.exists(file_path):
            print('File path is not exists')
            return
        with open(file_path, 'r') as f:
            data = json.load(f)
        self._MorseConverterEng__conv_table = {
            **data.get('morse_digits', {}),
            **data.get('morse_ops', {})
        }

    def __next__(self):
        keys = list(self._MorseConverterEng__conv_table.keys())
        if self._MorseConverterEng__cur_idx >= len(keys):
            raise StopIteration
        val = self._MorseConverterEng__conv_table[keys[self._MorseConverterEng__cur_idx]]
        self._MorseConverterEng__cur_idx += 1
        return val
