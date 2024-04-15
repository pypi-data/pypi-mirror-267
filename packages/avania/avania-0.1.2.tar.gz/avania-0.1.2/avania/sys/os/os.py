class os():
    @classmethod
    def mkdir(self, path, inquirer=False, inquirer_message=None, inquirer_color="blue", verbose=False):
        import os
        if inquirer_message is None:
            inquirer_message = "Create directory: %s? [Y/n] " % path
        if inquirer:
            from avania.sys.prompt import prompt
            if not prompt.prompt(message=inquirer_message, default=True, color=inquirer_color):
                return False
        try:
            os.makedirs(path, exist_ok=True)
            if verbose:
                prompt.print("Directory created: %s" % path, "green")
            return True
        except:
            if verbose:
                prompt.print("Failed to create directory: %s" % path, "red")
            return False

    @classmethod
    def create_file(self, path, content):
        import os
        from avania.sys.prompt import prompt
        prompt.print("test")

    @classmethod
    def listdir(self, path, verbose=False, fail_message=None):
        if fail_message is None:
            fail_message = "Failed to list directory: %s" % path
        try:
            import os
            return os.listdir(path)
        except:
            from avania.sys.prompt import prompt
            if verbose:
                prompt.print(fail_message % path, "red")
            return []
        
    @classmethod
    def exists(self, path, verbose=False):
        try:
            import os
            return os.path.exists(path)
        except:
            from avania.sys.prompt import prompt
            if verbose:
                prompt.print("Failed to check if path exists: %s" % path, "red")
            return False
        
    @classmethod
    def cp(self, copied_file, new_file, verbose=False, inquirer=False, inquirer_message=None, inquirer_color="blue",
           overwrite=False, success_message=None, fail_message=None):
        if not self.exists(copied_file, verbose=verbose):
            return False
        if success_message is None:
            success_message = "Copied %s to %s" % (copied_file, new_file)
        if fail_message is None:
            fail_message = "Failed to copy %s to %s" % (copied_file, new_file)
        if not overwrite and self.exists(new_file, verbose=verbose):
            from avania.sys.prompt import prompt
            if verbose:
                prompt.print("File %s already exists" % new_file, "yellow")
            return False
        if inquirer_message is None:
            inquirer_message = "Copy %s to %s? [Y/n] " % (copied_file, new_file)
        try:
            import os
            from avania.sys.prompt import prompt
            if inquirer:
                if not prompt.prompt(inquirer_message, default=True, color=inquirer_color):
                    return False
            with open(copied_file) as f:
                with open(new_file, 'w') as new_file:
                    new_file.write(f.read())
                    if verbose:
                        prompt.print(success_message, "green")
                    return True
        except:
            from avania.sys.prompt import prompt
            if verbose:
                prompt.print(fail_message, "red")
            return False
    
    @classmethod
    def read(self, path, verbose=False, fail_message=None):
        if fail_message is None:
            fail_message = "Failed to read file: %s" % path
        try:
            if not self.exists(path, verbose=verbose):
                return False
            with open(path) as f:
                return f.read()
        except:
            from avania.sys.prompt import prompt
            if verbose:
                prompt.print(fail_message, "red")
            return False
        
    @classmethod
    def avania__path__(self):
        try:
            import os
            return os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..' + '/avania'))
        except:
            return f"./avania"