from jinja2 import Environment, PackageLoader, select_autoescape


def render(template_name, context):
    env = Environment(
        loader=PackageLoader('infantographics', 'templates'),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        #  lstrip_blocks=True,
    )
    template = env.get_template(template_name)
    return template.render(**context)
