import numpy as np
from joblib import load
import time

def Calculate_Properties(input):
    
    ## Load Models and predict properties for a given microstructure,[0.4,0.33,0.,[0.4,0.33,0.09],[0.3,0.33,0.09],[0.5,0.33,0.09]09],[0.3,0.33,0.09],[0.5,0.33,0.09]
    properties = ['yield_stress_ZZ','yield_stress_XX','yield_stress_XY','yield_stress_XZ','Ex','Ez','Gxy','Gxz','Pxz','Pyx']

    pred_prop_dict = {}

    # Predict Properties
    for property in properties:

        # Load the model and the transformer
        model = load(f'../data/models_saved/{property}_model.joblib')
        poly = load(f'../data/models_saved/{property}_poly_transformer.joblib')

        # # New data
        # new_data = np.array([[0.4,0.33,0.09]])  # Example values

        # Transform the new data using the loaded transformer
        new_data_poly = poly.transform(input)

        # Use the loaded model to make a prediction
        predicted_y = model.predict(new_data_poly)

        pred_prop_dict[property] = predicted_y


    # Predict Hardening

    # Load plastic strain points from npy:
    plastic_strain_average_list = np.load('../data/plastic_strain_average_list.npy')

    shape = (len(input), len(plastic_strain_average_list))
    Hardening_2D_array = np.zeros(shape)

    for i in range(0,len(plastic_strain_average_list)):

        # Load the model and the transformer
        model = load(f'../data/models_saved/hardening_{i}_model.joblib')
        poly = load(f'../data/models_saved/{property}_poly_transformer.joblib')


        # Transform the input using the loaded transformer
        new_data_poly = poly.transform(input)

        # Use the loaded model to make a prediction
        predicted_y = model.predict(new_data_poly)
        Hardening_2D_array[:,i] = predicted_y
    
    pred_prop_dict['sigma_0'] = Hardening_2D_array

    # Save plastic_strain_average_list as a list
    pred_prop_dict['strain_0'] = plastic_strain_average_list

    return pred_prop_dict