# Mpox Analysis and Visualization for DRC

## Project Structure

```bash
.
├── data/
│   ├── geoBoundaries-COD-ADM1-all/
│   ├── geoBoundaries-COD-ADM1-all_dissolved/
│   ├── rdc_aires-de-sante/
│   ├── rdc_zones-de-sante/
│   └── test_data/
│       ├── generate_data.py
│       └── test_data.csv
├── templates/
│   └── report_template.html
├── config/
│   └── config.yaml
├── modules/
│   ├── config_loader.py
│   ├── data_processor.py
│   ├── plot_creator.py
│   └── report_generator.py
├── plots/
│   ├── province_map/
│   │   ├── plot.py
│   │   └── preprocess.py
│   └── time_series_barplot/
│       ├── plot.py
│       └── preprocess.py
├── requirements.txt
└── .gitignore
