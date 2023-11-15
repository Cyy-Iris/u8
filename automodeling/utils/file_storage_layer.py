import io
import logging
import os
from io import BytesIO
from typing import Optional

import dotenv
from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client

dotenv.load_dotenv()

environment = os.getenv("FILE_STORAGE_LAYER_ENV")


class FileStorageOperations:
    s3_client: Optional[S3Client] = None
    bucket_name = os.getenv("BUCKET_NAME")

    def __init__(self, s3_client: Optional[S3Client] = None) -> None:
        """
        Instantiates a FileStorageOperations object. If `environment` is set to `local`,
        the object will use the local filesystem. Otherwise, it will use S3.
        """
        if environment is None:
            raise ValueError("FILE_STORAGE_LAYER_ENV is not defined")
        if environment != "local":
            if self.bucket_name is None:
                raise ValueError("BUCKET_NAME is not defined")
            if s3_client is None:
                raise ValueError("s3_client is not defined")
        if s3_client and self.bucket_name and environment != "local":
            self.s3_client = s3_client

    def upload_file(self, input_file_content, output_file_path) -> str | None:
        """
        Uploads a file. If the environment is set to `local`, it will write the file to
        the local filesystem and return the path to the file. Otherwise, it will upload
        the file to S3 and return the path to the file in S3.
        """
        try:
            if environment == "local":
                output_directory = os.path.dirname(output_file_path)
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                with open(output_file_path, "w") as output_file:
                    output_file.write(input_file_content)
                return output_file_path
            else:
                if self.s3_client is not None and self.bucket_name is not None:
                    input_file_content_bytes = input_file_content.encode("utf-8")
                    self.s3_client.upload_fileobj(
                        io.BytesIO(input_file_content_bytes),
                        self.bucket_name,
                        output_file_path,
                    )
                    return output_file_path
                else:
                    raise ValueError("s3_client is not defined")
        except ClientError as error:
            logging.error("Error uploading file to S3 : ", error)
            return None
        except Exception as error:
            logging.error("Error uploading file : " + str(error))
            return None

    def get_file(self, file_path) -> str | None:
        """
        Gets a file. If the environment is set to `local`, it will return the path to
        the file in the local filesystem. Otherwise, it will download the file from S3
        and return the path to the file in the local filesystem.
        """
        try:
            if environment == "local":
                return file_path
            else:
                if self.s3_client is not None:
                    file_object = BytesIO()
                    if self.bucket_name is not None:
                        self.s3_client.download_fileobj(
                            self.bucket_name, file_path, file_object
                        )
                        new_file_path = f"data/s3/{file_path}"
                        output_directory = os.path.dirname(new_file_path)
                        if not os.path.exists(output_directory):
                            os.makedirs(output_directory)
                        with open(new_file_path, "wb") as output_file:
                            output_file.write(file_object.getvalue())

                        return new_file_path
                    else:
                        raise ValueError("bucket_name is not defined")
                else:
                    raise ValueError("s3_client is not defined")
        except ClientError as error:
            logging.error("Error getting file from S3 : ", error)
            return None
        except Exception as error:
            logging.error(f"File path: {file_path} Error getting file : {error}")
            return None
