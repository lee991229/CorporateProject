from c_execute import *


def obj_execute(command):
    exec = Execute(command)


class Connector:
    def __init__(self):
        super().__init__()

        input_string = input()
        self.check_header(input_string)

    def check_header(self, input_string):
        if input_string == 'req_store_info':
            obj_execute("req_store_info")
            print("You entered:", input_string)
        else:
            print('not entered')


if __name__ == '__main__':
    Connector()
