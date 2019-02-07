import os
import json
import hashlib
import gzip


def deserialize_log():
    if not os.path.isfile('./.lamby/log'):
        return {}
    with open('./.lamby/log') as log_file:
        return json.load(log_file)


def deserialize_config():
    if not os.path.isfile('./.lamby/config'):
        return {}
    with open('./.lamby/config') as config_file:
        return json.load(config_file)


def serialize_log(data):
    with open('./.lamby/log', 'w+') as log_file:
        log_file.write(json.dumps(data))
        log_file.close()


def serialize_config(data):
    with open('./.lamby/config', 'w+') as config_file:
        config_file.write(json.dumps(data))
        config_file.close()


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
