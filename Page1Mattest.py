import sys
sys.path.append("C:/Users/KDT114/Desktop/CorporateProject/venv/Lib/site-packages")


import matplotlib.pyplot as plt
import matplotlib.image as img

from DataRead import DataClass

class Page1Mattest:
    def __init__(self):
        super().__init__()
        self.dict_info = {'청룡동': [304, 164], '은천동': [276, 96], '미성동': [127, 170], '행운동': [363, 138], '성현동': [331, 83],
                          '난곡동': [149, 221], '인헌동': [419, 214], '대학동': [284, 268], '보라매동': [220, 72],
                          '서림동': [262, 197], '신림동': [190, 98], '서원동': [218, 133], '신사동': [130, 107], '삼성동': [204, 292],
                          '조원동': [69, 129], '남현동': [483, 223], '신원동': [184, 156], '낙성대동': [362, 194],
                          '중앙동': [320, 123], '청림동': [381, 90], '난향동': [133, 284]}
        self.img_test = img.imread(r'C:\Users\KDT114\Desktop\CorporateProject\mat_img\dongmap.jpg')
        self.img_gett = r'C:\Users\KDT114\Desktop\CorporateProject\mat_img\dongmap_1.jpg'

    def controls(self, command):
        """커맨더로 함수 실행"""
        if command == "거주인구":
            self.imgchange_1()
        elif command == '행정동별 세탁업 입점수':
            self.imgchange_2()
        elif command == "공시지가":
            self.imgchange_3()
        elif command == "행정동별 월별 매출액":
            self.imgchange_4()

    def imgchange_1(self):
        """
        거주인구 matplotlib를 뽑아냄
        matplotlib를 실행후 바로 종료 -> 이후 사진 저장하여 C#에게 넘겨주기 위함
        """
        plt.figure(figsize=(8, 8))
        plt.imshow(self.img_test)
        plt.rc('font', family='Malgun Gothic')
        db = DataClass()

        list_alldata = db.select_dong_population()  # 거주인구 데이터
        imgchange_1_dict_don = dict()

        for i in list_alldata:
            dong_nameall = db.select_dongname_by_dongcode(i[0])  # 동 이름 데이터모음
            dong_name = dong_nameall[0][0]  # 동 코드에 따른 해당 동 이름
            imgchange_1_dict_don[dong_name] = ""  # 딕셔너리에 이름값담아서 그 값에 따라 넣을려고 key 미리 넣어둠 추후 수정해야함
            self.dict_info[dong_name].append(i[1])
        for i in self.dict_info.keys():  # 해당 동에 정보리스트 담아주기
            imgchange_1_dict_don[i] = self.dict_info[i]

        area_list = list()
        cnt_col = 0

        for i in imgchange_1_dict_don.values():  # 담긴 동 정보를 차트화하는 로직
            x_pos = i[0]
            y_pos = i[1]
            value_ = i[2]
            area_size = int(value_/1000*1.2)
            if area_size < 20:
                color = '#FF1493'
            elif area_size < 25:
                color = '#4B0082'
            elif area_size < 30:
                color = '#0000FF'
            elif area_size < 35:
                color = '#FFFF00'
            else:
                color = '#FF0000'
            plt.plot(x_pos, y_pos, 'o', c=color, markersize=area_size, alpha=0.7, label="")
            if cnt_col%5 == 0:
                plt.plot(x_pos, y_pos, 'o', c=color, markersize=area_size, alpha=0.7, label=f"{area_size}+")

            plt.text(x_pos-6, y_pos+4, f"{area_size}")
            cnt_col += 1
            area_list.append(value_//1000)
        plt.legend(loc='best', markerscale=0.4, title="단위:천", borderpad=2, ncol=5)

        plt.savefig(self.img_gett, format='jpg', dpi=300)
        plt.show(block=False)
        # plt.show()
        plt.close()
        name = ""
        cnt_ = 0
        for i in imgchange_1_dict_don.keys():
            name = name + "," + i
            cnt_ += 1
            if cnt_ == 5:
                break
        print(self.img_gett, name)
        return

    def imgchange_2(self):
        """
        행정동별 세탁업 입점수 matplotlib를 뽑아냄
        matplotlib를 실행후 바로 종료 -> 이후 사진 저장하여 C#에게 넘겨주기 위함
        """
        plt.figure(figsize=(8, 8))
        plt.imshow(self.img_test)
        plt.rc('font', family='Malgun Gothic')
        db = DataClass()

        list_alldata = db.select_wash_stoer_count()  # 행정동별 세탁업 입점수 데이터
        imgchange_2_dict_don = dict()

        for i in list_alldata:
            dong_nameall = db.select_dongname_by_dongcode(i[0])  # 동 이름 데이터모음
            dong_name = dong_nameall[0][0]  # 동 코드에 따른 해당 동 이름
            imgchange_2_dict_don[dong_name] = ""
            self.dict_info[dong_name].append(i[1])
        for i in self.dict_info.keys():
            imgchange_2_dict_don[i] = self.dict_info[i]
        area_list = list()
        cnt_col = 0

        list_value = ["30+", '25+', '20+', '10+', "5+"]
        cnt_inx = 0

        for i in imgchange_2_dict_don.values():
            x_pos = i[0]
            y_pos = i[1]
            value_ = i[2]
            area_size = int(value_*2)
            if value_ < 6:
                color = '#FF1493'
            elif value_ < 10:
                color = '#4B0082'
            elif value_ < 18:
                color = '#0000FF'
            elif value_ < 25:
                color = '#FFFF00'
            else:
                color = '#FF0000'
            plt.plot(x_pos, y_pos, 'o', c=color, markersize=area_size, alpha=0.7, label="")
            if cnt_col % 5 == 0:
                plt.plot(x_pos, y_pos, 'o', c=color, markersize=area_size, alpha=0.7, label=list_value[cnt_inx])
                cnt_inx += 1
            plt.text(x_pos - 6, y_pos + 4, f"{value_}")
            cnt_col += 1
            area_list.append(area_size)

        plt.legend(loc='best', markerscale=0.4, title="단위:개", borderpad=2, ncol=5)
        #
        plt.savefig(self.img_gett, format='jpg', dpi=300)
        plt.show(block=False)
        # plt.show()
        plt.close()
        name = ""
        cnt_ = 0
        for i in imgchange_2_dict_don.keys():
            name = name + "," + i
            cnt_ += 1
            if cnt_ == 5:
                break
        print(self.img_gett, name)
        return

    def imgchange_3(self):
        """
        공시지가 matplotlib를 뽑아냄
        matplotlib를 실행후 바로 종료 -> 이후 사진 저장하여 C#에게 넘겨주기 위함
        """
        plt.figure(figsize=(8, 8))
        plt.imshow(self.img_test)
        plt.rc('font', family='Malgun Gothic')
        db = DataClass()

        list_alldata = db.select_dong_area_price()  # 공시지가 데이터

        imgchange_3_dict_don = dict()

        for i in list_alldata:
            dong_nameall = db.select_dongname_by_dongcode(i[0])  # 동 이름 데이터모음
            dong_name = dong_nameall[0][0]  # 동 코드에 따른 해당 동 이름
            imgchange_3_dict_don[dong_name] = ""
            self.dict_info[dong_name].append(i[1])
        for i in self.dict_info.keys():
            imgchange_3_dict_don[i] = self.dict_info[i]
        area_list = list()
        cnt_col = 0

        list_value = ["600+", '500+', '400+', '300+', "200+"]
        cnt_inx = 0
        for i in imgchange_3_dict_don.values():
            x_pos = i[0]
            y_pos = i[1]
            value_ = i[2]
            area_size = int(value_/100000*0.8)
            if area_size < 20:
                color = '#FF1493'
            elif area_size < 30:
                color = '#4B0082'
            elif area_size < 35:
                color = '#0000FF'
            elif area_size < 40:
                color = '#FFFF00'
            else:
                color = '#FF0000'
            plt.plot(x_pos, y_pos, 'o', c=color, markersize=area_size, alpha=0.7, label="")
            if cnt_col%5 == 0:
                plt.plot(x_pos, y_pos, 'o', c=color, markersize=area_size, alpha=0.7, label=list_value[cnt_inx])
                cnt_inx += 1
            plt.text(x_pos-6, y_pos+4, f"{int(value_/10000)}")
            cnt_col += 1
            area_list.append(area_size)
        plt.legend(loc='best', markerscale=0.4, title="단위:십만", borderpad=2, ncol=5)

        plt.savefig(self.img_gett, format='jpg', dpi=300)
        plt.show(block=False)
        # plt.show()
        plt.close()
        name = ""
        cnt_ = 0
        for i in imgchange_3_dict_don.keys():
            name = name + "," + i
            cnt_ += 1
            if cnt_ == 5:
                break
        print(self.img_gett, name)
        return

    def imgchange_4(self):
        """
        공시지가 matplotlib를 뽑아냄
        matplotlib를 실행후 바로 종료 -> 이후 사진 저장하여 C#에게 넘겨주기 위함
        """
        plt.figure(figsize=(8, 8))
        plt.imshow(self.img_test)
        plt.rc('font', family='Malgun Gothic')
        db = DataClass()

        list_alldata = db.select_dong_wash_sales_avg()  # 월별 매출 데이터

        imgchange_4_dict_don = dict()

        for i in list_alldata:
            dong_nameall = db.select_dongname_by_dongcode(i[0])  # 동 이름 데이터모음
            dong_name = dong_nameall[0][0]  # 동 코드에 따른 해당 동 이름
            imgchange_4_dict_don[dong_name] = ""
            self.dict_info[dong_name].append(i[1])
        for i in self.dict_info.keys():
            imgchange_4_dict_don[i] = self.dict_info[i]

        area_list = list()
        cnt_col = 0
        list_value = ["900+", '880', '850', '700+', "0"]
        cnt_inx = 0
        for i in imgchange_4_dict_don.values():
            x_pos = i[0]
            y_pos = i[1]
            value_ = i[2]

            area_size = int(value_/10*.6)
            if area_size < 46:
                color = '#FF1493'
            elif area_size < 50:
                color = '#4B0082'
            elif area_size < 52:
                color = '#0000FF'
            elif area_size < 53:
                color = '#FFFF00'
            else:
                color = '#FF0000'
            plt.plot(x_pos, y_pos, 'o', c=color, markersize=area_size, alpha=0.7, label="")
            if cnt_col%5 == 0:
                plt.plot(x_pos, y_pos, 'o', c=color, markersize=area_size, alpha=0.7, label=list_value[cnt_inx])
                cnt_inx += 1
            plt.text(x_pos-6, y_pos+4, f"{value_}")
            cnt_col += 1
            area_list.append(area_size)
        plt.legend(loc='best', markerscale=0.4, title="단위:만", borderpad=2, ncol=5)

        plt.savefig(self.img_gett, format='jpg', dpi=300)
        plt.show(block=False)
        # plt.show()
        plt.close()
        name = ""
        cnt_ = 0
        for i in imgchange_4_dict_don.keys():
            name = name + "," + i
            cnt_ += 1
            if cnt_ == 5:
                break
        print(self.img_gett, name)
        return


# if __name__ == '__main__':
#     test = ImageFromMat()
#     test.controls("행정동별 월별 매출액")
# elif control == "행정동별 세탁업 입점수":
#     imgchange_1(control)
# elif control == "공시지가":
#     imgchange_1(control)
