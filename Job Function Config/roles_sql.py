import pandas as pd
import os

def generate_role_sql():
    # Folder Configuration
    INPUT_FOLDER = "input"
    OUTPUT_FOLDER = "output"
    INPUT_FILE = "roles.csv" # Change this to your source filename
    OUTPUT_FILE = "insert_roles.sql"
    
    # Ensure folders exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    input_path = os.path.join(INPUT_FOLDER, INPUT_FILE)
    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)

    try:
        # 1. Load data
        df = pd.read_csv(input_path)
        
        defn_statements = []
        class_statements = []
        errors = []

        # 2. Iterate and Validate
        for index, row in df.iterrows():
            role = str(row['rolename']).strip()
            descr = str(row['description']).strip()
            line_num = index + 2 # Accounting for header

            # Length Validation (30 char limit)
            if len(role) > 30:
                errors.append(f"Row {line_num}: Role '{role}' is too long ({len(role)} chars)")
            if len(descr) > 30:
                errors.append(f"Row {line_num}: Description '{descr}' is too long ({len(descr)} chars)")

            # Construct PSROLEDEFN
            defn_sql = (
                f"INSERT INTO SYSADM.PSROLEDEFN values ('{role}', "
                "(SELECT VERSION FROM SYSADM.PSVERSION WHERE OBJECTTYPENAME = 'ROLM'), "
                f"'U', '{descr}', ' ', 'A', ' ', ' ', ' ', ' ', ' ', 'N', 'N', 'N', 'Y', 'Y', "
                "SYSDATE, '1940408', ' ');"
            )
            
            # Construct PSROLECLASS
            class_sql = f"INSERT INTO SYSADM.PSROLECLASS values ('{role}', '{role}');"

            defn_statements.append(defn_sql)
            class_statements.append(class_sql)

        # 3. Handle Errors
        if errors:
            print("--- VALIDATION ERRORS ---")
            for err in errors:
                print(err)
            print("\nSQL generation aborted. Please shorten strings to 30 chars or less.")
            return

        # 4. Save to Output Folder
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("-- PSROLEDEFN INSERTS\n")
            f.write("\n".join(defn_statements))
            f.write("\n\n-- PSROLECLASS INSERTS\n")
            f.write("\n".join(class_statements))
            f.write("\n\nCOMMIT;")

        print(f"Success: SQL script generated at '{output_path}'")

    except FileNotFoundError:
        print(f"Error: Could not find {input_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    generate_role_sql()