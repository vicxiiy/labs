# Функции и их проверки
def arithmetic_mean(values: list[float]) -> float:
    if len(values) == 0:
        return 0.0
    total = 0
    for value in values:
        total += value
    return total / len(values)


def normalize_name(name: str) -> str:
    parts = name.split()
    if len(parts) == 0:
        return ""
    return " ".join(part.capitalize() for part in parts)


def build_report(
    student: str,
    results: list[int],
    *,
    precision: int = 2,
    prefix: str = "Результат",
) -> str:
    clean_name = normalize_name(student)
    if len(results) == 0:
        return f"{prefix} {clean_name}: результатов нет"
    mean_value = arithmetic_mean(results)
    return f"{prefix} {clean_name}: среднее {mean_value:.{precision}f}, работ {len(results)}"


def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    result = []
    for tag in tags:
        clean = tag.strip()
        if lowercase:
            clean = clean.lower()
        if clean == "":
            continue
        if clean not in result:
            result.append(clean)
    return tuple(result)


def run_asserts() -> None:
    assert arithmetic_mean([1, 2, 3]) == 2
    assert arithmetic_mean([5]) == 5
    assert arithmetic_mean([2.5, 3.5]) == 3.0
    assert arithmetic_mean([]) == 0.0

    assert normalize_name("  иВАН   пЕтРоВ ") == "Иван Петров"
    assert normalize_name("анна") == "Анна"
    assert normalize_name("   ") == ""

    assert build_report("анна", [80, 90]) == "Результат Анна: среднее 85.00, работ 2"
    assert build_report("борис", [70, 71, 72], precision=1, prefix="Итог") == "Итог Борис: среднее 71.0, работ 3"
    assert build_report("илья", []) == "Результат Илья: результатов нет"

    assert collect_tags(" Python ", "python", "", "Git") == ("python", "git")
    assert collect_tags("A", "a", lowercase=False) == ("A", "a")
    assert collect_tags() == ()
    print("Все проверки assert пройдены.")


# Корректные вызовы функций
def show_calls() -> None:
    print("\n=== Вызовы функций ===")
    scores = [80, 95, 70]
    print(arithmetic_mean(scores))
    print(normalize_name("  мАРИЯ   иванова "))
    print(build_report("анна", scores))
    print(build_report("анна", scores, precision=0))
    print(build_report(prefix="Итог", student="анна", results=scores, precision=1))
    print(collect_tags(" Python ", "git", "PYTHON", ""))
    print(collect_tags("Python", "python", lowercase=False))


# Распаковка * и **
def show_unpacking() -> None:
    print("\n=== Распаковка * и ** ===")
    tag_list = ["Python", " git ", "python", "Linux"]
    print(collect_tags(*tag_list))
    print(tag_list)

    options = {"precision": 1, "prefix": "Итог"}
    print(build_report("борис", [60, 72, 68], **options))
    print(options)

    arguments = ["дарья", [95, 93, 97, 90]]
    print(build_report(*arguments, **options))


# Исследование LEGB
course = "Основы программирования"


def outer() -> None:
    counter = 0

    def inner() -> None:
        nonlocal counter
        step = 1
        counter += step
        print("inner: step =", step, "| counter =", counter, "| course =", course, "| len('abc') =", len("abc"))

    inner()
    inner()
    print("outer: counter =", counter)


def show_legb() -> None:
    print("\n=== LEGB ===")
    outer()
    print("global: course =", course)
    assert course == "Основы программирования"


# Ошибка изменяемого значения по умолчанию
def add_result(value, results=[]):
    results.append(value)
    return results


def add_result_fixed(value, results=None):
    if results is None:
        results = []
    results.append(value)
    return results


def show_default_bug() -> None:
    print("\n=== Изменяемое значение по умолчанию ===")
    print("Исходная версия:")
    print(add_result(1))
    print(add_result(2))
    print(add_result(3))
    print("Объект значения по умолчанию:", add_result.__defaults__)

    print("Исправленная версия:")
    print(add_result_fixed(1))
    print(add_result_fixed(2))
    print(add_result_fixed(3))
    print("Значение по умолчанию:", add_result_fixed.__defaults__)


# Практическое расширение
def apply_to_results(operation, values):
    return [operation(value) for value in values]


def add_bonus(score):
    return score + 5


def make_threshold_checker(threshold):
    def check(score):
        return score >= threshold
    return check


def show_extension() -> None:
    print("\n=== Функции как аргументы и замыкания ===")
    results = [55, 70, 88]
    print(apply_to_results(add_bonus, results))
    print(apply_to_results(lambda score: score * 2, results))
    print("Исходный список:", results)

    passed_60 = make_threshold_checker(60)
    passed_75 = make_threshold_checker(75)
    print(apply_to_results(passed_60, results))
    print(apply_to_results(passed_75, results))
    print("Значение в замыкании passed_60:", passed_60.__closure__[0].cell_contents)
    print("Значение в замыкании passed_75:", passed_75.__closure__[0].cell_contents)


def main() -> None:
    run_asserts()
    show_calls()
    show_unpacking()
    show_legb()
    show_default_bug()
    show_extension()


if __name__ == "__main__":
    main()

