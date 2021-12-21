from .models import Post, Comment, Category, Admin, Link
from exts import db


def get_obj_list(objects):
    obj_list = []
    for i in objects:
        obj_list.append(i.to_json())
    return obj_list
