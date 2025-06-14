import os
import pandas as pd
import glob

# Set directories and parameters
mainDir = "~/Lab/ACTI/psychopy_data"
behDir = "~/Lab/ACTI/psychopy_data"
subjectID = "A006"
task_name = ["p-1", "p-2", "p-3", "a-1", "a-2", "a-3"]

# Expand user home directory paths
mainDir = os.path.expanduser(mainDir)
behDir = os.path.expanduser(behDir)

subDir = f"{subjectID}/"
for task in task_name:
    # reset working dictionary
    workDir = os.path.join(behDir, subDir)
    os.chdir(workDir)
    print(f"current dictionary: {os.getcwd()}")

    # search log
    log_pattern = f"*MRI-{task}_*.log"
    log_files = glob.glob(log_pattern)
    print(f"Task {task} : {log_pattern}, find: {log_files}")

    if not log_files:
        print(f"Not found {task}  .log, skip this task")
        continue

    log_file = log_files[0]
    print(f"Find task {task} file: {log_file}")

    # read log
    raw_log = pd.read_csv(log_file, delimiter='\t', header=None)
    raw_log.columns = ["raw_time", "type", "event"]

    # Get MRI start time
    mri_start = raw_log[raw_log['event'] == "Keypress: 5"]['raw_time'].iloc[0]


    #Process observation_only_time
    s_obs = raw_log[raw_log['event'] == "observation_only_time: autoDraw = True"]['raw_time'].drop_duplicates() - mri_start
    e_obs = raw_log[raw_log['event'] == "observation_only_time: autoDraw = False"]['raw_time'].drop_duplicates() - mri_start
    if len(e_obs) == 2 * len(s_obs):
        e_obs = e_obs.iloc[::2]
    elif len(e_obs) != len(s_obs):
        print(f"Error：Task {task}，s_obs length {len(s_obs)}，e_obs length {len(e_obs)}")
        continue
    d_obs = e_obs.values - s_obs.values
    s_obs = s_obs.reset_index(drop=True)
    e_obs = e_obs.reset_index(drop=True)
    d_obs = pd.Series(d_obs, name='dur_observation_time')
     	

    # Process choose_combination_time
    s_chc = raw_log[raw_log['event'] == "choose_combination_time: autoDraw = True"]['raw_time'].drop_duplicates() - mri_start
    e_chc = raw_log[raw_log['event'] == "choose_combination_time: autoDraw = False"]['raw_time'].drop_duplicates() - mri_start
    d_chc = e_chc.values - s_chc.values
    s_chc = s_chc.reset_index(drop=True)
    e_chc = e_chc.reset_index(drop=True)
    d_chc = pd.Series(d_chc, name='dur_choose_combination_time')

    # Process choose_answer_time
    s_cha = raw_log[raw_log['event'] == "choose_answer_time: autoDraw = True"]['raw_time'].drop_duplicates() - mri_start
    e_cha = raw_log[raw_log['event'] == "choose_answer_time: autoDraw = False"]['raw_time'].drop_duplicates() - mri_start
    d_cha = e_cha.values - s_cha.values
    s_cha = s_cha.reset_index(drop=True)
    e_cha = e_cha.reset_index(drop=True)
    d_cha = pd.Series(d_cha, name='dur_choose_answer_time')

    # Process feedback_ans_time
    s_fb = raw_log[raw_log['event'] == "feedback_ans_time: autoDraw = True"]['raw_time'].drop_duplicates() - mri_start
    e_fb = raw_log[raw_log['event'] == "feedback_ans_time: autoDraw = False"]['raw_time'].drop_duplicates() - mri_start
    d_fb = e_fb.values - s_fb.values
    s_fb = s_fb.reset_index(drop=True)
    e_fb = e_fb.reset_index(drop=True)
    d_fb = pd.Series(d_fb, name='dur_feedback_ans_time')

    # Process test_question_time
    s_test = raw_log[raw_log['event'] == "test_question_time: autoDraw = True"]['raw_time'].drop_duplicates() - mri_start
    e_test = raw_log[raw_log['event'] == "test_question_time: autoDraw = False"]['raw_time'].drop_duplicates() - mri_start
    if len(s_test) > len(e_test):
        s_test = s_test.iloc[:len(e_test)]
    d_test = e_test.values - s_test.values
    s_test = s_test.reset_index(drop=True)
    e_test = e_test.reset_index(drop=True)
    d_test = pd.Series(d_test, name='dur_test_question_time')

    # Process end_txt_time
    s_end = raw_log[raw_log['event'] == "end_txt: autoDraw = True"]['raw_time'].drop_duplicates() - mri_start
    e_end = raw_log[raw_log['event'] == "window1: mouseVisible = True"]['raw_time'].iloc[1:2] - mri_start
    d_end = e_end.values - s_end.values
    s_end = s_end.reset_index(drop=True)
    e_end = e_end.reset_index(drop=True)
    d_end = pd.Series(d_end, name='dur_end_txt_time')

    # Calculate trial duration (from observation start to feedback end)
    if len(s_obs) == len(e_fb):
        d_trial = e_fb.values - s_obs.values
        d_trial = pd.Series(d_trial, name='dur_trial_total_time')
 
    # Combine data
    onset_log = pd.concat([s_obs.rename('start_observation_time'), d_obs,
                           s_chc.rename('start_choose_combination_time'), d_chc,
                           s_cha.rename('start_choose_answer_time'), d_cha,
                           s_fb.rename('start_feedback_ans_time'), d_fb,
                           d_trial], axis=1)
    onset_test = pd.concat([s_test.rename('start_test_question_time'), e_test.rename('end_test_question_time'), d_test], axis=1)
    onset_end = pd.concat([s_end.rename('start_end_txt_time'), e_end.rename('end_end_txt_time'), d_end], axis=1)

    # Save to CSV files
    onset_log.to_csv(f"{subjectID}_{task}_VRIT_onset_trial.csv", index=False)
    onset_test.to_csv(f"{subjectID}_{task}_VRIT_onset_test.csv", index=False)
    onset_end.to_csv(f"{subjectID}_{task}_VRIT_onset_end.csv", index=False)