import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("/Users/kungtzuyun/Lab/ACTI/psychopy_data/behavior_analysis_data/ACIT_test_rt_se_and_mean.csv")


order = ["a", "p"]
df_plot = (
    df.loc[df["pas_act"].isin(order)]  
      .set_index("pas_act")            
      .loc[order]                      
)


labels    = ["Active", "Passive"]
values    = df_plot["mean"].values     
errors    = df_plot["SE"].values        
colors    = ["#F2CC98", "#A1C3F5"]     
positions = [0, 1]                      


plt.figure(figsize=(6, 6))
plt.bar(
    positions,
    values,
    yerr=errors,          
    capsize=4,            
    color=colors,    
    linewidth=0.8
)


plt.xticks(positions, labels, rotation=0)
plt.ylabel("Reaction Time (sec.)")
plt.title("Mean Response Time in Test Phase (a vs. p)")
plt.grid(axis="y", linestyle="--", alpha=0.7)
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()


plt.savefig("ACIT_test_rt_bar_with_SE.png", dpi=300)
plt.show()