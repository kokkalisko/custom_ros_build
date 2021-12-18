from render_templates import generate_rendered_template

def generate_build_test_process(configuration):
    print('Generating files to build and test the packages')

    print('Firstly, generate the ros_entrypoint script')
    generate_rendered_template(configuration, 'ros_entrypoint.sh.tem')

    print('Generate the Dockerfile for building and testing')
    generate_rendered_template(configuration, 'build_test.Dockerfile.tem')

    print('Generate the script for building and testing')
    generate_rendered_template(configuration, 'build_test_script.sh.tem')