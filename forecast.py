import pandas as pd 
from prophet import Prophet

df = pd.read_csv('sample_data.csv')

# convert admission date column to type datetime
df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])

# eename columns to Prophet format
df = df.rename(columns={
    'Date of Admission': 'ds',
    'Expected Admission Length': 'y'
})

# instantiating a new Prophet object
m = Prophet()
m.fit(df)

# predictions made into a dataframe that forecasts 7 days into the future based on column 'ds' from df
future = m.make_future_dataframe(periods=7)
future.tail()

forecast = m.predict(future)
print(forecast)