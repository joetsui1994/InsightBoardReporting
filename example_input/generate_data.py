import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import geopandas as gpd
import random

# number of cases to generate
num_cases = 30000

# generate record_ids
record_ids = ["EPI_{:05d}".format(i) for i in range(1, num_cases + 1)]

# define possible values for categorical columns
loc_admin_1_shp_dir = "../geoBoundaries-COD-ADM1-all"
loc_admin_2_shp_dir = "../rdc_zones-de-sante"
loc_admin_3_shp_dir = "../rdc_aires-de-sante"
# read from geopandas dataframes
loc_admin_1_unique= gpd.read_file(loc_admin_1_shp_dir).shapeName.unique()
loc_admin_2_unique = gpd.read_file(loc_admin_2_shp_dir).Nom.unique()
loc_admin_3_unique = gpd.read_file(loc_admin_3_shp_dir).AS_.unique()
case_classifications = ["confirmed", "probable", "suspected", "negative", "unknown"]
case_status = ["alive", "died", "unknown"]
sexes = ["male", "female", "other", "unknown"]
health_worker = [True, False]
sex_worker = [True, False]

# specific to mpox
clades = ["IIa", "IIb", "Ia", "Ib"]
lineages = ["A", "A.1", "A.1.1", "A.2", "A.2.1", "A.2.3", "A.3", "B.1", "B.1.1", "B.1.10", "B.1.11", "B.1.12", "B.1.20", "B.1.22", "B.1.3", "B.1.4", "B.1.5", "B.1.6", "B.1.7", "B.1.9", "C.1", "C.1.1"]

# generate random values for categorical columns
loc_admin_1_values = np.random.choice(loc_admin_1_unique, size=num_cases)
loc_admin_2_values = np.random.choice(loc_admin_2_unique, size=num_cases)
loc_admin_3_values = np.random.choice(loc_admin_3_unique, size=num_cases)
case_classification_values = np.random.choice(case_classifications, size=num_cases)
case_status_values = np.random.choice(case_status, size=num_cases)
sex_values = np.random.choice(sexes, size=num_cases)
health_worker_values = np.random.choice(health_worker, size=num_cases)
sex_worker_values = np.random.choice(sex_worker, size=num_cases)
clade_values = np.random.choice(clades, size=num_cases)
lineage_values = np.random.choice(lineages, size=num_cases)

# generate 'date_notification' within a specific date range
start_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2023-12-31", "%Y-%m-%d")
date_range_days = (end_date - start_date).days
date_notification_values = [
    (start_date + timedelta(days=random.randint(0, date_range_days))).strftime(
        "%Y-%m-%d"
    )
    for _ in range(num_cases)
]
# generate date_of_onset based on date_notification, somewhere between 1 - 10 days after notification
date_onset_values = []
for i in range(num_cases):
    date_notif = datetime.strptime(date_notification_values[i], "%Y-%m-%d")
    days_after = random.randint(1, 10)  # onset occurs within 10 days after notification
    date_onset = date_notif + timedelta(days=days_after)
    if date_onset > end_date:
        date_onset = end_date
    date_onset_values.append(date_onset.strftime("%Y-%m-%d"))

# generate 'date_deceased' based on 'status'
date_deceased_values = []
for i in range(num_cases):
    if case_status_values[i] == "dead":
        date_notif = datetime.strptime(date_notification_values[i], "%Y-%m-%d")
        days_after = random.randint(
            0, 30
        )  # death occurs within 30 days after notification
        date_deceased = date_notif + timedelta(days=days_after)
        if date_deceased > end_date:
            date_deceased = end_date
        date_deceased_values.append(date_deceased.strftime("%Y-%m-%d"))
    else:
        date_deceased_values.append("NA")  # NA for alive cases

# generate 'age' and 'age_months' with constraints
age_values = []
age_months_values = []

for _ in range(num_cases):
    is_infant = np.random.rand() < 0.1  # 10% chance of being 12 months old or less
    if is_infant:
        age_months = np.random.randint(0, 13)  # age in months between 0 and 12
        age_months_values.append(age_months)
        age_values.append("NA")  # NA for 'age' if age in months is provided
    else:
        age = np.random.randint(1, 100)  # age in years between 1 and 99
        age_values.append(age)
        age_months_values.append("NA")  # NA for 'age_months' if 'age' is provided

# assemble the data into a DataFrame
data = pd.DataFrame(
    {
        "record_id": record_ids,
        "loc_admin_1": loc_admin_1_values,
        "loc_admin_2": loc_admin_2_values,
        "loc_admin_3": loc_admin_3_values,
        "notification_date": date_notification_values,
        "date_of_onset": date_onset_values,
        "case_classification": case_classification_values,
        "case_status": case_status_values,
        "date_of_death": date_deceased_values,
        "sex_at_birth": sex_values,
        "age_years": age_values,
        "age_months": age_months_values,
        "health_worker": health_worker_values,
        "sex_worker": sex_worker_values,
        "clade": clade_values,
        "lineage": lineage_values,
    }
)

# save the DataFrame to a CSV file
data.to_csv("./test_data.csv", index=False)
