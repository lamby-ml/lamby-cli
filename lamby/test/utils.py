import os
import string
import random
import filecmp


def create_file(filename, N):
    file = open(filename, 'w+')
    random_string = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=N))
    file.write(random_string + '\n')
    file.close()


def mutate_file(filename, N):
    assert os.path.isfile(filename)
    file = open(filename, 'a')
    random_string = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=N))
    file.write(random_string + '\n')
    file.close()


def cmp_files(file1, file2):
    filecmp.clear_cache()
    return filecmp.cmp(file1, file2)
