from jinja2 import Template


if __name__ == '__main__':

    try:
        file = open('/home/konstantinos/sm_ws/custom_ros_build/templates/main_script.tem', 'r')
        entire_file = file.read()
    # perform file operations
    finally:
        file.close()

    data = {'distro': 'noetic'}
    tm = Template(entire_file)
    msg = tm.render(data)

    print(msg)
