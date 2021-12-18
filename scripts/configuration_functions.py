import os
import git
import shutil

ubuntu_ROS_map = {
    'noetic': 'focal',
    'melodic': 'bionic',
    'lunar': 'xenial',
    'kinetic': 'xenial',
    'jade': 'trusty',
    'indigo': 'trusty'
}

docker_ros_distro_map = {
    'base': 'ros:{ros_distro}-ros-base',
    'core': 'ros:{ros_distro}-ros-core',
    'perception': 'ros:{ros_distro}-ros-perception',
    'robot': 'ros:{ros_distro}-ros-robot',
    'desktop': 'osrf/ros:{ros_distro}-desktop',
    'desktop-full': 'osrf/ros:{ros_distro}-desktop-full'
}

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
                               'Distributions older than indigo are not supported. Process will be abandoned')

        os.environ['ROS_DISTRO'] = distro_name
    
    configuration['ubuntu_distro'] = ubuntu_ROS_map[distro_name]

def process_pipeline_operations(configuration):
    if 'test' not in configuration:
        print('No particular guidelines on whether to perform tests for the packages were given.')
        print('Thus, by default tests will be performed')
        configuration['test'] = True
    elif not configuration['test']:
        print('Tests will not be performed')
        
    if 'generate_binaries' not in configuration:
        print('No particular guidelines on whether to generate binaries were given.')
        print('Thus, by default binaries will be generated for all packages')
        configuration['generate_binaries'] = True
    elif not configuration['generate_binaries']:
        print('Binaries will not be generated')
        
def process_docker_ros_image(configuration):
    # Set the docker ROS image that will be used for building the docker
    if 'docker_ros_distro' not in configuration:
        print(f'No docker ROS image has been given in configuration. The core image will be selected '
              'by default')
        configuration['docker_ros_distro'] = 'core'

    if configuration['docker_ros_distro'] not in docker_ros_distro_map:
        print(f'Docker ROS image {configuration["docker_ros_distro"]} is not supported. The core image will be '
              'selected by default')
        configuration['docker_ros_distro'] = 'core'
    
    docker_ros_image_unformatted = docker_ros_distro_map[configuration['docker_ros_distro']]
    
    # Format and set the Docker ROS image
    docker_ros_image = (docker_ros_image_unformatted).format(ros_distro = configuration['ros_distro'])
    configuration['docker_ros_image'] = docker_ros_image
        
# Process external packages 
def process_external_packages(configuration):
    # Check if an external package list is given
    if 'external_packages' in configuration:
        external_packages_list = configuration['external_packages']
    else:
        print('No list of external packages was found')
        configuration['external_packages'] = []
        return
    
    if len(external_packages_list) == 0:
        print('No external packages will be used')
        return

    # Boolean denoting whether to fallback to main/default branch if the
    # requested branch is not found or raise an exception
    fallback_to_ref_branch = configuration.get('fallback_to_ref_branch', False)

    for git_repo in external_packages_list:
        temp_package_path = os.path.join('/tmp/custom_ros_build/', git_repo['name'])
        
        try:
            # Clone the package into /tmp folder
            repo_info = git.Repo.clone_from(git_repo['url'], temp_package_path)
            
            # Check if given branch exists
            # If no branch is given in the configuration, the default/main branch will be used
            if 'branch' in git_repo:
                branch_names = [branch.name for branch in repo_info.branches]
                if git_repo['branch'] not in branch_names:
                    if fallback_to_ref_branch:
                        print(f'Instructed branch {git_repo["branch"]} was not found. The default '
                              'branch {repo_info.active_branch.name} will be used instead')
                        git_repo['branch'] = repo_info.active_branch.name
                    else:
                        raise RuntimeError(f'{git_repo["branch"]} branch does not exist for repo')
        except git.GitCommandError as e:
            # Ask user how to handle the missing repository condition
            exception_handle_question = f'Git repository {git_repo} with url {git_repo["url"]} was not ' \
                                        'found. Are you sure you want to continue? (y/n)'
            answer = input(exception_handle_question)
            if answer == 'y': 
                external_packages_list.remove(git_repo)
                continue
            elif answer == 'n':
                # Cleanup
                shutil.rmtree('/tmp/custom_ros_build/')
                raise e
            else: 
                print("Please enter y or n")
                     
    # Cleanup
    shutil.rmtree('/tmp/custom_ros_build/')
    print('Valid external packages: ')
    for git_repo in external_packages_list:
        print(f'\t{git_repo["name"]}')

def process_binaries_generation(configuration):
    print()
