import io
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def df_to_s3(df: pd.DataFrame, bucket_name: str, file_name: str):
    """
    Uploads a Pandas DataFrame as a CSV file to an S3 bucket.

    :param df: Pandas DataFrame to upload
    :param bucket_name: Name of the S3 bucket
    :param file_name: File name (including path if needed) in S3

    """
    # Convert DataFrame to CSV in memory
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    # Initialize S3 client
    s3 = boto3.client("s3")

    try:
        # Upload CSV to S3
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer.getvalue())
        print(f"File '{file_name}' uploaded successfully to S3 bucket '{bucket_name}'.")
    except NoCredentialsError:
        print("Credentials not available")
    except PartialCredentialsError:
        print("Incomplete credentials provided")
    except Exception as e:
        print(f"An error occurred: {e}")


def csv_from_s3(bucket_name, file_name):
    """
    Download a CSV file from an S3 bucket and load it into a Pandas DataFrame.

    :param bucket_name: Name of the S3 bucket
    :param file_name: File name (including path if needed) in S3
    :return: Pandas DataFrame containing the CSV data
    """
    # Create an S3 client
    s3_client = boto3.client("s3")

    try:
        # Download the file from S3 into a bytes buffer
        csv_buffer = io.BytesIO()
        s3_client.download_fileobj(bucket_name, file_name, csv_buffer)

        # Move the buffer's cursor to the beginning
        csv_buffer.seek(0)

        # Read the CSV data into a DataFrame
        df = pd.read_csv(csv_buffer)
        return df
    except NoCredentialsError:
        print("Credentials not available")
    except PartialCredentialsError:
        print("Incomplete credentials provided")
    except Exception as e:
        print(f"An error occurred: {e}")


def list_s3_files(bucket_name: str):
    """
    Lists all files in an S3 bucket along with their last modified dates.

    :param bucket_name: Name of the S3 bucket
    :return: Dictionary containing file names as keys and last modified dates as values
    """
    # Initialize S3 client
    s3_client = boto3.client("s3")

    try:
        # Get list of all objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        # Extract file information into a dictionary
        files_info = {}
        if "Contents" in response:
            for obj in response["Contents"]:
                files_info[obj["Key"]] = obj["LastModified"]
            return files_info
        else:
            print(f"No files found in bucket '{bucket_name}'")
            return {}

    except NoCredentialsError:
        print("Credentials not available")
    except PartialCredentialsError:
        print("Incomplete credentials provided")
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}
