# -*- coding: utf-8 -*-

"""
Database connection for Cl4ptr4p project.

Using Flask 1.0.2.

For more information on this file, see
README.md
"""

# CLOUD SETTINGS
APP_ENGINE = {
    'MYSQL_CLOUD': {
        'DB_HOST': "mysql+mysqldb://",
        'DB_USER': "user_here",
        'DB_PASSWD': "password_here",
        'DB_NAME': "awesomedb",
        'DB_PORT': "3306",
        'PROJECT_ID': "project-name:project-zone",
        'INSTANCE_NAME': "instance-name"
    },
    'POSTGRESQL_CLOUD': {
        'DB_HOST': "postgresql+psycopg2",
        'DB_USER': "postgres",
        'DB_PASSWD': "postgres",
        'DB_NAME': "postgres",
        'DB_PORT': "5432",
        'PROJECT_ID': "project-name:project-zone",
        'INSTANCE_NAME': "instance-name"
    }
}

# MYSQL_CLOUD = "mysql+mysqldb://user:password@/<dbname>?unix_socket=/cloudsql/<projectid>:<zone>:<instancename>"
if len(APP_ENGINE['MYSQL_CLOUD']['DB_PASSWD']) > 0:
    MYSQL_CLOUD = "{0}{1}:{2}@/{3}?unix_socket=/cloudsql/{4}:{5}".format(
        APP_ENGINE['MYSQL_CLOUD']['DB_HOST'],
        APP_ENGINE['MYSQL_CLOUD']['DB_USER'],
        APP_ENGINE['MYSQL_CLOUD']['DB_PASSWD'],
        APP_ENGINE['MYSQL_CLOUD']['DB_NAME'],
        APP_ENGINE['MYSQL_CLOUD']['PROJECT_ID'],
        APP_ENGINE['MYSQL_CLOUD']['INSTANCE_NAME']
    )
else:
    # MYSQL_CLOUD = "mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>"
    MYSQL_CLOUD = "{0}{1}@/{2}?unix_socket=/cloudsql/{3}:{4}".format(
        APP_ENGINE['MYSQL_CLOUD']['DB_HOST'],
        APP_ENGINE['MYSQL_CLOUD']['DB_USER'],
        APP_ENGINE['MYSQL_CLOUD']['DB_NAME'],
        APP_ENGINE['MYSQL_CLOUD']['PROJECT_ID'],
        APP_ENGINE['MYSQL_CLOUD']['INSTANCE_NAME']
    )


# POSTGRESQL_CLOUD = "postgresql+psycopg2://<user>:<password>@/<database>?host=/cloudsql/<project_id>:<region>:<instancename>"
POSTGRESQL_CLOUD = "{0}://{1}:{2}@/{3}?host=/cloudsql/{4}:{5}".format(
    APP_ENGINE['POSTGRESQL_CLOUD']['DB_HOST'],
    APP_ENGINE['POSTGRESQL_CLOUD']['DB_USER'],
    APP_ENGINE['POSTGRESQL_CLOUD']['DB_PASSWD'],
    APP_ENGINE['POSTGRESQL_CLOUD']['DB_NAME'],
    APP_ENGINE['POSTGRESQL_CLOUD']['PROJECT_ID'],
    APP_ENGINE['POSTGRESQL_CLOUD']['INSTANCE_NAME']
)
