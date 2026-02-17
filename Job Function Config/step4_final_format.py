import pandas as pd
import os

def run_step(perm_name, descr):
    OUTPUT_FOLDER = "output"
    INPUT_FILE = "step3_final_data.csv"

    # 1. Load data from Step 3
    df = pd.read_csv(os.path.join(OUTPUT_FOLDER, INPUT_FILE))
    
    # 2. Insert new columns at the start
    df.insert(0, "Permission List Name", perm_name)
    df.insert(1, "MARKET", "GBL")
    df.insert(2, "DESCR", descr)

    # 3. Save with dynamic filename as EXCEL (.xlsx)
    # This prevents the "smushing" issue
    file_name = f"{perm_name}_for_sql.xlsx"
    final_output_path = os.path.join(OUTPUT_FOLDER, file_name)
    
    # Use to_excel instead of to_csv
    # Note: You may need to install openpyxl (pip install openpyxl)
    df.to_excel(final_output_path, index=False)
    
    print(f"Step 4 Complete: Final Excel file created as '{file_name}'")
    return final_output_path