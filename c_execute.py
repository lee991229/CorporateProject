from DataRead import DataClass
import json


class Execute:
    def __init__(self, command=None):
        super().__init__()
        print('[ 실행 : class execute ]')

        self.data = DataClass()

        if command == 'req_store_info':
            self.select_tb_store()
        elif command == 'req_population_info':
            self.get_tb_dong_population()

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


if __name__ == '__main__':
    ex = Execute()
    ex.select_dong_wash_sales_avg()
