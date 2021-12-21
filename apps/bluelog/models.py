from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from exts import db


# 管理员
class Admin(db.Model, UserMixin):
    """存储用户信息和博客资料"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))  # 密码散列值
    blog_title = db.Column(db.String(60))  # 博客标题
    blog_sub_title = db.Column(db.String(100))  # 博客副标题
    name = db.Column(db.String(30))  # 用户姓名
    about = db.Column(db.Text)  # 关于信息

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 分类
class Category(db.Model):
    """存储文章分类"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)  # 分类名称

    # 与    文章    一对多关系
    posts = db.relationship('Post', back_populates='category')  # back_populates 反向填充


# 文章
# datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d_%H:%M") PRC北京时间
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))  # 标题
    body = db.Column(db.Text)  # 正文
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # 时间戳
    can_comment = db.Column(db.Boolean, default=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    category = db.relationship('Category', back_populates='posts')
    # 级联删除, 删除文章时级联删除该文章的评论
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')

    def to_json(self):
        item = self.__dict__
        if '_sa_instance_state' in item:
            del item['_sa_instance_state']
        return item


# 评论
class Comment(db.Model):
    """存储评论"""
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))  # 作者
    email = db.Column(db.String(254))  # 邮箱
    site = db.Column(db.String(255))   # 站点
    body = db.Column(db.Text)      # 正文
    from_admin = db.Column(db.Boolean, default=False)  # 判断评论是否是管理员的评论，默认为False
    reviewed = db.Column(db.Boolean, default=False)  # reviewed字段也存储布尔值，用来判断评论是否通过审核
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    post = db.relationship('Post', back_populates='comments')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')

    def to_json(self):
        item = self.__dict__
        if '_sa_instance_state' in item:
            del item['_sa_instance_state']
        return item


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))

