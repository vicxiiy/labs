# Задание 3. Подсчет ссылок и время жизни объекта
# Счетчик ссылок:
import sys

data = [1, 2, 3]
print("После создания:", sys.getrefcount(data))

alias = data
print("После создания alias:", sys.getrefcount(data))

container = [data]
print("После помещения в контейнер:", sys.getrefcount(data))

del alias
print("После del alias:", sys.getrefcount(data))

container.clear()
print("После очистки контейнера:", sys.getrefcount(data))
print()

# Слабая ссылка:
import weakref

class Record:
    pass

record = Record()
weak_record = weakref.ref(record)

print(weak_record())
del record
print(weak_record())
print()

# Практическая задача
class Record:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Record({self.name!r})"

registry = weakref.WeakValueDictionary()

first = Record("A")
second = Record("B")
temporary = Record("C")

registry["A"] = first
registry["B"] = second
registry["C"] = temporary

print("Реестр сразу после регистрации:", sorted(registry.keys()))

del temporary
print("После удаления temporary:", sorted(registry.keys()))
print("registry.get('C'):", registry.get("C"))

del first
print("После удаления first:", sorted(registry.keys()))
print("registry.get('A'):", registry.get("A"))
print("Оставшиеся записи:", dict(registry))
