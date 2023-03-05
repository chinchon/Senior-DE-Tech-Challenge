import pandas as pd
from pathlib import Path
from dateutil.parser import parse as date_parse
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
from hashlib import sha256


PATH_TO_DATA = Path("./data")
# to add prefix or suffix when new ones are encountered
PREFIXES = ["Mr.", "Mrs.", "Miss", "Ms.", "Dr.", "Mr."]
SUFFIXES = ["PhD", "MD", "DDS", "DVM", "Jr.", "I", "II", "III"]
AFFIXES = PREFIXES + SUFFIXES


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


def main():
    files = PATH_TO_DATA.glob("*.csv")
    for file in files:
        df = pd.read_csv(file)
        df = clean(df)
        columns = ["id", "first_name", "last_name", "email", "date_of_birth"]
        df.loc[df["is_successful"], columns].to_csv(f"{PATH_TO_DATA}/successful/{file.name}", index=False)
        df.loc[~df["is_successful"]].to_csv(f"{PATH_TO_DATA}/unsuccessful/{file.name}", index=False)
        file.rename(f"{PATH_TO_DATA}/processed/{file.name}")


if __name__ == "__main__":
    main()
