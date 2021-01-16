import os
import sys
import yaml

CONFIG_NAME = 'config.yaml'

def config_exists():
    if os.path.isfile(CONFIG_NAME):
        return True

def create_config():
    if config_exists():
        ans = input('You already have already setup a config file, do you want to overwrite it? (Y/N): ')
        if ans.lower() == 'y':
            try:
                os.remove(CONFIG_NAME)
            except OSError as e:
                print(f'Error deleting file {CONFIG_NAME}: {e}')
                sys.exit(1)
        else:
            sys.exit(0)
    print(f'Setting up config file "{CONFIG_NAME}".\n'
    'This will store the GitHub token for your account and the repository name you wish to run the program on.\n'
    'You can generate a new GitHub token here: https://github.com/settings/tokens\n')
    config_data = {}
    config_data['token'] = input('GitHub token: ')
    config_data['repo'] = input('Repository name: ')
    try:
        with open(CONFIG_NAME,'w') as f:
            yaml.dump(config_data, f)
    except OSError as e:
        print(f'Error writing file {CONFIG_NAME}: {e}')
        sys.exit(1)   
    print('\nConfig file created.')

if __name__ == '__main__':
    create_config()