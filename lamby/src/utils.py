import os
import json
import hashlib
import gzip
import glob


def deserialize_log():
    file_to_json('./.lamby/log')


def deserialize_config():
    file_to_json('./.lamby/config')


def serialize_log(data):
    json_to_file(data, './.lamby/log')


def serialize_config(data):
    json_to_file(data, './.lamby/config')


def json_to_file(obj, filename):
    with open(filename, 'w+') as file:
        file.write(json.dumps(obj))
        file.close()


def file_to_json(filename):
    if not os.path.isfile(filename):
        return {}
    with open(filename) as file:
        return json.load(file)


def file_sha256(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
        f.close()
    return hash_sha256.hexdigest()


# Currently done by hash comparison, a little hacky.
def diff_gzip(fname, compressed_object_path):
    current_hash = file_sha256(fname)
    with gzip.open(compressed_object_path, 'rb') as compressed_object:
        compressed_sha = hashlib.sha256()
        for chunk in iter(lambda: compressed_object.read(4096), b""):
            compressed_sha.update(chunk)
        compressed_object.close()
        return current_hash == compressed_sha.hexdigest()


def search_file_type(directory, ftype):
    results = []
    for file in glob.iglob(directory + '/**/*.' + ftype, recursive=True):
        results.append(file)
    return results
