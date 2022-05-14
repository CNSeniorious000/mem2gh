from records import *
from datetime import date


def test_yaml():
    mem = Memories(date(2022, 4, 9))
    mem.append(Record())
    mem.append(Record())
    mem.append(Record())
    mem.append(Record())
    mem.append(Record())
    mem.save_as_yaml("zyh")

    print(Memories.load_from_yaml("zyh"))


def test_pickle():
    mem = Memories(date(2022, 4, 9))
    mem.append(Record())
    mem.append(Record())
    mem.save_as_pickle("zyh")

    print(Memories.load_from_pickle("zyh"))


if __name__ == '__main__':
    test_yaml()
    test_pickle()
