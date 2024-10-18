from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from plotting_modules.time_series_barplot import (
    preprocess as time_series_barplot_preprocess,
    plot as time_series_barplot_plot,
)
from plotting_modules.spatial_map import (
    preprocess as spatial_map_preprocess,
    plot as spatial_map_plot,
)
from plotting_modules.age_sex_pyramid import (
    preprocess as age_sex_pyramid_preprocess,
    plot as age_sex_pyramid_plot,
)
from datetime import datetime

REPORT_ROOT_FOLDER = Path(__file__).parent.parent

PLOT_TYPES = {
    "time-series-barplot": {
        "preprocess": time_series_barplot_preprocess,
        "plot": time_series_barplot_plot,
    },
    "spatial-map": {
        "preprocess": spatial_map_preprocess,
        "plot": spatial_map_plot,
    },
    "age-sex-pyramid": {
        "preprocess": age_sex_pyramid_preprocess,
        "plot": age_sex_pyramid_plot,
    },
}


def create_section(data, section, in_dir, out_dir):
    # extract section type
    section_type = section["type"]

    # empty html
    html = ""

    # text block
    if section_type == "text":
        # extract section parameters
        content = section.get("content")
        text_color = section.get("text_color", "black")
        font_size = section.get("font_size", "16px")
        font_weight = section.get("font_weight", "normal")
        underline = section.get("underline", False)

        # text html
        html = f'<p class="markdown" contenteditable="true" style="color:{text_color}; font-size:{font_size}; font-weight:{font_weight}; text-decoration:{"underline" if underline else "none"};">{content}</p>'

    # text block with bullet points
    elif section_type == "bullet-points":
        # extract section parameters
        content = section.get("content", [])
        text_color = section.get("text_color", "black")
        font_size = section.get("font_size", "16px")
        font_weight = section.get("font_weight", "normal")

        # bullet points html
        html = f'<ul style="color:{text_color}; font-size:{font_size}; font-weight:{font_weight};">'
        for point in content:
            html += f"<li>{point}</li>"
        html += "</ul>"

    # plot
    elif section_type in PLOT_TYPES:
        # preprocess the data
        preprocess = PLOT_TYPES[section_type]["preprocess"]
        plot_data = preprocess(data, section)
        # generate the plot
        plotting_config = section.get("plotting")
        # look for any parameter in the plotting config that ends in 'file'
        # and look for them in the in_dir, if found, replace the path with absolute path
        for key, value in plotting_config.items():
            if key.endswith("file"):
                plotting_config[key] = "%s/%s" % (in_dir, value)
        plot = PLOT_TYPES[section_type]["plot"]
        html = plot(plot_data, plotting_config, out_dir)

    # horizontal line (divider)
    elif section_type == "horizontal-line":
        # extract section parameters
        linewidth = section.get("linewidth", "1px")
        line_color = section.get("line_color", "#ccc")
        margin = section.get("margin", "30px 0")

        # horizontal line html
        html = (
            f'<hr style="border-top:{linewidth} solid {line_color}; margin:{margin};">'
        )

    return html


def generate_report_html(data, config, in_dir, out_dir):
    # extract report parameters
    report_title = config.get("report_title", "Analysis Report")
    introductory_text = config.get("introductory_text", "")
    report_date = config.get("report_date", datetime.now().strftime("%Y-%m-%d"))
    sections = config.get("sections", [])
    html_template = config.get("html_template")

    # HTML component for each section
    sections_html = []
    for section in sections:
        section_html = create_section(data, section, in_dir, out_dir)
        sections_html.append(section_html)

    # set up Jinja2 template environment
    templates_folder = REPORT_ROOT_FOLDER / "templates"
    templates_folder.mkdir(exist_ok=True, parents=True)
    env = Environment(loader=FileSystemLoader(str(templates_folder)))
    # load template file
    template = env.get_template(html_template)

    # render HTML report
    report_html = template.render(
        report_title=report_title,
        introductory_text=introductory_text,
        report_date=report_date,
        plotly_script='<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>',
        sections_html=sections_html,
    )

    return report_html
