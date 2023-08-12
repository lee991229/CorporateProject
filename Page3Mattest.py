import sys
import time

sys.path.append("C:/Users/KDT114/Desktop/CorporateProject/venv/Lib/site-packages")

import numpy
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
        self.img_gett = r'C:\Users\kdt114\Desktop\CorporateProject\mat_img\dongmap_2.jpg'
        self.img_gett_2 = r'C:\Users\kdt114\Desktop\CorporateProject\mat_img\dongmap_3.jpg'
        self.img_gett_3 = r'C:\Users\kdt114\Desktop\CorporateProject\mat_img\dongmap_4.jpg'
        self.cnt = -0.2

    def controls(self, command: list):
        """커맨더를 통해 해당 카테고리에 맞는 차트를 생성하는 기능입니다."""
        result = command.split(chr(1))
        # print(command)
        # print(result)
        result_2 = result[0].split(chr(3))
        image_1 = result_2[0].split(chr(2))

        if image_1[0] == "주변 상권 수":
            self.imgchange_1(image_1[1:])

        elif image_1[0] == "연령대 비율":
            self.imgchange_2(image_1[1:])

        elif image_1[0] == "평균 영업 기간":
            self.imgchange_3(image_1[1:])
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

        label_1 = list()  # 해당 상권의 이름을 리스트화 함
        # label_2 = list()  # 해당 상권의 이름을 리스트화 함
        ratio_1 = list()  # 해당 상권의 갯수를 리스트화함
        # ratio_2 = list()  # 해당 상권의 갯수를 리스트화함
        for label, value in dong_cnt.items():
            label_1.append(label)
            ratio_1.append(value)
        subplot = (1, 1, 1)
        type_ = {"bar": [label_1, ratio_1], "broken": [label_1, ratio_1]}
        self.mat_cart(subplot, type_, False, 0)

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
        label_pop_list = ["DONG_M_RATE", "DONG_F_RATE", "PEOPLE_ID", "DONG_CODE"]
        for label, value in dong_info_dict.items():
            if label in label_pop_list:
                pass
            else:
                dong_info_dict[label] = int(dong_info_dict[label])
        # dong_info_dict["DONG_M_RATE"] = dong_info_dict["DONG_TOTAL"]*(dong_info_dict["DONG_M_RATE"]/100)
        dong_info_dict.pop("DONG_M_RATE")
        dong_info_dict.pop("DONG_F_RATE")
        dong_info_dict.pop("PEOPLE_ID")
        dong_info_dict.pop("DONG_CODE")
        # print(dong_info_dict) # 다듬은 이후 정상적으로 담긴 값
        labels = list()  # 해당 거주인구 상세정보 컬럼을 리스트화 함

        value_1 = list()  # 해당 거주인구 상세정보 밸류값을 리스트화 함
        value_2 = list()  # 해당 거주인구 상세정보 밸류값을 리스트화 함
        for label, vlaues in dong_info_dict.items():
            labels.append(label)
            if "DONG_M" in label:
                value_1.append(vlaues)
            elif "DONG_F" in label or "DONG_W" in label:
                value_2.append(vlaues)
        negative_value_1 = list()
        for idx, val in enumerate(value_2):
            negative_value_1.append(-val)
        label_1 = [f"{dong_name[0]} 전체 인구", "20대", "30대", "40대", "50대", "그외 연령대"]

        subplot = (1, 1, 1)
        type_ = {"Barh_1": [label_1, negative_value_1, "b"], "Barh_2": [label_1, value_2, "r"]}
        self.mat_cart(subplot, type_, True, 1)


    def imgchange_3(self, dong_name=None):
        """해당 행정동의 셀프빨래방 평균 영업기간을
        차트화 하는 기능입니다."""
        if dong_name is None:
            dong_name = "청룡동"
        label_1 = list()
        values_2 = list()
        values_3 = list()
        dong_wash_change = self.db.select_wash_change()
        for i in dong_wash_change.tolist():
            label = i[0]
            value_2 = i[1]
            value_3 = i[2]
            label_1.append(label)
            values_2.append(value_2)
            values_3.append(value_3)
        subplot = (1, 1, 1)
        type_ = {"bar_2": [label_1[1:], values_2[1:]], "bar_3": [label_1[1:], values_3[1:]]}
        self.mat_cart(subplot, type_, True, 2)

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """위 경도 값을 비교하여 거리 계산해주는 기능
        매물 주변 500m 상권을 파악하기 위해 필요함"""
        newport_ri = (lat1, lat2)
        cleveland_oh = (lon1, lon2)
        value = distance.distance(newport_ri, cleveland_oh).meters  # 단위는 meters
        return value

    def mat_cart(self, subplot_list, chart_type=dict[str:list], type_=type[bool], idx_page=type[int]):
        """라벨값과 벨류값을 받아 꺾은선그래프와 막대그래프를 생성하고
        저장하고 경로를 프린트하는 기능을 합니다.
        주의 : 해당 파일에 print가 1개이상일경우 C# process output기능이 정상적으로 작동하지 않을 수 있습니다."""
        plt.rc('font', family='Malgun Gothic')
        plt.rcParams["figure.figsize"] = (12, 8)

        if type_:
            plt.subplots(subplot_list[0])
        else:
            fig, ax_1 = plt.subplots()
            plt_ = [ax_1]
            for _ in chart_type:
                plt_.append(self.mat_twinx_clone(ax_1))
        try:
            for chart, value in chart_type.items():
                if "bar" in chart:
                    self.mat_bar_chatr(plt, value[0], value[1])  # 막대 그래프 만드는 함수
                elif "broken" in chart:
                    self.mat_broken_chart(plt, value[0], value[1])  # 꺾은선 그래프 만드는 함수
                elif "Barh" in chart:
                    self.mat_barh_chart(plt, value[0], value[1], value[2])  # 양방향 그래프 만드는 함수
        except:
            for chart, value in chart_type.items():
                if "bar" in chart:
                    self.mat_bar_chatr(plt_, value[0], value[1])  # 막대 그래프 만드는 함수
                elif "broken" in chart:
                    self.mat_broken_chart(plt_, value[0], value[1])  # 꺾은선 그래프 만드는 함수
                elif "Barh" in chart:
                    self.mat_barh_chart(plt_, value[0], value[1], value[2])  # 양방향 그래프 만드는 함수



        list_return_page = [self.img_gett, self.img_gett_2, self.img_gett_3]
        page = list_return_page[idx_page]

        plt.savefig(page, format='jpg', dpi=300)
        plt.show(block=False)
        # plt.show()
        plt.close()
        print(page)


    def mat_twinx_clone(self, plt_orginal):
        plt_clone = plt_orginal.twinx()
        return plt_clone

    def mat_bar_chatr(self, plt_, label_, value_):
        """차트 타입 :
        막대 그래프입니다."""
        if type(plt_) == type(plt):
            plt_.rc('font', family='Malgun Gothic')
            plt_.rcParams["figure.figsize"] = (20, 20)
            x = numpy.arange(len(label_))
            if self.cnt <= 0:
                type_chart = "상반기"
                color = '#FF0000'
            else:
                type_chart = "하반기"
                color = '#0000FF'
            plt_.bar(x+self.cnt, value_, label=type_chart, width=0.4, color=color, alpha=.5)
            for i, j in zip(x, value_):
                plt.text(i+self.cnt-.2, j, f"{j}")

            plt_.xticks(x, label_)
            plt_.title("행정동별 평균 영업기간", fontsize=24)
            plt_.legend()
            plt_.xlabel("동이름")
            plt_.ylabel("개수")
            plt_.tick_params(axis='x', bottom=False)
            self.cnt += 0.4
        elif type(plt_) == list:

            x = numpy.arange(len(label_))
            plt_[0].bar(x, value_, width=0.4, alpha=.5)
            for i, j in zip(x, value_):
                plt_[0].text(i-.1, j+1, f"{j}")
            # plt_[1].title("행정동별 평균 영업기간", fontsize=24)

    def mat_broken_chart(self, plt_, label_, value_):
        """차트 타입 :
        꺾은선 그래프입니다."""
        if type(plt_) == tuple:

            plt_[1].plot(label_, value_)
        else:

            plt_[0].plot(label_, value_, '-s', color='green', markersize=7, linewidth=5, alpha=0.7, label='Price')
            self.cnt += 1

    def mat_barh_chart(self, plt_, label_, value_, color_):
        """차트 타입 :
        수평 막대 그래프입니다."""
        if type(plt_) == type(plt):
            y = numpy.arange(0, len(label_))
            plt_.rcParams["figure.figsize"] = (12, 8)
            plt_.ylim([-0.2, 1.2])
            plt_.barh(y*.2, value_, color=color_, height=0.2, alpha=.7, linewidth=1, edgecolor='black')
            plt_.legend(ncols=2, labels=["남자", "여자"])
            plt_.title("행정동 연령대별 인원수", fontsize=24)
            plt_.yticks(y*.2, label_)
            plt_.ylabel('연령대')
            plt_.xlabel("연령별 인원수")
        else:
            plt_[int(self.cnt)].barh(label_, value_, color=color_)
            self.cnt += 1

    # def animation_mat(self, value: list):
    #     """value리스트를 파라미터로 받아서
    #     애니메이션 차트화 한후 gif파일로 저장시켜준다."""
    #     fig = plt.figure(figsize=(10, 10))
    #     axes = fig.add_subplot(1, 1, 1)
    #     axes.set_ylim(0, 100)
    #     self.y_ = [[] for _ in range(10)]
    #
    #     for idx, value in enumerate(value):
    #         for i in range(11):
    #             self.y_[idx].append(int(value / 10 * i))
    #
    #     ani = FuncAnimation(fig, self.animate, save_count=15, interval=100)
    #     ani.save('exAnimation.gif', writer='imagemagick', fps=60, dpi=100)
    #     plt.show()

    # def animate(self, i):
    #     """FuncAnimation 메서드를 통해 애니메이션 시키는
    #     함수 반복적으로 i값을 받아 값을 변화시키는 기능을한다.
    #     주의 :무조건 animation_mat 다움에 써야함 self.y_ 값이 생성되어야 함"""
    #     if i == 11:
    #         sys.exit()
    #     list_value = list()
    #     for j in self.y_:
    #         list_value.append(j[i % 11])
    #
    #     plt.bar(self.labels, list_value)


if __name__ == '__main__':
    test = Page3Mattest()
    test.controls(f"주변 상권 수{chr(2)}{37.120}{chr(2)}{127.00}")  # 주변상권 차트화에 필요한 파라미터는 "주변상권", "해당매물위경도값" 입니다.
    # test.controls(f"연령대 비율{chr(2)}청룡동")  # 거주인구 차트화에 필요한 파라미터는 "거주인구", "해당동 이름" 입니다.
    # test.controls(["평균 영업 기간", "청룡동"])  # 평균영업기간 차트화에 필요한 파라미터는 "평균영업기간", "해당동 이름" 입니다.
