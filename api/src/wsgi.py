import os

from app import create_app

config_name = os.environ.get('APP_CONFIG', 'dev')
if config_name == 'dev':
    print('WARNING: RUNNING IN DEVELOPMENT MODE. SET APP_CONFIG=prod IF DEPLOYING.')

application = create_app(config_name)

if __name__ == '__main__':
    application.run()
