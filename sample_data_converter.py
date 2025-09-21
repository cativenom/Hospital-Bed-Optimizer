import pandas as pd
import random

# read in file
f=pd.read_csv("/Users/tanaliu/Downloads/healthcare_dataset.csv")

# # make an expected number of patients admitted or discharged per day
# expected_count = np.random.poisson(2, 55500)

# status for patients (either admitted or discharged) on a specific date
types = ["admission", "discharge"]

# generate random data -- randomly assigns a 'type' (admission or discharge) and expected patient count on a date
patient_status = []
for i in range(len(f)):
    row = random.choice(types)
    patient_status.append(row)

expected_count = []

for i in range(len(f)):
    row = random.randint(1, 10)
    expected_count.append(row)

# columns to keep
keep_col = ['Date of Admission','Admission Type']
new_f = f[keep_col].copy()

# add patient status and expected patient count to the CSV
new_f['Patient Status'] = patient_status
new_f['Count'] = expected_count

# write the dataframe to a csv file
new_f.to_csv("sample_data.csv", index=False)