from DataRead import DataClass
import json
import psycopg2 as pg
import pandas as pd
import sys

sys.path.append("path_to_psycopg2_directory")

header_split = chr(1)
result_split = chr(2)


class Execute:
    def __init__(self, command='None'):
        super().__init__()

        self.data = DataClass()

        if command == 'req_store_info':
            self.select_tb_store()
        elif command == 'req_population_info':
            self.get_tb_dong_population()
        # elif command == 'get_real_estate_info':
        #     self.get_real_estate_info()
        elif "page_two_combo1" in command:
            result = command.split(header_split)[1]
            self.get_dong_real_estate_info(result)
        else:
            pass

    def get_dong_real_estate_info(self, dong_name):
        col_list = ['ESTATE_ADDR', 'ESTATE_AREA', 'ESTATE_PRICE']
        dong_estate_info = self.data.select_dong_real_estate_info(dong_name, col_list)
        list_ = []
        for i in dong_estate_info:
            area, price, addr = i
            a = f'{area}, {price}, {addr}{chr(1)}'
            list_.append(a)
            print(f'{area}{result_split}{price}{result_split}{addr}{chr(1)}')
        # print(dong_estate_info)
        # print(type(list_))
        # print(f"\"{list_[0]}\"")

    def select_tb_store(self):
        # 상권 데이터 출력
        df_list = self.data.select_data()
        print(df_list)

    # 행정동별 거주인구
    def get_tb_dong_population(self):
        df_list = self.data.select_dong_population()
        population_dict = {}
        for i in df_list:
            dong_code = i[0]
            population = i[1]
            population_data = self.data.select_dongname_by_dongcode(dong_code)
            population_dict[population_data[0][0]] = population
        print(population_dict)

    # 행정동별 공시지가
    def get_dong_area_price(self):
        df_list = self.data.select_dong_area_price()
        area_price_dict = {}
        for i in df_list:
            dong_code = i[0]
            population = i[1]
            population_data = self.data.select_dongname_by_dongcode(dong_code)
            area_price_dict[population_data[0][0]] = population
        print(area_price_dict)

    # 행정동별 매출액
    def select_dong_wash_sales_avg(self):
        df_list = self.data.select_dong_wash_sales_avg()
        area_price_dict = {}
        for i in df_list:
            dong_code = i[0]
            population = i[1]
            population_data = self.data.select_dongname_by_dongcode(dong_code)
            area_price_dict[population_data[0][0]] = population
        print(area_price_dict)

    # 매물 정보
    # def get_real_estate_info(self):
    #     df_list = self.data.select_real_estate_info()
    #     area_price_dict = {}
    #     for i in df_list:
    #         estate_id, dong_nm, area, price, floor, la, lo, addr = i
    #         print(f'{estate_id}, {dong_nm}, {area}, {price}, {floor}, {la}, {lo}, {addr}{chr(1)}')
    #         area_price_dict[i[1]] = estate_id, area, price, floor, la, lo, addr, chr(1)

        # print(area_price_dict)
        # result = json.dumps(area_price_dict)
        # result = bytes(result, "UTF-8")
        # result = eval(result)
        # print(result)

    # 행정동별 세탁업 입점수
    def get_dong_wash_stoer(self):
        wash_stoer_count_dict = {}
        ws_stoer_counts = self.data.select_wash_stoer_count()
        for i in ws_stoer_counts:
            dong_code = i[0]
            dong_name = self.data.select_dongname_by_dongcode(dong_code)
            ws_stoer_count = i[1]
            wash_stoer_count_dict[dong_name[0][0]] = ws_stoer_count
        print(wash_stoer_count_dict)


if __name__ == '__main__':
    ex = Execute()
    ex.get_tb_dong_population()
    # ex.get_dong_area_price()
    # ex.select_dong_wash_sales_avg()
    # ex.get_dong_wash_stoer()
    # ex.get_dong_real_estate_info("신사동")
    # ex.select_tb_store()
