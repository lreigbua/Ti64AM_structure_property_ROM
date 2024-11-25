# Structure-Propery Model of Additively Manufactured Ti64

## Introduction

Given the phase fractions and lamellar thickness of a Ti64 microstructure, this code yields the elasto-plastic properties of the given microstructure.

![image](https://github.com/user-attachments/assets/98ec1781-37c0-4ad9-9a7c-5c56719e981c)

The model used consists of a Reduced Order Model (ROM) of Crystal Plasticity (CP) Computational Homogenization FFT simulations with Damask. Using a surrogate model allows to obtain the solutions instantly without having to run expensive CP simulations.
The ROM interpolates a structure-property database generated with Crystal Plasticity simulations of 96 different combinations of microstructural parameters.
The procedure to obtain the properties of a given microstructure using CP simulations is shown below:

![image](https://github.com/user-attachments/assets/af9a0fc4-730a-40ff-bbe4-6ae2543393d1)

