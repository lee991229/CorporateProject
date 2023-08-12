import psycopg2 as pg
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import geopy.distance
from sklearn.preprocessing import MinMaxScaler

class AnalyzeData:
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
        self.create = 0

        # self.pearson_df()
        # df = self.concat_df()
        # self.minmax_result()
        df = self.concat_df()
        self.minmax_result(df)

    def concat_df(self):
        try_ = 0
        latlng_list = self.get_dong_estate_lat_lng(37.484977,126.959538)
        dfs_to_concat = []

        for latlng in latlng_list:
            new_df = self.in_500m_store_df(latlng)
            dfs_to_concat.append(new_df)
            try_ += 1

        # AttributeError: 'DataFrame' object has no attribute 'append'. Did you mean: '_append'?
        # pandas 2.0.0 버전 이후부터 'append()' Method가 완전히 제거되었음.
        completed_df = pd.concat(dfs_to_concat, ignore_index=True)

        return completed_df

    def end_conn(self):
        self.pgdb.close()

    # 매물 주소로 정보 반환
    def get_dong_estate_lat_lng(self, lat, lng):
        sql = f"select \"DONG_NM\" from \"TB_REAL_ESTATE\" where \"ESTATE_LA\" = '{lat}' and \"ESTATE_LO\" = '{lng}'"
        cur = self.pgdb.cursor()
        cur.execute(sql)
        dong_nm = cur.fetchone()[0]

        sql_ = f"select  \"ESTATE_LA\", \"ESTATE_LO\" from \"TB_REAL_ESTATE\" where \"DONG_NM\" = '{dong_nm}'"
        cur_ = self.pgdb.cursor()
        cur_.execute(sql_)
        latlng_list = cur_.fetchall()

        return latlng_list

    # STORE_APART의 값을 중복없이 열로 처리하여 분석 데이터프레임 생성
    def in_500m_store_df(self, latlng:tuple):
        store_df = pd.read_sql(f"select \"STORE_APART\", \"STORE_LO\", \"STORE_LA\" from \"TB_STORE\"", self.engine)
        data = []
        user_facility = ['카페', 'PC방', '편의점', '서점']
        service_facility = ['헬스장', '미용실', '기숙사/고시원', '목욕탕/사우나']
        rival_facility = ['셀프 빨래방', '세탁소']

        for i, row in store_df.iterrows():
            distance = geopy.distance.distance(latlng, (store_df.STORE_LO[i], store_df.STORE_LA[i])).km * 1000
            if store_df.STORE_APART[i] in user_facility:
                idx = '사용자'
            elif store_df.STORE_APART[i] in service_facility:
                idx = '용역'
            elif store_df.STORE_APART[i] in rival_facility:
                idx = '경쟁'
            if distance <= 500.000000 and idx == '경쟁':
                data.append(
                    [store_df.STORE_APART[i], distance, idx])


        df = pd.DataFrame(data, columns=['apart', 'distance', 'type'])

        score = 0
        total = 0

        for i in range(len(df)):
            distance = df.loc[i, 'distance']
            if distance <= 100:
                score = 1.0
            elif 100 < distance <= 200:
                score = 0.9
            elif 200 < distance <= 300:
                score = 0.7
            elif 300 < distance <= 400:
                score = 0.5
            elif 400 < distance <= 500:
                score = 0.3

            total += score
            df.loc[i, 'score'] = score

        df['total'] = total
        rival_df = df.loc[[0]]

        return rival_df

        # # 'type'이 같은 경우 갯수를 세어 'count' 열을 추가하는 작업
        # df['count'] = df.groupby('type')['apart'].transform('count')

        # 새로운 데이터프레임 생성 (distance 열을 제외하고)
        # new_df = df.drop_duplicates('type')[['type', 'count']]
        # new_df = new_df.sort_values(by='count', ascending=False)
        # new_df = df.set_index(keys='type')
        # new_df = new_df.transpose()
        # new_df['total'] = new_df['사용자'] + new_df['용역']
        # new_df['lat'] = latlng[0]
        # new_df['lng'] = latlng[1]

        # new_df = new_df[['apart', 'distance', 'type', 'lat', 'lng']]

        # return new_df

    def pearson_df(self):
        df = pd.read_csv('./pearson_person.csv', thousands=',')  # 천단위 표시용 쉼표 제거
        df = df.apply(lambda x: x.str.replace(',', '').astype(float) if x.name in df.select_dtypes(
            include=[object]).columns else x)
        Analyzed_df = df.corr(method='pearson')
        Analyzed_df.to_csv('output_person.csv', index=False)


    def minmax_result(self, df):
        train_array = np.arange(0, 11).reshape(-1, 1)
        scaler = MinMaxScaler()
        scaler.fit(train_array)
        train_scaled=scaler.transform(train_array)

        test_array = df['total'].values.reshape(-1, 1)
        test_min = test_array.min()
        test_max = test_array.max()

        test_scaled = scaler.transform((test_array - test_min) / (test_max - test_min))
        scaled_list = np.round(test_scaled.reshape(-1), 2) * 100
        df['total'] = scaled_list
        df.to_csv('output_rival.csv', index=False)


# if __name__ == '__main__':
    # Analyze = AnalyzeData()