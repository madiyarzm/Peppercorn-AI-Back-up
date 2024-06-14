from schemas.email_structure import TextProperties, LayoutProperties, Structure, Section, EmailScaffold

def render_text_properties_to_style(text_properties: TextProperties) -> str:
    return " ".join(f'{key.replace("_", "-")}: {value};' for key, value in text_properties.dict().items() if value is not None)

def render_layout_properties_to_style(layout_properties: LayoutProperties) -> str:
    return " ".join(f'{key.replace("_", "-")}: {value};' for key, value in layout_properties.dict().items() if value is not None)

def render_structure_to_html(structure: Structure) -> str:
    layout_style = render_layout_properties_to_style(structure.layout_properties)
    html_output = [f'<div style="{layout_style}">']
    for text_prop in structure.text_properties:
        text_style = render_text_properties_to_style(text_prop)
        html_output.append(f'<p style="{text_style}">{text_prop.text}</p>')
    for element in structure.elements:
        html_output.append(render_structure_to_html(element))
    html_output.append("</div>")
    return "".join(html_output)

def render_email_to_html(email: EmailScaffold) -> str:
    html_output = ["<html><head><style>", "body {margin: 0; padding: 0;}", "</style></head><body>"]
    overall_style = render_layout_properties_to_style(email.overall_layout)
    html_output.append(f'<div style="{overall_style}">')
    for section in email.sections:
        html_output.append(f'<div><h2>{section.title}</h2>')
        for structure in section.structures:
            html_output.append(render_structure_to_html(structure))
        html_output.append("</div>")
    html_output.append("</div></body></html>")
    return "".join(html_output)
