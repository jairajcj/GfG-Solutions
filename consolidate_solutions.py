import os

source_dir = os.path.abspath("GfG_Solutions")
output_file = os.path.abspath("All_Solutions.txt")

files = [f for f in os.listdir(source_dir) if f.endswith(".py")]
files.sort()

print(f"Consolidating {len(files)} solutions into {output_file}...")

with open(output_file, "w", encoding="utf-8") as outfile:
    for filename in files:
        # Parse date and name from filename: YYYY-MM-DD_Problem_Name.py
        try:
            date_part = filename[:10] # YYYY-MM-DD
            name_part = filename[11:-3].replace("_", " ") # Remove .py and underscores
        except:
            date_part = "Unknown"
            name_part = filename

        outfile.write("="*80 + "\n")
        outfile.write(f"Date: {date_part}\n")
        outfile.write(f"Problem: {name_part}\n")
        outfile.write(f"Filename: {filename}\n")
        outfile.write("="*80 + "\n\n")

        file_path = os.path.join(source_dir, filename)
        with open(file_path, "r", encoding="utf-8") as infile:
            outfile.write(infile.read())
        
        outfile.write("\n\n")

print("Done.")
