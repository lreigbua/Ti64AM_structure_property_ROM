import numpy as np
from joblib import load
import time
import math as m
from pathlib import Path

def Calculate_Properties(input):

    module_path = Path(__file__).resolve().parent
    
    ## Load Models and predict properties for a given microstructure,[0.4,0.33,0.,[0.4,0.33,0.09],[0.3,0.33,0.09],[0.5,0.33,0.09]09],[0.3,0.33,0.09],[0.5,0.33,0.09]
    properties = ['yield_stress_ZZ','yield_stress_XX','yield_stress_XY','yield_stress_XZ','Ex','Ez','Gxy','Gxz','Pxz','Pyx']

    pred_prop_dict = {}

    # Predict Properties
    for property in properties:

        # Load the model and the transformer
        model = load(module_path / f'models_saved/{property}_model.joblib')
        poly = load(module_path / f'models_saved/{property}_poly_transformer.joblib')

        # # New data
        # new_data = np.array([[0.4,0.33,0.09]])  # Example values

        # Transform the new data using the loaded transformer
        new_data_poly = poly.transform(input)

        # Use the loaded model to make a prediction
        predicted_y = model.predict(new_data_poly)

        pred_prop_dict[property] = predicted_y


    # Predict Hardening

    # Load plastic strain points from npy:
    plastic_strain_average_list = np.load(module_path / 'models_saved/plastic_strain_average_list.npy')

    shape = (len(input), len(plastic_strain_average_list))
    Hardening_2D_array = np.zeros(shape)

    for i in range(0,len(plastic_strain_average_list)):

        # Load the model and the transformer
        model = load(module_path / f'models_saved/hardening_{i}_model.joblib')
        poly = load(module_path / f'models_saved/hardening_{i}_poly_transformer.joblib')


        # Transform the input using the loaded transformer
        new_data_poly = poly.transform(input)

        # Use the loaded model to make a prediction
        predicted_y = model.predict(new_data_poly)
        Hardening_2D_array[:,i] = predicted_y
    
    pred_prop_dict['sigma_0'] = Hardening_2D_array

    # Save plastic_strain_average_list as a list
    pred_prop_dict['strain_0'] = plastic_strain_average_list

    return pred_prop_dict


## Takes a dictionary of elasto-plastic properties and writes material info in Abaqus inp format:
def write_inp(prop_dict, output_file = None, name = 'Material-1'):
    """
    Takes a dictionary of elasto-plastic properties and writes material info in Abaqus inp format.
    :param prop_dict: Dictionary containing material properties
    :param output_file: Output file path
    :param name: Material name
    :return: Material information in Abaqus inp format as string
    """


    #Calculate Hill Parameters from yield stresses
    sigma_0 = prop_dict['yield_stress_ZZ']
    R11 = prop_dict['yield_stress_XX']/sigma_0
    R22 = R11
    R33 = 1
    R12 = prop_dict['yield_stress_XY']/(sigma_0/m.sqrt(3))
    R13 = prop_dict['yield_stress_XZ']/(sigma_0/m.sqrt(3))
    R23 = R13

    hardening_string = ''

    # calculate e_plastic as e_plastic = e_total - sigma/Ez as requested by Abaqus.
    # prop_dict['strain_0'] is equal to e_total - e_yield, which is not Abaqus wants.
    e_plastic = prop_dict['strain_0'] - prop_dict['sigma_0']/prop_dict['Ez']
    e_plastic -= e_plastic[0]

    for i in range(len(prop_dict['strain_0'])):
        hardening_string += f"\n{prop_dict['sigma_0'][i]},{e_plastic[i]}"

    #Write Material info in Abaqus inp format:
    Material_Abaqus_text =f'''**
*Material, name={name}
*Density
 4.43e-09,
*Damage Initiation, criterion=JOHNSON COOK
 -0.09, 0.25, -0.5,   0.,   0.,   0.,   0.,   0.
*Damage Evolution, type=DISPLACEMENT
 0.1,
*Elastic, type=ENGINEERING CONSTANTS
{prop_dict['Ex']},{prop_dict['Ex']},{prop_dict['Ez']}, {prop_dict['Pyx']}, {prop_dict['Pxz']}, {prop_dict['Pxz']}, {prop_dict['Gxy']}, {prop_dict['Gxz']}
{prop_dict['Gxz']},
*Plastic{hardening_string}
*Potential
{R11}, {R22},  {R33},  {R12},  {R12},  {R23}
'''

    if output_file is not None:
        with open(output_file, 'w') as f:
            # Write the string to the file
            f.write(Material_Abaqus_text)

    return Material_Abaqus_text


