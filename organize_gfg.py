import os
import re
import shutil

source_dir = os.path.abspath("GfG_Raw")
target_dir = os.path.abspath("GfG_Solutions")

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

month_map = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12"
}

def clean_problem_name(name):
    # Remove special characters, replace spaces with underscores
    name = re.sub(r"[^\w\s-]", "", name)
    name = name.strip().replace(" ", "_")
    return name

count = 0

print(f"Scanning {source_dir}...")

for folder in os.listdir(source_dir):
    # Match folder pattern: "Month YYYY GFG SOLUTION"
    match = re.match(r"([A-Za-z]+) (\d{4}) GFG SOLUTION", folder)
    if match:
        month_name, year = match.groups()
        if month_name not in month_map:
            print(f"Skipping folder with unknown month: {folder}")
            continue
            
        month_num = month_map[month_name]
        folder_path = os.path.join(source_dir, folder)
        
        files = os.listdir(folder_path)
        py_files = [f for f in files if f.endswith(".py")]
        md_files = [f for f in files if f.endswith(".md")]
        
        # Create a map of day -> problem_name from .md files
        # Expected .md format: "DD(MonthAbbr) Problem Name.md"
        # e.g., "01(April) Pairs violating the BST property.md"
        day_problem_map = {}
        for md in md_files:
            # Flexible regex for md file: start with digits, then (something), then name
            md_match = re.match(r"^(\d+)\([A-Za-z]+\)\s+(.*)\.md$", md)
            if md_match:
                day_str = md_match.group(1)
                problem_name = md_match.group(2)
                day_problem_map[int(day_str)] = problem_name
        
        for py_file in py_files:
            # Expected .py format: "Month-DD.py" e.g. "April-01.py"
            # Regex: MonthName-DD.py
            py_match = re.match(r"([A-Za-z]+)-(\d+)\.py", py_file)
            if py_match:
                p_month, p_day = py_match.groups()
                # Check if p_month matches folder month (just in case)
                if p_month != month_name and p_month not in month_name: 
                    # Handle "Feb" vs "February" if needed, but usually filenames match folder context or are consistent
                    # verification: filenames appear to be "April-01.py" in "April 2024" folder.
                    pass
                
                day_num = int(p_day)
                formatted_day = f"{day_num:02d}"
                
                problem_name = day_problem_map.get(day_num, f"Problem_{formatted_day}")
                clean_name = clean_problem_name(problem_name)
                
                new_filename = f"{year}-{month_num}-{formatted_day}_{clean_name}.py"
                src_path = os.path.join(folder_path, py_file)
                dst_path = os.path.join(target_dir, new_filename)
                
                shutil.copy2(src_path, dst_path)
                count += 1
                if count % 100 == 0:
                    print(f"Processed {count} files...")

                if count % 100 == 0:
                    print(f"Processed {count} files...")

def process_antilneeraj():
    global count
    raw_dir = os.path.join(os.path.dirname(source_dir), "GfG_Raw_AntilNeeraj", "POTD Solutions")
    if not os.path.exists(raw_dir):
        print(f"AntilNeeraj directory not found: {raw_dir}")
        return

    print(f"Scanning {raw_dir}...")
    for filename in os.listdir(raw_dir):
        # Format: DD_MM_YYYY_ProblemName.py
        match = re.match(r"(\d{2})_(\d{2})_(\d{4})_(.*)\.py", filename)
        if match:
            day, month, year, problem_part = match.groups()
            clean_name = clean_problem_name(problem_part)
            new_filename = f"{year}-{month}-{day}_{clean_name}.py"
            
            src_path = os.path.join(raw_dir, filename)
            dst_path = os.path.join(target_dir, new_filename)
            
            shutil.copy2(src_path, dst_path)
            count += 1
            if count % 100 == 0:
                print(f"Processed {count} files...")

process_antilneeraj()
print(f"Total files processed: {count}")
