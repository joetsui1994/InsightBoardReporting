from pathlib import Path
import pandas as pd
from drc_mpox_reporting.modules.config_loader import load_config
from drc_mpox_reporting.modules.data_processor import preprocess_data
from drc_mpox_reporting.modules.report_generator import generate_report_html

# load data
data = pd.read_csv("src/drc_mpox_reporting/data/test_data/test_data.csv")
# lowercase all columns (schema mismatch)
data.columns = data.columns.str.lower()

# load configuration
config = load_config("src/drc_mpox_reporting/config/config.yaml")

# lowercase all column names
data.columns = data.columns.str.lower()

# preprocess data (non-plot-specific)
processed_data = preprocess_data(data, config)

# generate report HTML
report_html = generate_report_html(processed_data, config)

# write report to an HTML file
output_file = Path(".") / "output" / "report.html"
output_file.parent.mkdir(exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    f.write(report_html)

print(f"Report generated and saved to '{output_file}'.")
