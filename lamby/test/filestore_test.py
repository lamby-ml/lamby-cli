# import boto3
# from moto import mock_s3
# from botocore.client import Config
# from src.utils import (file_upload, file_download)
# from src.settings import (MINIO_IP_ADDRESS,
#                           TEST_BUCKET,
#                           ACCESS_KEY,
#                           SECRET_KEY)


# @mock_s3
# class test_file_upload_setup()

# # test_client = boto3.resource('s3',
# #                              endpoint_url=MINIO_IP_ADDRESS,
# #                              aws_access_key_id=ACCESS_KEY,
# #                              aws_secret_access_key=SECRET_KEY,
# #                              config=Config(signature_version='s3v4'),
# #                              region_name='us-east-1')
# def test_file_upload_basic(runner):
#     with runner.isolated_filesystem():
#         filename = '../../sandbox/upload.onnx'
#         file_key = 'upload.onnx'

#         status = file_upload(filename, file_key, TEST_BUCKET)

#         assert status == 0
#         # check that file exists on file store in the correct bucket ???


# def test_file_download_basic(runner):
#     with runner.isolated_filesystem():

#         # file_key = 'download.onnx'
#         # file_destination = '../../sandbox/download.onnx'

#         # status = file_download(file_key, file_destination, TEST_BUCKET)

#         assert True

#         # check contents of file?


# def test_file_upload_invalid_file(runner):
#     with runner.isolated_filesystem():
#         # filename = 'fake.onnx'
#         # file_key = 'fake.onnx'

#         # status = file_upload(filename, file_key, TEST_BUCKET)

#         # assert status == -1

#         assert True


# def test_file_download_invalid_file(runner):
#     with runner.isolated_filesystem():

#         # file_key = 'fake.onnx'
#         # file_destination = '../'

#         # status = file_download(file_key, file_destination, TEST_BUCKET)

#         # assert status == -1

#         assert True
