import os
import sys
import json
from datetime import datetime, timezone
from services.genie.crud.aws_s3 import list_s3_files

with open(
    os.path.abspath(os.path.join(os.getcwd(), "../../..", "sources.json")), "r"
) as f:
    sources = json.load(f)


def refresh_date_check(
    data_source: str, sources: list[dict] = sources, verbose: bool = True
) -> bool:
    """
    Checks if the current date has passed the refresh date for a data source.

    This function compares the current date against a refresh date specified in the sources
    configuration for a given data source. It helps control when data should be updated
    or refreshed.

    Args:
        data_source (str): The name of the data source to check, must match a key in sources.json
        sources (dict, optional): Dictionary containing data source configurations.
            Defaults to sources loaded from sources.json.
        verbose (bool, optional): Whether to print status messages. Defaults to True.

    Returns:
        bool: True if current date is >= refresh date, False otherwise

    Raises:
        Exception: If data_source is not found in sources.json keys
    """
    if data_source not in sources.keys():
        raise Exception("Value provided for data_source not found in sources.json keys")

    refresh_date_str = sources[data_source]["refresh_date"]
    refresh_date = datetime.strptime(refresh_date_str, "%m-%d-%Y")
    current_date = datetime.now()

    if current_date < refresh_date:
        if verbose:
            print(f"Refresh date for {data_source} not yet reached.")
        return False
    else:
        return True


def refresh_interval_check(
    data_source: str, s3_bucket: str, file_name: str, sources: dict = sources
) -> bool:
    """
    Checks if the current date has passed the refresh interval for a data source.

    This function compares the current date against a refresh intervalspecified in the sources
    configuration for a given data source. It helps control when data should be updated
    or refreshed.
    """
    if data_source not in sources.keys():
        raise Exception("Value provided for data_source not found in sources.json keys")

    latest_refresh_dt = list_s3_files(s3_bucket)[file_name]
    refresh_interval_hours = sources[data_source]["refresh_interval_hours"]

    if (
        (datetime.now(timezone.utc) - latest_refresh_dt).total_seconds() / 3600
    ) < refresh_interval_hours:
        return False, refresh_interval_hours
    else:
        return True, refresh_interval_hours
