import pandas as pd
import os

def generate_role_user_sql():
    # Folder Configuration
    INPUT_FOLDER = "input"
    OUTPUT_FOLDER = "output"
    INPUT_FILE = "role_assignments.csv"  # Ensure your CSV matches this name
    OUTPUT_FILE = "insert_role_users.sql"
    
    # Ensure folders exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    input_path = os.path.join(INPUT_FOLDER, INPUT_FILE)
    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)

    try:
        # 1. Load data
        # Expected CSV columns: ROLENAME, ROLEUSER
        df = pd.read_csv(input_path)
        
        sql_statements = []
        errors = []

        # 2. Iterate and Validate
        for index, row in df.iterrows():
            role = str(row['ROLENAME']).strip()
            user = str(row['ROLEUSER']).strip()
            line_num = index + 2

            # Length Validation for Rolename (PeopleSoft limit)
            if len(role) > 30:
                errors.append(f"Row {line_num}: Role '{role}' exceeds 30 chars.")

            # 3. Construct the SQL based on your template
            # Template: insert into psroleuser select a.oprid,'rolename', 'N' from psoprdefn a where a.oprid in('roleuser');
            sql = (
                f"INSERT INTO PSROLEUSER SELECT a.OPRID, '{role}', 'N' "
                f"FROM PSOPRDEFN a WHERE a.OPRID IN ('{user}');"
            )
            
            sql_statements.append(sql)

        # 4. Handle Errors
        if errors:
            print("--- VALIDATION ERRORS ---")
            for err in errors:
                print(err)
            print("\nGeneration aborted. Please fix the roles listed above.")
            return

        # 5. Save to Output Folder
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("-- ROLE TO USER ASSIGNMENTS\n")
            f.write("\n".join(sql_statements))
            f.write("\n\nCOMMIT;")

        print(f"Success: SQL script generated at '{output_path}'")
        print(f"Processed {len(sql_statements)} assignments.")

    except FileNotFoundError:
        print(f"Error: Could not find {input_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    generate_role_user_sql()