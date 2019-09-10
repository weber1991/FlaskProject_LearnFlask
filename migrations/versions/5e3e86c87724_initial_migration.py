"""initial migration

Revision ID: 5e3e86c87724
Revises: 
Create Date: 2019-07-23 00:01:28.477757

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5e3e86c87724'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User_flask',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user_flask')
    op.create_foreign_key(None, 'comment', 'post', ['post_id'], ['id'])
    op.create_foreign_key(None, 'post', 'User_flask', ['user_id'], ['id'])
    op.create_foreign_key(None, 'post_tags', 'post', ['post_id'], ['id'])
    op.create_foreign_key(None, 'post_tags', 'tag', ['tag_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post_tags', type_='foreignkey')
    op.drop_constraint(None, 'post_tags', type_='foreignkey')
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.create_table('user_flask',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('password', mysql.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='MyISAM'
    )
    op.drop_table('User_flask')
    # ### end Alembic commands ###