from jinja2 import Template
import os

def generate_rendered_template(configuration, template_filename):

    try:
        template_path = os.path.join(os.path.dirname(__file__),
                                     '../templates', template_filename)
        file = open(template_path, 'r')
        entire_file = file.read()
    finally:
        file.close()

    template_file = Template(entire_file)
    rendered_text = template_file.render(configuration)

    try:
        rendered_filename = template_filename.rsplit('.', 1)[0]
        final_template_file = os.path.join(configuration['destination_folder'],
                                           rendered_filename)
        file = open(final_template_file, 'w')
        file.write(rendered_text)
    finally:
        file.close()

    st = os.stat(final_template_file)
