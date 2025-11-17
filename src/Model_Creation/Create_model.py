import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from joblib import dump
from scipy.io import loadmat

#read a matlab struct from a mat file and save it into a pd dataframe

mat = loadmat('./microstructures_object_array_final.mat')
raw_rows = mat['final_microstructure_array'][0]

column_names = raw_rows[0].dtype.names

data = []

for raw_row in raw_rows:
    row=[]
    for array in raw_row:
        if len(array[0]) == 1:
            row.append(array[0][0])
        else:
            row.append(array[0])

    data.append(row)

df =  pd.DataFrame(data, columns= column_names )

num_rows = df.shape[0]

# Separate the last 5 rows into a validation set
validation_df = df.iloc[num_rows - 6:]

# The rest of the rows go into the training set
training_df = df.iloc[:num_rows - 6]

df = training_df

df["R11"] = df["yield_stress_XX"]/df["yield_stress_ZZ"]

## Create Regression model for all independent variables and save them:
# Choose polynomial degree for polynomial multi-variate regression
polynomial_degree = 5

# Select appropriate features from the dataset
X = df[['lath_thickness','f_alpha','f_beta']].values

properties = ['yield_stress_ZZ','yield_stress_XX','yield_stress_XY','yield_stress_XZ','Ex','Ez','Gxy','Gxz','Pxz','Pyx']

for property in properties:
    y = df[property].values

    # Polynomial features
    poly = PolynomialFeatures(degree=polynomial_degree)
    X_poly = poly.fit_transform(X)

    # Linear Regression model
    model = LinearRegression()
    model.fit(X_poly, y)

    dump(model, f'./models_saved/{property}_model.joblib')
    dump(poly, f'./models_saved/{property}_poly_transformer.joblib')

hardening = df['yield_stress_hardening_ZZ'].values

for i in range(0,len(hardening[0])): #loop over all hardening values

    stress_values_this_plastic = [sub_arr[i] for sub_arr in hardening] # get stress value at this plastic strain for all microstructures
    poly = PolynomialFeatures(degree=polynomial_degree)
    X_poly = poly.fit_transform(X)

    # Linear Regression model
    model = LinearRegression()
    model.fit(X_poly, stress_values_this_plastic)

    dump(model, f'./models_saved/hardening_{i}_model.joblib')
    dump(poly, f'./models_saved/hardening_{i}_poly_transformer.joblib')


# Read Plastic Strain data and calculate average plastic strain
plastic_strain = df['plastic_strain_ZZ'].values

plastic_strain_average_list = []

for i in range(len(plastic_strain[0])):

    plastic_values_this_strain = [sub_array[i] for sub_array in plastic_strain]
    plastic_strain_average_list.append( sum(plastic_values_this_strain) / len(plastic_values_this_strain) )

# Save plastic_strain_average_list
np.save('./models_saved/plastic_strain_average_list.npy', plastic_strain_average_list)