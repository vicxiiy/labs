# ------------------------------ Практическая задача ------------------------------
import sys
import tracemalloc

ELEMENTS = 100_000
RANGE_COPIES = 1000

# ------------------------------ ИЗМЕРЕНИЯ ------------------------------

# Часть 1: размеры отдельных объектов.
def measure_object_sizes():
    ten_numbers = list(range(1, 11))
    samples = [
        ("пустой список", []),
        ("список из 10 чисел", ten_numbers),
        ("кортеж из 10 чисел", tuple(ten_numbers)),
        ("строка из 10 символов", "abcdefghij"),
        ("целое число", 12345),
        ("None", None),
    ]
    return [{"name": name, "size": sys.getsizeof(obj)} for name, obj in samples]

# Часть 2: моменты, когда размер списка меняется при append().
def measure_list_growth(total=100):
    items = []
    last_size = sys.getsizeof(items)
    changes = [{"length": 0, "size": last_size}]
    for value in range(total):
        items.append(value)
        size = sys.getsizeof(items)
        if size != last_size:
            changes.append({"length": len(items), "size": size})
            last_size = size
    return changes

# Часть 3: память, выделенная при создании объекта через tracemalloc.
def measure_scenario(name, factory, elements, copies=1):
    tracemalloc.start()
    try:
        if copies == 1:
            holder_size = 0
            sample = factory(elements)
        else:
            holder = [factory(elements) for _ in range(copies)]
            holder_size = sys.getsizeof(holder)
            sample = holder[0]
        current, peak = tracemalloc.get_traced_memory()
        outer_size = sys.getsizeof(sample)
    finally:
        tracemalloc.stop()

    return {
        "name": name,
        "elements": elements,
        "copies": copies,
        "outer_size": outer_size,
        "current": (current - holder_size) / copies,
        "peak": (peak - holder_size) / copies,
    }

# Отношение пиковых объёмов двух сценариев (None, если делить на 0).
def calculate_ratio(first, second):
    if second["peak"] <= 0:
        return None
    return first["peak"] / second["peak"]

# Запускает все измерения и собирает результаты в одну структуру.
def collect_results():
    list_scenario = measure_scenario(
        "list(range(N))", lambda n: list(range(n)), ELEMENTS
    )
    range_scenario = measure_scenario(
        "range(N)", lambda n: range(n), ELEMENTS, copies=RANGE_COPIES
    )
    return {
        "object_sizes": measure_object_sizes(),
        "list_growth": measure_list_growth(),
        "scenarios": [list_scenario, range_scenario],
        "peak_ratio": calculate_ratio(list_scenario, range_scenario),
    }

# ------------------------------ ФОРМАТИРОВАНИЕ ------------------------------

def kilobytes(value):
    return f"{value / 1024:.2f}"


def format_object_sizes(sizes):
    lines = ["1. Размеры отдельных объектов (sys.getsizeof)"]
    for item in sizes:
        lines.append(f"   {item['name']:<24}{item['size']:>6} байт")
    return lines


def format_list_growth(changes):
    lines = ["2. Рост списка (показаны только изменения размера)"]
    for item in changes:
        lines.append(f"   длина {item['length']:>3}   размер {item['size']:>4} байт")
    return lines


def format_scenarios(scenarios, ratio):
    lines = ["3. Сравнение сценариев (tracemalloc)"]
    header = (f"   {'Сценарий':<16}{'Элементов':>10}{'Объектов':>10}"
              f"{'Внешний, байт':>15}{'Текущий, КБ':>13}{'Пиковый, КБ':>13}")
    lines.append(header)
    for s in scenarios:
        lines.append(
            f"   {s['name']:<16}{s['elements']:>10}{s['copies']:>10}"
            f"{s['outer_size']:>15}{kilobytes(s['current']):>13}{kilobytes(s['peak']):>13}"
        )
    lines.append("   Значения памяти даны на один объект (для range среднее по "
                 "нескольким объектам).")

    first, second = scenarios
    lines.append("")
    lines.append(f"   Пик {second['name']} на один объект: {second['peak']:.1f} байт")
    if ratio is None:
        lines.append("   Отношение пиков: не определено (пик второго сценария равен 0)")
    else:
        lines.append(
            f"   Отношение пиков ({first['name']} / {second['name']}): {ratio:.0f}"
        )
    return lines


def format_report(results):
    lines = ["ОТЧЁТ О ПОТРЕБЛЕНИИ ПАМЯТИ", "-" * 72, ""]
    lines += format_object_sizes(results["object_sizes"])
    lines.append("")
    lines += format_list_growth(results["list_growth"])
    lines.append("")
    lines += format_scenarios(results["scenarios"], results["peak_ratio"])
    return "\n".join(lines)


# ------------------------------ ЗАПУСК ------------------------------
def main():
    results = collect_results()
    print(format_report(results))


if __name__ == "__main__":
    main()
