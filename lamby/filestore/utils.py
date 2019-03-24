from botocore.exceptions import ClientError

from filestore import fs


def get_object_from_key(key, bucket='development'):
    """
    Fetch an object from the minio server.
    """
    try:
        return fs.client.Object(fs.default_bucket_name, key)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            raise Exception('Cannot find bucket named %s' %
                            fs.default_bucket_name)

        elif error_code == 'NoSuchKey':
            raise Exception('Cannot find object with key %s\n' % key)
        else:
            raise Exception('Unknown client error %s' % error_code)


def get_object_body(obj):
    """
    Convert an object to a string.
    """
    return obj.get()['Body'].read().decode('utf-8')


def download_file_from_key(key, path, bucket='development'):
    """
    Download an object into a physical file at the given path on the server.
    """
    try:
        with open(path, 'wb') as data:
            fs.default_bucket.download_fileobj(key, data)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            raise Exception('Cannot find object with key %s' % key)
        else:
            raise Exception('Unknown client error %s' % error_code)
