import pandas as pd
import os

def run_step(target_column):
    INPUT_FOLDER = "input"
    OUTPUT_FOLDER = "output"
    DEPT_FILE = "FASO_NAVS.xlsx"
    TAB_NAME = "Security Build for NAVS"

    file_path = os.path.join(INPUT_FOLDER, DEPT_FILE)
    df = pd.read_excel(file_path, sheet_name=TAB_NAME)
    df.columns = df.columns.astype(str).str.strip()

    filtered_df = df[df[target_column].astype(str).str.lower().str.strip() == 'x'].copy()
    filtered_df['Clean_NAV'] = filtered_df['NAV_PERMS'].str.split(':').str[0].str.strip()
    
    final_selection = filtered_df[['NAV_PERMS', target_column, 'Clean_NAV']]
    
    interim_path = os.path.join(OUTPUT_FOLDER, "interim_filtered_dept.csv")
    final_selection.to_csv(interim_path, index=False)
    print(f"Step 1 Complete: Filtered {len(final_selection)} rows for {target_column}.")