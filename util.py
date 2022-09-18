import random


def shuffled(seq):
    lst = [*seq]
    random.shuffle(lst)
    return lst
