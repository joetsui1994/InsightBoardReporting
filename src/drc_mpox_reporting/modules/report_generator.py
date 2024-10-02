from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from drc_mpox_reporting.modules.plot_creator import create_plot

REPORT_ROOT_FOLDER = Path(__file__).parent.parent


def create_section(section_config, data):
    section_type = section_config["type"]

    # text blocks
    if section_type == "text":
        parameters = section_config.get("parameters", {})
        content = parameters.get("content", "")
        text_color = parameters.get("text_color", "black")
        font_size = parameters.get("font_size", "16px")
        font_weight = parameters.get("font_weight", "normal")

        # return a dict that contains HTML for text
        return {
            "type": "text",
            "html": f'<p class="markdown" contenteditable="true" style="color:{text_color}; font-size:{font_size}; font-weight:{font_weight};">{content}</p>',
        }

    # plots
    elif section_type in [
        "time-series-barplot",
        "multi-province-time-series-barplot",
        "province-map",
        "multi-week-province-map",
        "age-sex-pyramid-plot",
        "multi-province-age-sex-pyramid-plot",
        "zone-sante-map",
        "multi-week-zone-sante-map",
    ]:
        plot_html = create_plot(data, section_config)

        # return the plot as a dictionary with type 'plot'
        return {"type": "plot", "html": plot_html}

    # horizontal line (divider)
    elif section_type == "horizontal-line":
        return {
            "type": "horizontal-line",
            "html": '<hr style="border: 0; border-top: 1px solid #ccc; margin: 30px 0;">',
        }

    else:
        raise ValueError(f"Unsupported section type: {section_type}")


def generate_report_html(data, config):
    reporting = config.get("reporting", {})
    title = reporting.get("title", "Analysis Report")
    introductory_text = reporting.get("introductory_text", "")
    date = reporting.get("date", "")
    sections = reporting.get("sections", [])
    html_template = reporting.get("html_template", "")

    # HTML component for each section
    sections_html = []
    for section_config in sections:
        section_html = create_section(section_config, data)
        sections_html.append(section_html["html"])

    # set up Jinja2 template environment
    templates_folder = REPORT_ROOT_FOLDER / "templates"
    templates_folder.mkdir(exist_ok=True, parents=True)
    env = Environment(loader=FileSystemLoader(str(templates_folder)))
    # load template file
    template = env.get_template(html_template)

    # render HTML report
    report_html = template.render(
        report_title=title,
        introductory_text=introductory_text,
        date=date,
        plotly_script='<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>',
        sections_html=sections_html,
    )

    return report_html
