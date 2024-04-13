def smotefn():
    str = '''
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('/content/Dataset/creditcard.csv')
data.head()

# Separate features and target variable
X = data.drop("Class", axis=1)
y = data["Class"]

# Impute missing values
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Drop rows with missing values in the target variable y
missing_indices = y[y.isnull()].index
X_imputed = np.delete(X_imputed, missing_indices, axis=0)
y = y.dropna()

# Visualize class distribution after SMOTE
plt.figure(figsize=(8, 6))
sns.countplot(x="Class", data=data)
plt.title("Class Distribution Before SMOTE")
plt.xlabel("Class")
plt.ylabel("Count")
plt.show()

# Apply SMOTE
smote = SMOTE()
X_smote, y_smote = smote.fit_resample(X_imputed, y)

# Concatenate original and synthetic data
synthetic_data = pd.DataFrame(X_smote, columns=X.columns)
synthetic_data["Class"] = y_smote

# Print basic information about the synthetic dataset
print("Basic information about the synthetic dataset:")
print(synthetic_data.info())

# Check class distribution after SMOTE
print("Class distribution after SMOTE:")
print(y_smote.value_counts())

# Visualize class distribution after SMOTE
plt.figure(figsize=(8, 6))
sns.countplot(x="Class", data=synthetic_data)
plt.title("Class Distribution After SMOTE")
plt.xlabel("Class")
plt.ylabel("Count")
plt.show()
    '''
    return str

