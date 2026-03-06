import pandas as pd
import os

def run_step(target_column):
    INPUT_FOLDER = "input"
    OUTPUT_FOLDER = "output"
    DEPT_FILE = "UWASC.xlsx"

    file_path = os.path.join(INPUT_FOLDER, DEPT_FILE)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # 1. Open the Excel file pointer (fast, doesn't load data yet)
    xl = pd.ExcelFile(file_path)
    
    target_df = None
    found_tab = None

    print(f"Searching for column '{target_column}' across all tabs...")

    # 2. Iterate through sheet names
    for sheet in xl.sheet_names:
        # Read only the header row (nrows=0) to check for the column
        # This is lightning fast and prevents stalling
        head = pd.read_excel(xl, sheet_name=sheet, nrows=0)
        columns = head.columns.astype(str).str.strip().tolist()

        if target_column in columns:
            print(f"🎯 Found '{target_column}' in tab: '{sheet}'")
            # 3. Found it! Now load only THIS tab
            target_df = pd.read_excel(xl, sheet_name=sheet)
            target_df.columns = target_df.columns.astype(str).str.strip()
            found_tab = sheet
            break # Stop searching other tabs

    if target_df is not None:
        # Use the stricter boolean/x check we discussed
        # Checks for 'x', 'true', or actual Boolean True
        val_as_str = target_df[target_column].astype(str).str.lower().str.strip()
        mask = (val_as_str == 'x') | (val_as_str == 'true') | (val_as_str == '1')
        
        filtered_df = target_df[mask].copy()

        if 'NAV_PERMS1' in filtered_df.columns:
            filtered_df['Clean_NAV'] = filtered_df['NAV_PERMS1'].astype(str).str.split(':').str[0].str.strip()
            
            final_selection = filtered_df[['NAV_PERMS1', target_column, 'Clean_NAV']]
            
            interim_path = os.path.join(OUTPUT_FOLDER, "interim_filtered_dept.csv")
            final_selection.to_csv(interim_path, index=False)
            print(f"Step 1 Complete: Processed tab '{found_tab}'. Filtered {len(final_selection)} rows.")
        else:
            print(f"Error: Found the column in '{found_tab}', but 'NAV_PERMS1' is missing on that tab.")
    else:
        print(f"Error: Could not find a tab containing the column '{target_column}'.")

if __name__ == "__main__":
    # Now you can call it with your specific column name
    run_step('App Programmer')