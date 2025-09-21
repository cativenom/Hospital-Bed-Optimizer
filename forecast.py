import pandas as pd 
from prophet import Prophet

df = pd.read_csv('sample_data.csv')

# convert admission date column to type datetime
df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])

# rename columns to Prophet format
df = df.rename(columns={
    'Date of Admission': 'ds',
    'Count': 'y'
    })

# calculate net changes: +1 if patient admitted, -1 if patient discharged
df["net"] = df.apply(
    "net" row: row["Count"] if row["Type"].lower() == "admission" else -row["Count"],
    axis=1
    )

# aggregate net changes per type per day
daily_net_changes = df.groupby(["ds", "Type"])["net"].sum().reset_index()

# starts with a base level occupancy (starting number of patients occupying a bed on any given day without
# having made changes yet) and simulates running total of patients for each admission type

base_occupancy = 20
types_forecast = []

for type in daily_net_changes['Admission Type'].unique():
    # gives us the time series of net admissions/discharges for a specific admission type
    type_df = daily_net_changes[daily_net_changes['Admission Type'] == type].copy()

    # ensures that there’s one row for every single day, even if there are no events on that day b/c Prophet needs a 
    # continuous time series
    type_df = type_df.set_index("ds").asfreq("D", fill_value=0).reset_index()

    # calculates the running total of patients over time by adding the net changes in admitted patients over time to the base occupancy
    type_df["occupancy"] = type_df["net"].cumsum() + base_occupancy


df["admission_type"] = type




# instantiating a new Prophet object
m = Prophet()
m.fit(df)

# predictions made into a dataframe that forecasts 7 days into the future based on column 'ds' from df
future = m.make_future_dataframe(periods=7)
future.tail()

forecast = m.predict(future)
print(forecast)

