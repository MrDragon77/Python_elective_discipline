import json
import copy
import os

class MorseConverterEng():
     def __init__(self, file_path):
          self.__cur_idx = 0

          try:
               if file_path is None or not os.path.exists(file_path): raise Exception('File path is not exists')
               with open(file_path, 'r') as file:
                    self.__conv_table = json.load(file)['morse_eng']
          except Exception as e:
              print(e)

     def __getitem__(self, key):
          return self.__conv_table[key]

     def __setitem__(self, key, val):
          pass

     def __len__(self):
         return len(self.__conv_table)

     def __call__(self, key):
         return self.__conv_table[key]

     def __iter__(self):
         self.__cur_idx = 0
         return self

     def __next__(self):
        if self.__cur_idx >= self.__len__():
            raise StopIteration
        else:
            self.__cur_idx += 1
            return self.__conv_table[chr(ord('a') + self.__cur_idx - 1)]

     def __missing__(self, key):
         return self.__cur_idx['a']

     def __deepcopy__(self, memo):
         new_table = copy.deepcopy(self.__conv_table, memo)

         new_mc = MorseConverterEng('')
         new_mc.__cur_idx = self.__cur_idx
         new_mc.__conv_table = new_table

         return new_mc
