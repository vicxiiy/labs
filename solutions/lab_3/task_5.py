students = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61],
}

CATEGORIES = ("отличный", "хороший", "удовлетворительный", "недостаточный")
NO_RESULTS = "нет результатов"


# Базовые функции
def mean(values):
    if len(values) == 0:
        return None
    total = 0
    for value in values:
        total += value
    return total / len(values)


def minimum(values):
    if len(values) == 0:
        return None
    result = values[0]
    for value in values:
        if value < result:
            result = value
    return result


def maximum(values):
    if len(values) == 0:
        return None
    result = values[0]
    for value in values:
        if value > result:
            result = value
    return result


def classify(score):
    if score >= 90:
        return "отличный"
    elif score >= 75:
        return "хороший"
    elif score >= 60:
        return "удовлетворительный"
    else:
        return "недостаточный"


# Итоги студента и группы
def student_summary(name, results):
    if len(results) == 0:
        return {"name": name, "count": 0, "mean": None, "min": None,
                "max": None, "category": NO_RESULTS}
    average = mean(results)
    return {
        "name": name,
        "count": len(results),
        "mean": average,
        "min": minimum(results),
        "max": maximum(results),
        "category": classify(average),
    }


def find_top_students(students):
    best = None
    leaders = []
    for name, results in students.items():
        average = mean(results)
        if average is None:
            continue
        if best is None or average > best:
            best = average
            leaders = [name]
        elif average == best:
            leaders.append(name)
    return leaders


def group_summary(students):
    categories = {category: 0 for category in CATEGORIES}
    categories[NO_RESULTS] = 0
    total = 0
    count = 0
    for name, results in students.items():
        summary = student_summary(name, results)
        categories[summary["category"]] += 1
        for value in results:
            total += value
            count += 1
    if count == 0:
        group_mean = None
    else:
        group_mean = total / count
    return {
        "students": len(students),
        "results": count,
        "mean": group_mean,
        "categories": categories,
        "leaders": find_top_students(students),
    }


# Отчёт
def format_number(value):
    if value is None:
        return "—"
    return f"{value:.2f}"


def format_plain(value):
    if value is None:
        return "—"
    return str(value)


def format_report(student_data, group_data):
    lines = ["=== Результаты студентов ==="]
    for item in student_data:
        lines.append(
            f"{item['name']}: работ {item['count']}, среднее {format_number(item['mean'])}, "
            f"мин {format_plain(item['min'])}, макс {format_plain(item['max'])}, "
            f"категория — {item['category']}"
        )

    lines.append("")
    lines.append("=== Рейтинг ===")
    ranked = [item for item in student_data if item["mean"] is not None]
    ranked = sorted(ranked, key=lambda item: item["mean"], reverse=True)
    if len(ranked) == 0:
        lines.append("Рейтинг пуст")
    for place, item in enumerate(ranked, 1):
        lines.append(f"{place}. {item['name']} — {format_number(item['mean'])}")

    lines.append("")
    lines.append("=== Группа ===")
    lines.append(f"Студентов: {group_data['students']}, результатов: {group_data['results']}")
    lines.append(f"Общий средний результат: {format_number(group_data['mean'])}")
    if len(group_data["leaders"]) == 0:
        lines.append("Лидеры: нет")
    else:
        lines.append("Лидеры: " + ", ".join(group_data["leaders"]))
    for category, number in group_data["categories"].items():
        lines.append(f"{category}: {number}")
    return "\n".join(lines)


def analyze_group(students):
    student_data = [student_summary(name, results) for name, results in students.items()]
    group_data = group_summary(students)
    return format_report(student_data, group_data)


# Проверка
def run_tests() -> None:
    print("\n=== Тестовые сценарии ===")

    original = {name: results.copy() for name, results in students.items()}
    report = analyze_group(students)
    assert students == original
    assert group_summary(students)["leaders"] == ["Дарья"]
    assert group_summary(students)["mean"] == 1032 / 13
    print("1. Обычный набор данных: OK")

    one = {"Мария": [80, 90]}
    data = group_summary(one)
    assert data["leaders"] == ["Мария"]
    assert data["mean"] == 85
    assert data["categories"]["хороший"] == 1
    print("2. Один студент: OK")

    tie = {"Ира": [80, 90], "Олег": [85, 85], "Петр": [60]}
    assert group_summary(tie)["leaders"] == ["Ира", "Олег"]
    print("3. Несколько лидеров: OK")

    empty = {}
    data = group_summary(empty)
    assert data["students"] == 0
    assert data["mean"] is None
    assert data["leaders"] == []
    assert "Рейтинг пуст" in analyze_group(empty)
    print("4. Пустая группа: OK")

    without = {"Лев": [], "Нина": [70]}
    data = group_summary(without)
    assert student_summary("Лев", [])["category"] == NO_RESULTS
    assert data["categories"][NO_RESULTS] == 1
    assert data["leaders"] == ["Нина"]
    assert data["mean"] == 70
    print("5. Студент без результатов: OK")

    for score, expected in ((0, "недостаточный"), (59, "недостаточный"),
                            (60, "удовлетворительный"), (74, "удовлетворительный"),
                            (75, "хороший"), (89, "хороший"),
                            (90, "отличный"), (100, "отличный")):
        assert classify(score) == expected
    print("6. Граничные значения категорий: OK")

    assert minimum([4, 2, 9]) == 2
    assert maximum([4, 2, 9]) == 9
    assert minimum([]) is None
    assert maximum([]) is None
    assert mean([]) is None
    assert mean([1, 2]) == 1.5
    print("7. Минимум, максимум и среднее: OK")

    print("Все сценарии пройдены.")


def main() -> None:
    print(analyze_group(students))
    run_tests()


if __name__ == "__main__":
    main()

