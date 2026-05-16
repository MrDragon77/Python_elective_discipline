class StrConverter():
     def __init__(self, t_str, converter):
          self.__str_val = t_str
          self.__converter = converter

     def __str__(self):
         words = self.__str_val.split()
         word_conv = lambda x: '   '.join([ self.__converter(i) for i in x])
         return '       '.join(map(word_conv,words))
      #getter
     @property
     def str(self):
         return self.__str_val

     @str.setter
     def str(self,val):
         self.__str_val = val
