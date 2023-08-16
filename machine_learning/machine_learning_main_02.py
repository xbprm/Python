import numpy as np
import pandas as pd
from sklearn import linear_model, preprocessing
from sklearn.model_selection import train_test_split

# Load the data from a comma-separated values file into a DataFrame
df = pd.read_csv('data.csv')

# Get some summary statistics about the numeric columns in the dataframe
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
stats = df[numeric_cols].describe().T
print("Data Summary:")
print(stats)

# Select the features (X) and target variable (y)
X = df[[col for col in df if col not in ['target']]].values
y = df['target'].values

# Normalize the data
min_max_scaler = preprocessing.MinMaxScaler()
X = min_max_scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

# Fit the model to the training data
logreg = linear_model.LogisticRegression()
logreg.fit(X_train, y_train)

# Evaluate the model on the testing data
acc = logreg.score(X_test, y_test)
print("\nAccuracy:", acc)