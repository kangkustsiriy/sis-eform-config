import step1_filter
import step2_merge
import step3_lookup
import step4_final_format

def main():
    print("--- 🛠️  SECURITY BUILD CONFIGURATOR ---")
    
    # 1. Gather all inputs at the very beginning
    target_col = input("Enter Target Column (e.g., FA Manager 1): ")
    perm_list = input("Enter Permission List Name: ")
    # Description is set to match the target column name automatically
    description = target_col 
    
    print("\n🚀 Executing Pipeline...")
    print("-" * 30)

    # 2. Run the sequence
    try:
        step1_filter.run_step(target_col)
        step2_merge.run_step()
        step3_lookup.run_step()
        
        # Step 4 returns the final file path for confirmation
        final_path = step4_final_format.run_step(perm_list, description)

        print("-" * 30)
        print(f"✅ PROCESS COMPLETE!")
        print(f"Permission List: {perm_list}")
        print(f"Final Output: {final_path}")
        
    except Exception as e:
        print(f"\n❌ ERROR OCCURRED: {e}")

if __name__ == "__main__":
    main()