import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.datasets import fetch_california_housing
from joblib import dump
from scipy.io import loadmat
import matplotlib.pyplot as plt

f_alpha = 1.0
f_beta = 0.0
lath_thickness = 2.7

