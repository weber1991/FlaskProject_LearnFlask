import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from webapp.models import db, User, Post, Tag, Comment
from webapp import create_app

'''
Flask Script扩展提供向Flask插入外部脚本的功能
包括:运行一个开发用的服务器;一个定制的Python shell;
设置数据库的脚本，cronjobs，及其他运行在web应用之外的命令行任务；使得脚本和系统分开；
Flask Script和Flask本身的工作方式类似，只需定义和添加从命令行中被Manager实例调用的命令；
'''
env = os.environ.get("WEBAPP_ENV", "Dev") # 调用系统的环境变量的值，如果没有则使用dev
app = create_app("webapp.config.%sConfig" % env.capitalize())

# 不调用系统变量，直接使用开发
# 模式
#app = create_app('webapp.config.DevConfig')


# 调用扩展，实例化Migrate
migrate = Migrate(app, db)

# 调用flask_script扩展
manager = Manager(app)

# 添加指令方式1-利用add_command方法来添加，命令为server，启动Server() 
manager.add_command("server", Server())

# 添加db指令，指向migrate命令对象
manager.add_command("db", MigrateCommand)  

# 创建一个python命令行-利用@manger.shell来修饰
# 使用：1、返回上下文；2、上下文包含的是flask的实例，默认导入以及你想要的东西。
# 用途：测试models，db，......
@manager.shell
def make_shell_context():
    return dict(app = app,
    db=db, 
    User=User, 
    Post=Post, 
    Tag = Tag,
    Comment = Comment,
    good = "good")

# 添加指令方式2-利用@manage.command来修饰：命令为函数名，
@manager.command
def hello():
    print("hello!")


if __name__ == '__main__':
    # 随机生成例子文章的脚本
    # import random
    # import datetime
    # user = User.query.get(1)
    # tag_one = Tag('Python')
    # tag_two = Tag('Flask')
    # tag_three = Tag('sqlalchemy')
    # tag_four = Tag('Jinja')
    # tag_list = [tag_one, tag_two, tag_three, tag_four]
    # s = "example post"

    # for i in range(100):
    #     new_post = Post("post" + str(i))
    #     new_post.user = user    
    #     new_post.publish_date=datetime.datetime.now()  
    #     new_post.text = s  
    #     new_post.tags = random.sample(tag_list, random.randint(1,3))    
    #     db.session.add(new_post)
    # db.session.commit()
    manager.run()