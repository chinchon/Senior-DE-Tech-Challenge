import pandas as pd
from pathlib import Path
from dateutil.parser import parse as date_parse
from datetime import datetime
from dateutil.relativedelta import relativedelta

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


def clean(df):
    df[["first_name", "last_name"]] = df["name"].apply(clean_name)
    df["date_of_birth"] = df["date_of_birth"].apply(date_parse)
    df["above_18"] = df["date_of_birth"].apply(lambda x: relativedelta(datetime(2022, 1, 1), x).years >= 18)
    df["date_of_birth"] = df["date_of_birth"].apply(lambda x: x.strftime("%Y%d%d"))
    return df


df = clean(df)
df