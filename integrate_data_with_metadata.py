import os
import glob
import pandas as pd
import numpy as np

# Set main directory and parameters
main_dir = "/Users/kungtzuyun/Lab/ACTI/psychopy_data"
task_name = ["p-1", "p-2", "p-3", "a-1", "a-2", "a-3"]
all_data = pd.DataFrame()

# Get list of subject directories
subject_dirs = [d for d in os.listdir(main_dir) if d.startswith("B")]

# Process each subject
for subject_id in subject_dirs:
    bind_data = pd.DataFrame()
    sub_dir = os.path.join(main_dir, subject_id)
    
    # Process each task
    for task in task_name:
        # Find CSV file matching the pattern
        pattern = os.path.join(sub_dir, f"*ACTI-*{task}*.csv")
        csv_files = glob.glob(pattern)
        print(f"Subject: {subject_id}, Task: {task}, Pattern: {pattern}, Found files: {len(csv_files)}")
        if not csv_files:
            continue
        
        # Read CSV file
        raw_csv = pd.read_csv(csv_files[0], na_values=["", "NA"], keep_default_na=False)
        print(f"Columns in {csv_files[0]}: {raw_csv.columns.tolist()}")
        
        # Rename first column to QCat
        raw_csv.rename(columns={raw_csv.columns[0]: "QCat"}, inplace=True)
        
        # Define required columns
        required_columns = [
            "QCat", "Qpicksub", "colorAll", "trial.thisIndex",
            "key_resp_color_dot.keys", "key_resp_color_dot.rt",
            "key_resp_confirm.rt", "key_resp_corr_color.rt",
            "key_resp_confirm_2.rt", "key_resp_corr_color.corr",
            "key_resp_corr_color_2.keys", "key_resp_corr_color_2.corr",
            "key_resp_confirm_4.rt", "correct_answer", "chosen_ans",
            "right_wrong", "correct_combo"
        ]
        
        # Select only available required columns
        available_columns = [col for col in required_columns if col in raw_csv.columns]
        print(f"Available columns: {available_columns}")
        filter_data = raw_csv[available_columns].copy()
        print(f"filter_data shape: {filter_data.shape}")
        
        # Determine run number and passive/active indicator
        run_no = {"p-1": "1", "p-2": "2", "p-3": "3", "a-1": "1", "a-2": "2", "a-3": "3"}[task]
        pa = "p" if task.startswith("p") else "a"
        
        # Increment trial index to make it 1-based
        if "trial.thisIndex" in filter_data.columns:
            filter_data["trial.thisIndex"] += 1
        
        # Add metadata columns
        filter_data["subID"] = subject_id        # Subject ID
        filter_data["pas_act"] = pa            # p or a
        filter_data["runN"] = run_no           # Run number
        filter_data["session"] = task          # Task (e.g., p-1, a-2)
        filter_data["QuestionN"] = 0
        filter_data["QuestionALLN"] = 0
        
        # Append to subject's combined data
        bind_data = pd.concat([bind_data, filter_data], ignore_index=True)
        print(f"bind_data shape after concat: {bind_data.shape}")
    
    # Calculate QuestionN (cycles every 6) and QuestionALLN (cycles every 12)
    if not bind_data.empty and "QCat" in bind_data.columns:
        k = 1  # QuestionN counter
        j = 1  # QuestionALLN counter
        for i in range(len(bind_data)):
            bind_data.at[i, "QuestionN"] = k
            bind_data.at[i, "QuestionALLN"] = j
            if (i < len(bind_data) - 1 and 
                pd.notna(bind_data.at[i + 1, "QCat"]) and 
                bind_data.at[i + 1, "QCat"] != bind_data.at[i, "QCat"]):
                k = (k % 6) + 1
                j = (j % 12) + 1
    
    # Save subject's combined data
    subject_file = os.path.join(main_dir, f"{subject_id}_VRIT_beh.csv")
    print(f"Saving {subject_id}_VRIT_beh.csv with shape: {bind_data.shape}")
    bind_data.to_csv(subject_file, index=False)
    
    # Append to all subjects' data
    all_data = pd.concat([all_data, bind_data], ignore_index=True)
    print(f"all_data shape after concat: {all_data.shape}")

# Save all subjects' data
all_data_file = os.path.join(main_dir, "VRIT_beh_all.csv")
print(f"Saving VRIT_beh_all.csv with shape: {all_data.shape}")
all_data.to_csv(all_data_file, index=False)