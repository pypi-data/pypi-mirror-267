from .database import database

class MysqliMetaClass(type):
    __config__ = None
    __database_name__ = None
    __has_database__ = False

    def __new__(cls, name, bases, attrs):
        print(cls)
        # 如果__config__和__database_name__为None，则获取config和database_name
        if cls.__config__ is None and cls.__database_name__ is None:
            attrs['config'], attrs['database_name'] = cls.__get_config__()
        if attrs['has_database'] is False:
            pass
        return type.__new__(cls, name, bases, attrs)


    @staticmethod
    def __get_config__():
        try:
            from config.database import mysql_host, mysql_user, mysql_password, mysql_port
            return {
                'host': mysql_host,
                'user': mysql_user,
                'password': mysql_password,
                'port': mysql_port,
            }
        except:
            # 如果 config/database.py 不存在，则提示
            print('Error: Config file not found')
            return {
                'host': 'localhost',
                'user': 'root',
                'password': '',
                'port': 3306,
            }
        
    @staticmethod
    def __get_database_name__():
        try:
            from config.database import mysql_database
            return mysql_database
        except:
            # 如果 config/database.py 不存在，则提示
            print('Error: Config file not found')
            return 'avania'
    
    