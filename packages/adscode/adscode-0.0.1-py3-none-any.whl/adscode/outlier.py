def outlier():
    str = '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN

# Load the dataset
data = pd.read_csv('/content/drive/MyDrive/Sem 8/ADS/Bengaluru_House_Data.csv')

# Display the first few rows of the dataset
print(data.head())

# Drop irrelevant columns
data = data.drop(["area_type", "availability", "location", "size", "society"], axis=1)

# Drop rows with missing values
data = data.dropna()

# Function to convert total_sqft to numeric (handling different formats)
def convert_to_numeric(x):
    try:
        return float(x)
    except:
        tokens = x.split('Sq. Meter')
        if len(tokens) == 2:
            return float(tokens[0]) * 10.764 # Convert Sq. Meter to Sq. ft
        else:
            return np.nan

# Convert total_sqft to numeric
data['total_sqft'] = data['total_sqft'].apply(convert_to_numeric)
data.head()

# Drop rows with missing or NaN values
data = data.dropna()

# Standardize the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Isolation Forest
iso_forest = IsolationForest(contamination=0.1)
iso_forest.fit(data_scaled)
outliers_iso = iso_forest.predict(data_scaled)

# DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
outliers_dbscan = dbscan.fit_predict(data_scaled)

# Visualize outliers
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.scatter(data_scaled[:,0], data_scaled[:,1], c=outliers_iso, cmap='coolwarm')
plt.title('Isolation Forest Outlier Detection')
plt.xlabel('Scaled Total Sqft')
plt.ylabel('Scaled Price')

plt.subplot(1, 2, 2)
plt.scatter(data_scaled[:,0], data_scaled[:,1], c=outliers_dbscan, cmap='coolwarm')
plt.title('DBSCAN Outlier Detection')
plt.xlabel('Scaled Total Sqft')
plt.ylabel('Scaled Price')

plt.tight_layout()
plt.show()
    '''
    return str