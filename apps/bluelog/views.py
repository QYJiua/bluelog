import json

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user, login_required

from util.Const import Const
from .models import Admin, Comment, Category, Post, Link
from .util import get_obj_list
from forms import LoginForm
from flask_wtf.csrf import generate_csrf


bluelog_bp = Blueprint('albumy', __name__)

Const.ENCODING = 'utf-8'


@bluelog_bp.after_app_request
def after_request(response):
    # 调用函数生成csrf token
    csrf_token = generate_csrf()
    print('csrf_token', csrf_token)
    # 设置cookie传给前端
    response.set_cookie('csrf_token', csrf_token)
    return response



@bluelog_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'code': 20000, 'msg': '用户已经登录'})
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # print(username, password)
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin)
                return jsonify({'code': 20000, 'msg': '登录成功'})
        else:
            return jsonify({'code': 20000, 'msg': '用戶名或者密码错误'})
    else:
        return jsonify({'code': 400, 'msg': '请求数据格式错误'})


@bluelog_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'code': 20000, 'msg': '用戶退出成功'})


@bluelog_bp.route('/index', methods=['POST'])
def index():
    """首页"""
    data = json.loads(request.get_data().decode(Const.ENCODING))
    if not data or ('page' not in data and 'perPage' not in data):
        return jsonify({'code': 400, 'msg': '请求数据格式错误'})
    page = data.get('page', 1)
    per_page = data.get('perPage')
    print(per_page)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    print(len(posts))
    post_list = get_obj_list(posts)
    return jsonify({'code': 20000, 'data': post_list})


@bluelog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    """显示属于category_id类的文章"""
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perPage', type=int)
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    post_list = get_obj_list(posts)
    return jsonify({'code': 20000, 'data': post_list})


@bluelog_bp.route('/post/<int:post_id>', methods=['GET'])
def show_post(post_id):
    """显示文章
    http://localhost:5000/post/2?perPage=5
    """
    post = Post.query.get(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perPage', type=int)
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.desc()).paginate(page, per_page)
    comments = pagination.items
    comment_list = get_obj_list(comments)
    post_dict = post.to_json()
    return jsonify({'code': 20000, 'comments': comment_list, 'post': post_dict})


@bluelog_bp.route('/addComment', methods=['POST'])
def add_comment():
    """发表评论"""
    data = json.loads(request.get_data().decode(Const.ENCODING))

