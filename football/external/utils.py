import os
import json
from datetime import datetime as dt
from config import settings

def check_local_relevant(rel_path: str, ttl_days: int = 1) -> bool:
    strf_code = settings.STRFTIME_CODE
    
    # Check if the file exists
    if os.path.exists(rel_path):
        
        # Relevance check based on file modification time
        dt_curr = dt.strptime(dt.now().strftime(strf_code), strf_code)
        dt_file = dt.strptime(dt.fromtimestamp(os.path.getmtime(rel_path)).strftime(strf_code), strf_code)
        if (dt_curr - dt_file).days < ttl_days:
            print(f"Local file ({rel_path}) is relevant. Loading data ...")
            return True
        else:
            print(f"{rel_path} is older than {ttl_days} day(s). Fetching data from API ...")
            return False
    else:
        print(f"Relative path to file ({rel_path}) not found. Fetching data from API ...")
        return False
