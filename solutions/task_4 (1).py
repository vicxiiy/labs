# Задание 4. Строки, Unicode и форматирование
student = "Анна Смирнова"
course = "Основы программирования на Python"
completed = 7
total = 10

print("1. Первый и последний символ имени")
print("Первый символ:", student[0])
print("Последний символ:", student[-1])
print()

print("2. Срезы имени и фамилии")
print("Имя:", student[0:4])
print("Фамилия:", student[5:])
print()

print("3. Верхний и нижний регистр")
print("Верхний регистр:", student.upper())
print("Нижний регистр:", student.lower())
print()

print("4. Инициалы")
initials = student[0] + "." + student[5] + "."
print("Инициалы:", initials)
print()

print("5. Название курса в обратном порядке")
print("Курс наоборот:", course[::-1])
print()

print("6. Форматирование тремя способами")
percent = completed / total * 100

result_percent = "%s — %s: %d/%d (%.1f%%)" % (student, course, completed, total, percent)
result_format = "{} — {}: {}/{} ({:.1f}%)".format(student, course, completed, total, percent)
result_fstring = f"{student} — {course}: {completed}/{total} ({percent:.1f}%)"

print("Через %:", result_percent)
print("Через .format:", result_format)
print("Через f-строку:", result_fstring)
print()

print("7. Unicode")
symbol = "Я"
print("Символ:", symbol)
print("Кодовая позиция (ord):", ord(symbol))
print("Востановленный функцией chr:", chr(ord(symbol)))
encoded = symbol.encode("utf-8")
print("UTF-8 байты:", encoded)
print("Длина байтов:", len(encoded))

# 8. Попытка изменить строку (неработающая строка)
# student[0] = "Б"
# TypeError: 'str' object does not support item assignment

