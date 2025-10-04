import io
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import pandas as pd


def post_s3(data, bucket_name: str, file_name: str):
    """
    Uploads data to an S3 bucket as either a CSV file (for pandas DataFrames) or JSON file (for dictionaries/lists).

    :param data: Data to upload - pandas DataFrame for CSV, dict/list for JSON
    :param bucket_name: Name of the S3 bucket
    :param file_name: File name (including path if needed) in S3
    :return: bool: True if successful, False otherwise
    """
    # Initialize S3 client
    s3 = boto3.client("s3")

    try:
        # Determine file type and process accordingly
        if file_name.lower().endswith(".csv"):
            # Handle DataFrame input for CSV
            if not isinstance(data, pd.DataFrame):
                raise ValueError(
                    f"Data must be a pandas DataFrame for CSV files, got {type(data).__name__}"
                )

            # Convert DataFrame to CSV in memory
            csv_buffer = io.StringIO()
            data.to_csv(csv_buffer, index=False)
            file_content = csv_buffer.getvalue()
            content_type = "text/csv"

        elif file_name.lower().endswith(".json"):
            # Handle dict/list input for JSON
            if not isinstance(data, (dict, list)):
                raise ValueError(
                    f"Data must be a dict or list for JSON files, got {type(data).__name__}"
                )

            # Convert data to JSON string
            file_content = json.dumps(data, indent=2, default=str)
            content_type = "application/json"

        else:
            raise ValueError(
                f"Unsupported file type: {file_name}. Only .csv and .json files are supported."
            )

        # Upload file to S3
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_content,
            ContentType=content_type,
        )

        print(f"File '{file_name}' uploaded successfully to S3 bucket '{bucket_name}'.")
        return True

    except NoCredentialsError:
        print("Credentials not available")
        return False
    except PartialCredentialsError:
        print("Incomplete credentials provided")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def list_s3_objects(bucket_name: str):
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

def get_s3(bucket_name, file_name):
    """
    Download a file from an S3 bucket and return it as a pandas DataFrame (for CSV) or dictionary (for JSON).

    :param bucket_name: Name of the S3 bucket
    :param file_name: File name (including path if needed) in S3
    :return: Pandas DataFrame for CSV files, dictionary for JSON files
    """
    # Create an S3 client
    s3_client = boto3.client("s3")

    try:
        # Download the file from S3 into a bytes buffer
        file_buffer = io.BytesIO()
        s3_client.download_fileobj(bucket_name, file_name, file_buffer)

        # Move the buffer's cursor to the beginning
        file_buffer.seek(0)

        # Determine file type and process accordingly
        if file_name.lower().endswith(".csv"):
            # Read CSV data into a DataFrame
            df = pd.read_csv(file_buffer)
            return df
        elif file_name.lower().endswith(".json"):
            # Read JSON data into a dictionary
            json_data = json.loads(file_buffer.read().decode("utf-8"))
            return json_data
        else:
            raise ValueError(
                f"Unsupported file type: {file_name}. Only .csv and .json files are supported."
            )

    except NoCredentialsError:
        print("Credentials not available")
        return None
    except PartialCredentialsError:
        print("Incomplete credentials provided")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
