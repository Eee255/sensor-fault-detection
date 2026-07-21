
import pandas as pd 
import yaml
from src.sensor_fault_detection.constants import SCHEMA_FILE_PATH
df = pd.read_csv("artifacts/07_21_2026_22_29_39/data_ingestion/ingested/train.csv")


schema = []

for column in df.columns:
    dtype = str(df[column].dtype)
    schema.append({column: dtype})

schema_dir = {"Columns": schema}

with open(SCHEMA_FILE_PATH, 'w') as f:
    yaml.dump(schema_dir, f)


print("schema.yaml written with", len(schema), "columns")