import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

full_path = 'C:\kuliah\mvc-mvp-mvvm-main\mvc-mvp-mvvm-main\mvc-mvp-mvvm\mvp_test_data.csv'
# Read data from CSV file
data = pd.read_csv(full_path)

# Define the categories and values columns
categories_columns = ['view_total', 'spin_total']
values_columns = ['time', 'memory']

# Color for the box plots
box_color = 'red'

for category_column in categories_columns:
    for value_column in values_columns:
        # Extract categories and values
        categories = data[category_column]
        values = data[value_column]

        # Group values by categories
        grouped_data = {category: [] for category in categories.unique()}
        for category, value in zip(categories, values):
            grouped_data[category].append(value)

        # Create a boxplot
        plt.figure(figsize=(12, 8))  # Adjust size as needed
        bp = plt.boxplot(grouped_data.values(), patch_artist=True, labels=grouped_data.keys(), showfliers=False,
                         boxprops=dict(color='black', facecolor=box_color), medianprops=dict(color='black'))

        # Add labels and title
        if category_column == 'view_total':
            plt.xlabel('Number of Views', fontsize=14)
            plt.title(f'Boxplot of {value_column.capitalize()} by Number of Views', fontsize=16)
        elif category_column == 'spin_total':
            plt.xlabel('Number of Spinners', fontsize=14)
            plt.title(f'Boxplot of {value_column.capitalize()} by Number of Spinners', fontsize=16)
        plt.ylabel(value_column.capitalize(), fontsize=14)

        # Add median, Q1, Q3 annotations
        for i, category in enumerate(grouped_data.keys()):
            median = np.median(grouped_data[category])
            q1 = np.percentile(grouped_data[category], 25)
            q3 = np.percentile(grouped_data[category], 75)
            plt.text(i + 1, q1 - 0.03 * np.ptp(plt.ylim()), f'Q1={int(q1)}', ha='center', va='top', fontsize=10)
            plt.text(i + 1, median - 0.01 * np.ptp(plt.ylim()), f'Median={int(median)}', ha='center', va='top', fontsize=10)
            plt.text(i + 1, q3 + 0.03 * np.ptp(plt.ylim()), f'Q3={int(q3)}', ha='center', va='bottom', fontsize=10)

        # Add average annotation with an offset
        for i, category in enumerate(grouped_data.keys()):
            avg = np.mean(grouped_data[category])
            plt.scatter(i + 1, avg, color='black', zorder=5)  # Add 'X' symbol for average
            plt.text(i + 1, avg + 0.01 * np.ptp(plt.ylim()), f'Avg={int(avg)}', ha='center', va='bottom', fontsize=10)

        # Add grid lines
        plt.grid(True, linestyle='--', alpha=0.7)

        # Save plot to a PDF file
        plt.savefig(f'plot_{category_column}_{value_column}.pdf', bbox_inches='tight', pad_inches=0.2, dpi=300, format='pdf', transparent=True)
        plt.close()  # Close the figure to avoid display in interactive environments

print("Done!")
