import pandas as pd
import os

# --- SETTINGS ---
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
DEPT_FILE = "FASO_NAVS.xlsx"
TAB_NAME = "Security Build for NAVS"  # The specific tab name
TARGET_COLUMN = "FA Manager 1" 
ALLNAVS_FILE = "all_navs_ownersnames.xlsx"
# ----------------

# 1. Load the file AND specify the tab
file_path = os.path.join(INPUT_FOLDER, DEPT_FILE)

# Added sheet_name here to point to the correct tab
df = pd.read_excel(file_path, sheet_name=TAB_NAME)

# 2. Clean headers (removes spaces from column names)
df.columns = df.columns.astype(str).str.strip()

print(f"Tab '{TAB_NAME}' loaded successfully.")
print(f"Columns found: {list(df.columns[:5])}...") # Prints first 5 columns to verify

# 3. Filter logic
try:
    # Look for 'x' in the target column
    filtered_df = df[df[TARGET_COLUMN].astype(str).str.lower().str.strip() == 'x'].copy()
    
    # 4. Split NAV_PERMS
    # Taking text to the left of the first ":"
    filtered_df['Clean_NAV'] = filtered_df['NAV_PERMS'].str.split(':').str[0].str.strip()

    # 5. Save the test output
    output_path = os.path.join(OUTPUT_FOLDER, "filter_test_result.csv")
    filtered_df[['NAV_PERMS', 'Clean_NAV', TARGET_COLUMN]].to_csv(output_path, index=False)

    print("-" * 30)
    print(f"Success! Found {len(filtered_df)} rows marked with 'x'.")
    print(f"Check the result here: {output_path}")

except KeyError as e:
    print(f"ERROR: Could not find column {e}.")
    print("Double check if the column name matches the Excel header exactly.")


# --- STEP 2: LOAD ALLNAVS AND MERGE ---

# 1. Load the Master AllNavs file
# Ensure 'allnavs.xlsx' is in your 'input' folder
allnavs_path = os.path.join(INPUT_FOLDER, ALLNAVS_FILE)
df_allnavs = pd.read_excel(allnavs_path)

# 2. Clean AllNavs headers just in case
df_allnavs.columns = df_allnavs.columns.astype(str).str.strip()

# 3. Perform the Merge
# We match 'Clean_NAV' from your first sheet to the ID column in AllNavs
# Change 'JobFunctionID' to the actual column name in your allnavs.xlsx
print("Merging with AllNavs...")
merged_df = pd.merge(
    filtered_df, 
    df_allnavs, 
    left_on='Clean_NAV', 
    right_on='TO_CHAR(A.PORTAL_NAVPATH)', 
    how='inner'
)

# 4. Save the result to the output folder to verify
merge_output_path = os.path.join(OUTPUT_FOLDER, "step2_merge_result.csv")
merged_df.to_csv(merge_output_path, index=False)

print("-" * 30)
print(f"Step 2 Success!")
print(f"Rows matched in AllNavs: {len(merged_df)}")
print(f"Verification file saved: {merge_output_path}")