#average averge add error bar
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/kungtzuyun/Lab/ACTI/psychopy_data/behavior_analysis_data/ACIT_answer_corr_se_and_mean.csv')


df = df[df['pas_act'].isin(['p', 'a'])]


conditions = df['pas_act'].unique()


for condition in conditions:
 
    subset = df[df['pas_act'] == condition]
    if not subset.empty:
        
        trials = subset['trial']
        mean_values = subset['mean']
        se_values = subset['SE']
        

        fig, ax1 = plt.subplots()

        ax1.errorbar(trials, mean_values, yerr=se_values, marker='o', color = 'red' if condition == 'a' else 'blue', label='Mean', capsize=5)

        ax1.set_xlabel('Trial')
        ax1.set_ylabel('Mean Reaction Time')

        ax1.set_ylim(0, 1)
        ax1.set_yticks([i / 10 for i in range(11)])

        plt.title(f"Condition: {condition}")
        fig.tight_layout()
        fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
        
  
        outpath = f'/Users/kungtzuyun/Lab/ACTI/psychopy_data/behavior_analysis_data/pics/ans_rt_{condition}_plot.png'
        plt.savefig(outpath, dpi=300)
        plt.show()
