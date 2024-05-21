import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define a function to summarize the data with the corrected metrics
def summarize_data(df, time_adjustment):
    summary = df.groupby('level').agg(
        generator=('generator', 'first'),
        completion_rate=('completionPercentage', lambda x: 1 if (x == 1.0).any() else 0),
        solve_consistency=('completionPercentage', 'mean'),
        average_jumps=('numJumps', 'mean'),
        average_kills=('totalKills', 'mean'),
        average_time=('remainingTime', lambda x: (time_adjustment - (x.mean() / 1000)))
    ).reset_index()
    return summary

# Define a function to summarize data by generator
def summarize_data_by_generator(df):
    summary = {
        'completion_rate': df['completion_rate'].mean(),
        'completion_rate_std': df['completion_rate'].std(),
        'solve_consistency': df['solve_consistency'].mean(),
        'solve_consistency_std': df['solve_consistency'].std(),
        'average_jumps': df['average_jumps'].mean(),
        'average_jumps_std': df['average_jumps'].std(),
        'average_kills': df['average_kills'].mean(),
        'average_kills_std': df['average_kills'].std(),
        'average_time': df['average_time'].mean(),
        'average_time_std': df['average_time'].std()
    }
    return pd.DataFrame(summary, index=[0])

# Replace the level number with the level name
level_dict = {
    "lvl-1.txt": "lvl_1-1",
    "lvl-2.txt": "lvl_1-2",
    "lvl-3.txt": "lvl_1-3",
    "lvl-4.txt": "lvl_2-1",
    "lvl-5.txt": "lvl_3-1",
    "lvl-6.txt": "lvl_3-3",
    "lvl-7.txt": "lvl_4-1",
    "lvl-8.txt": "lvl_4-2",
    "lvl-9.txt": "lvl_5-1",
    "lvl-10.txt": "lvl_5-3",
    "lvl-11.txt": "lvl_6-1",
    "lvl-12.txt": "lvl_6-2",
    "lvl-13.txt": "lvl_6-3",
    "lvl-14.txt": "lvl_7-1",
    "lvl-15.txt": "lvl_8-1"
}

# Load and process original levels data
original_levels = pd.read_csv('original_levels.csv')
original_levels['level'] = original_levels['level'].map(level_dict)
original_levels['generator'] = original_levels['level']
original_summary = summarize_data(original_levels, 30)
original_summary = summarize_data_by_generator(original_summary)

# Load and process TOAD-GAN generated levels data
toadgan_results = pd.read_csv('toadgan_results.csv')
toadgan_summary = summarize_data(toadgan_results, 20)
toadgan_summary = summarize_data_by_generator(toadgan_summary)

# Load and process TOAD-GAN fitness-sampled levels data
toadgan_fitness_results = pd.read_csv('toadgan_fitness_results.csv')
toadgan_fitness_summary = summarize_data(toadgan_fitness_results, 20)
toadgan_fitness_summary = summarize_data_by_generator(toadgan_fitness_summary)

# Load and process LVE generated levels data
lve_results = pd.read_csv('lve_toadgan_results.csv')
lve_summary = summarize_data(lve_results, 20)
lve_summary = summarize_data_by_generator(lve_summary)

# Prepare data for plotting
methods = ['Original Levels', 'TOAD-GAN', 'TOAD-GAN Fitness', 'LVE']
metrics = ['completion_rate', 'solve_consistency', 'average_jumps', 'average_kills', 'average_time']
metric_labels = ['Completion Rate', 'Solve Consistency', 'Average Jumps', 'Average Kills', 'Average Time']
summaries = [original_summary, toadgan_summary, toadgan_fitness_summary, lve_summary]

# Collect data for each metric
data = {}
for metric in metrics:
    data[metric] = {
        'means': [summary[metric].iloc[0] for summary in summaries],
        'stds': [summary[f'{metric}_std'].iloc[0] for summary in summaries]
    }

x = np.arange(len(methods))  # the label locations
width = 0.2  # the width of the bars

# Create subplots for each metric
fig, axs = plt.subplots(len(metrics), 1, figsize=(12, len(metrics) * 6))

for i, metric in enumerate(metrics):
    means = data[metric]['means']
    stds = data[metric]['stds']
    
    rects = axs[i].bar(x, means, width, yerr=stds, capsize=5, label=metric.capitalize())
    
    # Add some text for labels, title and custom x-axis tick labels, etc.
    axs[i].set_xlabel('Generation Method')
    axs[i].set_ylabel(metric_labels[i])
    axs[i].set_title(f'{metric_labels[i]} by Generation Method')
    axs[i].set_xticks(x)
    axs[i].set_xticklabels(methods)
    axs[i].legend()

fig.tight_layout()

plt.savefig('plots/summarized_metrics_comparison.png')
plt.close()
