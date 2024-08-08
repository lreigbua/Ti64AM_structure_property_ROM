import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.datasets import fetch_california_housing


# Load the California housing dataset
california = fetch_california_housing()
df = pd.DataFrame(california.data, columns=california.feature_names)
df['PRICE'] = california.target

# Select appropriate features from the dataset
# Assuming you want to use features like 'MedInc' (median income), 'HouseAge', and 'AveRooms' (average rooms)
X = df[['MedInc', 'HouseAge', 'AveRooms']].values
y = df['PRICE'].values


# Polynomial features
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
print(X_poly[0])

# Linear Regression model
model = LinearRegression()
model.fit(X_poly, y)

# New data with median income, house age, and average number of rooms
new_data = np.array([[3, 20, 5]])  # Example values for median income, house age, and average rooms
new_data_poly = poly.transform(new_data)
print(new_data_poly)


# Predicting the price
predicted_price = model.predict(new_data_poly)
print(predicted_price)