import os
import nbformat as nbf
import pandas as pd

def create_notebook(csv_file, output_dir):
    base_name = os.path.splitext(os.path.basename(csv_file))[0]
    notebook_name = f"{base_name}_graph.ipynb"
    notebook_path = os.path.join(output_dir, notebook_name)

    nb = nbf.v4.new_notebook()
    graph_code = f"""\
import pandas as pd
import plotly.express as px
df = pd.read_csv(r'..\processed_data\{file_name}')

# ignore all rows with total values
df = df[~df['geo'].str.contains('Total')]
value_col = df.columns[-1]
aggregated_obs_values = df.groupby(['geo', 'year'])[value_col].sum()

threshold = 0.25 * df["year"].nunique()

group = df.groupby('geo')

countries_to_remove = []

for geo, group_data in group:
    year_counts = group_data['year'].value_counts()
    missing_counts = df["year"].nunique() - year_counts.count()
    
    if missing_counts > threshold:
        countries_to_remove.append(geo)

df_copy = df[~df['geo'].isin(countries_to_remove)]
aggregated_obs_values = df_copy.groupby(['geo', 'year'])[value_col].sum()

top_threshold = aggregated_obs_values.groupby('geo').mean().quantile(0.9)
top_countries = aggregated_obs_values.groupby('geo').mean()
top_countries = top_countries[top_countries > top_threshold].index
filtered_top_df = aggregated_obs_values.loc[top_countries].reset_index()

bottom_threshold = aggregated_obs_values.groupby('geo').mean().quantile(0.1)
bottom_countries = aggregated_obs_values.groupby('geo').mean()
bottom_countries = bottom_countries[bottom_countries < bottom_threshold].index
filtered_bottom_df = aggregated_obs_values.loc[bottom_countries].reset_index()


fig = px.line(filtered_top_df, x='year', y=[value_col], color='geo', 
              markers=True, title=f'Top 10% Countries by Aggregated {{value_col}}')
fig.show()

fig = px.line(filtered_bottom_df, x='year', y=[value_col], color='geo', 
              markers=True, title=f'Bottom 10% Countries by Aggregated {{value_col}}')
fig.show()

"""
    nb.cells.append(nbf.v4.new_code_cell(graph_code))

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

    print(f"Notebook created: {notebook_path}")

if __name__ == "__main__":
    input_dir = "./processed_data"
    output_dir = "./plots_notebooks"

    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".csv"):
            create_notebook(os.path.join(input_dir, file_name), output_dir)