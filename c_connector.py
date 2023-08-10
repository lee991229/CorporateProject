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

        # if input_string == 'req_store_info':
        #     obj_execute("req_store_info")
        #     # print("You entered:", input_string)
        #
        # elif input_string == 'Hello world to python':
        #     obj_execute("get_real_estate_info")
        #
        # elif 'page_two_combo1' in input_string:
        #     # print(input_string)
        #     obj_execute(input_string)
        # elif 'page_two_combo2' in input_string:
        #     # print(input_string)
        #     obj_execute(input_string)
        # elif "page_two_estate_click" in input_string:
        #     obj_execute(input_string)
        # else:
        #     print(input_string)


if __name__ == '__main__':
    Connector()
