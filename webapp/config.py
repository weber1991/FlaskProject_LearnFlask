

class Config(object):
    # CSRF的密钥，设置才可以防止跨站点
    SECRET_KEY = 'woshizuiqiang'

class ProdConfig(Config):
    '''生产模式'''
    pass

class DevConfig(Config):
    '''
    开发模式，调用本地的数据库
    '''
    debug = True
    # "mysql+pymysql://user:password@ip:port/db_name"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:weber@localhost:3306/learn_flask"

    SQLALCHEMY_ECHO = True # 输出显示sql语句