import os

DATABASES = {
    'default': {
        'NAME': os.getenv('DBNAME','unsetdbname'),
        'USER': os.getenv('DBUSER','unsetdbuser'),
        'PASSWORD': os.getenv('DBPASS','unsetdbpass'),
        'HOST': os.getenv('DBHOST','unsetdbhost'),
        'PORT': os.getenv('DBPORT','unsetdbport'),
    }
}