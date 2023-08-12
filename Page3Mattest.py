import sys
sys.path.append("C:/Users/KDT114/Desktop/CorporateProject/venv/Lib/site-packages")

import numpy as np
from matplotlib.animation import FuncAnimation


import matplotlib.pyplot as plt
import matplotlib.image as img
from DataRead import DataClass
from geopy import distance


class Page3Mattest:
    """3번 페이지 차트 시각화 및 이미지 저장을 위한 클래스입니다."""
    db = DataClass()

    def __init__(self):
        super().__init__()
        self.img_gett = r'C:\Users\KDT114\Desktop\CorporateProject\mat_img\dongmap_2.jpg'

    def controls(self, command: list):
        """커맨더를 통해 해당 카테고리에 맞는 차트를 생성하는 기능입니다."""
        if command[0] == "주변상권":
            self.imgchange_1(command[1:])
        elif command[0] == "거주인구":
            self.imgchange_2(command[1:])
        elif command[0] == "평균영업기간":
            self.imgchange_3(command[1:])

    def imgchange_1(self, estate_pos=None):
        """매물 위치 정보를 받으면 그 값을 토대로 주변 500m 상권 갯수 파악 이후 차트화하는 기능
        3페이지 차트 표시에 띄울 목적입니다."""
        if estate_pos is None:
            estate_pos = ["37.482718", "126.939435"]
        storedata = self.db.select_data()  # 상권 데이터
        if len(estate_pos) > 1:  # 매물 정보가 파라미터로 들어오면 그 값으로 계산 할 것
            pos_x = estate_pos[0]
            pos_y = estate_pos[1]

        dong_cnt = dict()  # 주변 상권 갯수 체크를 위한 딕셔너리형태의 변수
        for i in storedata:
            store_pos_x = i[6]
            store_pos_y = i[7]
            if self.haversine_distance(pos_x, store_pos_x, pos_y, store_pos_y) <= float(
                    500):  # return값이 500이하라면 500m주변으로 해당됨
                if i[2] in dong_cnt.keys():  # 해당 상권이 중복되면 +1을 아니라면 1을 적용
                    dong_cnt[i[2]] = dong_cnt[i[2]] + 1
                else:
                    dong_cnt[i[2]] = 1

        self.ratio = list()  # 해당 상권의 갯수를 리스트화함
        self.labels = list()  # 해당 상권의 이름을 리스트화 함
        for i in dong_cnt.keys():
            self.labels.append(i)
        for i in dong_cnt.values():
            self.ratio.append(i)
        self.mat_cart(self.labels, self.ratio)

    def imgchange_2(self, dong_name=None):
        """해당 행정동의 거주인구 수 및 연령대별 성별,
        인구 분포도를 차트화 하는 기능입니다."""
        dong_code = None
        if dong_name is None:
            dong_name = "청룡동"
            dong_code = "11620595"
        dong_population = self.db.select_dong_population()
        for i in dong_population:
            code = i[0]
            name = self.db.select_dongname_by_dongcode(code)
            if name[0][0] == dong_name[0]:
                dong_code = i[0]
                break
        dong_people_detail = self.db.select_people_detail(dong_code)  # 행정동별 거주인구 정보 데이터

        # 행정동별 거주인구 세부 정보 데이터 칼럼명입니다. 다듬기 위해 딕셔너리로 넣어놨어요
        dong_info_dict = {'PEOPLE_ID': '', 'DONG_CODE': '', 'DONG_TOTAL': '', 'DONG_MAN': '', 'DONG_WOMAN': '',
                          'DONG_M_RATE': '', 'DONG_F_RATE': '', 'DONG_M_20': '', 'DONG_F_20': '', 'DONG_M_30': '',
                          'DONG_F_30': '', 'DONG_M_40': '', 'DONG_F_40': '', 'DONG_M_50': '', 'DONG_F_50': '',
                          'DONG_M_ETC': '', 'DONG_F_ETC': ''}

        # 행정동별 거주인구 세부정보 데이터가 float형태이므로 다듬기 및 딕셔너리화 하는 로직입니다.
        for label, value in zip(dong_info_dict, dong_people_detail[0]):
            dong_info_dict[label] = value
        for i in dong_info_dict.items():
            if i[0] == "DONG_M_RATE" or i[0] == "DONG_F_RATE":
                pass
            else:
                dong_info_dict[i[0]] = int(dong_info_dict[i[0]])

        print(dong_info_dict) # 다듬은 이후 정상적으로 담긴 값
        for label, vlaue in dong_info_dict.items():
            print(label, vlaue)


    def imgchange_3(self):
        """해당 행정동의 셀프빨래방 평균 영업기간을
        차트화 하는 기능입니다."""
        pass

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """위 경도 값을 비교하여 거리 계산해주는 기능
        매물 주변 500m 상권을 파악하기 위해 필요함"""
        newport_ri = (lat1, lat2)
        cleveland_oh = (lon1, lon2)
        value = distance.distance(newport_ri, cleveland_oh).meters  # 단위는 meters
        return value

    def mat_cart(self, label, value):
        """라벨값과 벨류값을 받아 꺾은선그래프와 막대그래프를 생성하고
        저장하고 경로를 프린트하는 기능을 합니다.
        주의 : 해당 파일에 print가 1개이상일경우 C# process output기능이 정상적으로 작동하지 않을 수 있습니다."""
        plt.rc('font', family='Malgun Gothic')
        plt.rcParams["figure.figsize"] = (10, 10)

        fig, ax1 = plt.subplots()

        ax1.plot(label, value, '-s', color='green', markersize=7, linewidth=5, alpha=0.7, label='Price')
        ax1.set_xlabel('주변 상권')
        ax1.tick_params(axis='both', direction='in')

        ax2 = ax1.twinx()
        bar = ax2.bar(label, value, color='blue', label='Demand', alpha=0.7, width=0.7)
        ax2.tick_params(axis='y', direction='in')

        for rect in bar:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%.1f' % height, ha='center', va='bottom', size=12)

        plt.savefig(self.img_gett, format='jpg', dpi=300)
        plt.show(block=False)
        plt.close()
        print(self.img_gett)

    def animation_mat(self, value: list):
        """value리스트를 파라미터로 받아서
        애니메이션 차트화 한후 gif파일로 저장시켜준다."""
        fig = plt.figure(figsize=(10, 10))
        axes = fig.add_subplot(1, 1, 1)
        axes.set_ylim(0, 100)
        self.y_ = [[] for _ in range(10)]

        for idx, value in enumerate(value):
            for i in range(11):
                self.y_[idx].append(int(value / 10 * i))

        ani = FuncAnimation(fig, self.animate, save_count=15, interval=100)
        ani.save('exAnimation.gif', writer='imagemagick', fps=60, dpi=100)
        plt.show()

    def animate(self, i):
        """FuncAnimation 메서드를 통해 애니메이션 시키는
        함수 반복적으로 i값을 받아 값을 변화시키는 기능을한다.
        주의 :무조건 animation_mat 다움에 써야함 self.y_ 값이 생성되어야 함"""
        if i == 11:
            sys.exit()
        list_value = list()
        for j in self.y_:
            list_value.append(j[i % 11])

        plt.bar(self.labels, list_value)


if __name__ == '__main__':
    test = Page3Mattest()
    # test.controls(["주변상권", "37.482718",  "126.939435"])  # 주변상권 차트화에 필요한 파라미터는 "주변상권, "해당매물위경도값" 입니다.
    test.controls(["거주인구", "청룡동"])  # 거주인구 차트화에 필요한 파라미터는 "거주인구", "해당동 이름" 입니다.
    # test.controls(["평균영업기간", "청룡동"])  # 평균영업기간 차트화에 필요한 파라미터는 "평균영업기간", "해당동 이름" 입니다.
