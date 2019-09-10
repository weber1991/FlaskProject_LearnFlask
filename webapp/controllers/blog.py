from flask import Flask, render_template, Blueprint
import datetime
from webapp.models import db, Post, Tag, Comment, User, tags
from webapp.forms import CommentForm
from sqlalchemy import func


# 获取最新的五个文章以及根据热度来获取标签，其中func是个统计函数,有待下一步了解
def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()
    ).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(
        tags
    ).group_by(Tag).order_by().limit(5).all() 
    # 书中是使用order_by("total DESC")，但报错。
    #  order_by是排序的意思，这里有待了解，使用空，则默认升序
    return recent, top_tags


# 博客的蓝图
blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder="../templates/blog",
    url_prefix="/blog"
)

@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(
        Post.publish_date.desc()
    ).paginate(page, 10)
    recent, top_tags = sidebar_data()
    return render_template('home.html',posts=posts,recent=recent,top_tags=top_tags)



@blog_blueprint.route('/post/<int:post_id>', methods=('GET', 'POST'))
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        new_comment.date = datetime.datetime.now()
        db.session.add(new_comment)
        db.session.commit()
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'post.html',
        post = post,
        tags = tags,
        comments = comments,
        recent = recent,
        top_tags = top_tags,
        form = form
    )

@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(title = tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    print(posts)
    recent, top_tags = sidebar_data()

    return render_template(
        'tag.html',
        tag = tag,
        posts = posts,
        recent = recent,
        top_tags = top_tags
    )

@blog_blueprint.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template(
        'user.html',
        user = user,
        posts = posts,
        recent = recent,
        top_tags = top_tags
    )

@blog_blueprint.errorhandler(400)
def error_400(error):
    return render_template('404.html'), 404


@blog_blueprint.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500
