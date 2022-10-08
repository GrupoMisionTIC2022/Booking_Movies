import os

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    # SECRET_KEY = config('SECRET_KEY'  , default='S#perS3crEt_007')
    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_007')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI ="postgres://iqqemzfsythoou:694b4875b438ee27529cf2b358c02e3e92088f50ae27acfeee5f897b6d014ff7@ec2-52-204-157-26.compute-1.amazonaws.com:5432/dfuo4sb2tepsc5"
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')    
    


class ProductionConfig(Config):
    DEBUG = True

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE'   , 'postgresql'),
        os.getenv('DB_USERNAME' , 'iqqemzfsythoou'),
        os.getenv('DB_PASS'     , '694b4875b438ee27529cf2b358c02e3e92088f50ae27acfeee5f897b6d014ff7'),
        os.getenv('DB_HOST'     , 'ec2-52-204-157-26.compute-1.amazonaws.com'),
        os.getenv('DB_PORT'     , 5432),
        os.getenv('DB_NAME'     , 'dfuo4sb2tepsc5')
    ) 

class DebugConfig(Config):
    DEBUG = False


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
