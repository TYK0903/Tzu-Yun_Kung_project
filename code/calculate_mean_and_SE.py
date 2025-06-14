#calculate se
import pandas as pd
import numpy as np


data = pd.read_csv("/Users/kungtzuyun/Lab/ACTI/psychopy_data/behavior_analysis_data/ACIT_all_clean_modified.csv")


data = data[data['pas_act'].isin(['p', 'a'])]


grouped = data.groupby(['trial', 'pas_act'])['answer_corr']
results = grouped.agg(
    mean='mean',
    n='count',
    sd='std'
)
results['SE'] = results['sd'] / np.sqrt(results['n'])


results.to_csv('ACIT_answer_corr_se_and_mean.csv')