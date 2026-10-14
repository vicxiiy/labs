# Задание 5. Информационная карточка вычислительного эксперимента
"""
Информационная карточка вычислительного эксперимента.

Программа запрашивает у пользователя сведения об исследователе и об
эксперименте (имя исследователя, название эксперимента, число запусков,
длительность одного запуска, а также вещественную и мнимую части
комплексного коэффициента), выполняет ряд простых вычислений без
использования условных операторов и циклов, и выводит оформленную
карточку с результатами, а также диагностическую строку
с типами всех введённых значений.
"""

# Ввод данных
researcher_name = input("Введите имя исследователя: ")
experiment_name = input("Введите название эксперимента: ")
runs_count = int(input("Введите количество выполненных запусков: "))
run_duration = float(input("Введите длительность одного запуска в секундах: "))
coeff_real = float(input("Введите действительную часть коэффициента: "))
coeff_imag = float(input("Введите мнимую часть коэффициента: "))

# Вычисления
total_duration_seconds = runs_count * run_duration
total_duration_minutes = total_duration_seconds / 60
coefficient = complex(coeff_real, coeff_imag)
magnitude_squared = coeff_real ** 2 + coeff_imag ** 2
has_runs = bool(runs_count)

# Вывод карточки
separator = "=" * 40

print(separator)
print(f"ЭКСПЕРИМЕНТ: {experiment_name}")
print(f"Исследователь: {researcher_name}")
print(f"Запуски: {runs_count}")
print(f"Общее время: {total_duration_seconds:.2f} с ({total_duration_minutes:.2f} мин)")
print(f"Коэффициент: {coefficient}")
print(f"Квадрат модуля: {magnitude_squared:.2f}")
print(f"Есть выполненные запуски: {has_runs}")
print(separator)

# Диагностическая строка с типами введённых значений
print(
    "Типы введённых значений: "
    f"researcher_name={type(researcher_name).__name__}, "
    f"experiment_name={type(experiment_name).__name__}, "
    f"runs_count={type(runs_count).__name__}, "
    f"run_duration={type(run_duration).__name__}, "
    f"coeff_real={type(coeff_real).__name__}, "
    f"coeff_imag={type(coeff_imag).__name__}"
)


