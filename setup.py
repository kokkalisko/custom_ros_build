from setuptools import find_packages
from setuptools import setup
import os

# Define the package name
package_name = 'custom_ros_build'

# Get a list of scripts to install
scripts = []
for root, dirnames, filenames in os.walk('scripts'):
    for filename in filenames:
        scripts.append(os.path.join(root,filename))
    break

# Get long description
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    long_description = f.read()

kwargs = {
    'name':package_name,
    'version':'0.1.0',
    'python_requires':'>3.5.2',
    'install_requires':[
    	'PyYAML >= 3.0.9',
        'bloom',
        'gitpython',
        'jinja2'
    	],
    'include_package_data':True,
    'zip_safe':True,
    'packages': find_packages(),
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

