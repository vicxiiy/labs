measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]


# Этап 1. Первый проход
def first_pass(values: list[int]) -> tuple[int, int, int, int]:
    total = 0
    minimum = values[0]
    maximum = values[0]
    even_count = 0
    for value in values:
        total += value
        if value < minimum:
            minimum = value
        if value > maximum:
            maximum = value
        if value % 2 == 0:
            even_count += 1
    return total, minimum, maximum, even_count


# Этап 2. Второй проход
def count_above_average(values: list[int], average: float) -> int:
    count = 0
    for value in values:
        if value > average:
            count += 1
    return count


# Этап 3. Вычисление среднего и сбор результата
def analyze(values: list[int]) -> dict:
    total, minimum, maximum, even_count = first_pass(values)
    average = total / len(values)
    above_average = count_above_average(values, average)
    return {
        "sum": total,
        "min": minimum,
        "max": maximum,
        "even": even_count,
        "average": average,
        "above_average": above_average,
    }


def show_statistics() -> None:
    result = analyze(measurements)
    print("=== Статистика списка измерений ===")
    print("Данные:", measurements)
    print("Сумма:", result["sum"])
    print("Минимум:", result["min"])
    print("Максимум:", result["max"])
    print("Чётных значений:", result["even"])
    print("Среднее арифметическое:", result["average"])
    print("Значений больше среднего:", result["above_average"])


# Линейный поиск первого вхождения
def linear_search(items: list[int], target: int) -> tuple[int, int]:
    comparisons = 0
    for index in range(len(items)):
        comparisons += 1
        if items[index] == target:
            return index, comparisons
    return -1, comparisons


def run_user_search() -> None:
    print("\n=== Линейный поиск числа в списке измерений ===")
    target = int(input("Число для поиска: "))
    index, _ = linear_search(measurements, target)
    print(index)


# Дополнительный алгоритмический эксперимент
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def show_primes() -> None:
    print("\n=== Проверка простоты ===")
    for number in (1, 2, 3, 4, 9, 17, 25, 97, 100, 7919, 7921):
        print(f"{number}: {'простое' if is_prime(number) else 'не простое'}")


# Практическое расширение
def selection_sort(items: list[int]) -> None:
    size = len(items)
    for i in range(size - 1):
        min_index = i
        for j in range(i + 1, size):
            if items[j] < items[min_index]:
                min_index = j
        if min_index != i:
            items[i], items[min_index] = items[min_index], items[i]


def binary_search(items: list[int], target: int) -> tuple[int, int]:
    low = 0
    high = len(items) - 1
    comparisons = 0
    while low <= high:
        middle = (low + high) // 2
        comparisons += 1
        if items[middle] == target:
            return middle, comparisons
        elif items[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1, comparisons


def show_sort_and_binary() -> None:
    print("\n=== Сортировка выбором и бинарный поиск ===")
    data = measurements.copy()
    selection_sort(data)
    print("Исходный список:", measurements)
    print("Отсортированный:", data)
    for target in (21, 7, 10):
        index, comparisons = binary_search(data, target)
        print(f"Бинарный поиск {target}: индекс {index}, сравнений {comparisons}")


def make_dataset(size: int) -> list[int]:
    return [(i * 7919 + 13) % 10007 for i in range(size)]


def run_comparison() -> None:
    print("\n=== Сравнение поисков по числу сравнений ===")
    search_rows = []
    for size in (10, 100, 1000):
        data = make_dataset(size)
        selection_sort(data)

        linear_total = linear_max = binary_total = binary_max = 0
        for target in data:
            _, linear_count = linear_search(data, target)
            _, binary_count = binary_search(data, target)
            linear_total += linear_count
            binary_total += binary_count
            if linear_count > linear_max:
                linear_max = linear_count
            if binary_count > binary_max:
                binary_max = binary_count
        _, linear_miss = linear_search(data, -1)
        _, binary_miss = binary_search(data, -1)
        search_rows.append((size, linear_total / size, linear_max, linear_miss,
                            binary_total / size, binary_max, binary_miss))

    print("Поиск (каждый элемент набора + отсутствующее значение -1):")
    print(f"{'n':>5} | {'линейный: средн.':>16} | {'макс.':>5} | {'нет':>5} | "
          f"{'бинарный: средн.':>16} | {'макс.':>5} | {'нет':>5}")
    for size, l_avg, l_max, l_miss, b_avg, b_max, b_miss in search_rows:
        print(f"{size:>5} | {l_avg:>16.1f} | {l_max:>5} | {l_miss:>5} | "
              f"{b_avg:>16.1f} | {b_max:>5} | {b_miss:>5}")
        assert l_max == size and l_miss == size
        assert b_max <= size.bit_length()


# Тестовые сценарии
checks_done = 0


def check(expected, actual) -> None:
    global checks_done
    assert expected == actual, f"ожидалось {expected}, получено {actual}"
    checks_done += 1


def run_tests() -> None:
    result = analyze(measurements)
    check(144, result["sum"])
    check(7, result["min"])
    check(21, result["max"])
    check(4, result["even"])
    check(14.4, result["average"])
    check(6, result["above_average"])
    check((5, 5, 5, 0), first_pass([5]))
    check((-8, -7, 3, 1), first_pass([-4, 3, -7]))

    check((0, 1), linear_search(measurements, 12))
    check((1, 2), linear_search(measurements, 15))
    check((3, 4), linear_search(measurements, 18))
    check((8, 9), linear_search(measurements, 7))
    check((-1, 10), linear_search(measurements, 100))
    check((-1, 0), linear_search([], 5))

    for number, expected in ((1, False), (2, True), (3, True), (4, False),
                             (9, False), (25, False), (49, False), (97, True),
                             (100, False), (7919, True), (7921, False)):
        check(expected, is_prime(number))

    sorted_measurements = [7, 9, 11, 12, 15, 15, 18, 18, 18, 21]
    for source, expected in ((measurements.copy(), sorted_measurements), ([], []),
                             ([5], [5]), ([3, 2, 1], [1, 2, 3]), ([1, 2, 3], [1, 2, 3]),
                             ([-2, 5, -9, 0], [-9, -2, 0, 5]), ([4, 4, 4], [4, 4, 4])):
        selection_sort(source)
        check(expected, source)
    check([12, 15, 11, 18, 18, 9, 21, 15, 7, 18], measurements)

    sample = [1, 3, 5, 7, 9, 11]
    check((3, 3), binary_search(sample, 7))
    check((0, 2), binary_search(sample, 1))
    check((5, 3), binary_search(sample, 11))
    check((-1, 3), binary_search(sample, 4))
    check((-1, 2), binary_search(sample, 0))
    check((-1, 3), binary_search(sample, 12))
    check((-1, 0), binary_search([], 5))

    print(f"\nВсе {checks_done} проверок пройдены.")


def main() -> None:
    show_statistics()
    show_primes()
    show_sort_and_binary()
    run_comparison()
    run_tests()
    run_user_search()


if __name__ == "__main__":
    main()

