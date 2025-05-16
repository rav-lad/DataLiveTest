import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data
data = {
    'name': ['Alice', 'Bob', 'Carol'],
    'age': [23, 30, 28],
    'score': [89.5, 76.0, 91.2]
}

# Create DataFrame
df = pd.DataFrame(data)

# Plot age distribution
plt.figure(figsize=(8, 5))
sns.histplot(df['age'], bins=5, kde=True)
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()