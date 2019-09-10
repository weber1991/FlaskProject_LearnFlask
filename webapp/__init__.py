from flask import Flask, redirect, url_for
from webapp.models import db
from webapp.controllers.blog import blog_blueprint

# 使用工厂模式
def create_app(object_name):
    # 实例一个flask项目
    app = Flask(__name__)

    # 调用选择的模式
    # 在config.py文件里面：webapp.config.DecConfig / webapp.config.ProConfig
    app.config.from_object(object_name)
    
    # 将数据库和app建立关联
    db.init_app(app)

    # 定义初始页
    @app.route('/')
    def index():
        return redirect(url_for('blog.home'))

    # 注册蓝图
    app.register_blueprint(blog_blueprint)
    return app