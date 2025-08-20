import os, sys, json
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..", "..")))
from config import settings

import cfbd
from cfbd.rest import ApiException
from external.aws import df_to_s3
from utilities.refresh_date import refresh_date_check

with open(os.path.abspath(os.path.join(os.getcwd(), "..", "..", "external", "sources.json")), "r") as f:
    sources = json.load(f)

# THE CFBD API docs can be found here:
# https://github.com/CFBD/cfbd-python/tree/main


def nfl_draft(seasons: list[int] = sources["cfbd_nfl_draft"]["seasons"]):
    """Retrieves NFL draft data for specified seasons from the CFBD API.

    Args:
        seasons (list[int], optional): List of NFL draft years to retrieve data for.
            Defaults to seasons defined in sources.json.

    Returns:
        list: List of CFBD draft pick objects containing detailed information about each draft pick.
            Each object includes player info, college, draft position, and team details.

    Raises:
        ApiException: If there's an error retrieving data from the CFBD API.
    """
    configuration = cfbd.Configuration()
    configuration.api_key["Authorization"] = settings.CFBD_API_KEY
    configuration.api_key_prefix["Authorization"] = "Bearer"
    api_instance = cfbd.DraftApi(cfbd.ApiClient(configuration))

    responses = []
    for season in seasons:
        try:
            api_response = api_instance.get_draft_picks(year=season)
            responses.append(api_response)
        except ApiException as e:
            print(e, f"Failed to retrieve draft picks for: {season} season")

    responses = [item for sublist in responses for item in sublist]
    return responses


def upload_nfl_draft():
    """Processes and uploads NFL draft data to an S3 bucket.

    Retrieves draft data using nfl_draft(), performs data cleaning operations including:
    - Removes hometown information
    - Converts CFBD objects to pandas DataFrame
    - Removes internal configuration fields
    - Standardizes column names
    - Replaces NaN values with None

    The cleaned data is then uploaded to the 'lox-football' S3 bucket as 'cfbd_draft.csv'.

    Note:
        Requires valid AWS credentials and CFBD API key in settings.
    """
    if refresh_date_check("cfbd_nfl_draft"):
        draft = nfl_draft()
        for pick in draft:
            if hasattr(pick, "hometown_info"):
                pick.hometown_info = None

        draft_dicts = [vars(pick) for pick in draft]
        draft_df = pd.DataFrame(draft_dicts)

        draft_df = draft_df.drop(["_configuration", "discriminator"], axis=1)
        draft_df.columns = [col.lstrip("_") for col in draft_df.columns]
        draft_df.replace(np.NaN, None, inplace=True)

        df_to_s3(draft_df, "lox-football", "cfbd_draft.csv")
