import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.stats import poisson

# make an expected admission length
expected_stay = np.random.poisson(2, 55500)

# read in file
f=pd.read_csv("/Users/tanaliu/Downloads/healthcare_dataset.csv")

# columns to keep
keep_col = ['Age','Medical Condition','Date of Admission','Admission Type']
new_f = f[keep_col].copy()

# add expected admission length column to the csv file
new_f['Expected Admission Length'] = expected_stay

# write the dataframe to a csv file
new_f.to_csv("sample_data.csv", index=False)