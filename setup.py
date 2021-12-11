from setuptools import setup
import os

# Get a list of scripts to install
scripts = []

# Get long description
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    long_description = f.read()

kwargs = {
    'name':'custom_ros_build',
    'version':'0.1.0',
    'packages':['custom_ros_build'],
    'install_requires':[
    	'PyYAML >= 3.0.9',
        'bloom',
        'gitpython'
        'jinja2'
    	],
    'zip_safe':True,
    'scripts': scripts,
    'author': 'Konstantinos Kokkalis',
    'author_email': 'kokkalisko@gmail.com',
    'maintainer':'Konstantinos Kokkalis',
    'maintainer_email':'kokkalisko@gmail.com',
    'description':'Custom scripts to build and generate binaries for ROS1 packages',
    'long_description': long_description,
    'keywords': ['ROS', 'build', 'catkin'],
    'license':'Apache 2.0'
}

setup(**kwargs)

