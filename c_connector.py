from c_execute import *


def obj_execute(command):
    Execute(command)

header_split = chr(1)

class Connector:
    def __init__(self):
        super().__init__()

        input_string = input()
        self.check_header(input_string)

    def check_header(self, input_string):
        obj_execute(input_string)

if __name__ == '__main__':
    Connector()