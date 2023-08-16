import pandas as pd

# Load data from a csv file
data = pd.read_csv('data.csv')

# Get some basic correlation and statistics
data.corr()
data.describe()

# Prepare the training and test sets
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Train a model
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Use a machine learning model
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
model.score(X_test, y_test)