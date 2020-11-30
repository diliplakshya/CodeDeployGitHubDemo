import os
import boto3
from dotenv import load_dotenv
import zipfile
from botocore.exceptions import ClientError

load_dotenv(verbose=True)

class DownloadManger():
    def __init__(self):
        self.bucket_name = "dev-s3-datastax"
        self.AWS_S3_CREDENTIALS = {"aws_access_key_id" : os.getenv("AWS_KEY_ID"), "aws_secret_access_key" : os.getenv("AWS_ACCESS_KEY")}

    def unzip_files(self, input_file, output_path):
        with zipfile.ZipFile(input_file, 'r') as zip_ref:
            zip_ref.extractall(output_path)
            os.remove(input_file)

    def upload_file(self, input_path):
        zip_output_path, zip_file = os.path.split(input_path)
        self.unzip_files(input_path, zip_output_path)

        s3 = boto3.client('s3', **self.AWS_S3_CREDENTIALS)

        for root, dirs, files in os.walk(zip_output_path):
            for file in files:
                s3.upload_file(os.path.join(root, file), self.bucket_name, os.path.join("backend/CSVFiles", file))

    def download_file(self, output_path):
        s3 = boto3.client('s3', **self.AWS_S3_CREDENTIALS)

        list = s3.list_objects_v2(Bucket=self.bucket_name, StartAfter="backend")['Contents']

        for s3_key in list:
            s3_object = s3_key['Key']

            if not s3_object.startswith("backend"):
                continue

            if s3_object.endswith("/"):
                if not os.path.exists(s3_object):
                    os.makedirs(s3_object)
            else:
                if not os.path.exists(output_path):
                    os.makedirs(output_path)

                local_file_name = os.path.join(output_path, os.path.split(s3_object)[1])
                s3.download_file(self.bucket_name, s3_object, local_file_name)

    def create_presigned_post(self, object_name,
                              fields=None, conditions=None, expiration=3600):
        """Generate a pre-signed URL S3 POST request to upload a file

        :param bucket_name: string
        :param object_name: string
        :param fields: Dictionary of prefilled form fields
        :param conditions: List of conditions to include in the policy
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Dictionary with the following keys:
            url: URL to post to
            fields: Dictionary of form fields and values to submit with the POST
        :return: None if error.
        """

        # Generate a presigned S3 POST URL
        s3_client = boto3.client('s3', **self.AWS_S3_CREDENTIALS)

        try:
            response = s3_client.generate_presigned_post(self.bucket_name,
                                                         object_name,
                                                         Fields=fields,
                                                         Conditions=conditions,
                                                         ExpiresIn=expiration)
        except ClientError as e:
            print(e)
            return None

        # The response contains the pre-signed URL and required fields
        return response