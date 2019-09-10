from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "User_flask"   # table name

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    # 这个不会在表中增加字段
    posts = db.relationship(
        'Post',
        backref = 'user',  # 这个是用来反向引用时所调用的属性，可以自由改动
        lazy = 'dynamic',  # 代表加载我们指定对象的方式，有子查询方式，动态方式;
    )

    def __init__(self, username):
        self.username = username
    
    def __repr__(self):
        return "<User '{}'>".format(self.username)


# 中间第三章表，因为不需要用query，所以直接使用table来创建
tags = db.Table('post_tags',
db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())

    comments = db.relationship(
        'Comment',
        backref = "Post",
        lazy = 'dynamic',
    )
    user_id = db.Column(db.Integer(), db.ForeignKey('User_flask.id'))  # 这个用table名，而不是类名

    tags = db.relationship(
        "Tag",
        secondary = tags,
        backref = db.backref('posts', lazy='dynamic')
    )
    
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Post  '{}'>".format(self.title)

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])

# db.Table是更底层的操作，db.Model也是基于此；而因为不需要对这个表操作，需要用db.Table

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title
    
    def __repr__(self):
        return "<Tag '{}' >".format(self.title)