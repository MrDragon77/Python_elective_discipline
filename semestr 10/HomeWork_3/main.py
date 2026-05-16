import copy
from morse_converter_eng import MorseConverterEng
from str_converter import StrConverter
from morse_calc_converter import MorseCalcConverter
from morse_int import MorseInt
from expr_to_morse import ExprToMorse
from morse_evaluator import MorseEvaluator

mc = MorseConverterEng(None)
mc = MorseConverterEng('morse_codes.json')
print(mc['c'])
mc['a'] = 'taraababm'
print(mc['a'])
print(len(mc))
print(mc('a'))

for val in mc:
     print(val)


s = StrConverter('', copy.deepcopy(mc))
s.str='mipt is the university of russia'

print(s)


#тесты
print('\nMorseCalcConverter')
mcc = MorseCalcConverter('morse_codes.json')
print('0 =>', mcc['0'])
print('+ =>', mcc['+'])
print('len =', len(mcc))
for v in mcc:
    print(v)

print('\nMorseInt')
a = MorseInt(25)
b = MorseInt(7)
print(f'a = {repr(a)},  morse: {a}')
print(f'b = {repr(b)},  morse: {b}')
print(f'a + b = {int(a + b)},  morse: {a + b}')
print(f'a - b = {int(a - b)},  morse: {a - b}')
print(f'a * b = {int(a * b)},  morse: {a * b}')
print(f'a // b = {int(a // b)},  morse: {a // b}')
print(f'a > b:  {a > b}')
print(f'a < b:  {a < b}')
print(f'a == b: {a == b}')
print(f'a != b: {a != b}')

c = MorseInt(str(a))
print(f'From morse string: {repr(c)}, match: {int(c) == 25}')

neg = MorseInt(-3)
print(f'Negative: {repr(neg)},  morse: {neg}')

print('\nExprToMorse')
to_morse = ExprToMorse()
expr1 = '15 + 7 ='
expr2 = '100 * 3 ='
expr3 = '42 - 10'

print(f'"{expr1}"  ->  {to_morse(expr1)}')
print(f'"{expr2}"  ->  {to_morse(expr2)}')
print(f'"{expr3}"  ->  {to_morse(expr3)}')

print('\nMorseEvaluator')
ev = MorseEvaluator()
print(ev(to_morse(expr1)))
print()
print(ev(to_morse(expr2)))
print()
print(ev(to_morse(expr3)))
