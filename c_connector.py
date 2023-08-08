from c_execute import *
import psycopg2 as pg
import pandas as pd

def obj_execute(command):
    exec = Execute(command)


class Connector:
    def __init__(self):
        super().__init__()

        input_string = input()
        self.check_header(input_string)
        self.pgdb = pg.connect(
            host='10.10.20.114',
            # host='localhost',
            dbname='Data',
            user='postgres',
            password='ilsan1236526',
            port=5432
        )
    def check_header(self, input_string):
        print('엥?')
        if input_string == 'req_store_info':
            obj_execute("req_store_info")
            print("You entered:", input_string)
        elif input_string == 'Hello world to python':
            print('???')
            obj_execute("get_real_estate_info")
        else:
            print('not entered')


if __name__ == '__main__':
    Connector()
