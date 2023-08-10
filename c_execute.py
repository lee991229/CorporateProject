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

        elif "page_two_combo2" in command:
            result = command.split(header_split)[1]
            header = command.split(header_split)[0]
            result = result.split(result_split)
            if "이상" in result[1]:
                self.get_dong_real_estate_info2(result[0], '이상')
            elif "이하" in result[1]:
                self.get_dong_real_estate_info2(result[0], '이하')
            else:
                self.get_dong_real_estate_info2(result[0], '')

        elif "page_two_estate_click" in command:
            """
            세번째 페이지 정보들 받아오기
            1. 해당 매물 정보들 
            2. 해당 행정동 거주 인구수
            3. 해당 행정동 평균 영업기간
            4. 해당 매물 행정동 상권변화지표
            """
            # print('확인1', command)
            result = command.split(header_split)[1]
            # print('확인2', result)
            result = result.split("^")
            # print('확인3', result)
            self.get_estate_info(result)
        else:
            pass

    def get_estate_info(self, result):
        addr, dong_name = result
        col_list = ['ESTATE_LA', 'ESTATE_LO']
        result1 = self.data.select_estate_info(addr, col_list)
        # if len(result1) > 1:
        #     result1 = result1[0]
        dong_code = self.data.select_dong_code(dong_name)
        result2 = self.data.select_dong_sign(dong_code)
        print(result1[0][0], header_split, result1[0][1], header_split, result2[0][0], header_split, dong_name,
              header_split, dong_code)

    # 매물 확인 화면 1콤보박스 체인지 인덱스
    def get_dong_real_estate_info(self, dong_name):
        col_list = ['ESTATE_ADDR', 'ESTATE_AREA', 'ESTATE_PRICE']
        dong_estate_info = self.data.select_dong_real_estate_info(dong_name, col_list)
        # list_ = []
        count = 1
        for i in dong_estate_info:
            area, price, addr = i
            # a = f'{area}, {price}, {addr}{chr(1)}'
            # list_.append(a)
            if count == len(dong_estate_info):
                print(f'{area}{result_split}{price}{result_split}{addr}')
            else:
                print(f'{area}{result_split}{price}{result_split}{addr}{chr(1)}')
                count += 1

    # 매물 확인 화면 2콤보박스 체인지 인덱스
    def get_dong_real_estate_info2(self, dong_name, esrare_type):
        col_list = ['ESTATE_ADDR', 'ESTATE_AREA', 'ESTATE_PRICE']

        if esrare_type == '':
            self.get_dong_real_estate_info(dong_name)
            return
        else:
            dong_estate_info = self.data.select_dong_real_estate_info2(dong_name, esrare_type, col_list)
        # list_ = []
        count = 1
        for i in dong_estate_info:
            area, price, addr = i
            # a = f'{area}, {price}, {addr}{chr(1)}'
            # list_.append(a)
            if count == len(dong_estate_info):
                print(f'{area}{result_split}{price}{result_split}{addr}')
            else:
                print(f'{area}{result_split}{price}{result_split}{addr}{chr(1)}')
                count += 1
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
    # ex.get_tb_dong_population()
    # ex.get_dong_area_price()
    # ex.select_dong_wash_sales_avg()
    # ex.get_dong_wash_stoer()
    ex.get_dong_real_estate_info("신사동")
    # ex.select_tb_store()
