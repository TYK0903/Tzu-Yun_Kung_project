import pandas as pd
from scipy.stats import ttest_rel

# Load your data (adjust path as needed)
df = pd.read_csv('/Users/kungtzuyun/Lab/ACTI/psychopy_data/behavior_analysis_data/ACIT_all_clean_modified.csv', delimiter=',')

# Check if each subject has both 'p' and 'a' conditions
pas_act_per_sub = df.groupby('subID')['pas_act'].nunique()
if (pas_act_per_sub < 2).any():
    print("Warning：participants below lack condition data：", pas_act_per_sub[pas_act_per_sub < 2].index.tolist())
else:
    print("All participants have 'p' and 'a' condition。")

# Group by 'subID' and 'pas_act', calculate mean 'test_rt'
sub_pas_test_rt = df.groupby(['subID', 'pas_act'])['test_rt'].mean().unstack()

# Extract 'test_rt' for 'p' and 'a' conditions
test_rt_p = sub_pas_test_rt['p']
test_rt_a = sub_pas_test_rt['a']

# Remove subjects with missing data
sub_pas_test_rt = sub_pas_test_rt.dropna()

# Perform paired t-test
t_stat, p_value = ttest_rel(test_rt_a, test_rt_p)

# Output results
print(f"Pair t test：t  = {t_stat:.3f}, p value = {p_value:.3f}")