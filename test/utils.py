import os
import string
import random
import shutil
import gzip
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


def unzip_to(zipped_filename, dest_filename):
    with gzip.open(zipped_filename, 'rb') as compressed_file:
        with open(dest_filename, 'wb') as uncompressed_file:
            shutil.copyfileobj(compressed_file, uncompressed_file)
            compressed_file.close()
            uncompressed_file.close()


def cmp_files(file1, file2):
    filecmp.clear_cache()
    return filecmp.cmp(file1, file2)
