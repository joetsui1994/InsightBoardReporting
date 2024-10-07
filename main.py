from pathlib import Path
import pandas as pd
import argparse
import yaml
import json

from modules.data_filtering import apply_filters
from modules.report_generator import generate_report_html
from modules.populate_variables import find_and_replace

def create_report(args):
    print(f"Creating an HTML report from the linelist file, this should just take a few seconds...")

    # load config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    # load linelist
    linelist = pd.read_csv(args.linelist)

    # load global filtering config
    filtering_config = config.get("filtering", [])
    # apply filters
    filtered_linelist = apply_filters(linelist, filtering_config)

    # load report config
    reporting_config = config.get("reporting", {})
    # generate report HTML
    report_html = generate_report_html(filtered_linelist, reporting_config, args.in_dir, args.out_dir)

    # write report to an HTML file
    output_file = Path(args.out_dir) / "report.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_html)

    print(f"Report generated and saved to '{output_file}'. Exiting...")

def populate_variables(args):
    print(f"Finding and replacing variables in the HTML file, this should just take a few seconds...")

    # load config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    # load linelist
    linelist = pd.read_csv(args.linelist)

    # get global parameters
    global_vars = config.get("parameters", {})

    # load HTML file
    with open(args.in_file, "r", encoding="utf-8") as f:
        html = f.read()

    # find and replace variables
    populated_html, replacements_count = find_and_replace(html, linelist, global_vars)

    # write populated HTML to a new file
    output_file = Path(args.out_dir) / f"{Path(args.in_file).stem}.populated.html"
    filename_counter = 1
    while output_file.exists():
        output_file = Path(args.out_dir) / f"{Path(args.in_file).stem}.populated.{filename_counter}.html"
        filename_counter += 1
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(populated_html)

    print(f"{replacements_count} variables replaced and HTML file saved to '{output_file}'. Exiting...")

def list_variables(args):
    from modules.populate_variables import VARIABLES

    # extract only variable names and descriptions
    VARIABLES = {variable: VARIABLE["description"] for variable, VARIABLE in VARIABLES.items()}

    # print
    if args.json:
        print(json.dumps(VARIABLES, indent=4))
    else:
        print("List of variables that can be computed:")
        for variable, description in VARIABLES.items():
            print(f"{variable}: {description}")

def cli():
    parser = argparse.ArgumentParser(description="Command line tool for the report generation given a linelist file in .csv format (output from InsightBoard).")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # create report
    parser_create = subparsers.add_parser('create', help='Create a report from a linelist file according to an HTML template.')
    parser_create.add_argument("--config", help="Path to the configuration file.")
    parser_create.add_argument("--linelist", help="Path to the input linelist file (.csv).")
    parser_create.add_argument("--in_dir", help="Path to the input directory (for storing any resources needed by the report, e.g., shapefiles).")
    parser_create.add_argument("--out_dir", help="Path to the output directory.")
    parser_create.add_argument("--populate_vars", action='store_true', help="Populate variables in the HTML file before generating the report.")
    parser_create.set_defaults(func=create_report)

    # populate variables
    parser_populate = subparsers.add_parser('populate', help='Populate any variable placeholders (enclosed by double curly braces) in an HTML file with corresponding values extracted from a linelist file. Any variables that cannot be computed from the linelist will be left as is.')
    parser_populate.add_argument("--config", help="Path to the configuration file.")
    parser_populate.add_argument("--linelist", help="Path to the input linelist file (.csv).")
    parser_populate.add_argument("--in_file", help="Path to the input html file, where the variables will be populated.")
    parser_populate.add_argument("--out_dir", help="Path to the output directory.")
    parser_populate.set_defaults(func=populate_variables)

    # list variables
    parser_list = subparsers.add_parser('list', help='List all variables that can be computed.')
    parser_list.add_argument("--json", action='store_true', help="Output the list of variables in JSON format, otherwise a comma-separated list in plain text.")
    parser_list.set_defaults(func=list_variables)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    cli()