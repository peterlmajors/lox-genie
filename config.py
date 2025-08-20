from pydantic_settings import BaseSettings

# Enforce Type Hints on Environment Variables
class Settings(BaseSettings):
    
    ENV: str
    
    GCP_SA_TYPE: str
    GCP_SA_PROJECT_ID: str
    GCP_SA_PRIVATE_KEY_ID: str
    GCP_SA_PRIVATE_KEY: str
    GCP_SA_CLIENT_EMAIL: str
    GCP_SA_CLIENT_ID: str
    GCP_SA_AUTH_URI: str
    GCP_SA_TOKEN_URI: str
    GCP_SA_AUTH_PROVIDER_CERT_URL: str
    GCP_SA_CLIENT_CERT_URL: str
    GCP_SA_UNIVERSE_DOMAIN: str
    
    CFBD_API_KEY: str
    
    SLEEPER_IFL_25: str
    SLEEPER_IFL_24: str
    SLEEPER_FSASFOR_2024: str
    
    AWS_IAM_ACCOUNT_ID: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    
    NFL_YEAR: int = 2025
    CFBD_DATA_PY_YEARS: range = range(2001, 2025)
    NFL_DATA_PY_YEARS: range = range(2001, 2025)

    OFFENSE_STATS: list[str] = ["pass_yd", "pass_td", "pass_int", "pass_2pt", "rush_yd", "rush_td", "rush_2pt", "rec", "rec_yd", "rec_td", "rec_2pt", "fum", "fum_lost", "bonus_rec_te", "st_td"]
    DEFENSE_STATS: list[str] = ["sack", "int", "ff", "fum_rec", "fum_rec_td", "safe", "def_td", "def_st_td", "def_st_ff", "def_st_fum_rec", "blk_kick", "st_fum_rec", "st_ff", "pts_allow_0", "pts_allow_1_6", "pts_allow_7_13", "pts_allow_14_20", "pts_allow_21_27", "pts_allow_28_34", "pts_allow_35p"]
    KICKER_STATS: list[str] = ["fgm_0_19", "fgm_20_29", "fgm_30_39", "fgm_40_49", "fgm_50_59", "fgm_60p", "fgmiss", "xpm", "xpmiss"]

    STRFTIME_CODE: str = '%Y-%m-%d %H:%M EDT'
    
    class Config:
        env_file = ".env"

settings = Settings()