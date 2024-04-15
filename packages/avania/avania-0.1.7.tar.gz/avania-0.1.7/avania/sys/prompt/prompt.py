class prompt():
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "purple": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }

    @classmethod
    def print(self, message, color = 'white'):
        if color in self.colors:
            print("%s%s%s" % (self.colors[color], message, self.colors["reset"]))
        else:
            print(message)

    @classmethod
    def prompt(self, message, default = False, color = "blue"):
        if color in self.colors:
            response = input("%s%s%s" % (self.colors[color], message, self.colors["reset"]))
        else:
            response = input(message)
        if response == "":
            return default
        elif response.lower() in ["y", "yes"]:
            return True
        elif response.lower() in ["n", "no"]:
            return False
        else:
            return prompt(message, default, color)
        
    @classmethod
    def print_github(self):
        prompt.print("Please visit https://github.com/StarLxa/avania-core for more information", "green")