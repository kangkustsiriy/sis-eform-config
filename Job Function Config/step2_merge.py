import pandas as pd
import os

def run_step():
    # --- CONFIG ---
    INPUT_FOLDER = "input"
    OUTPUT_FOLDER = "output"
    ALLNAVS_FILE = "all_navs_ownersnames.xlsx"
    ALLNAVS_TAB = "Export Worksheet"
    INTERIM_FILE = "interim_filtered_dept.csv" # The file created by Step 1

    # 1. Load the files
    df_dept_cleaned = pd.read_csv(os.path.join(OUTPUT_FOLDER, INTERIM_FILE))
    allnavs_path = os.path.join(INPUT_FOLDER, ALLNAVS_FILE)
    df_allnavs = pd.read_excel(allnavs_path, sheet_name=ALLNAVS_TAB)

    # 2. Clean AllNavs headers
    df_allnavs.columns = df_allnavs.columns.astype(str).str.strip()

    # 3. Perform Merge (The VLOOKUP)
    # We match 'Clean_NAV' from Step 1 to 'JobFunctionID' in AllNavs
    merged_df = pd.merge(
        df_dept_cleaned, 
        df_allnavs, 
        left_on='Clean_NAV', 
        right_on='TO_CHAR(A.PORTAL_NAVPATH)', 
        how='inner'
    )

    # 4. Final Output for this stage
    final_output = os.path.join(OUTPUT_FOLDER, "step2_merged_data.csv")
    merged_df.to_csv(final_output, index=False)

    print(f"Step 2 Complete. {len(merged_df)} rows successfully matched and merged.")
    print(f"Resulting file: {final_output}")