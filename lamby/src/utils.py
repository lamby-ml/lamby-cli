import os
import json
import hashlib
import gzip
import glob
import shutil
import os.path
import boto3
from botocore.client import Config
from src.settings import (MINIO_IP_ADDRESS,
                          ACCESS_KEY,
                          SECRET_KEY)

client = boto3.resource('s3',
                        endpoint_url=MINIO_IP_ADDRESS,
                        aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY,
                        config=Config(signature_version='s3v4'),
                        region_name='us-east-1')


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


# File upload utility
# Method checks that designated bucket exists, creates if it doesn't
# Checks if designated file exists, exit status 1 if it doesn't
# Return status 1 if file upload otherwise fails
def file_upload(file_path, file_key, bucket):
    # Check that bucket is available
    try:
        client.head_bucket(Bucket=bucket)
    except Exception:
        # The bucket does not exist or you have no access.
        client.create_bucket(Bucket=bucket)

    # Verify file exists
    if os.path.isfile(file_path):
        try:
            client.Bucket(bucket).upload_file(file_path, file_key)
        except Exception:
            return -1
    else:
        return -1

    return 0


# File download utility
# Method checks that bucket exists and is accessible
# downloads requested file key, returns -1 on failure
def file_download(file_key, file_destination, bucket):
    # check that bucket is available
    try:
        client.head_bucket(Bucket=bucket)
    except Exception:
        # bucket doesn't exist or no access available
        return -1

    # attempt to download file
    try:
        # not sure what to designate the download location file as
        client.meta.client.download_file(bucket, file_key, file_destination)
    except Exception:
        return -1

    return 0
