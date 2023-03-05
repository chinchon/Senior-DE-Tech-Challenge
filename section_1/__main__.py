import pandas as pd
from pathlib import Path


PATH_TO_CSV = Path("applications_dataset_1.csv")

df = pd.read_csv(PATH_TO_CSV)
