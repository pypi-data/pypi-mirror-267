import mysql.connector
from .mate import MysqliMetaClass

class mysqli(metaclass=MysqliMetaClass):
    config = None
    connection = None

    def __get_connection__(self):
            try:
                connection = mysql.connector.connect(**self.config)
                return connection
            except mysql.connector.Error as e:
                print('Error: Connection failed')
                print(e)
            return None
    
    def __connect__(self):
        if self.connection is None:
            self.connection = self.__get_connection__()
        return self.connection
    
    def __call__(self, sql: str, values: dict = None, type: str = 'fetchall'):
        # 检查values是否为None，如果是None则将values设置为一个空元组
        if values == None:
            values = ()
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, values)
            self.connection.commit()
            if type == 'fetchall':
                return cursor.fetchall()
            elif type == 'fetchone':
                return cursor.fetchone()
            elif type == 'fetchmany':
                return cursor.fetchmany()
            elif type == 'execute':
                return cursor.rowcount
            elif type == 'lastrowid':
                return cursor.lastrowid
            cursor.close()
        except Exception as e:
            print('Error: Query failed')
            print(e)
        return self

    @classmethod
    def insert(self, table: str, keys: list, values: list):
        print("111"*111)
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table, ', '.join(keys), ', '.join(['%s' for key in keys]))
        print(sql)
        return self(sql, values, 'execute')
    
    def print(self, a):
        print(a, self.d)
    
    def update(self, table: str, keys: list, values: list, where: str):
        sql = 'UPDATE {} SET {} WHERE {}'.format(table, ', '.join([key + ' = %s' for key in keys]), where)
        return self(sql, values, 'execute')
    
    def delete(self, table: str, where: str):
        sql = 'DELETE FROM {} WHERE {}'.format(table, where)
        return self(sql, type = 'execute')
    
    def select(self, table: str, keys: list, where: str = None, values: dict = None, type: str = 'fetchall'):
        sql = 'SELECT {} FROM {}'.format(', '.join(keys), table)
        if where is not None:
            sql += ' WHERE {}'.format(where)
        return self(sql, values, type)
    
    def find(self, table: str, keys: list, where: str = None, values: dict = None):
        return self.select(table, keys, where, values, 'fetchone')
    
    def __del__(self):
        # self.connection.close()
        print('Connection closed')
        del self
