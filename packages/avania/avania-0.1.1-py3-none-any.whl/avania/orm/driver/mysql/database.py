import mysql.connector

class database():
    def __init__(self, config: dict, database: str = None):
        # 单独获取config中的database键值对
        self.database_name = config['database']
        # 连接mysql，但是不连接到任何数据库，注意config中有database键值对，所以要删除
        del config['database']
        self.connection = mysql.connector.connect(**config)
        # 创建一个游标
        self.cursor = self.connection.cursor()
        # 检查是否存在数据库，如果不存在则创建数据库
        self.cursor.execute('SHOW DATABASES')
        databases = self.cursor.fetchall()
        databases = [database[0] for database in databases]
        if self.database_name not in databases:
            self.cursor.execute('CREATE DATABASE {}'.format(self.database_name))
        # 关闭游标
        self.cursor.close()
        # 关闭连接  
        self.connection.close()
        # 销毁class
        del self