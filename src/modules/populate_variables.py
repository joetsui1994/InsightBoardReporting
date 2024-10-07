import re
import pandas as pd
from typing import Dict


# function to compute total number of cases (all classifications)
def total_cases(data):
    return len(data)

# function to compute total number of deaths
def total_deaths(data):
    return len(data[data["case_status"] == "died"])

# function to compute total number of confirmed cases
def total_confirmed_cases(data):
    return len(data[data["case_classification"] == "confirmed"])

# function to compute total number of probable cases
def total_probable_cases(data):
    return len(data[data["case_classification"] == "probable"])

# function to compute total number of suspected cases
def total_suspected_cases(data):
    return len(data[data["case_classification"] == "suspected"])

# function to compute total number of negative cases
def total_negative_cases(data):
    return len(data[data["case_classification"] == "negative"])

# function to compute total number of unknown cases
def total_unknown_cases(data):
    return len(data[data["case_classification"] == "unknown"])

# function to compute total number of male cases (all classifications)
def total_male_cases(data):
    total_male_count = len(data[data["sex_at_birth"] == "male"])
    return total_male_count

# function to compute total number of female cases (all classifications)
def total_female_cases(data):
    total_female_count = len(data[data["sex_at_birth"] == "female"])
    return total_female_count

# function to compute total number of health workers among all cases (all classifications)
def total_health_workers(data):
    total_health_workers_count = len(data[data["health_worker"]])
    return total_health_workers_count

# function to compute total number of sex workers among all cases (all classifications)
def total_sex_workers(data):
    total_sex_workers_count = len(data[data["sex_worker"]])
    return total_sex_workers_count

# function to compute median age among all cases (all classifications)
def total_median_age(data):
    return int(data["age_years"].median())

# function to compute lower quartile age among all cases (all classifications)
def total_lower_quartile_age(data):
    return int(data["age_years"].quantile(0.25))

# function to compute upper quartile age among all cases (all classifications)
def total_upper_quartile_age(data):
    return int(data["age_years"].quantile(0.75))

# function to get date of earliest case by date of notification
def earliest_case_date(data):
    # convert notification date to datetime
    data["notification_date"] = pd.to_datetime(data["notification_date"])
    # return the minimum date
    return data["notification_date"].min().strftime("%Y-%m-%d")

# dictionary of variables that can be computed
VARIABLES: Dict[str, Dict] = {
    "total_cases": {
        "function": lambda data: total_cases(data),
        "description": "Total number of cases (regardless of case classification) in the linelist.",
    },
    "total_deaths": {
        "function": lambda data: total_deaths(data),
        "description": "Total number of deaths in the linelist.",
    },
    "total_deaths_percentage": {
        "function": lambda data: "%.2f" % (total_deaths(data) / total_cases(data) * 100),
        "description": "Percentage of total cases that resulted in death.",
    },
    "total_confirmed_cases": {
        "function": lambda data: total_confirmed_cases(data),
        "description": "Total number of confirmed cases in the linelist.",
    },
    "total_confirmed_cases_percentage": {
        "function": lambda data: "%.2f" % (total_confirmed_cases(data) / total_cases(data) * 100),
        "description": "Percentage of total cases that are confirmed.",
    },
    "total_probable_cases": {
        "function": lambda data: total_probable_cases(data),
        "description": "Total number of probable cases in the linelist.",
    },
    "total_probable_cases_percentage": {
        "function": lambda data: "%.2f" % (total_probable_cases(data) / total_cases(data) * 100),
        "description": "Percentage of total cases that are probable.",
    },
    "total_suspected_cases": {
        "function": lambda data: total_suspected_cases(data),
        "description": "Total number of suspected cases in the linelist.",
    },
    "total_suspected_cases_percentage": {
        "function": lambda data: "%.2f" % (total_suspected_cases(data) / total_cases(data) * 100),
        "description": "Percentage of total cases that are suspected.",
    },
    "total_negative_cases": {
        "function": lambda data: total_negative_cases(data),
        "description": "Total number of negative cases in the linelist.",
    },
    "total_negative_cases_percentage": {
        "function": lambda data: "%.2f" % (total_negative_cases(data) / total_cases(data) * 100),
        "description": "Percentage of total cases that are negative.",
    },
    "total_unknown_cases": {
        "function": lambda data: total_unknown_cases(data),
        "description": "Total number of unknown cases in the linelist.",
    },
    "total_unknown_cases_percentage": {
        "function": lambda data: "%.2f" % (total_unknown_cases(data) / total_cases(data) * 100),
        "description": "Percentage of total cases that are unknown.",
    },
    "total_health_workers": {
        "function": lambda data: total_health_workers(data),
        "description": "Total number of health workers among all cases in the linelist.",
    },
    "total_health_workers_percentage": {
        "function": lambda data: "%.2f" % (total_health_workers(data) / total_cases(data) * 100),
        "description": "Percentage of total cases that are health workers.",
    },
    "total_sex_workers": {
        "function": lambda data: total_sex_workers(data),
        "description" : "Total number of sex workers among all cases in the linelist.",
    },
    "total_sex_workers_percentage": {
        "function": lambda data: "%.2f" % (total_sex_workers(data) / total_cases(data) * 100),
        "description": "Percentage of total cases that are sex workers.",
    },
    "total_male_cases": {
        "function": lambda data: total_male_cases(data),
        "description": "Total number of cases (regardless of case classification) in the linelist that are male.",
    },
    "total_male_cases_percentage": {
        "function": lambda data: "%.2f" % (total_male_cases(data) / total_cases(data) * 100),
        "description": "Percentage of total cases that are male.",
    },
    "total_female_cases": {
        "function": lambda data: total_female_cases(data),
        "description": "Total number of cases (regardless of case classification) in the linelist that are female.",
    },
    "total_female_cases_percentage": {
        "function": lambda data: "%.2f" % (total_female_cases(data) / total_cases(data) * 100),
        "description": "Percentage of total cases that are female.",
    },
    "total_median_age": {
        "function": lambda data: total_median_age(data),
        "description": "Median age of all cases (regardless of case classification) in the linelist.",
    },
    "total_lower_quartile_age": {
        "function": lambda data: total_lower_quartile_age(data),
        "description": "Lower quartile age of all cases (regardless of case classification) in the linelist.",
    },
    "total_upper_quartile_age": {
        "function": lambda data: total_upper_quartile_age(data),
        "description": "Upper quartile age of all cases (regardless of case classification) in the linelist.",
    },
    "earliest_case_date": {
        "function": lambda data: earliest_case_date(data),
        "description": "Date of the earliest case in the linelist.",
    },
}

def find_and_replace(html, data, extra_vars={}) -> str:
    # regular expression to match variables enclosed in {{ }}
    pattern = re.compile(r"{{\s*(\w+)\s*}}")

    # initialize a counter for the number of replacements
    replacements_count = 0

    # function to replace each variable with its computed value
    def replace_variable(match):
        nonlocal replacements_count  # ensure we can modify the outer variable
        variable_name = match.group(1)
        # check if the variable is extra_vars
        if variable_name in extra_vars:
            replacements_count += 1
            return str(extra_vars[variable_name])
        # check if the variable is in the VARIABLES dictionary
        if variable_name in VARIABLES:
            # compute the value using the associated function
            value = VARIABLES[variable_name]["function"](data)
            replacements_count += 1
            return str(value)
        else:
            return f"{{{{ {variable_name} }}}}"  # leave it as is if not found

    # populate all variables in the HTML with computed values
    updated_html = pattern.sub(replace_variable, html)

    return updated_html, replacements_count