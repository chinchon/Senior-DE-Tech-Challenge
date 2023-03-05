import pandas as pd
from pathlib import Path
from dateutil.parser import parse as date_parse
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
from hashlib import sha256


PATH_TO_CSV = Path("applications_dataset_1.csv")
# to add prefix or suffix when new ones are encountered
PREFIXES = ["Mr.", "Mrs.", "Miss", "Ms.", "Dr.", "Mr."]
SUFFIXES = ["PhD", "MD", "DDS", "DVM", "Jr.", "I", "II", "III"]
AFFIXES = PREFIXES + SUFFIXES

df = pd.read_csv(PATH_TO_CSV)


def clean_name(name):
    names = [x for x in name.split(" ") if x not in AFFIXES]
    assert len(names) == 2, f"len of names: {names} more than 2, try adding the affixes"
    first_name, last_name = names
    return pd.Series([first_name, last_name], index=["first_name", "last_name"])


def valid_email(email):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(com|net)"  # assuming only .com or .net is valid
    return bool(re.fullmatch(pattern, email))


def clean(df):
    df[["first_name", "last_name"]] = df["name"].apply(clean_name)
    df["date_of_birth"] = df["date_of_birth"].apply(date_parse)
    df["above_18"] = df["date_of_birth"].apply(
        lambda x: relativedelta(datetime(2022, 1, 1), x).years >= 18
    )
    df["date_of_birth"] = df["date_of_birth"].apply(lambda x: x.strftime("%Y%d%d"))
    df["is_valid_email"] = df["email"].apply(valid_email)
    df["is_valid_mobile_no"] = df["mobile_no"].apply(lambda x: len(x) == 8)

    df["is_successful"] = df.apply(
        lambda row: (
            row["is_valid_mobile_no"] and row["above_18"] and row["is_valid_email"]
        ),
        axis=1,
    )
    df["id"] = df.apply(
        lambda row: (
            row["last_name"]
            + "_"
            + sha256(row["date_of_birth"].encode("utf-8")).hexdigest()[:5]
        ),
        axis=1,
    )
    return df


df = clean(df)
df.to_csv("out.csv")
