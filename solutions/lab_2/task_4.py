# Задание 4. Циклические ссылки и сборщик мусора
import gc

first = []
second = []

first.append(second)
second.append(first)

print("first ссылается на second:", first[0] is second)
print("second ссылается на first:", second[0] is first)
print()

# Состояние сборщика, пороги и статистика
print("Автоматический сборщик включён:", gc.isenabled())
print("Пороги поколений:", gc.get_threshold())
print("Текущие счётчики поколений:", gc.get_count())
print("Статистика поколений:")
for number, stats in enumerate(gc.get_stats()):
    print(f"  поколение {number}: {stats}")
print()

# Удаление цикла и ручная сборка
import sys

first_id = id(first)
second_id = id(second)
print("id first:", first_id)
print("id second:", second_id)

print("Счётчик ссылок first (getrefcount):", sys.getrefcount(first))

del first
del second


def alive(ids):
    return sum(1 for obj in gc.get_objects() if id(obj) in ids)

print("Объектов цикла в памяти после del (до сборки):", alive({first_id, second_id}))
collected = gc.collect()
print("gc.collect() вернул:", collected)
print("Объектов цикла в памяти после gc.collect():", alive({first_id, second_id}))
print()

# Дополнительный эксперимент: отключённый сборщик
def make_cycle():
    a = []
    b = []
    a.append(b)
    b.append(a)
    return a, b

gc.collect()
print("Сборщик включён до эксперимента:", gc.isenabled())
gc.disable()
try:
    print("Сборщик включён во время эксперимента:", gc.isenabled())
    ids = set()
    cycles = []
    for _ in range(5):
        a, b = make_cycle()
        ids.add(id(a))
        ids.add(id(b))
        cycles.append((a, b))
    print("Создано объектов в циклах:", len(ids))
    del a, b
    cycles.clear()
    print("Из них ещё в памяти после удаления ссылок:", alive(ids))
    collected = gc.collect()
    print("gc.collect() вернул:", collected)
    print("Из них в памяти после gc.collect():", alive(ids))
finally:
    gc.enable()
print("Сборщик включён после эксперимента:", gc.isenabled())
print()

# Практическая задача: граф из четырёх узлов
baseline = gc.collect()
print("Собрано до создания графа:", baseline)

node_a = {"name": "A", "links": []}
node_b = {"name": "B", "links": []}
node_c = {"name": "C", "links": []}
node_d = {"name": "D", "links": []}

node_a["links"].append(node_b)
node_b["links"].append(node_c)
node_c["links"].append(node_a)

for node in (node_a, node_b, node_c, node_d):
    names = [linked["name"] for linked in node["links"]]
    print(f"Узел {node['name']} ссылается на: {names}")

del node_a, node_b, node_c

after_graph = gc.collect()
print("Собрано после удаления графа:", after_graph)

assert node_d["name"] == "D"
assert node_d["links"] == []
print("Независимый узел D доступен:", node_d)
