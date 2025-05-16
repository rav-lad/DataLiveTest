import pandas as pd
import matplotlib.pyplot as plt

data = {
    'name': ['Alice', 'Bob', 'Carol'],
    'age': [23, 30, 28],
    'score': [89.5, 76.0, 91.2]
}

df = pd.DataFrame(data)

plt.hist(df['age'], bins=3, edgecolor='black')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Age Distribution')
plt.show()