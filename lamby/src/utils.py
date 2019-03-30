import glob
import gzip
import hashlib
import json
import os
import shutil
import requests
import click
import sys


def post_request(payload, url):
    try:
        return requests.post(os.getenv('LAMBY_WEB_URI') +
                             url, json=payload)
    except requests.exceptions.ConnectionError:
        click.echo('Could not reach lamby web. Aborting authorization.')
        sys.exit(1)
    except requests.exceptions.Timeout:
        click.echo('Connection timed out. Aborting authorization.')
        sys.exit(1)
    except requests.exceptions.TooManyRedirects:
        click.echo(
            'Too many redirects to reach lamby web. Aborting authorization.')
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        click.echo(e)
        sys.exit(1)


# def get_request():


def deserialize_log():
    return file_to_json('./.lamby/log')


def deserialize_config():
    return file_to_json('./.lamby/config')


def deserialize_meta():
    return file_to_json('./.lamby/meta')


def serialize_log(data):
    json_to_file(data, './.lamby/log')


def serialize_config(data):
    json_to_file(data, './.lamby/config')


def serialize_meta(data):
    json_to_file(data, './.lamby/meta')


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
    return search_pattern(directory + '/**/*.' + ftype)


def search_pattern(pattern):
    results = []
    for file in glob.iglob(pattern, recursive=True):
        results.append(file)
    return results


def unzip_to(zipped_filename, dest_filename):
    with gzip.open(zipped_filename, 'rb') as compressed_file:
        with open(dest_filename, 'wb') as uncompressed_file:
            shutil.copyfileobj(compressed_file, uncompressed_file)
            compressed_file.close()
            uncompressed_file.close()
