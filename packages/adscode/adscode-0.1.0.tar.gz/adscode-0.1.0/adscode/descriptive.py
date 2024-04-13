def descriptive_weather():
    str = '''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset from CSV file
df = pd.read_csv('/content/seattle-weather.csv')

# Drop 'date' column for correlation calculation
df_numeric = df.drop(columns=['date'])

# Convert 'weather' column to categorical type
df_numeric['weather'] = df_numeric['weather'].astype('category')

# Encode 'weather' column with label encoding
df_numeric['weather'] = df_numeric['weather'].cat.codes

# Display the first few rows of the dataframe
print("First few rows of the dataset:")
print(df_numeric.head())

# Summary statistics
print("Summary statistics:")
print(df_numeric.describe())

# Correlation matrix
print("Correlation matrix:")
print(df_numeric.corr())


# Box plot for temperature variables
plt.figure(figsize=(10, 6))
sns.boxplot(data=df[['temp_max', 'temp_min']])
plt.title('Box Plot of Maximum and Minimum Temperature')
plt.xlabel('Temperature')
plt.ylabel('Value (°C)')
plt.show()

# Histogram of precipitation
plt.figure(figsize=(8, 6))
plt.hist(df['precipitation'], bins=10, color='skyblue', edgecolor='black')
plt.title('Histogram of Precipitation')
plt.xlabel('Precipitation (mm)')
plt.ylabel('Frequency')
plt.show()

# Bar plot of weather categories
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='weather')
plt.title('Weather Categories')
plt.xlabel('Weather')
plt.ylabel('Count')
plt.show()

# Pairplot for visualizing relationships between variables
sns.pairplot(df)
plt.show()
    '''
    return str

def descriptive_iris():
    str = '''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

# Load the Iris dataset
iris = load_iris()

# Convert to DataFrame
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)

# Add target column to DataFrame
df['species'] = iris.target

# Display the first few rows of the dataframe
print("First few rows of the dataset:")
print(df.head())

# Summary statistics
print("\nSummary statistics:")
print(df.describe())

# Correlation matrix
print("\nCorrelation matrix:")
print(df.corr())

# Box plot for feature variables
plt.figure(figsize=(10, 6))
sns.boxplot(data=df.drop(columns=['species']))
plt.title('Box Plot of Iris Features')
plt.xlabel('Features')
plt.ylabel('Value')
plt.show()

# Histogram of each feature
plt.figure(figsize=(10, 8))
for i, feature in enumerate(df.columns[:-1]):
    plt.subplot(2, 2, i+1)
    sns.histplot(df[feature], kde=True)
    plt.title(f'Histogram of var->feature. enclose in curly bracket')
    plt.xlabel(feature)
    plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Bar plot of target variable
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='species')
plt.title('Species Counts')
plt.xlabel('Species')
plt.ylabel('Count')
plt.show()

# Pairplot for visualizing relationships between features
sns.pairplot(df, hue='species')
plt.show()
'''
    return str