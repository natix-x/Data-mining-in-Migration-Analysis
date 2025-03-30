import os
import pandas as pd
from glob import glob
import nbformat as nbf

def preprocess_csv(file_path, drop_columns):
    df = pd.read_csv(file_path)
    df = df.drop(columns=drop_columns, errors="ignore")
    return df

input_dir = "data"
output_dir = "data\preprocessed_data"
drop_columns = ["DATAFLOW", "LAST UPDATE", "OBS_FLAG", "CONF_STATUS", "freq"]

csv_files = glob(os.path.join(input_dir, "*.csv"))

def process_all_csv(csv_files, drop_columns, output_dir):
    for file_path in csv_files:
        df_processed = preprocess_csv(file_path, drop_columns)
        base_name = os.path.basename(file_path)
        output_file = os.path.join(output_dir, base_name.replace(".csv", "_preprocessed.csv"))
        df_processed.to_csv(output_file, index=False)
        print(f"Preprocessed {file_path} into {output_file}")

# process_all_csv(csv_files, drop_columns, output_dir)

def create_notebooks_from_csv(preprocessed_dir, notebooks_output_dir):
    for csv_file in glob(os.path.join(preprocessed_dir, "*_preprocessed.csv")):
        notebook_file = os.path.join(notebooks_output_dir, os.path.basename(csv_file).replace(".csv", ".ipynb"))
        nb = nbf.v4.new_notebook()
        base_csv = os.path.basename(csv_file)
        code = [
            "import pandas as pd",
            f"df = pd.read_csv('../preprocessed_data/{base_csv}')",
            """if "unit" in df.columns and "Per hundred thousand inhabitants" in df["unit"].unique():
    df = df[df["unit"] == "Per hundred thousand inhabitants"]
df = df.drop(columns=["unit"])

if "unit" in df.columns and (df["unit"] == "Person").all():
    df = df.drop(columns=["unit"])

if "geo" in df.columns:
    df = df[~df["geo"].str.startswith("Euro")]
for col in df.columns:
    if df[col].nunique() == 1:
        df = df.drop(columns=[col])
    """,
            "df.head()",
            "df.info()",
            "df.duplicated().sum()",
            "df.isnull().sum()",
            """for col in df:
    unique_vals = df[col].unique()
    print(f"{col}: {unique_vals[:40]}")
    if len(unique_vals) > 40:
        print(f"... and {len(unique_vals) - 40} others")""",


        "df",
        """obs_value_name = None # WYPELNIC
if obs_value_name:
    df = df.rename(columns={"OBS_VALUE": obs_value_name})""",
        f"""df.to_csv("../initially_processed_data/{base_csv}.csv", index=False)"""
        ]
        nb["cells"] = [nbf.v4.new_code_cell(line) for line in code]
        with open(notebook_file, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
        print(f"Created notebook: {notebook_file}")

preprocessed_dir = "data\preprocessed_data"
notebooks_output_dir = "data\preprocessed_data_notebooks"
create_notebooks_from_csv(preprocessed_dir, notebooks_output_dir)