def generate_tab_html(sectionName, figure_list):
    """
    Generate HTML for a tabbed section with multiple figures.
    figure_list is a list of tuples, where each tuple contains fig_html and figure_name.
    """
    # HTML output
    html_output = []
    
    # Start the parent div for the tab section
    html_output.append(f'<div id="{sectionName}-section" class="tab-section">')

    # Generate the div for the tab buttons
    html_output.append(f'<div id="{sectionName}-tabs" class="tab">')
    
    # Generate the tab buttons
    for index, (fig_html, figure_name) in enumerate(figure_list):
        figure_id = figure_name.replace(" ", "-")  # Replace spaces with dashes for IDs
        default_open = 'id="defaultOpen"' if index == 0 else ''
        active_class = ' active' if index == 0 else ''
        html_output.append(
            f'<button class="tablinks{active_class}" onclick="openTab(event, \'{figure_id}\', \'{sectionName}\')" {default_open}>{figure_name}</button>'
        )
    html_output.append('</div>')  # Close the tab buttons div
    
    # Generate the tab content sections
    for index, (fig_html, figure_name) in enumerate(figure_list):
        figure_id = figure_name.replace(" ", "-")
        display_style = ' style="display: block;"' if index == 0 else ''
        html_output.append(f'<div id="{sectionName}-{figure_id}" class="tabcontent"{display_style}>')
        html_output.append(f'    {fig_html}')
        html_output.append(f'    <h3>{figure_name}</h3>')
        html_output.append('</div>')
    
    # Close the parent div for the tab section
    html_output.append('</div>')
    
    # Join the HTML lines into a single string and return
    return "\n".join(html_output)
