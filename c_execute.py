# import json
# 호현이 코드
# import Page1Mattest
# import Page3Mattest
import Create_map
from DataRead import *

header_split = chr(1)
data_split = chr(2)

class Execute:
    def __init__(self, command=None):
        super().__init__()
        self.data = DataClass()
        # 호현이 코드
        # self.Page1Mattest = Page1Mattest.Page1Mattest()
        # self.Page3Mattest = Page3Mattest.Page3Mattest()

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
            self.get_estate_info(result)

    def get_page_1_mat(self, command):
        result = command.split(header_split)[1]
        # self.Page1Mattest.controls(result)


    def get_page_2_map(self, command):
        if 'start' in command:
            url = Create_map.open_html_()
            print(url)
        else:
            # C#의 첫번째 콤보박스 행정동입니다.
            result_all = command.split(header_split)[1]
            data_all = result_all.split(data_split)
            dong_nm = data_all[0]
            if len(data_all) < 2:
                dong_address = "서울시 관악구 %s" % dong_nm # "서울시 관악구 청룡동"
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
                dong_address = "서울시 관악구 %s %s" % (dong_nm, data_all[1])  # "서울시 관악구 청룡동 10평 이하"
                # 행정동 매물 정보 반환
                col_list = ['ESTATE_TYPE', 'ESTATE_LA', 'ESTATE_LO', 'ESTATE_AREA', 'ESTATE_PRICE', 'ESTATE_FLOOR']
                dong_estate_info = self.data.select_dong_real_estate_info(dong_nm, col_list)
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
        result = command.split(header_split)[1]
        # self.Page3Mattest.controls(result)

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
            ws_stoer_count = self.data.select_wash_stoer_count(dong_code)
            wash_stoer_count_dict[dong_name] = ws_stoer_count

        print(wash_stoer_count_dict)

    def get_estate_info(self, result):
        addr, dong_name = result
        col_list = ['ESTATE_LA', 'ESTATE_LO']
        result1 = self.data.select_estate_info(addr, col_list)
        dong_code = self.data.select_dong_code(dong_name)
        result2 = self.data.select_dong_sign(dong_code)

        tu_latlng = tuple(result1)
        radius_dict = self.data.calculate_distance(tu_latlng)
        html_script_1 = Create_map.create_radius_html(result1, radius_dict)
        html_script_2 = Create_map.complete_html_(html_script_1)
        url = Create_map.save_html_(html_script_2, 'kakao_map_radius.html')

        # print() : url이 추가 되었습니다.
        print(result1[0][0], header_split, result1[0][1], header_split, result2[0][0], header_split, dong_name,
              header_split, dong_code, header_split, url)


if __name__ == '__main__':
    ex = Execute()
    # ex.select_dong_wash_sales_avg()