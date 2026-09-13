# Structure-Property Model of Additively Manufactured Ti64

## Introduction

Given the phase fractions and lamellar thickness of an Additively Manufactured Ti64 microstructure, this code yields the elasto-plastic properties of the given microstructure.

![image](https://github.com/user-attachments/assets/98ec1781-37c0-4ad9-9a7c-5c56719e981c)

The model used consists of a Reduced Order Model (ROM) of Crystal Plasticity (CP) FFT simulations with Damask. Using a ROM allows to obtain the solutions instantly without having to run expensive CP simulations.

The ROM interpolates a structure-property database generated with Crystal Plasticity simulations of 96 different combinations of microstructural parameters.

The module with the methods to run the model is found in ./SP_Ti64AM_ROM.

In case of interest, the code used to create the regression model from the database is in "./Model_Creation/Create_model.py"

The database is saved in "./Model_Creation/microstructures_object_array_final.mat"

A jupyter notebook with data analysis of the database can be found in "./Model_Creation/Data_analysis_and_interpolation_study.ipynb"

The code to generate the database using CP simulations can be found in: https://github.com/lreigbua/Generate_Ti64_PBF_Property_Database_with_Damask

## How to run example

```bash
# Download repository and build
git clone https://github.com/lreigbua/Ti64AM_structure_property_ROM.git
cd Ti64AM_structure_property_ROM
pip install -e .

#Go to example folder
cd examples

#Run python script
python example.py
```

## Citation & Documentation

If you use this code in your research, please cite the foundational doctoral thesis. The full text also serves as the primary documentation for this repository, containing comprehensive details on the computational model's theoretical background, architecture, and validation.

**DOI:** [10.48730/pkpm-t966](https://doi.org/10.48730/pkpm-t966)

```bibtex
@phdthesis{reigbuades2026,
  author       = {Reig Buades, Luis Miguel},
  title        = {An integrated process-structure-property-performance modelling framework for additive layer manufacturing of Ti-6Al-4V},
  school       = {University of Strathclyde},
  year         = {2026},
  doi          = {10.48730/pkpm-t966},
  url          = {[https://doi.org/10.48730/pkpm-t966](https://doi.org/10.48730/pkpm-t966)}
}
```
