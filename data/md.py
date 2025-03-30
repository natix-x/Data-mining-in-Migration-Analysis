import os

# Define the base directories
data_dir = "c:\\Users\\izabe\\Documents\\datamining\\data"
notebooks_dir = os.path.join(data_dir, "preprocessed_data_notebooks")
output_file = os.path.join(data_dir, "dataset_links.md")

# Define a function to generate dataset links
def generate_links(data_dir, notebooks_dir, output_file):
    # Get all CSV files in the data directory
    csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    
    # Start writing the Markdown file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Dataset Links\n\n")
        f.write("Below are the links to the datasets and their corresponding notebooks:\n\n")
        
        for csv_file in csv_files:
            # Extract the base name without extension
            base_name = os.path.splitext(csv_file)[0]
            
            # Construct the online dataset link (you can customize this if needed)
            online_link = f"https://ec.europa.eu/eurostat/databrowser/view/{base_name}/"
            
            # Check if a corresponding notebook exists
            notebook_file = os.path.join(notebooks_dir, f"{base_name}_preprocessed.ipynb")
            if os.path.exists(notebook_file):
                notebook_link = f"./preprocessed_data_notebooks/{base_name}_preprocessed.ipynb"
                notebook_status = f"[Notebook File]({notebook_link})"
            else:
                notebook_status = "Notebook File: *Not Found*"
            
            # Write the dataset entry
            f.write(f"- **{base_name}**\n")
            f.write(f"  - [Online Dataset]({online_link})\n")
            f.write(f"  - {notebook_status}\n\n")
    
    print(f"Markdown file with dataset links created: {output_file}")

# Generate the dataset links
generate_links(data_dir, notebooks_dir, output_file)