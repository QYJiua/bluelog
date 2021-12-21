安装虚拟环境
python -m venv env

激活虚拟环境
win
.\env\Scripts\activate
linux
source env/bin/activate

激活虚拟环境后安装python依赖包
pip install -r requirements.txt

flask中的migrate 用命令行进行迁移
python manage.py db init 初始化  生成migrations文件夹 只做一次就可以
python manage.py db migrate 生成迁移文件
python manage.py db upgrade 执行迁移
python manage.py downgrade 回退操作

Flask扩展之【Flask-script】--通过命令行运行文件的插件
python app.py runserver
如需指定ip和端口：
python manage.py runserver -h 127.0.0.1 -p 8090


sqlalchemy.exc.ArgumentError: Mapper mapped class Result->result could not assemble any primary key 报错解决
解决：按照报错字面的意思，和主键有关，最后发现是我要操作的这张mysql表没有设置主键，才有了这个报错，后来查到资料，flask-sqlachemy要求每张表都要有主键，我设置了主键后这个问题解决了；
拓展：如果你不用flask-sqlachemy，用pymysql等其他方式操作数据库是没有这个问题的，数据表没有主键也不会报这个错



数据库操作
查
models中的类
Armodel.query.filter(Armodel.ar_id==data.get('arId')).first()  查找
表为空时，查找语句出错
exists = db.session.query(db.exists().where(Armodel.ar_id == data.get('arId'))).scalar()






 
