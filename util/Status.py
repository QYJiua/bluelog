from enum import Enum


class Status(Enum):
    ERROR = '错误'
    CREATED = '模型构建已启动'
    COMPLETED = '模型构建已完成'
    CONVERTED = '模型转换成功'







