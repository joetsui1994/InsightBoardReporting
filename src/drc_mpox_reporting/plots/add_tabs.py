def generate_tab_html(sectionName, figure_list):
    # HTML output
    html_output = []
    
    # generate the div for the tab buttons
    html_output.append(f'<div id="{sectionName}-tabs" class="tab">')
    
    # generate the tab buttons
    for index, (filepath, figure_name) in enumerate(figure_list):
        figure_id = figure_name.replace(" ", "-")  # replace spaces with dashes for IDs
        default_open = 'id="defaultOpen"' if index == 0 else ''
        html_output.append(
            f'<button class="tablinks" onclick="openTab(event, \'{figure_id}\', \'{sectionName}\')" {default_open}>{figure_name}</button>'
        )
    html_output.append('</div>')
    
    # generate the tab content sections
    for filepath, figure_name in figure_list:
        figure_id = figure_name.replace(" ", "-")
        html_output.append(f'<div id="{sectionName}-{figure_id}" class="tabcontent">')
        html_output.append(f'    <img src="{filepath}" alt="{figure_name}" style="width:100%">')
        html_output.append(f'    <h3>{figure_name}</h3>')
        html_output.append('</div>')
    
    # join the HTML lines into a single string and return
    return "\n".join(html_output)