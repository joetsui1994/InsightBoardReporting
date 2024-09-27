import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import geopandas as gpd
import random

# number of cases to generate
num_cases = 10000

# generate EPI_IDs
EPI_IDs = ['EPI_{:05d}'.format(i) for i in range(1, num_cases + 1)]

# define possible values for categorical columns
province_shp_dir = '../geoBoundaries-COD-ADM1-all'
zones_sante_shp_dir = '../rdc_zones-de-sante'
aires_sante_shp_dir = '../rdc_aires-de-sante'
# read in from shapefiles
provinces = gpd.read_file(province_shp_dir).shapeISO.unique()
zones_sante = gpd.read_file(zones_sante_shp_dir).Pcode.unique()
aires_sante = gpd.read_file(aires_sante_shp_dir).PCODE.unique() # not sure if this is the right column
case_classifications = ['confirmed', 'probable', 'suspected', 'negative', 'unknown']
statuses = ['alive', 'died', 'unknown']
sexes = ['male', 'female', 'other', 'unknown']

# generate random values for categorical columns
province_values = np.random.choice(provinces, size=num_cases)
zones_sante_values = np.random.choice(zones_sante, size=num_cases)
aires_sante_values = np.random.choice(aires_sante, size=num_cases)
case_classification_values = np.random.choice(case_classifications, size=num_cases)
status_values = np.random.choice(statuses, size=num_cases)
sex_values = np.random.choice(sexes, size=num_cases)

# generate 'date_notification' within a specific date range
start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
end_date = datetime.strptime('2023-12-31', '%Y-%m-%d')
date_range_days = (end_date - start_date).days

date_notification_values = [
    (start_date + timedelta(days=random.randint(0, date_range_days))).strftime('%Y-%m-%d')
    for _ in range(num_cases)
]

# generate 'date_deceased' based on 'status'
date_deceased_values = []
for i in range(num_cases):
    if status_values[i] == 'dead':
        date_notif = datetime.strptime(date_notification_values[i], '%Y-%m-%d')
        days_after = random.randint(0, 30)  # death occurs within 30 days after notification
        date_deceased = date_notif + timedelta(days=days_after)
        if date_deceased > end_date:
            date_deceased = end_date
        date_deceased_values.append(date_deceased.strftime('%Y-%m-%d'))
    else:
        date_deceased_values.append('NA')  # NA for alive cases

# generate 'age' and 'age_months' with constraints
age_values = []
age_months_values = []

for _ in range(num_cases):
    is_infant = np.random.rand() < 0.1  # 10% chance of being 12 months old or less
    if is_infant:
        age_months = np.random.randint(0, 13)  # age in months between 0 and 12
        age_months_values.append(age_months)
        age_values.append('NA')  # NA for 'age' if age in months is provided
    else:
        age = np.random.randint(1, 100)  # age in years between 1 and 99
        age_values.append(age)
        age_months_values.append('NA')  # NA for 'age_months' if 'age' is provided

# assemble the data into a DataFrame
data = pd.DataFrame({
    'EPI_ID': EPI_IDs,
    'province': province_values,
    'zones_sante': zones_sante_values,
    'aires_sante': aires_sante_values,
    'date_notification': date_notification_values,
    'case_classification': case_classification_values,
    'status': status_values,
    'date_deceased': date_deceased_values,
    'sex': sex_values,
    'age': age_values,
    'age_months': age_months_values
})

# save the DataFrame to a CSV file
data.to_csv('./test_data.csv', index=False)