import pandas as pd
from modules.config_loader import load_config
from modules.data_processor import preprocess_data
from modules.report_generator import generate_report_html

# load data
data = pd.read_csv('data/test_data/test_data.csv')

# load configuration
config = load_config('config/config.yaml')

# preprocess data (non-plot-specific)
processed_data = preprocess_data(data, config)

# generate report HTML
report_html = generate_report_html(processed_data, config)

# write report to an HTML file
output_file = 'output/report.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(report_html)

print(f"Report generated and saved to '{output_file}'.")
