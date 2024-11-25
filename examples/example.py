import numpy as np

import sys
sys.path.insert(0, '../')
import SP_Ti64AM_ROM

# The input is a 2D array of microstructure parameters. Each row is a microstructure
# expressed as an array in the form (lath thickness, f_alpha, f_beta).
input = np.array([[0.4,0.33,0.09], [0.4,0,0], [1.42,0.88,0.12]])

# Calculate properties for the given inputs. This consists of loading the input array into the following function:
Properties_dict = SP_Ti64AM_ROM.Calculate_Properties(input)

# The properties are saved in a dictionary, where each key is a property that
# saves an array the given property for each microstructure array in the input 
# array in the same order
    
# Print the yield stresses in the Z direction (Building direction) 
print("Yield Stresses in BD:",Properties_dict['yield_stress_ZZ'])

# Print the young modulus in the X direction (horizontal direction) 
print("Young Modulus in X:",Properties_dict['Ex'])

# Print the hardining behavior for the first microstructure in the input array, the hardening is saved as a 2D numpy array where the 
# rows are the microstructures and the columns are the hardening stresses at different plastic strains
print("Hardening for the first microstructure:",Properties_dict['sigma_0'][0,:])

# Print the plastic strains at which the hardening stresses are calculated:
print("Plastic Strains:",Properties_dict['strain_0']) # These are the same for all microstructures

# Print the entire dictionary:
# print(Properties_dict)