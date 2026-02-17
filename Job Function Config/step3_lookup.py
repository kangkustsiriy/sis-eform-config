import pandas as pd
import os

def run_step():
    # --- CONFIG ---
    INPUT_FOLDER = "input"
    OUTPUT_FOLDER = "output"
    ALLNAVS_FILE = "all_navs_ownersnames.xlsx"
    LOOKUP_TAB = "Auth Access"
    MERGED_FILE = "step2_merged_data.csv"

    # Columns to keep in the final file (per your screenshot)
    COLS_TO_KEEP = ['Menu', 'Menubar', 'MENUITEM2', 'Page', 'Display only', 'Actions', '7']

    # 1. Load the Lookup Table
    allnavs_path = os.path.join(INPUT_FOLDER, ALLNAVS_FILE)
    df_lookup = pd.read_excel(allnavs_path, sheet_name=LOOKUP_TAB)
    df_lookup.columns = df_lookup.columns.astype(str).str.strip()

    # Create Mapping (Force string to avoid 1.0 vs 1 issues)
    mapping = dict(zip(df_lookup['If this'].astype(str), df_lookup['Than AU'].astype(str)))

    # 2. Load Step 2 Data
    df_merged = pd.read_csv(os.path.join(OUTPUT_FOLDER, MERGED_FILE))

    # 3. Apply Mapping
    # Note: Ensure the case matches your CSV (e.g., 'Actions' vs 'ACTIONS')
    for col in ['Actions', '7']: # Adjusting to match your requested columns
        if col in df_merged.columns:
            # Clean numeric data: convert to string and remove decimals
            df_merged[col] = df_merged[col].astype(str).str.split('.').str[0].str.strip()
            df_merged[col] = df_merged[col].map(mapping).fillna(df_merged[col])

    # 4. Filter for only the requested columns
    # We wrap this in a list comprehension to avoid errors if a col is missing
    final_cols = [c for c in COLS_TO_KEEP if c in df_merged.columns]
    df_final = df_merged[final_cols]

    # 5. Save the Final Data
    final_path = os.path.join(OUTPUT_FOLDER, "step3_final_data.csv")
    df_final.to_csv(final_path, index=False)

    print("-" * 30)
    print(f"Step 3 Complete!")
    print(f"Columns preserved: {list(df_final.columns)}")
    print(f"Final data saved: {final_path}")