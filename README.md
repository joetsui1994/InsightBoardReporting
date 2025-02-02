# InsightBoardReporting

**InsightBoardReporting** is a command-line tool for generating HTML reports from linelist CSV files (output from InsightBoard [https://github.com/globaldothealth/InsightBoard](https://github.com/globaldothealth/InsightBoard)). The tool allows you to create detailed reports using HTML templates, apply custom filters to linelist data, compute and populate variables within templates, and generate plots.

## Table of Contents

- [InsightBoardReporting](#insightboardreporting)
  - [Table of Contents](#table-of-contents)
  - [Demo](#demo)
  - [Features](#features)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Install via pip](#install-via-pip)
  - [Usage](#usage)
    - [Command-Line Interface](#command-line-interface)
    - [Subcommands](#subcommands)
  - [Variables](#variables)
      - [Using Variables in Templates](#using-variables-in-templates)
      - [Available Variables](#available-variables)

## Demo

Check it out here: <a href="https://joetsui1994.github.io/InsightBoardReporting/" target="_blank">after applying `populate`</a>

## Features

- **Generate HTML Reports**: Create detailed reports from linelist CSV files using HTML templates.
- **Data Filtering**: Apply custom filters to linelist data to focus on specific subsets.
- **Variable Population**: Automatically compute and populate variables within HTML templates.
- **Plot Generation**: Generate plots such as time-series bar plots, spatial maps, and age-sex pyramids.
- **Customizable Templates**: Use and modify HTML templates to suit reporting needs.

## Installation

### Prerequisites

- **Python 3.11 or higher**
- **pip** package manager

### Install via pip

You can install the package directly from the repository (assuming it's hosted on GitHub):

```bash
pip install git+https://github.com/joetsui1994/InsightBoardReporting.git
```

Alternatively, if you have downloaded the source code, navigate to the root directory and install using:

```bash
pip install .
```

## Usage

The tool provides a command-line interface with three subcommands: `create`, `populate`, and `list`.

### Command-Line Interface

```bash
insightboardreporting [subcommand] [options]
```

### Subcommands

`create`

Generates an HTML report from a linelist CSV file according to the specified configuration and template.

##### Usage

```bash
insightboardreporting create --config CONFIG --linelist LINELIST --in_dir IN_DIR --out_dir OUT_DIR
```

##### Options

- `--config`: Path to the configuration file.
- `--linelist`: Path to the linelist CSV file.
- `--in_dir`: Path to the input directory containing additional files (e.g., shapefiles).
- `--out_dir`: Path to the output directory to save the generated report.
- `--populate_vars`: Populate variables in the HTML file before generating the report.

##### Example

```bash
insightboardreporting create \
    --config/ ./config/config.yaml \
    --linelist ./example_input/linelist.csv \
    --in_dir ./example_input \
    --out_dir ./example_output
```

`populate`

Populates variable placeholders in an HTML file with computed values from the linelist data.

##### Usage

```bash
insightboardreporting populate --config CONFIG --linelist LINELIST --in_dir IN_DIR --out_dir OUT_DIR
```

##### Options

- `--config`: Path to the configuration file.
- `--linelist`: Path to the linelist CSV file.
- `--in_dir`: Path to the input directory containing additional files (e.g., shapefiles).
- `--out_dir`: Path to the output directory to save the populated HTML file.

##### Example

```bash
insightboardreporting populate \
    --config/ ./config/config.yaml \
    --linelist ./example_input/linelist.csv \
    --in_dir ./example_input \
    --out_dir ./example_output
```

`list`

Lists all variables that can be computed and used within templates.

##### Usage

```bash
insightboardreporting list [--json]
```

##### Options

- `--json`: Output the list of variables in JSON format.

##### Example

```bash
insightboardreporting list --json
```

## Variables

Variables are placeholders in templates that get computed and replaced with actual values from the data.

#### Using Variables in Templates

Variables can be used in templates by enclosing them in double curly braces:

```html
<p>Total number of cases in linelist: {{ total_cases }}</p>
<p>Total number of confirmed cases in linelist: {{ total_confirmed_cases }}</p>
<p>Total number of deaths in linelist: {{ total_deaths }}</p>
<p>Median age of cases in linelist: {{ median_age }}</p>
```

#### Available Variables

The following variables can be computed and used within templates:

- `total_cases`: Total number of cases (regardless of case classification) in the linelist.
- `total_deaths`: Total number of deaths in the linelist.
- `total_deaths_percentage`: Percentage of total cases that resulted in death.
- `total_confirmed_cases`: Total number of confirmed cases in the linelist.
- `total_confirmed_cases_percentage`: Percentage of total cases that are confirmed.
- `total_probable_cases`: Total number of probable cases in the linelist.
- `total_probable_cases_percentage`: Percentage of total cases that are probable.
- `total_suspected_cases`: Total number of suspected cases in the linelist.
- `total_suspected_cases_percentage`: Percentage of total cases that are suspected.
- `total_negative_cases`: Total number of negative cases in the linelist.
- `total_negative_cases_percentage`: Percentage of total cases that are negative.
- `total_unknown_cases`: Total number of unknown cases in the linelist.
- `total_unknown_cases_percentage`: Percentage of total cases that are unknown.
- `total_health_workers`: Total number of health workers among all cases in the linelist.
- `total_health_workers_percentage`: Percentage of total cases that are health workers.
- `total_sex_workers`: Total number of sex workers among all cases in the linelist.
- `total_sex_workers_percentage`: Percentage of total cases that are sex workers.
- `total_male_cases`: Total number of cases (regardless of case classification) in the linelist that are male.
- `total_male_cases_percentage`: Percentage of total cases that are male.
- `total_female_cases`: Total number of cases (regardless of case classification) in the linelist that are female.
- `total_female_cases_percentage`: Percentage of total cases that are female.
- `total_median_age`: Median age of all cases (regardless of case classification) in the linelist.
- `total_lower_quartile_age`: Lower quartile age of all cases (regardless of case classification) in the linelist.
- `total_upper_quartile_age`: Upper quartile age of all cases (regardless of case classification) in the linelist.
- `earliest_case_date`: Date of the earliest case in the linelist.
