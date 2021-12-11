#!/usr/bin/env python3

from catkin_pkg.packages import find_packages
from generate_build_test import generate_build_test_process
import git

import yaml

import os
import sys
import argparse
import shutil

ubuntu_ROS_map = {
    'noetic': 'focal',
    'melodic': 'bionic',
    'lunar': 'xenial',
    'kinetic': 'xenial',
    'jade': 'trusty',
    'indigo': 'trusty'
}

# Setup the parser
def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=('Generates the debian binaries of packages existing '
                                                  'inside the workspace'))
    parser.add_argument('-f', '--config_file', default=os.path.join(os.getcwd(), 'src', 'config.yaml'),
                        help="The path of the configuration file")
    parser.add_argument('-d', '--destination_folder', default=os.path.join(os.getcwd(), 'generated_files'),
                        help="The path of the destination folder")
    parser.add_argument('-w', '--workspace_folder', default=os.path.join(os.getcwd()),
                        help="The path of the workspace folder that contains all the packages to be")

    namespace, unknown_args = parser.parse_known_args(args)
    return namespace

# TODO: currently not used
# Get the paths of the source code of the packages existing in the workspace
def get_workspace_packages():
    cwd = os.getenv('PWD', os.curdir)
    source_path = os.path.join(cwd, 'src')

    return find_packages(source_path)

def process_ROS_distro(configuration):
    # Check for global environmental variable
    distro_name = os.getenv('ROS_DISTRO')

    # If not a valid distro version, check inside the configuration file
    if distro_name not in ubuntu_ROS_map:
        if "ros_distro" not in configuration:
            raise KeyError("ros_distro key not found in yaml configuration file")

        distro_name = configuration['ros_distro']

        # Check if given ROS_DISTRO is actually supported
        if distro_name not in ubuntu_ROS_map:
            raise RuntimeError(f'ROS distribution given in configuration ({distro_name}) is not supported. '
                               'Process will be abandoned')

        os.environ['ROS_DISTRO'] = distro_name
    
    configuration['ubuntu_distro'] = ubuntu_ROS_map[distro_name]
    return configuration

def process_destination_folder(destination_folder_path: str):
    if not os.path.exists(destination_folder_path):
        print(f'Destination folder path {destination_folder_path} does not exist')
        print('Destination folder will be created')
        os.mkdir(destination_folder_path)

    return destination_folder_path

def process_workspace_folder(workspace_folder_path: str):
    # Check if the workspace folder exist
    if not os.path.exists(workspace_folder_path):
        print(f'Workspace folder path {workspace_folder_path} does not exist')
        print('No packages from local workspace will be used')
        return None

    # Check for a src folder
    src_folder_path = os.path.join(workspace_folder_path, 'src')
    if not os.path.exists(src_folder_path):
        print('Workspace does not contain a src folder')
        return None
    
    # Check if the src folder contains any packages
    packages = find_packages(src_folder_path)
    
    if len(packages):
        return packages
    else: 
        return None

# Process external packages 
def process_external_packages(external_packages_list):
    if len(external_packages_list) == 0:
        print('No external packages will be used')
        return
    
    for git_repo in external_packages_list:
        temp_package_path = os.path.join('/tmp/custom_ros_build/', git_repo['name'])
        
        # Clone the package into /tmp folder 
        repo_info = git.Repo.clone_from(git_repo['url'], temp_package_path)
        
        # Check if given branch exists
        # If no branch is given in the configuration, the default/main branch will be used
        if 'branch' in git_repo:
            branch_names = [branch.name for branch in repo_info.branches]
            if git_repo['branch'] not in branch_names:
                raise RuntimeError('{0} branch does not exist for repo'.format(git_repo['branch']))
        
    # Cleanup
    shutil.rmtree('/tmp/custom_ros_build/')
        

# Process the given configuration file
def process_configuration_file(config_file_path: str):
    if not os.path.exists(config_file_path):
        raise RuntimeError(
            'Configuration file not existing. Process will be abandoned')

    # Parse the configuration file
    with open(config_file_path) as f:
        configuration = yaml.load(f, Loader=yaml.FullLoader)

    return process_ROS_distro(configuration)

def main():
    args = parse_args()
    
    configuration = process_configuration_file(args.config_file)
    configuration['destination_folder'] = process_destination_folder(args.destination_folder)
    configuration['workspace_packages'] = process_workspace_folder(args.workspace_folder)
    process_external_packages(configuration['external_packages'])
    
    generate_build_test_process(configuration)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        sys.exit(str(e))
