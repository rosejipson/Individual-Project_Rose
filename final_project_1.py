# -*- coding: utf-8 -*-
"""Final_Project_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WPs08zmfObuot2rV8m5gv3JxgVaFr4js
"""

# Install xlsxwriter package for Excel file handling
!pip install xlsxwriter

# Import necessary libraries
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import joblib
from bs4 import BeautifulSoup
from scipy import stats
from google.colab import drive
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder

# Mount Google Drive
drive.mount('/content/drive')

# Define the path that want to save the Excel file in Google Drive
save_path_1= '/content/drive/My Drive/Project/team_stats.xlsx'
save_path_2= '/content/drive/My Drive/Project/merged_data.xlsx'
save_path_3= '/content/drive/My Drive/Project/Full_Dataframe.xlsx'

# Define team URLs in a dictionary
team_urls = {
    "Arsenal": "https://fbref.com/en/squads/18bb7c10/2023-2024/Arsenal-Stats",
    "Manchester_City": "https://fbref.com/en/squads/b8fd03ef/2023-2024/Manchester-City-Stats",
    "Tottenham_Hotspur": "https://fbref.com/en/squads/361ca564/2023-2024/Tottenham-Hotspur-Stats",
    "Manchester_United": "https://fbref.com/en/squads/19538871/2023-2024/Manchester-United-Stats",
    "Chelsea": "https://fbref.com/en/squads/cff3d9bb/2023-2024/Chelsea-Stats",
    "Liverpool": "https://fbref.com/en/squads/822bd0ba/2023-2024/Liverpool-Stats"
}

# Function to scrape and clean all tables on the page for a given team URL
def scrape_and_clean_team_tables(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables on the page
    tables = soup.find_all('table')

    # List to store cleaned DataFrames
    cleaned_dfs = []

    # Iterate through all tables, clean and store them
    for index, table in enumerate(tables):
        # Load the table into a DataFrame
        df = pd.read_html(str(table))[0]

        # Drop the top level of multi-level columns, if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(0)

        # Rename columns if necessary
        df.columns = [col if not isinstance(col, tuple) else col[1] for col in df.columns]

        # Check if the first column contains strings before applying string methods
        if df.iloc[:, 0].dtype == 'object':
            # Remove rows with aggregate labels (like totals or headers repeated in the body)
            df = df[~df.iloc[:, 0].str.contains("Player|Squad", na=False)]

        # Reset the index to tidy up the DataFrame
        df.reset_index(drop=True, inplace=True)

        # Replace NaN values with 0
        df.fillna(0, inplace=True)

        # Add the cleaned DataFrame to the list
        cleaned_dfs.append(df)

    return cleaned_dfs

import warnings
from sklearn.exceptions import UndefinedMetricWarning
# Suppress UndefinedMetricWarning and UserWarning
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
warnings.filterwarnings("ignore", category=UserWarning)


# Dictionary to store cleaned DataFrames for each team
team_cleaned_data = {}

# Loop through each team and clean their tables
for team, url in team_urls.items():
    print(f"\nProcessing tables for {team}...\n")
    team_cleaned_data[team] = scrape_and_clean_team_tables(url)

# Combine all tables for each team into one DataFrame per team
team_combined_data = {team: pd.concat(dfs, axis=1) for team, dfs in team_cleaned_data.items()}

# Save the combined data to an Excel file with each team on a different sheet
with pd.ExcelWriter(save_path_1) as writer:
    for team, df in team_combined_data.items():
        df.to_excel(writer, sheet_name=team, index=False)

print(f"Data has been saved to '{save_path_1}'")

# Combine the tables for each team into three DataFrames: combined_df, goalkeeping_df, and goal_fix_df
combined_data = {}
goalkeeping_data = {}
scr_fix_data = {}

for team, dfs in team_cleaned_data.items():
    # Identifying goalkeeping tables by checking for specific column names
    goalkeeping_tables = []
    non_gk_tables = []
    Scr_fix_tables = []

    for df in dfs:
        if 'Save%' in df.columns or 'PSxG' in df.columns:
            goalkeeping_tables.append(df)
        elif 'Result' in df.columns or 'Date' in df.columns:
            Scr_fix_tables.append(df)
        else:
            non_gk_tables.append(df)

    # Combine the non-goalkeeping tables into one DataFrame
    if non_gk_tables:
        combined_data[team] = pd.concat(non_gk_tables, axis=1)

    # Combine the goalkeeping tables into one DataFrame
    if goalkeeping_tables:
        goalkeeping_data[team] = pd.concat(goalkeeping_tables, axis=1)

    # Combine the scores and fixtures tables into one DataFrame
    if Scr_fix_tables:
        scr_fix_data[team] = pd.concat(Scr_fix_tables, axis=1)

# Combine all teams' data into a single DataFrame for each category
combined_df = pd.concat(combined_data.values(), keys=combined_data.keys(), axis=0)
goalkeeping_df = pd.concat(goalkeeping_data.values(), keys=goalkeeping_data.keys(), axis=0)
scr_fix_df = pd.concat(scr_fix_data.values(), keys=scr_fix_data.keys(), axis=0)

# Remove duplicate columns in combined_df and goalkeeping_df
combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]
goalkeeping_df = goalkeeping_df.loc[:, ~goalkeeping_df.columns.duplicated()]

# Save the combined data to an Excel file with three sheets
with pd.ExcelWriter(save_path_2) as writer:
    combined_df.to_excel(writer, sheet_name='Combined', index=True)
    goalkeeping_df.to_excel(writer, sheet_name='Goalkeeping', index=True)
    scr_fix_df.to_excel(writer, sheet_name='Scores_and_Fixtures', index=True)

print(f"Data has been saved to '{save_path_2}'")

import seaborn as sns
import matplotlib.pyplot as plt

# Define statistics to visualize (replace with your desired columns)
stats_to_plot = ["Gls", "Ast", "Sh"]

for stat in stats_to_plot:
  # Get data for the specific statistic
  data = combined_df[stat]

  # Create the KDE plot
  sns.kdeplot(data)

  # Label the plot
  plt.xlabel(stat)
  plt.ylabel("Density")
  plt.title(f"Distribution of Player {stat}")

  # Show the plot
  plt.show()

  # Optional: Clear the plot for the next iteration
  plt.clf()

save_percentage_column = "Save%"  # Replace with the actual column name
import matplotlib.pyplot as plt

# Get the save percentage data
save_percentages = goalkeeping_df[save_percentage_column]

# Plot a histogram
plt.hist(save_percentages, bins=10, edgecolor='black')  # Adjust bins as needed
plt.xlabel(save_percentage_column)
plt.ylabel("Frequency")
plt.title("Distribution of Goalkeeper Save Percentages")
plt.grid(True)
plt.show()

goalkeeping_efficiency = goalkeeping_df.groupby(level=0).agg({
    'Save%': 'mean',
    'GA': 'sum'
})

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.bar(goalkeeping_efficiency.index, goalkeeping_efficiency['GA'], color='red', alpha=0.7, label='Goals Against')
ax1.set_xlabel('Teams')
ax1.set_ylabel('GA', color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()
ax2.plot(goalkeeping_efficiency.index, goalkeeping_efficiency['Save%'], color='blue', marker='o', label='Save Percentage')
ax2.set_ylabel('Save Percentage', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

fig.suptitle('Goalkeeping Efficiency: Save Percentage vs Goals Conceded')
plt.xticks(rotation=45)
fig.tight_layout()
plt.show()

# Summarize team performance metrics
team_performance = combined_df.groupby(level=0).agg({
    'Gls': 'sum',
    'Ast': 'sum',
    'Sh': 'sum'
})

team_performance.plot(kind='bar', figsize=(8, 4))
plt.title('Team Performance: Gls, Ast, and Sh')
plt.xlabel('Teams')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.legend(loc='upper right')
plt.show()

import seaborn as sns

# Correlation matrix of selected metrics
metrics = ['Gls', 'Ast', 'Sh', 'xG', 'Cmp', 'GA']
team_correlation = combined_df[metrics].corr()

plt.figure(figsize=(10, 6))
sns.heatmap(team_correlation, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix of Key Metrics')
plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Assuming 'Goals' and 'xG' (Expected Goals) are in combined_df
team_stats = combined_df.groupby(level=0)[['Gls', 'xG']].sum()

plt.figure(figsize=(8, 6))
plt.scatter(team_stats['xG'], team_stats['Gls'], s=100, color='teal', alpha=0.6, edgecolor='black')

# Add trendline
z = np.polyfit(team_stats['xG'], team_stats['Gls'], 1)
p = np.poly1d(z)
plt.plot(team_stats['xG'], p(team_stats['xG']), linestyle='--', color='red')

for team in team_stats.index:
    plt.text(team_stats['xG'][team] + 0.05, team_stats['Gls'][team], team, fontsize=10)

plt.title('Goals vs. Expected Goals (xG) by Teams')
plt.xlabel('Expected Goals (xG)')
plt.ylabel('Goals Scored')
plt.grid(True)
plt.show()

mean_goals = combined_df.groupby(level=0)['Gls'].mean().sort_values()

plt.figure(figsize=(8, 6))
mean_goals.plot(kind='barh', color='orchid')
plt.title('Mean Goals Scored by Team')
plt.xlabel('Mean Goals')
plt.ylabel('Team')
plt.show()

mean_goals = combined_df.groupby(level=0)['Gls'].mean()
std_goals = combined_df.groupby(level=0)['Gls'].std()

plt.figure(figsize=(10, 6))
mean_goals.plot(kind='bar', yerr=std_goals, capsize=4, color='salmon')
plt.title('Mean Goals with Error Bars')
plt.xlabel('Team')
plt.ylabel('Mean Goals')
plt.xticks(rotation=45)
plt.show()

print("Columns in combined_df before merging:")
print(combined_df.columns)

from sklearn.impute import SimpleImputer
# Step 1: Merging DataFrames with suffixes to handle overlapping columns

full_df = combined_df.join(goalkeeping_df, how='inner', lsuffix='_combined', rsuffix='_goalkeeping')
full_df = full_df.join(scr_fix_df[['Formation']], how='inner', lsuffix='', rsuffix='_scr_fix')

# Check if 'Formation' is in full_df
print("Columns in full_df after merging:")
print(full_df.columns)

# Save the DataFrame to check manually
full_df.to_excel('/content/drive/My Drive/Project/full_df_output.xlsx', index=True)
print("Full DataFrame saved for inspection.")

arsenal_combined = full_df.loc['Arsenal']

# Step 2: Feature Engineering - Selecting relevant features
# Assuming 'Formation' is in the 'scr_fix_df' and now in 'full_df'

features = full_df.drop(columns=['Formation'], axis=1)  # Drop target column from features
target = full_df['Formation']  # Target column

# Convert mixed-type columns to strings to handle mixed types
for column in features.select_dtypes(include=['object']).columns:
    features[column] = features[column].astype(str)

# Encode categorical features if any
label_encoders = {}
for column in features.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    features[column] = le.fit_transform(features[column])
    label_encoders[column] = le

# Step 3: Label Encoding for target if necessary
# If formations are categorical, encode them
target_le = LabelEncoder()
target = target_le.fit_transform(target)

# Step 5: Model Training
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV


# Step 4: Splitting the Data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Initialize the SVM model with a radial basis function (RBF) kernel
svm_model = SVC(kernel='rbf', C=1, gamma='auto')

# Perform 5-fold cross-validation
svm_cv_scores = cross_val_score(svm_model, features, target, cv=5, scoring='accuracy')

# Print the cross-validation results
svm_model.fit(X_train, y_train)
svm_cv_scores = cross_val_score(svm_model, features, target, cv=5)

print(f"SVM 5-fold Cross-Validation Accuracy: {svm_cv_scores.mean()}")

# Define the parameter grid
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1],
    'kernel': ['rbf', 'poly', 'sigmoid']
}

# Initialize the SVM model
svm_model = SVC()

# Perform grid search with cross-validation
grid_search = GridSearchCV(svm_model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(features, target)

# Get the best parameters and best score from the grid search
best_params = grid_search.best_params_
best_score = grid_search.best_score_

print(f"Best Parameters: {best_params}")
print(f"Best Cross-Validation Accuracy: {best_score}")

# Train the SVM model with the best parameters found by GridSearchCV
best_svm_model = SVC(**best_params)
best_svm_model.fit(X_train, y_train)

# Evaluate the model on the test set
svm_test_accuracy = best_svm_model.score(X_test, y_test)
print(f"SVM Test Accuracy with Best Parameters: {svm_test_accuracy}")

# Predict on the test set and print the classification report
y_pred = best_svm_model.predict(X_test)
#print("Classification Report for SVM on Test Set:")
#print(classification_report(y_test, y_pred))


# Define the scoring metrics
scoring = {
    'accuracy': 'accuracy',
    'precision': 'precision_weighted',
    'recall': 'recall_weighted',
    'f1': 'f1_weighted'
}

# Perform grid search with cross-validation and multiple metrics
grid_search = GridSearchCV(svm_model, param_grid, cv=5, scoring=scoring, refit='accuracy')
grid_search.fit(features, target)

# Get the best parameters and the corresponding scores
best_params = grid_search.best_params_
best_score = grid_search.best_score_
best_results = grid_search.cv_results_

print(f"Best Parameters: {best_params}")
print(f"Best Cross-Validation Accuracy: {best_score}")


# Print other metrics
print(f"Precision: {best_results['mean_test_precision'][grid_search.best_index_]}")
print(f"Recall: {best_results['mean_test_recall'][grid_search.best_index_]}")
print(f"F1-Score: {best_results['mean_test_f1'][grid_search.best_index_]}")

from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score,classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_validate

# Step 4: Splitting the Data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Define the scoring metrics
scoring = {
    'accuracy': make_scorer(accuracy_score),
    'precision': make_scorer(precision_score, average='weighted'),
    'recall': make_scorer(recall_score, average='weighted'),
    'f1': make_scorer(f1_score, average='weighted')
}

# Perform cross-validation on the Random Forest model
rf_cv_results = cross_validate(rf_model, features, target, cv=5, scoring=scoring)

# Perform cross-validation on the Gradient Boosting model
gb_cv_results = cross_validate(gb_model, features, target, cv=5, scoring=scoring)

# Print the cross-validation results
print("Random Forest Cross-Validation Results:")
for metric in scoring.keys():
    print(f"{metric.capitalize()}: {rf_cv_results['test_' + metric].mean()}")

print("\nGradient Boosting Cross-Validation Results:")
for metric in scoring.keys():
    print(f"{metric.capitalize()}: {gb_cv_results['test_' + metric].mean()}")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Assuming 'full_df' is the DataFrame with all teams' data and 'Formation' as the target
arsenal_combined = full_df.loc['Arsenal']

# Step 2: Feature Engineering - Selecting relevant features
# Assuming 'Formation' is in the 'scr_fix_df' and now in 'full_df'

features = arsenal_combined.drop(columns=['Formation'], axis=1)  # Drop target column from features
target = arsenal_combined['Formation']  # Target column

# Convert mixed-type columns to strings to handle mixed types
for column in features.select_dtypes(include=['object']).columns:
    features[column] = features[column].astype(str)

# Encode categorical features if any
label_encoders = {}
for column in features.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    features[column] = le.fit_transform(features[column])
    label_encoders[column] = le

# Step 3: Label Encoding for target if necessary
# If formations are categorical, encode them
target_le = LabelEncoder()
target = target_le.fit_transform(target)

# Step 4: Splitting the Data with stratification to maintain class distribution
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42, stratify=target)

# Initialize the SVM model
best_model = SVC(kernel='rbf', C=1, gamma='auto')  # Example using SVM with RBF kernel
best_model.fit(X_train, y_train)

# Predict on the test set
y_pred = best_model.predict(X_test)

# Evaluate the model
test_accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy for Arsenal Formation Prediction: {test_accuracy}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=target_le.classes_))

# Predict the best formation for the entire Arsenal dataset
arsenal_predictions = best_model.predict(features)

# Convert the predictions back to the original formation labels
arsenal_predicted_formations = target_le.inverse_transform(arsenal_predictions)

# Add the predicted formations to the original DataFrame
arsenal_combined['Predicted_Formation'] = arsenal_predicted_formations

# Save the results to an Excel file
arsenal_combined.to_excel('/path/to/save/arsenal_predicted_formations_svm.xlsx', index=False)
print("Predicted formations for Arsenal saved to 'arsenal_predicted_formations_svm.xlsx'")