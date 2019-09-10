from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


# 评论表单
class CommentForm(Form):
    name = StringField(
        '姓名',
        validators = [DataRequired(), Length(max=255)]
    )
    text = TextAreaField('评论内容', validators=[DataRequired()])