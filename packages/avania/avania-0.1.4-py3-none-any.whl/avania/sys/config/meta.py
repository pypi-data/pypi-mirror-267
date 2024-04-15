class ConfigMetaClass(type):
    path = 'config'
    template_base_path = '/'
    template_path = '/sys/config/templates'

    def __new__(cls, name, bases, attrs):
        cls.update_template_base_path()
        cls.check_folder()
        return type.__new__(cls, name, bases, attrs)
    
    @classmethod
    def update_template_base_path(self):
        from avania.sys.os import os
        self.template_base_path = os.avania__path__()
        return self

    @classmethod
    def check_folder(self):
        from avania.sys.os import os
        if not os.listdir(self.path):
            self.create_folder()
        return self
    
    @classmethod
    def create_folder(self):
        from avania.sys.os import os
        if os.mkdir(self.path, inquirer=True, inquirer_message="Create config folder? [Y/n] ", verbose=True):
            self.create_templates()
        

    @classmethod
    def create_templates(self):
        from avania.sys.prompt import prompt
        # 询问是否创建模板文件
        # 如果create的为True
        if prompt.prompt("Create all template files? [Y/n] ", default=True):
            from avania.sys.os import os
            # 从avania/config/templates中复制所有文件到config文件夹
            for file in os.listdir(f'{self.template_base_path}{self.template_path}'):
                # 创建文件
                self.create_template(file.replace('.py', ''), inquirer=False)
        
    @classmethod
    def create_template(self, name, inquirer = True, verbose = True):
        from avania.sys.os import os
        from avania.sys.os.config import git_url
        from avania.sys.prompt import prompt
        return os.cp(f'{self.template_base_path}{self.template_path}/{name}.py', f'config/{name}.py', verbose=verbose, inquirer=inquirer, inquirer_message=f'Create {name}.json? [Y/n] ',
              success_message=f'Created {name}.py', fail_message=f'Failed to create {name}.py')

    @classmethod
    def get_file(self, name):
        from avania.sys.os import os
        result = os.read(f'{self.path}/{name}.py')
        if not result:
            if self.create_template(name):
                return self.get(name)
            else:
                return None
        else:
            return result

    # 解析python文件的内容，返回一个JSON对象
    # 文件内容为xxx=xxx
    # 返回{"xxx": "xxx"}
    @classmethod
    def parse_file(self, text):
        result = {}
        try:
            for line in text.split('\n'):
                if line:
                    key, value = line.split('=')
                    # 去掉两边的空格
                    key, value = key.strip(), value.strip()
                    # 如果value为True或False，转换为bool类型
                    if value.lower() == 'true':
                        value = True
                    elif value.lower() == 'false':
                        value = False
                    # 否则如果value为字符串，去掉两边的引号
                    elif value[0] == value[-1] == "'" or value[0] == value[-1] == '"':
                        value = value[1:-1]
                    # 否则如果value为数字，转换为int类型
                    else:
                        try:
                            value = int(value)
                        except:
                            pass
                    result[key] = value
        except:
            return None
        return result
        


    @classmethod
    def get_attr(self, name, attr):
        datum = self.parse_file(self.get_file(name))
        if datum is None:
            return None
        return datum.get(attr, None)
        

            
       