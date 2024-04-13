def performance_supervised():
    str = '''
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load the dataset
# Assuming the dataset is named 'consumer_reviews.csv'
data = pd.read_csv('/content/1429_1.csv')

# Display the first few rows of the dataset to understand its structure
data.head()

data.dtypes

data.shape

data.isnull().sum()

# Handling missing values
# Fill missing values for categorical features with mode
categorical_features = ['name', 'asins', 'reviews.date', 'reviews.dateAdded', 'reviews.didPurchase', 'reviews.username']
for feature in categorical_features:
    data[feature].fillna(data[feature].mode()[0], inplace=True)

# Fill missing values for numerical features with median
numerical_features = ['reviews.numHelpful', 'reviews.rating']
for feature in numerical_features:
    data[feature].fillna(data[feature].median(), inplace=True)

# Drop columns with a high number of missing values or not relevant for analysis
data.drop(columns=['reviews.id', 'reviews.userCity', 'reviews.userProvince'], inplace=True)

# Feature Engineering
# Extract year and month from reviews.date
data['reviews.date'] = pd.to_datetime(data['reviews.date'], errors='coerce', format='%Y-%m-%dT%H:%M:%S.%f%z')
data['reviews_year'] = data['reviews.date'].dt.year
data['reviews_month'] = data['reviews.date'].dt.month

# Drop the original 'reviews.date' column if needed
data.drop(columns=['reviews.date'], inplace=True)

# Drop rows with missing values after conversion
data.dropna(inplace=True)

# Now continue with the rest of your data preprocessing steps and modeling

# Encode categorical variables if any
label_encoders = {}
for column in data.select_dtypes(include=['object']).columns:
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])

data.isnull().sum()

# Prepare the data for supervised learning
# Assuming 'reviews.doRecommend' is the target variable
X = data.drop(columns=['reviews.doRecommend'])
y = data['reviews.doRecommend']

# Encode categorical variables if any
label_encoders = {}
for column in X.select_dtypes(include=['object']).columns:
    label_encoders[column] = LabelEncoder()
    X[column] = label_encoders[column].fit_transform(X[column])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Predict on the test set
y_pred = clf.predict(X_test)

# Evaluate the performance
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

import matplotlib.pyplot as plt
import seaborn as sns

# Distribution of ratings
plt.figure(figsize=(8, 6))
sns.countplot(x='reviews.rating', data=data)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.show()

# Distribution of recommendations
plt.figure(figsize=(6, 4))
sns.countplot(x='reviews.doRecommend', data=data)
plt.title('Distribution of Recommendations')
plt.xlabel('Recommendation')
plt.ylabel('Count')
plt.xticks(ticks=[0, 1], labels=['No', 'Yes'])
plt.show()
'''

    return str

def performance_unsupervised():
    str = '''
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Prepare the data for unsupervised learning
# Assuming we're using a subset of features for clustering
X_cluster = data[['reviews.rating', 'reviews.numHelpful']]

# Apply KMeans clustering
kmeans = KMeans(n_clusters=2)  # assuming 2 clusters for demonstration
kmeans.fit(X_cluster)

# Predict cluster labels
cluster_labels = kmeans.labels_

# Evaluate clustering performance
silhouette_score_value = silhouette_score(X_cluster, cluster_labels)
print("Silhouette Score:", silhouette_score_value)

# Plotting the clusters
plt.figure(figsize=(8, 6))
plt.scatter(X_cluster.iloc[:, 0], X_cluster.iloc[:, 1], c=cluster_labels, cmap='viridis', alpha=0.5)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker='x', c='red', s=100)
plt.title('KMeans Clustering')
plt.xlabel('Rating')
plt.ylabel('Number of Helpful Reviews')
plt.legend(['Cluster 1', 'Cluster 2', 'Cluster Centroids'])
plt.show()
'''
    
    return str

def performance_ipl_supervized():
    str = '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load the IPL dataset
# Assuming the dataset is named 'ipl_data.csv'
ipl_data = pd.read_csv('/content/ipl.csv')

ipl_data.head()
ipl_data.columns
ipl_data.shape
ipl_data.info()
ipl_data.isnull().sum()

import missingno as mn
mn.matrix(data,figsize=(12,3),color=(0.30,0.60,0.71))
plt.xlabel('Features',fontdict={'fontsize':20})
plt.ylabel("Number of Records",fontdict={'fontsize':20})
plt.title("Check Null values using visualization",fontdict={'fontsize':23})

ipl_data.drop(['mid'],axis=1,inplace=True)
ipl_data.head()

ipl_data.bat_team.unique()

playing_teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals',
                    'Mumbai Indians', 'Kings XI Punjab', 'Royal Challengers Bangalore',
                    'Delhi Daredevils', 'Sunrisers Hyderabad']

ipl_data = ipl_data[(ipl_data['bat_team'].isin(playing_teams)) & (ipl_data['bowl_team'].isin(playing_teams))]

ipl_data.shape

ipl_data.head()

ipl_data.drop(['batsman','bowler','venue'],axis=1,inplace=True)


ipl_data.drop(['striker','non-striker'],axis=1,inplace=True)

from datetime import datetime
ipl_data['date'] = ipl_data['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

ipl_data.head()

encoding_data  = pd.get_dummies(data=ipl_data,columns=['bat_team','bowl_team'])
encoding_data.shape

encoding_data.head()

X_train = encoding_data.drop(labels='total',axis=1)[encoding_data['date'].dt.year <= 2016]
X_test = encoding_data.drop(labels='total',axis=1)[encoding_data['date'].dt.year >= 2017]

Y_train = encoding_data[encoding_data['date'].dt.year <= 2016]['total'].values
Y_test = encoding_data[encoding_data['date'].dt.year >= 2017]['total'].values

Y_train = pd.DataFrame({"Total":Y_train})

Y_train.head()

Y_test = pd.DataFrame({'Total':Y_test})

Y_test.head()

X_train.drop(labels='date',axis=1,inplace=True)
X_test.drop(labels='date',axis=1,inplace=True)

from sklearn import metrics

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

lin_model = LinearRegression()
lin_model.fit(X_train,Y_train)

lin_model.score(X_train,Y_train)

lin_pred=lin_model.predict(X_test)
lin_pred

import xgboost as xg

xgmodel = xg.XGBRegressor()

xgmodel.fit(X_train,Y_train)

xgmodel.score(X_train,Y_train)

score_Prod=xgmodel.predict(X_test)

score_Prod

playing_teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals',
                    'Mumbai Indians', 'Kings XI Punjab', 'Royal Challengers Bangalore',
                    'Delhi Daredevils', 'Sunrisers Hyderabad']

ipl_data = ipl_data[(ipl_data['bat_team'].isin(playing_teams)) & (ipl_data['bowl_team'].isin(playing_teams))]

ipl_data = pd.get_dummies(ipl_data, columns=['venue', 'bat_team', 'bowl_team', 'batsman', 'bowler'])

from datetime import datetime
ipl_data['date'] = ipl_data['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

# Split the data into features (X) and target variable (y)
X = ipl_data.drop(columns=['total'])
y = ipl_data['total']

X.head()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train.drop(labels='date',axis=1,inplace=True)
X_test.drop(labels='date',axis=1,inplace=True)

# Train a Random Forest Regressor model
rf_regressor = RandomForestRegressor()
rf_regressor.fit(X_train, y_train)

# Predict on the test set
y_pred = rf_regressor.predict(X_test)

# Evaluate the performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("Mean Squared Error:", mse)
print("R2 Score:", r2)

# Visualization
# Distribution of total scores
plt.figure(figsize=(8, 6))
sns.histplot(ipl_data['total'], bins=20, kde=True)
plt.title('Distribution of Total Scores')
plt.xlabel('Total Score')
plt.ylabel('Count')
plt.show()

'''
    
    return str

def performance_webtraffic():
    str = '''
#supervised

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the dataset
data = pd.read_csv('traffic.csv')


# Randomly sample 50% of the dataset
sampled_data = data.sample(frac=0.001, random_state=42)

print("Original Dataset Shape:", data.shape)
print("Sampled Dataset Shape:", sampled_data.shape)

# Prepare the data for supervised learning
X = data.drop(columns=['event'])  # Features
y = data['event']  # Target variable

# Encode categorical variables if any
X_encoded = pd.get_dummies(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100,n_jobs=-1)
clf.fit(X_train, y_train)

# Predict on the test set
y_pred = clf.predict(X_test)

# Evaluate the performance
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

#unsupervised

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_encoded)

# Apply KMeans clustering
kmeans = KMeans(n_clusters=3)  # assuming 3 clusters for demonstration
kmeans.fit(X_scaled)

# Predict cluster labels
cluster_labels = kmeans.labels_

# Add cluster labels back to the original dataset
sampled_data['cluster'] = cluster_labels

# View the distribution of clusters
print(sampled_data['cluster'].value_counts())

'''
    
    return str