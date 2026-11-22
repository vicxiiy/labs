submissions = [
    ("anna", "lab_01", 5),
    ("boris", "lab_01", 4),
    ("anna", "lab_02", 5),
    ("daria", "lab_01", 3),
    ("boris", "lab_02", 5),
    ("anna", "lab_01", 4),
]


# Построение структур данных
def build_structures(records):
    students = set()
    laboratories = set()
    attempts_by_student = {}
    best_results = {}
    attempts_count = {}
    students_by_lab = {}
    for student, lab, score in records:
        add_submission(students, laboratories, attempts_by_student,
                       best_results, attempts_count, students_by_lab,
                       (student, lab, score))
    return (students, laboratories, attempts_by_student,
            best_results, attempts_count, students_by_lab)


# Добавление новой записи без полного повторного построения
def add_submission(students, laboratories, attempts_by_student,
                   best_results, attempts_count, students_by_lab, record):
    student, lab, score = record
    key = (student, lab)

    students.add(student)
    laboratories.add(lab)

    if student not in attempts_by_student:
        attempts_by_student[student] = []
    attempts_by_student[student].append((lab, score))

    if key not in best_results or score > best_results[key]:
        best_results[key] = score

    attempts_count[key] = attempts_count.get(key, 0) + 1

    if lab not in students_by_lab:
        students_by_lab[lab] = set()
    students_by_lab[lab].add(student)


(students, laboratories, attempts_by_student,
 best_results, attempts_count, students_by_lab) = build_structures(submissions)


def show_structures() -> None:
    print("=== Построенные структуры ===")
    print("Студенты:", sorted(students))
    print("Лабораторные:", sorted(laboratories))
    print("Попытки по студентам:", attempts_by_student)
    print("Лучшие результаты:", best_results)
    print("Количество попыток:", attempts_count)


# Студенты, сдававшие обе работы
def show_both_labs() -> None:
    both = students_by_lab["lab_01"] & students_by_lab["lab_02"]
    print("\n=== Сдавали обе работы ===")
    print(sorted(both))
    print("Только lab_01:", sorted(students_by_lab["lab_01"] - students_by_lab["lab_02"]))
    print("Хотя бы одну работу:", sorted(students_by_lab["lab_01"] | students_by_lab["lab_02"]))


# Добавление новой записи
def show_update() -> None:
    print("\n=== Добавление новой записи ===")
    new_record = ("daria", "lab_02", 4)
    add_submission(students, laboratories, attempts_by_student,
                   best_results, attempts_count, students_by_lab, new_record)
    print("Добавлено:", new_record)
    print("Попытки daria:", attempts_by_student["daria"])
    print("Лучший результат (daria, lab_02):", best_results[("daria", "lab_02")])
    print("Попыток (daria, lab_02):", attempts_count[("daria", "lab_02")])
    print("Сдавали обе работы:", sorted(students_by_lab["lab_01"] & students_by_lab["lab_02"]))

    repeat = ("anna", "lab_01", 3)
    add_submission(students, laboratories, attempts_by_student,
                   best_results, attempts_count, students_by_lab, repeat)
    print("Добавлено:", repeat)
    print("Лучший результат (anna, lab_01):", best_results[("anna", "lab_01")])
    print("Попыток (anna, lab_01):", attempts_count[("anna", "lab_01")])


# Практическое расширение: текстовые запросы
def execute_query(line: str) -> str:
    parts = line.split()
    if len(parts) == 0:
        return "Пустая команда"

    command = parts[0]
    arguments = parts[1:]

    match command:
        case "student":
            if len(arguments) != 1:
                return "Формат: student <имя>"
            name = arguments[0]
            if name not in attempts_by_student:
                return f"Студент {name} не найден"
            return f"Попытки {name}: {attempts_by_student[name]}"
        case "best":
            if len(arguments) != 2:
                return "Формат: best <имя> <работа>"
            key = (arguments[0], arguments[1])
            if key not in best_results:
                return f"Нет данных для {arguments[0]}, {arguments[1]}"
            return f"Лучший результат {arguments[0]}, {arguments[1]}: {best_results[key]}"
        case "attempts":
            if len(arguments) != 2:
                return "Формат: attempts <имя> <работа>"
            key = (arguments[0], arguments[1])
            if key not in attempts_count:
                return f"Нет данных для {arguments[0]}, {arguments[1]}"
            return f"Попыток {arguments[0]}, {arguments[1]}: {attempts_count[key]}"
        case "completed":
            if len(arguments) != 1:
                return "Формат: completed <работа>"
            lab = arguments[0]
            if lab not in students_by_lab:
                return f"Работа {lab} не найдена"
            return f"Работу {lab} сдавали: {sorted(students_by_lab[lab])}"
        case _:
            return f"Неизвестная команда: {command}"


def run_queries() -> None:
    print("\n=== Текстовые запросы ===")
    queries = [
        "student anna",
        "best anna lab_01",
        "attempts boris lab_02",
        "completed lab_01",
        "student petr",
        "best anna lab_09",
        "completed lab_09",
        "delete anna",
        "best anna",
        "",
    ]
    for query in queries:
        print(f"> {query}")
        print(execute_query(query))


def run_interactive() -> None:
    print("\n=== Ввод запроса ===")
    line = input("Запрос: ")
    print(execute_query(line))


# Проверки
def run_tests() -> None:
    fresh = build_structures(submissions)
    assert fresh[0] == {"anna", "boris", "daria"}
    assert fresh[1] == {"lab_01", "lab_02"}
    assert fresh[2]["anna"] == [("lab_01", 5), ("lab_02", 5), ("lab_01", 4)]
    assert fresh[3][("anna", "lab_01")] == 5
    assert fresh[4][("anna", "lab_01")] == 2
    assert fresh[5]["lab_01"] & fresh[5]["lab_02"] == {"anna", "boris"}
    assert execute_query("best anna lab_01") == "Лучший результат anna, lab_01: 5"
    assert execute_query("student petr") == "Студент petr не найден"
    assert execute_query("hello") == "Неизвестная команда: hello"
    print("\nВсе проверки пройдены.")


def main() -> None:
    show_structures()
    show_both_labs()
    show_update()
    run_queries()
    run_tests()
    run_interactive()


if __name__ == "__main__":
    main()

