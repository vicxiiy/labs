# Задание 2. Имена, объекты и сравнение
a = 1000
b = a
c = int("1000")

print("Типы:", type(a), type(b), type(c))
print("Идентификаторы:", id(a), id(b), id(c))
print("a == b:", a == b)
print("a is b:", a is b)
print("a == c:", a == c)
print("a is c:", a is c)

# Изменение c на None и проверка
c = None
print("c is None:", c is None)

# Фрагмент со строками
first = "python"
second = "py" + "thon"

print(first == second)
print(first is second)
