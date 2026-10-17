# Задание 1. Имена, ссылки и изменяемость
# Эксперимент A
a = 10
b = a
print(a, b)
print(id(a), id(b))
a += 1
print(a, b)
print(id(a), id(b))
print()

# Эксперимент B
first = [10, 20]
second = first
print(first, second)
print(id(first), id(second))
second.append(30)
print(first, second)
print(id(first), id(second))
print()

# 1. Переназначение second на новый список с теми же элементами
second = list(first)
print("После переназначения second = list(first):")
print("first :", first, id(first))
print("second:", second, id(second))
print()

# 2. Сравнение == и is
print("first == second:", first == second)
print("first is second:", first is second)
print()

# 3. Изменение нового списка
second.append(40)
print("После second.append(40):")
print("first :", first)
print("second:", second)
print()

# -------------------- Практическое задание -------------------------
import copy

# 1. Создаём первую конфигурацию
config_1 = {
    "name": "Учебный проект",
    "participants": ["Анна", "Борис", "Виктор"],
    "launch_params": [
        ["режим", "тестовый"],
        ["язык", "русский"]
    ]
}

# 2. Получаем вторую конфигурацию простым присваиванием
config_2 = config_1

print("=== ДО ИЗМЕНЕНИЙ (присваивание) ===")
print("config_1:", config_1)
print("config_2:", config_2)
print("Это один объект?", config_1 is config_2)
print()

# 3. Меняем что-то во второй конфигурации — и смотрим, как это повлияет на первую
config_2["participants"].append("Галина")
config_2["launch_params"][0][1] = "рабочий"

print("=== ПОСЛЕ ИЗМЕНЕНИЙ (через config_2) ===")
print("config_1:", config_1)
print("config_2:", config_2)
print("Это всё ещё один объект?", config_1 is config_2)
print()

# Вывод о нежелательном совместном изменении
print("Вывод: при простом присваивании объекты общие, изменения видны в обеих конфигурациях.")
print()

# 4. Создаём действительно независимую копию конфигурации
config_3 = copy.deepcopy(config_1)

print("=== ДО ИЗМЕНЕНИЙ (deepcopy) ===")
print("config_1:", config_1)
print("config_3:", config_3)
print("Это один объект?", config_1 is config_3)
print()

# Меняем в независимой копии
config_3["participants"].append("Дмитрий")
config_3["launch_params"][1][1] = "английский"

print("=== ПОСЛЕ ИЗМЕНЕНИЙ config_3 ===")
print("config_1:", config_1)
print("config_3:", config_3)
print()

# 5. Подтверждаем независимость с помощью assert
assert config_1 is not config_3
assert config_1["participants"] is not config_3["participants"]
assert config_1["launch_params"] is not config_3["launch_params"]
assert config_1["launch_params"][1] is not config_3["launch_params"][1]
assert config_1["participants"] == ["Анна", "Борис", "Виктор", "Галина"]
assert config_1["launch_params"][1][1] == "русский"
assert config_3["participants"][-1] == "Дмитрий"
assert config_3["launch_params"][1][1] == "английский"
print("assert прошёл: config_3 независима от config_1")
print()

print("=== ИТОГ ===")
print("Общие объекты: config_1 и config_2 (один словарь со всем содержимым).")
print("Независимые объекты: config_3 (deepcopy), включая вложенные списки.")
