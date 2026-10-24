# Задание 2. Поверхностное и глубокое копирование
import copy

original = [
    ["Python", 5],
    ["Algorithms", 4],
]

alias = original
shallow = original.copy()
deep = copy.deepcopy(original)

def print_state():
    structures = [("original", original), ("alias", alias),
                  ("shallow", shallow), ("deep", deep)]

    print("Содержимое:")
    for name, s in structures:
        print(f"  {name:9}{s}")

    print("id внешних списков:")
    for name, s in structures:
        print(f"  {name:9}{id(s)}")

    print("id первого вложенного списка (s[0]):")
    for name, s in structures:
        print(f"  {name:9}{id(s[0])}")

    print("id объекта с первой оценкой (s[0][1]):")
    for name, s in structures:
        print(f"  {name:9}{id(s[0][1])}   значение: {s[0][1]}")

print("---------- ИСХОДНЫЕ ДАННЫЕ ----------")
print_state()

print("\n---------- ПОСЛЕ original.append([\"Databases\", 5]) ----------")
original.append(["Databases", 5])
print_state()

print("\n---------- ПОСЛЕ original[0][1] = 3 ----------")
original[0][1] = 3
print_state()
print()

for name, s in [("alias", alias), ("shallow", shallow), ("deep", deep)]:
    new_outer = s is not original
    new_nested = s[0] is not original[0] and s[1] is not original[1]
    print(f"{name:8} новый внешний: {new_outer}; новые вложенные: {new_nested}")

# Матрица
print("\n---------- Матрица ----------")

wrong_matrix = [[0] * 3] * 3
print("До изменения:", wrong_matrix)
print("id строк:", id(wrong_matrix[0]), id(wrong_matrix[1]), id(wrong_matrix[2]))
print("Строки — один объект?", wrong_matrix[0] is wrong_matrix[1] is wrong_matrix[2])

wrong_matrix[0][0] = 1
print("После wrong_matrix[0][0] = 1:", wrong_matrix)

correct_matrix = [[0] * 3 for _ in range(3)]
print("\nДо изменения:", correct_matrix)
print("id строк:", id(correct_matrix[0]), id(correct_matrix[1]), id(correct_matrix[2]))
print("Строки — один объект?", correct_matrix[0] is correct_matrix[1] is correct_matrix[2])

correct_matrix[0][0] = 1
print("После correct_matrix[0][0] = 1:", correct_matrix)
