import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read data from CSV files
mvc_full_path = 'C:\kuliah\mvc-mvp-mvvm-main\mvc-mvp-mvvm-main\mvc-mvp-mvvm\mvc_test_data.csv'
mvp_full_path = 'C:\kuliah\mvc-mvp-mvvm-main\mvc-mvp-mvvm-main\mvc-mvp-mvvm\mvp_test_data.csv'

mvc_data = pd.read_csv(mvc_full_path)
mvp_data = pd.read_csv(mvp_full_path)

# Define the categories and values columns
categories_columns = ['view_total', 'spin_total']
values_columns = ['time', 'memory']

# Colors for the box plots
mvc_color = 'yellow'
mvp_color = 'red'

for category_column in categories_columns:
    for value_column in values_columns:
        # Extract categories and values for both datasets
        mvc_categories = mvc_data[category_column]
        mvc_values = mvc_data[value_column]
        mvp_categories = mvp_data[category_column]
        mvp_values = mvp_data[value_column]

        # Group values by categories for both datasets
        mvc_grouped_data = {category: [] for category in mvc_categories.unique()}
        mvp_grouped_data = {category: [] for category in mvp_categories.unique()}

        for category, value in zip(mvc_categories, mvc_values):
            mvc_grouped_data[category].append(value)

        for category, value in zip(mvp_categories, mvp_values):
            mvp_grouped_data[category].append(value)


        # Create a combined figure for both datasets
        plt.figure(figsize=(12, 8))  # Adjust size as needed

        # Plot MVC data
        bp_mvc = plt.boxplot(mvc_grouped_data.values(), patch_artist=True, positions=np.array(range(len(mvc_grouped_data))) * 2.0 - 0.3, widths=0.4,
                             boxprops=dict(color='black', facecolor=mvc_color), medianprops=dict(color='black'))

        # Plot MVP data
        bp_mvp = plt.boxplot(mvp_grouped_data.values(), patch_artist=True, positions=np.array(range(len(mvp_grouped_data))) * 2.0 + 0.3, widths=0.4,
                             boxprops=dict(color='black', facecolor=mvp_color), medianprops=dict(color='black'))

        # Add labels and title
        if category_column == 'view_total':
            plt.xlabel('Number of Views', fontsize=14)
            plt.title(f'Boxplot of {value_column.capitalize()} by Number of Views', fontsize=16)
        elif category_column == 'spin_total':
            plt.xlabel('Number of Spinners', fontsize=14)
            plt.title(f'Boxplot of {value_column.capitalize()} by Number of Spinners', fontsize=16)
        plt.ylabel(value_column.capitalize(), fontsize=14)
        
        plt.xticks(np.arange(0, len(mvc_grouped_data) * 2, 2), mvc_grouped_data.keys())

        # Add grid lines
        plt.grid(True, linestyle='--', alpha=0.7)

        # Calculate IQR to set y-axis limits
        all_values = np.concatenate([mvc_values, mvp_values])
        q1 = np.percentile(all_values, 25)
        q3 = np.percentile(all_values, 75)
        iqr = q3 - q1
        y_min = max(min(all_values), q1 - 1.5 * iqr)
        y_max = min(max(all_values), q3 + 1.5 * iqr)
        plt.ylim(y_min, y_max)

        # Save plot to a PDF file
        plt.savefig(f'plot_{category_column}_{value_column}.pdf', bbox_inches='tight', pad_inches=0.2, dpi=300, format='pdf', transparent=True)
        plt.close()  # Close the figure to avoid display in interactive environments

print("Done!")
