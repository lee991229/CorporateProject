import sys

sys.path.append("C:/Users/KDT114/Desktop/CorporateProject/venv/Lib/site-packages")
import psycopg2 as pg
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import os


class DataClass:
    def __init__(self):
        # print(sys.path)
        self.pgdb = pg.connect(
            host='10.10.20.114',
            # host='localhost',
            dbname='Data',
            user='postgres',
            password='ilsan1236526',
            port=5432
        )
        self.engine = create_engine(f'postgresql://postgres:ilsan1236526@10.10.20.114:5432/Data')

    def end_conn(self):
        self.pgdb.close()

    # 동 코드로 상권 변화지표 반환
    def select_dong_sign(self, dong_code):
        df = pd.read_sql(f"select \"DONG_SIGN\" from \"TB_DONG\" where \"DONG_CODE\" = {dong_code}", self.engine)
        return df.values

    # 매물 상세 정보 데이터들 정제
    def select_estate_info(self, addr, col_list):
        size = len(col_list)
        sql = "select "

        if size > 1:
            for col in col_list:
                if col == col_list[0]:
                    sql += f'\"{col}\"'
                else:
                    sql += f',\"{col}\"'

        sql += f" from \"TB_REAL_ESTATE\" where \"ESTATE_ADDR\" = '{addr}'"

        df = pd.read_sql(sql, self.engine)
        df = df.drop_duplicates(subset=['ESTATE_LA', 'ESTATE_LO'])
        return df.values

    # 2페이지 테이블 띄울 매물 데이터
    def select_dong_real_estate_info(self, dongname, col_list):
        size = len(col_list)
        sql = "select "

        if size > 1:
            for col in col_list:
                if col == col_list[0]:
                    sql += f'\"{col}\"'
                else:
                    sql += f',\"{col}\"'

        sql += f" from \"TB_REAL_ESTATE\" where \"DONG_NM\" = '{dongname}'"

        df = pd.read_sql(sql, self.engine)
        return df.values

    def select_dong_real_estate_info2(self, dongname, esrare_type, col_list):
        size = len(col_list)
        sql = "select "

        if size > 1:
            for col in col_list:
                if col == col_list[0]:
                    sql += f'\"{col}\"'
                else:
                    sql += f',\"{col}\"'

        sql += f" from \"TB_REAL_ESTATE\" where \"DONG_NM\" = '{dongname}' and \"ESTATE_TYPE\" = '{esrare_type}'"

        df = pd.read_sql(sql, self.engine)
        return df.values

    # 행정동 별 입점해 있는 세탁업 수
    def select_wash_stoer_count(self):
        df = pd.read_sql(f"select * from \"TB_WASH_STORE\"", self.engine)
        counted = df['DONG_CODE'].value_counts().reset_index().values.tolist()
        return counted

    # 상권 데이터 반환
    def select_data(self):
        df = pd.read_sql(f"select * from \"TB_STORE\"", self.engine)
        return df.values

    # 행정동별 행정동코드,거주인구를 내림차순 반환
    def select_dong_population(self):
        df = pd.read_sql(f"select \"DONG_CODE\",\"DONG_POPULATION\" from \"TB_PEOPLE\"", self.engine)
        df = df.sort_values(by='DONG_POPULATION', ascending=False)
        return df.values

    # 행정동별 행정동코드, 공시지가 내림차순 반환
    def select_dong_area_price(self):
        df = pd.read_sql(f"select \"DONG_CODE\",\"DONG_AREA_PRICE\" from \"TB_ESTATE\"", self.engine)
        df = df.sort_values(by='DONG_AREA_PRICE', ascending=False)
        return df.values

    # 행정동별 행정동코드, 매출액 내림차순 반환
    def select_dong_wash_sales_avg(self):
        df = pd.read_sql(f"select \"DONG_CODE\",\"DONG_WASH_SALES_AVG\" from \"TB_ESTATE\"", self.engine)
        df = df.sort_values(by='DONG_WASH_SALES_AVG', ascending=False)
        return df.values

    # 행정동명에 따른 행정동 코드 반환
    def select_dong_code(self, dongname):
        cursor = self.pgdb.cursor()
        cursor.execute(f"select \"DONG_CODE\" from \"TB_DONG\" where \"DONG_NAME\" = '{dongname}'")
        dong_code = cursor.fetchone()[0]
        return dong_code

    # 동코드를 받아서 동이름을 반환
    def select_dongname_by_dongcode(self, dongcode):
        df = pd.read_sql(f"select \"DONG_NAME\" from \"TB_DONG\" where \"DONG_CODE\" = {dongcode}", self.engine)
        return df.values

    # def select_dongcode_by_dongname(self, dong_name):
    #     df = pd.read_sql(f"select \"DONG_CODE\" from \"TB_DONG\" where \"DONG_NAME\" = {dong_name}", self.engine)
    #     return df.values

    # 행정동들 정보 반환
    def select_dong_info(self):
        df = pd.read_sql(f"select * from \"TB_DONG\"", self.engine)
        return df.values

    # # 행정동별 평균 영업기간
    # def select_dong_info(self):
    #     df = pd.read_sql(f"select * from \"TB_DONG\"", self.engine)
    #     return df.values

    # def select_real_estate_info(self):
    #     df = pd.read_sql(
    #         f"select \"ESTATE_ID\",\"DONG_NM\",\"ESTATE_AREA\",\"ESTATE_PRICE\",\"ESTATE_FLOOR\",\"ESTATE_LA\",\"ESTATE_LO\",\"ESTATE_ADDR\" from \"TB_REAL_ESTATE\"",
    #         self.engine)
    #     return df.values

    # 매물 정보 반환
    def select_real_estate_info(self, dongname, col_list):
        size = len(col_list)
        sql = "select "

        if size > 1:
            for col in col_list:
                if col == col_list[0]:
                    sql += f'\"{col}\"'
                else:
                    sql += f',\"{col}\"'

        sql += f" from \"TB_REAL_ESTATE\" where \"DONG_NM\" = '{dongname}'"

        df = pd.read_sql(sql, self.engine)
        return df.values.tolist()
    # 인구 상세정보
    def select_people_detail(self, dongcode):
        df = pd.read_sql(f"select * from \"TB_PEOPLE_DETAIL\" where \"DONG_CODE\" = {dongcode}", self.engine)
        return df.values
    # 평균 영업기간, 증감률
    def select_wash_change(self):
        df = pd.read_sql(
            f"select \"DONG_NAME\",\"DONG_AVG_PERIOD\",\"CHANGE_RATE\" from \"TB_WASH_CHANGE\"",
            self.engine)
        return df.values


if __name__ == '__main__':
    db = DataClass()
    a = db.select_wash_change()
    print(a)
    # for i in a[0]:
    #     print(i)
    #     print(type(i))

# list_1 = []
# dict_1 = {}
# for i in a:
#     dong_code = i[0]
#     population = i[1]
#     # print(dong_code)
#     population_data = db.select_dong(dong_code)
#     list_1.append(population_data[0][0])
#     dict_1[population_data[0][0]] = population
# print(dict_1)

# print(a)
