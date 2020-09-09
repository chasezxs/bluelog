from flask_script import Manager
from flask_migrate import MigrateCommand

from bluelog import create_app, register_logging
from bluelog.models import *

app = create_app(config_name='development')
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
