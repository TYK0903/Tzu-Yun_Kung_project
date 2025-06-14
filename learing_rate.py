import pandas as pd
import statsmodels.api as sm


data = pd.read_csv("/Users/kungtzuyun/Lab/ACTI/psychopy_data/behavior_analysis_data/ACIT_all_clean_modified.csv")

data = data[['subID', 'pas_act', 'trial', 'right_wrong']]


data['trial'] = pd.to_numeric(data['trial'], errors='coerce')


grouped = data.groupby(['subID', 'pas_act'])

beta_list = []


for (subID, pas_act), group in grouped:

    X = group['trial'].dropna() 
    y = group['right_wrong'].loc[X.index]  
    

    if len(X) > 1:

        X = sm.add_constant(X)
        

        model = sm.OLS(y, X).fit()
        

        beta = model.params['trial']
        
  
        beta_list.append({'subID': subID, 'pas_act': pas_act, 'beta': beta})
    else:
        print(f"Warning: Not enough data for subID {subID} and pas_act {pas_act}")

beta_df = pd.DataFrame(beta_list)

print(beta_df)


beta_df.to_csv('learning_rate_per_pas_act.csv', index=False)