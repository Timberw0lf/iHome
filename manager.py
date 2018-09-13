# -*- coding:utf-8 -*-
import redis
from flask import Flask
from flask import session
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager


class Config(object):
    """封装配置的类"""
    DEBUG = True

    # 秘钥
    SECRET_KEY = 'q7pBNcWPgmF6BqB6b5VICF7z7pI+90o0O4CaJsFGjzRsYiya9SEgUDytXvzFsIaR'

    # 配置mysql数据库：真实开发需要写数据库的真实ip
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置redis数据库：实际开发使用数据库的真实ip
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 配置session参数
    # 指定session存储到redis
    SESSION_TYPE = 'redis'
    # 指定session存储到的位置
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 开启session数据的签名、混淆session_data
    SESSION_USE_SIGNER = True
    # 设置session的有效期：
    PERMANENT_SESSION_LIFETIME = 3600 * 24

app = Flask(__name__)

# 创建脚本管理器对象
manager = Manager(app)


# 加载配置参数
app.config.from_object(Config)

# 创建连接到mysql数据库的对象
db = SQLAlchemy(app)


# 创建连接到redis数据库的对象（配置写法模仿mysql数据库的配置参数）
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 数据库迁移
Migrate(app, db)

# 将迁移脚本添加到脚本管理器
manager.add_command('db', MigrateCommand)

# 开启CSRF保护：Flask中需要自己将csrf_token写入到浏览器的cookies
CSRFProtect(app)

# 使用flask_session将session数据写入到redis数据库
Session(app)


@app.route('/')
def index():
    session['name'] = 'wq'
    return 'index!'


if __name__ == '__main__':
    # 记得在edit_configurations中加载script_parameters == runserver
    manager.run()
