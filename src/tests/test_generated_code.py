import pandas as pd
import matplotlib.pyplot as plt

# Define age bins and labels
bins = [0, 12, 18, 30, 50, 80]
labels = ['0-12', '13-18', '19-30', '31-50', '51-80']

# Create a new column for age groups
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

# Count the number of passengers in each age group
age_group_counts = df['age_group'].value_counts().sort_index()

# Plotting
plt.figure(figsize=(10, 6))
age_group_counts.plot(kind='bar', color='red')
plt.title('Passenger Age Group Distribution')
plt.xlabel('Age Group')
plt.ylabel('Number of Passengers')
plt.xticks(rotation=0)
plt.show()