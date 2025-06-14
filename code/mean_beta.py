import os
import numpy as np
import pandas as pd
from nilearn.image import load_img, mean_img
import matplotlib.pyplot as plt
import seaborn as sns


base_dir = "/Users/kungtzuyun/Lab/ACTI/first_level/"  
n_subs = 20              
n_conds = 130             
subjects = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
print(f"Find {len(subjects)} participants：{subjects}")

data = []

for sub in subjects:
    sub_dir = os.path.join(base_dir, sub)
    for cond in range(1, n_conds + 1):
        fname = f"con_{cond:04d}.nii"
        fpath = os.path.join(sub_dir, fname)
        if not os.path.exists(fpath):
            print(f"No file: {fpath}")
            continue
        
        con_img = load_img(fpath)
        values = con_img.get_fdata()
        mean_beta = np.nanmean(values[values != 0]) 
        
        data.append({
            "subject": sub,
            "condition": f"cond{cond}",
            "mean_beta": mean_beta
        })

df = pd.DataFrame(data)
df.to_csv("wholebrain_mean_activation.csv", index=False)

plt.figure(figsize=(14, 6))
sns.barplot(data=df, x="condition", y="mean_beta", ci="sd", capsize=0.1)
plt.title("Whole-brain Mean Activation per Condition")
plt.ylabel("Average Beta (All Voxels)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("mean_activation_barplot.png", dpi=300)
plt.close()


output_dir = "group_avg_maps"
os.makedirs(output_dir, exist_ok=True)

for cond in range(1, n_conds + 1):
    imgs = []
    for sub in subjects:  
        fpath = os.path.join(base_dir, sub, f"con_{cond:04d}.nii")
        if os.path.exists(fpath):
            imgs.append(load_img(fpath))
    if imgs:
        avg_img = mean_img(imgs)
        avg_img.to_filename(os.path.join(output_dir, f"group_avg_con_{cond:04d}.nii"))

print("Done!")
print("- pics：mean_activation_barplot.png")
print("- Data：wholebrain_mean_activation.csv")
print("- Average pics：group_avg_maps/*.nii")