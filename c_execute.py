# import json
import sys

sys.path.append("C:/Users/KDT114/Desktop/CorporateProject/venv/Lib/site-packages")

import Create_map
import Page1Mattest
import Page3Mattest
from DataRead import *

header_split = chr(1)
result_split = chr(2)


class Execute:
    def __init__(self, command=None):
        super().__init__()
        self.data = DataClass()
        self.Page1Mattest = Page1Mattest.Page1Mattest()
        self.Page3Mattest = Page3Mattest.Page3Mattest()

        # self.mattest = imgchange_1()
        if command == 'req_store_info':
            self.select_tb_store()
        elif command == 'req_population_info':
            self.get_tb_dong_population()
        elif 'page_1' in command:
            self.get_page_1_mat(command)
        elif 'page_2' in command:
            self.get_page_2_map(command)
        elif 'page_3' in command:
            self.get_page_3_mat(command)
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

            result = command.split(header_split)[1]
            result = result.split("^")
            print(result)
            self.get_estate_info(result)
        else:
            pass

    def get_page_1_mat(self, command):
        result = command.split(header_split)[1]
        self.Page1Mattest.controls(result)

    def get_page_2_map(self, command):
        if 'start' in command:
            url = Create_map.open_html_()
            print(url)
        else:
            # C#의 첫번째 콤보박스 행정동입니다.
            result_all = command.split(header_split)[1]
            data_all = result_all.split(result_split)
            dong_nm = data_all[0]
            if len(data_all) < 2:
                dong_address = "서울시 관악구 %s" % dong_nm  # "서울시 관악구 청룡동"
                # 행정동명으로 행정동 코드 반환
                dong_code = self.data.select_dong_code(dong_nm)
                # 행정동 코드로 세탁업체 정보 반환
                dong_wash_positions = self.data.select_wash_store(dong_code)
                # 카카오 REST API로 주소 검색 -> 좌표 반환
                address_latlng = Create_map.get_dong_latlng(dong_address)
                # 좌표,세탁업체 정보로 html 스크립트 작성
                first_html = Create_map.wash_store_marker(address_latlng, dong_wash_positions, '4')
                # html 스크립트 완성
                html_complete = Create_map.complete_html_(first_html)
                file_name = "kakao_map_marker.html"
                # .html작성 후 html url 반환
                url = Create_map.save_html_(html_complete, file_name)
                print(url)
            elif len(data_all) == 2:
                dong_address = "서울시 관악구 %s" % (dong_nm)  # "서울시 관악구 청룡동"
                type = data_all[1][-2:]  # 10평 '이하'
                # 행정동 매물 정보 반환
                col_list = ['ESTATE_TYPE', 'ESTATE_LA', 'ESTATE_LO', 'ESTATE_AREA', 'ESTATE_PRICE', 'ESTATE_FLOOR']
                dong_estate_info = self.data.select_dong_real_estate_info(dong_nm, col_list, type)
                # 마커 생성을 위한 자료형으로 변환
                custom_dict = self.data.create_custom_dict('estatePositions', dong_estate_info.tolist())
                # 행정동명으로 행정동 코드 반환
                dong_code = self.data.select_dong_code(dong_nm)
                # 행정동 코드로 세탁업체 정보 반환
                dong_wash_positions = self.data.select_wash_store(dong_code)
                # 카카오 REST API로 주소 검색 -> 좌표 반환
                address_latlng = Create_map.get_dong_latlng(dong_address)
                # 좌표,세탁업체 정보로 html 스크립트 작성
                first_html = Create_map.wash_store_marker(address_latlng, dong_wash_positions, '5')
                # 매물 정보로 html 스크립트 작성
                second_html = Create_map.create_estate_cluster(custom_dict, first_html)
                # html 스크립트 완성
                html_complete = Create_map.complete_html_(second_html)
                file_name = "kakao_map_marker.html"
                # .html작성 후 html url 반환
                url = Create_map.save_html_(html_complete, file_name)
                print(url)

    def get_page_3_mat(self, command):
        if "map" in command:
            print("map을 타세용")
        else:
            result = command.split(header_split)[1]
            self.Page3Mattest.controls(result)

    # 매물 확인 화면 1콤보박스 체인지 인덱스
    def get_dong_real_estate_info(self, dong_name):
        col_list = ['ESTATE_ADDR', 'ESTATE_AREA', 'ESTATE_PRICE']
        dong_estate_info = self.data.select_dong_real_estate_info1_1(dong_name, col_list)
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

        if esrare_type == "모두보기":
            dong_estate_info = self.data.select_dong_real_estate_info1_1(dong_name, col_list)
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
            # print('모두보기 들어옴?')
            # self.get_dong_real_estate_info(dong_name)
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

    # 행정동별 세탁업 입점수
    def get_dong_wash_stoer(self):
        dong = self.data.select_dong_info()
        wash_stoer_count_dict = {}
        for i in dong:
            dong_code = i[1]
            dong_name = i[2]
            ws_stoer_count = self.data.select_wash_stoer_count()
            wash_stoer_count_dict[dong_name] = ws_stoer_count

        print(wash_stoer_count_dict)

    # # 동 코드로 상권 변화지표 반환
    # def select_dong_sign(self, dong_code):
    #     df = pd.read_sql(f"select \"DONG_SIGN\" from \"TB_DONG\" where \"DONG_CODE\" = {dong_code}", self.engine)
    #     return df.values

    def get_estate_info(self, result):
        addr, dong_name = result
        print(addr, dong_name)
        col_list = ['ESTATE_LA', 'ESTATE_LO']
        result1 = self.data.select_estate_info(addr, col_list)
        dong_code = self.data.select_dong_code(dong_name)
        result2 = self.data.select_dong_sign(dong_code)
        print(result1)
        radius_dict = self.data.calculate_distance(result1)
        html_script_1 = Create_map.create_radius_html(result1[0], radius_dict)
        html_script_2 = Create_map.complete_html_(html_script_1)
        url = Create_map.save_html_(html_script_2, 'kakao_map_radius.html')

        # print() : url이 추가 되었습니다.
        print(result1[0][0], header_split, result1[0][1], header_split, result2[0][0], header_split, dong_name,
              header_split, dong_code, header_split, url)

    # def get_estate_info(self, result):
    #     addr, dong_name = result
    #     col_list = ['ESTATE_LA', 'ESTATE_LO']
    #     result1 = self.data.select_estate_info(addr, col_list)
    #     # if len(result1) > 1:
    #     #     result1 = result1[0]
    #     dong_code = self.data.select_dong_code(dong_name)
    #     result2 = self.data.select_dong_sign(dong_code)
    #
    #     # print(dong_code)
    #     # print(result2)
    #     print(result1[0][0], header_split, result1[0][1], header_split, result2[0][0], header_split, dong_name,
    #           header_split, dong_code)


if __name__ == '__main__':
    ex = Execute()
    a = ["서울특별시 관악구 봉천동 464-13", "성현동"]
    ex.get_estate_info(a)
    # ex.get_dong_area_price()
    # ex.select_dong_wash_sales_avg()
    # ex.get_dong_wash_stoer()
    # ex.get_dong_real_estate_info("신사동")
    # ex.select_tb_store()
