# import datetime
# import json
# import logging
# import os
# import threading
# import uuid
# import zipfile
#
# # from pyodm import Node, Task
from exts import db
#
# from apps.swcj.models import Armodel, Archives
# # from ReadConfig import ReadConfig
# from util.Status import Status
#
#
# def get_options(data):
#     options = {}
#     if 'feature_quality' in data:
#         options['feature-quality'] = data.get('feature_quality')
#     if 'feature_type' in data:
#         options['feature-type'] = data.get('feature_type')
#     if 'min_num_features' in data:
#         options['min-num-features'] = data.get('min_num_features')
#     if 'matcher_type' in data:
#         options['matcher-type'] = data.get('matcher_type')
#     if 'camera_lens' in data:
#         options['camera-lens'] = data.get('camera_lens')
#     if 'mesh_size' in data:
#         options['mesh-size'] = data.get('mesh_size')
#     if 'mesh_octree_depth' in data:
#         options['mesh-octree-depth'] = data.get('mesh_octree_depth')
#     if 'pc_quality' in data:
#         options['pc-quality'] = data.get('pc_quality')
#     if 'orthophoto_resolution' in data:
#         options['orthophoto-resolution'] = data.get('orthophoto_resolution')
#     return options
#
#
# def create_node():
#     ip, port = '10.0.0.188', 3000
#     return Node(ip, port)
#
#
# def get_task_by_uuid(task_uuid):
#     n = create_node()
#     u = uuid.UUID(task_uuid)
#     t = Task(n, u)
#     return t
#
#
def update_archives(archives, source):
    try:
        archives.source = source
        db.session.commit()
    except Exception as e:
        db.session.rollback()

#
# def get_res_data(task, data, task_status=None):
#     try:
#         info = task.info()
#         res_data = {'uuid': info.uuid, 'name': info.name + '', 'date_created': str(info.date_created),
#                     'output': info.output,
#                     'processing_timd': info.processing_time, 'status': str(info.status), 'last_error': info.last_error,
#                     'options': info.options, 'images_count': info.images_count, 'progress': int(info.progress),
#                     'arId': data.get('arId')}
#         if task_status:
#             task.remove()   # 转换成功，移除NodeODM中的任务
#     except Exception as e:
#         get_model_info = Armodel.query.filter(Armodel.ar_id == data.get('arId')).first()
#         if get_model_info:
#             res_data = get_model_info.res_info
#             res_data = json.loads(res_data.strip('"'))
#         else:
#             res_data = {}
#     if task_status:
#         res_data['task_status'] = task_status
#     res_data = json.dumps(res_data)  # 模型信息
#     return res_data
#
#
# # 创建任务
# def create_task(image_names, options=None):
#     node = create_node()
#     if options:
#         task = node.create_task(image_names, options, skip_post_processing=True)
#     else:
#         task = node.create_task(image_names, skip_post_processing=True)
#     return task
#
#
# def unzip_file(zip_src):
#     dst_dir = zip_src
#     for f in os.listdir(zip_src):
#         if '.zip' in f:
#             zip_src = os.path.join(zip_src, f)
#             r = zipfile.is_zipfile(zip_src)
#             if r:
#                 fz = zipfile.ZipFile(zip_src, 'r')
#                 for file in fz.namelist():
#                     fz.extract(file, dst_dir)
#             return r
#         return False
#
#
# def get_obj2gltfcmd(convert_path):
#     obj_path = os.path.join(convert_path, 'odm_textured_model_geo.obj')
#     gltf_path = os.path.join(convert_path, 'odm_textured_model_geo.gltf')
#     obj2gltfcmd = 'obj2gltf -i ' + obj_path + ' -o ' + gltf_path
#     return gltf_path, obj2gltfcmd
#
#
# def get_start_task_uuid_status(model_info):
#     task_uuid = model_info.get('task_uuid')
#     task_status = Status[model_info.get("task_status")].value
#     return task_uuid, task_status
#
#
# # 线程
# class MyThread(threading.Thread):
#     def __init__(self, image_names, options=None):
#         threading.Thread.__init__(self)
#         self.image_names = image_names
#         self.options = options
#         self.task = create_task(self.image_names, self.options)
#         # self.task = create_task(self.image_names, self.options)
#
#     def get_result(self):
#         return self.task
#
#
# class DateEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return obj.strftime("%Y-%m-%d %H:%M:%S")
#         else:
#             return json.JSONEncoder.default(self, obj)
#
#
#
#
