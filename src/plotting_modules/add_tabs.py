def generate_tabbed_html(sectionName, figures, add_title=False):
    """
    Generate HTML for a tabbed section with multiple figures.
    figures is a list of tuples, where each tuple contains fig_html and figure_name.
    """
    # HTML output
    html_output = []
    
    # start the parent div for the tab section
    html_output.append(f'<div id="{sectionName}-section" class="tab-section">')

    # generate the div for the tab buttons
    html_output.append(f'<div id="{sectionName}-tabs" class="tab">')
    
    # generate the tab buttons
    for index, (fig_html, figure_name) in enumerate(figures):
        figure_id = figure_name.replace(" ", "-")  # replace spaces with dashes for IDs
        figure_name = figure_name[0].upper() + figure_name[1:] # capitalize the first letter
        default_open = 'id="defaultOpen"' if index == 0 else ''
        active_class = ' active' if index == 0 else ''
        html_output.append(
            f'<button class="tablinks{active_class}" onclick="openTab(event, \'{figure_id}\', \'{sectionName}\')" {default_open}>{figure_name}</button>'
        )
    html_output.append('</div>')  # close the tab buttons div
    
    # generate the tab content sections
    for index, (fig_html, figure_name) in enumerate(figures):
        figure_id = figure_name.replace(" ", "-")
        display_style = ' style="display: block;"' if index == 0 else ''
        html_output.append(f'<div id="{sectionName}-{figure_id}" class="tabcontent"{display_style}>')
        html_output.append(f'    {fig_html}')
        if add_title:
            html_output.append(f'    <h3>{figure_name}</h3>')
        html_output.append('</div>')
    
    # cloase parent div for the tab section
    html_output.append('</div>')
    
    # join the HTML lines into a single string and return
    return "\n".join(html_output)
