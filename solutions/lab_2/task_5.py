import sys
import tracemalloc

# Часть 1. Размер отдельных объектов
empty_list = []
ten_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
ten_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
ten_chars = "abcdefghij"
number = 12345
nothing = None

print("Пустой список:", sys.getsizeof(empty_list), "байт")
print("Список из 10 чисел:", sys.getsizeof(ten_list), "байт")
print("Кортеж из 10 чисел:", sys.getsizeof(ten_tuple), "байт")
print("Строка из 10 символов:", sys.getsizeof(ten_chars), "байт")
print("Целое число:", sys.getsizeof(number), "байт")
print("None:", sys.getsizeof(nothing), "байт")

print("Размер одного элемента списка:", sys.getsizeof(ten_list[4]), "байт")
print("Сумма размеров 10 чисел:", sum(sys.getsizeof(x) for x in ten_list), "байт")
print("Список + числа:", sys.getsizeof(ten_list) + sum(sys.getsizeof(x) for x in ten_list), "байт")
print()

# Часть 2. Рост списка
growing = []
last_size = sys.getsizeof(growing)
print(f"len={len(growing):3}  size={last_size}")
for value in range(100):
    growing.append(value)
    size = sys.getsizeof(growing)
    if size != last_size:
        print(f"len={len(growing):3}  size={size}")
        last_size = size
print("Итого: len =", len(growing), "size =", sys.getsizeof(growing))
print()

# Часть 3. Измерение через tracemalloc

# Через list(range(100_000)):
COUNT = 1000

tracemalloc.start()
numbers = list(range(100_000))
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("list(range(100_000)):")
print(f"  Текущий объём: {current / 1024:.2f} КБ")
print(f"  Пиковый объём: {peak / 1024:.2f} КБ")
print("  sys.getsizeof(list):", sys.getsizeof(numbers), "байт")
list_peak = peak
del numbers
print()

# Через range(100_000):
tracemalloc.start()
ranges = [range(100_000) for _ in range(COUNT)]
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

holder_size = sys.getsizeof(ranges)
one_range_current = (current - holder_size) / COUNT
one_range_peak = (peak - holder_size) / COUNT

print(f"range(100_000), {COUNT} объектов:")
print(f"  Текущий объём: {current / 1024:.2f} КБ")
print(f"  Пиковый объём: {peak / 1024:.2f} КБ")
print(f"  На один range: текущий {one_range_current:.1f} байт, пиковый {one_range_peak:.1f} байт")
print("  sys.getsizeof(range):", sys.getsizeof(ranges[0]), "байт")
del ranges
print()

print(f"Отношение пиков (список / один range): {list_peak / one_range_peak:.0f}")

# Дополнительные замеры для итогового анализа
from array import array

def peak_of(factory):
    tracemalloc.start()
    result = factory()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak

print(f"list(range(100_000)):           {peak_of(lambda: list(range(100_000))) / 1024:.2f} КБ")
print(f"array('i', range(100_000)):     {peak_of(lambda: array('i', range(100_000))) / 1024:.2f} КБ")
print(f"sum(range(100_000)):            {peak_of(lambda: sum(range(100_000))) / 1024:.2f} КБ")
print(f"sum(x for x in range(100_000)): {peak_of(lambda: sum(x for x in range(100_000))) / 1024:.2f} КБ")

grown_ten = []
for i in range(10):
    grown_ten.append(i)
print("Список из 10, выросший через append():", sys.getsizeof(grown_ten), "байт")
print("Список из 10, созданный сразу:        ", sys.getsizeof([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), "байт")
print("Кортеж из 10:                         ", sys.getsizeof((0, 1, 2, 3, 4, 5, 6, 7, 8, 9)), "байт")
