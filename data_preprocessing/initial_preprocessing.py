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
            """
for col in df.columns:
    if df[col].nunique() == 1:
        df = df.drop(columns=[col])
        
if "unit" in df.columns and "Per hundred thousand inhabitants" in df["unit"].unique():
    df = df[df["unit"] == "Per hundred thousand inhabitants"]
    df = df.drop(columns=["unit"])

if "unit" in df.columns and (df["unit"] == "Person").all():
    df = df.drop(columns=["unit"])

def remove_euro(row):
    return any(value.startswith('Euro') for value in row.astype(str))

df = df[~df.apply(remove_euro, axis=1)]

def remove_total(row):
    return any(value.startswith('Total') for value in row.astype(str))

df = df[~df.apply(remove_total, axis=1)]

df = df.dropna(subset=["OBS_VALUE"])

for col in df.columns:
    if "Foreign country" in col:
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
        f"""df.to_csv("../initially_processed_data/{base_csv}", index=False)""",
            f"""import seaborn as sns
import matplotlib.pyplot as plt

# Set the figure size for better visualization
plt.figure(figsize=(20, 15))

# Create subplots - one for each column (except OBS_VALUE)
columns_to_analyze = [col for col in df.columns if col != 'OBS_VALUE']
num_columns = len(columns_to_analyze)
fig, axes = plt.subplots(num_columns, 1, figsize=(12, 6*num_columns))

# For each column, aggregate OBS_VALUE and create a visualization
for i, column in enumerate(columns_to_analyze):
    # Group by the column and aggregate OBS_VALUE (using mean)
    grouped_data = df.groupby(column)['OBS_VALUE'].mean().sort_values(ascending=False)
    
    # For columns with too many unique values, take top 20
    if len(grouped_data) > 20:
        grouped_data = grouped_data.head(20)
    
    # Create the plot
    ax = axes[i]
    grouped_data.plot(kind='bar', ax=ax)
    ax.set_title(f'Average OBS_VALUE by {{column}}')
    ax.set_ylabel('Average OBS_VALUE')
    ax.set_xlabel(column)
    ax.tick_params(axis='x', rotation=90)

plt.tight_layout()
plt.show()
""",
"""
df_copy = df.copy()

if "TIME_PERIOD" in df_copy.columns:
    max_time = df_copy["TIME_PERIOD"].max()
    df_filtered = df_copy[df_copy["TIME_PERIOD"] == max_time]

if "geo" in df_filtered.columns and "OBS_VALUE" in df_filtered.columns:
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    df_filtered.groupby("geo")["OBS_VALUE"].mean().sort_values(ascending=False).plot(kind="bar")
    plt.title(f"OBS_VALUE by geo for TIME_PERIOD {{max_time}}")
    plt.ylabel("OBS_VALUE")
    plt.xlabel("geo")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
""",
"""
aggregated_obs_values = df.groupby(['geo', 'TIME_PERIOD'])['OBS_VALUE'].sum()

threshold = 0.25 * df["TIME_PERIOD"].nunique()

group = df.groupby('geo')

countries_to_remove = []

for geo, group_data in group:
    time_period_counts = group_data['TIME_PERIOD'].value_counts()
    missing_counts = df["TIME_PERIOD"].nunique() - time_period_counts.count()
    
    if missing_counts > threshold:
        countries_to_remove.append(geo)

df_copy = df[~df['geo'].isin(countries_to_remove)]
aggregated_obs_values = df_copy.groupby(['geo', 'TIME_PERIOD'])['OBS_VALUE'].sum()

top_threshold = aggregated_obs_values.groupby('geo').mean().quantile(0.9)
top_countries = aggregated_obs_values.groupby('geo').mean()
top_countries = top_countries[top_countries > top_threshold].index
filtered_top_df = aggregated_obs_values.loc[top_countries].reset_index()

bottom_threshold = aggregated_obs_values.groupby('geo').mean().quantile(0.1)
bottom_countries = aggregated_obs_values.groupby('geo').mean()
bottom_countries = bottom_countries[bottom_countries < bottom_threshold].index
filtered_bottom_df = aggregated_obs_values.loc[bottom_countries].reset_index()


import plotly.express as px

fig = px.line(filtered_top_df, x='TIME_PERIOD', y='OBS_VALUE', color='geo', 
              markers=True, title='Top 10% Countries by Aggregated OBS_VALUE')
fig.show()

fig = px.line(filtered_bottom_df, x='TIME_PERIOD', y='OBS_VALUE', color='geo', 
              markers=True, title='Bottom 10% Countries by Aggregated OBS_VALUE')
fig.show()
"""
        ]
        nb["cells"] = [nbf.v4.new_code_cell(line) for line in code]
        with open(notebook_file, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
        print(f"Created notebook: {notebook_file}")

preprocessed_dir = "data\preprocessed_data"
notebooks_output_dir = "data\preprocessed_data_notebooks"
create_notebooks_from_csv(preprocessed_dir, notebooks_output_dir)

for csv_file in glob(os.path.join("data\initially_processed_data", "*_preprocessed.csv")):
    df = pd.read_csv(csv_file)
    columns_to_print = [col for col in df.columns if col not in ["TIME_PERIOD", "OBS_VALUE"]]
    print(f"Columns in {os.path.basename(csv_file)}: {columns_to_print}")
