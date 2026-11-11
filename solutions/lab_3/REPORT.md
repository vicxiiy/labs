# Лабораторная работа № 3. Алгоритмы, коллекции и функции
## Цель работы

Научиться переводить условие задачи в алгоритм, выбирать подходящую структуру данных и разделять программу на небольшие функции с понятными контрактами.

## Задачи работы

После выполнения работы студент должен уметь:

- применять условия, циклы и сопоставление с образцом;
- реализовывать поиск, подсчет и накопление;
- работать со списками, кортежами, словарями и множествами;
- выбирать структуру данных с учетом назначения и сложности операций;
- создавать функции с позиционными и именованными параметрами;
- использовать аннотации типов и строки документации;
- объяснять области видимости имен по правилу LEGB;
- декомпозировать прикладную задачу на функции;
- оценивать сложность простых алгоритмов.

## Ход работы

## Задание 1. Условия и классификация данных
### Части 1-3. Проверка диапазонов, определение уровня результата и сопоставление с образцом

Назначаем уровни результата:
```
LEVELS = ("недостаточный", "удовлетворительный", "хороший", "отличный")

def get_level(score: int, absences: int) -> str:
    if score >= 90:
        index = 3
    elif score >= 75:
        index = 2
    elif score >= 60:
        index = 1
    else:
        index = 0
```
Учитываем, что, если пропущено более трех занятий, уровень снижается на одну ступень, но не может стать ниже уровня «недостаточный»:
```
    if absences > 3 and index > 0:
        index -= 1
    return LEVELS[index]
```
Сформулировали пояснения для типов работы, для неизвестного значения создали отдельную ветвь:
```
def describe_work(work_type: str) -> str:
    match work_type:
        case "exam":
            return "экзаменационная работа"
        case "project":
            return "проектная работа"
        case "practice":
            return "практическая работа"
        case _:
            return "неизвестный тип работы"
```
Проверка на то, что результат и количество пропусков входят в допустимые диапазоны: 
```
def process_record(score: int, work_type: str, absences: int) -> tuple[str, str | None]:
    if score < 0 or score > 100:
        return f"Ошибка: результат {score} вне диапазона 0–100", None
    elif absences < 0 or absences > 5:
        return f"Ошибка: пропусков {absences} вне диапазона 0–5", None
    else:
        level = get_level(score, absences)
        work = describe_work(work_type)
        text = f"{work}: результат {score}, пропусков {absences}, уровень — {level}"
        return text, level
```
Итоговая программа, выводящая результат:
```
def run_single() -> None:
    score = int(input("Результат (0–100): "))
    work_type = input("Тип работы (exam / project / practice): ").strip()
    absences = int(input("Пропусков (0–5): "))
    print(process_record(score, work_type, absences)[0])
```
### Часть 4. Тестовые сценарии
```
def run_tests() -> None:
    scenarios = [
        (0, "exam", 0, "недостаточный"),
        (59, "project", 1, "недостаточный"),
        (60, "practice", 0, "удовлетворительный"),
        (74, "exam", 3, "удовлетворительный"),
        (75, "project", 0, "хороший"),
        (89, "practice", 4, "удовлетворительный"),
        (90, "exam", 0, "отличный"),
        (100, "exam", 5, "хороший"),
        (60, "exam", 5, "недостаточный"),
        (50, "practice", 5, "недостаточный"),
        (101, "exam", 0, "Ошибка"),
        (80, "exam", 6, "Ошибка"),
        (70, "lab", 1, "неизвестный тип работы"),
    ]
    print("\n=== Тестовые сценарии ===")
    for number, (score, work_type, absences, expected) in enumerate(scenarios, 1):
        text, _ = process_record(score, work_type, absences)
        status = "OK" if expected in text else "FAIL"
        print(f"{number:2}. ({score}, {work_type}, {absences}) | ожидание: {expected} | {status}")
        print(f"    {text}")
```
### Практическое расширение
Обработали список из десяти записей вида (score, work_type, absences), сформировали готовую строку результата и подсчитали число студентов каждого уровня:
```
def run_group() -> None:
    records = [
        (95, "exam", 0),
        (82, "project", 2),
        (67, "practice", 1),
        (45, "exam", 4),
        (91, "project", 5),
        (75, "practice", 3),
        (59, "exam", 0),
        (100, "practice", 1),
        (60, "project", 4),
        (88, "exam", 4),
    ]
    summary = {level: 0 for level in LEVELS}
```
Выводим индивидуальные результаты:
```
    print("\n=== Индивидуальные результаты ===")
    for number, (score, work_type, absences) in enumerate(records, 1):
        text, level = process_record(score, work_type, absences)
        print(f"{number:2}. {text}")
        if level is not None:
            summary[level] += 1
```
А также сводку по уровням:
```
    print("\n=== Сводка по уровням ===")
    for level in LEVELS:
        print(f"{level}: {summary[level]}")
```
```
def main() -> None:
    run_single()
    run_tests()
    run_group()

if __name__ == "__main__":
    main()
```
