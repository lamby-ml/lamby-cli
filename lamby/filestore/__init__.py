import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError


"""
###########
Boto3 Notes
###########

Exception Error Codes
---------------------
BucketAlreadyExists
BucketAlreadyOwnedByYou
NoSuchBucket
NoSuchKey
NoSuchUpload
ObjectAlreadyInActiveTierError
ObjectNotInActiveTierError
"""


class Filestore(object):
    def __init__(self, default_bucket_name):
        self.client = boto3.resource(
            's3',
            endpoint_url=os.getenv('MINIO_SERVER_URI'),
            aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('MINIO_SECRET_KEY'),
            config=Config(signature_version='s3v4'),
            region_name='us-east-1'
        )
        self.default_bucket_name = default_bucket_name
        self.create_default_bucket()
        self.default_bucket = self.client.Bucket(self.default_bucket_name)

    def create_default_bucket(self):
        try:
            self.client.create_bucket(Bucket=self.default_bucket_name)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code != 'BucketAlreadyOwnedByYou' and \
                    error_code != 'BucketAlreadyExists':
                raise
        except Exception as e:
            raise Exception('Unexpected Error: %s' % str(e))

    def clear_testing_bucket(self):
        try:
            bucket = self.client.Bucket('testing')
            bucket.delete_objects(Delete={
                'Objects': [{'Key': obj.key} for obj in bucket.objects.all()]
            })
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code != 'NoSuchBucket' and error_code != 'NoSuchKey':
                raise
        except Exception as e:
            raise Exception('Unexpected Error: %s' % str(e))

    def get_object_body_from_key(self, key):
        return self.get_object_body(self.get_object_from_key(key))

    def get_object_from_key(self, key):
        """
        Fetch an object from the minio server.
        """
        try:
            return self.client.Object(self.default_bucket_name, key)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                raise Exception('Cannot find bucket named %s' %
                                self.default_bucket_name)
            elif error_code == 'NoSuchKey':
                raise Exception('Cannot find object with key %s\n' % key)
            else:
                raise Exception('Unknown client error %s' % error_code)

    def get_object_body(self, obj):
        """
        Convert an object to a string.
        """
        return obj.get()['Body'].read().decode('utf-8')

    def upload_file(self, path, project_id):
        try:
            path = os.path.abspath(path)
            with open(os.path.abspath(path), 'rb') as f:
                base = os.path.basename(path)
                key = os.path.splitext(base)[0]
                self.default_bucket.put_object(
                    Body=f,
                    Key="{}/{}".format(project_id, key)
                )
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                raise Exception('Cannot find bucket named %s' %
                                self.default_bucket_name)
        except Exception as e:
            raise Exception(f'Unexpected Error: {e}')

    def download_file_from_key(self, key, path):
        """
        Download an object into a physical file at the given path on the
        server.
        """
        try:
            with open(path, 'wb') as data:
                self.default_bucket.download_fileobj(key, data)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                raise Exception('Cannot find object with key %s' % key)
            else:
                raise Exception('Unknown client error %s' % error_code)


fs = Filestore(os.getenv('LAMBY_ENV', default='development'))
