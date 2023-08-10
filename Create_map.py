import requests
import webbrowser

from DataRead import *

APP_KEY = '2221b45b290135e593397273c1e6f5f6'
URL = 'https://dapi.kakao.com/v2/local/search/address.json?query='
headers = {'Authorization': 'KakaoAK {}'.format(APP_KEY)}

html_path = "http://localhost:63342/CorporateProject/HTML/kakao_map.html"


def get_dong_latlng(dong_nm):
    result = ""
    r = requests.get(URL + dong_nm, headers=headers)

    if r.status_code == 200:
        try:
            result_address = r.json()["documents"][0]["address"]
            result = result_address["y"], result_address["x"]
        except Exception as e:
            return print(e)
    else:
        result = "ERROR[" + str(r.status_code) + "]"

    return result


def open_html_():
    message = f"initializeMap%2C"
    url = html_path + f"?message={message}"
    return url


def focus_marker(x, y, nm):
    message = f"focus_marker%2C{x}%3A{y}%3A{nm}"
    url = html_path + f"?message={message}"
    webbrowser.open(url)


def wash_store_marker(address_latlng, wash_list: list, zoomlevel):
    javascript_key = "4f4f0002f704a308f73391878f370e5f"
    result = ""

    result = result + "<!DOCTYPE html>" + "\n"
    result = result + "<html>" + "\n"
    result = result + "<head>" + "\n"
    result = result + "    <meta charset='utf-8'>" + "\n"
    result = result + "    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">" + "\n"
    result = result + "    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>" + "\n"
    result = result + "    <link href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300&display=swap\" rel=\"stylesheet\">" + "\n"
    result = result + "    <style>" + "\n"
    result = result + "    .wrap {position: absolute;left: 0;bottom: 40px;width: 200px;height: 100px;margin-left: -100px;text-align: left;overflow: hidden;font-size: 12px;font-family: 'Noto Sans KR', sans-serif;line-height: 1.5;}" + "\n"
    result = result + "    .wrap * {padding: 0;margin: 0;}" + "\n"
    result = result + "    .wrap .info {width: 180px;height: 70px;border-radius: 5px;overflow: hidden;background: #fff;border: 0;box-shadow: 0 1px 2px #888;}" + "\n"
    result = result + "    .info .info-content {padding: 10px 0 0 5px;height: 5px;background: #fff;border-bottom: 1px solid #fff;font-size: 12px;font-weight: normal;}" + "\n"
    result = result + "    .info .close {position: absolute;top: 10px;right: 10px;color: #888;width: 17px;height: 17px;background: url('https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/overlay_close.png');}" + "\n"
    result = result + "    .info .close:hover {cursor: pointer;}" + "\n"
    result = result + "    .info:after {content: '';position: absolute;margin-left: -12px;left: 50%;bottom: 0;width: 22px;height: 12px;background: url('https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/vertex_white.png')}" + "\n"
    result = result + "    </style>" + "\n"
    result = result + "</head>" + "\n"
    result = result + "<body>" + "\n"
    result = result + "<div id='map' style='width:800px;height:600px;display:inline-block;'></div>" + "\n"
    result = result + "<div id='roadview' style='width:800px;height:300px;display:inline;'></div>" + "\n"
    result = result + "<script type='text/javascript' src='//dapi.kakao.com/v2/maps/sdk.js?appkey=" + javascript_key + "&libraries=services,drawing,clusterer'></script>" + "\n"
    result = result + "<script>" + "\n"
    result = result + "    var container = document.getElementById('map'); " + "\n"
    result = result + "    var options = {" + "\n"
    result = result + "           center: new kakao.maps.LatLng(" + str(address_latlng[0]) + ", " + str(
        address_latlng[1]) + ")," + "\n"
    result = result + "           level:" + zoomlevel + "\n"
    result = result + "    }; " + "\n"
    result = result + "    var map = new kakao.maps.Map(container, options); " + "\n"
    result = result + "    var positions =" + str(wash_list) + ";" + "\n"

    result = result + "    var markerPosition  = new kakao.maps.LatLng(" + str(address_latlng[0]) + ", " + str(
        address_latlng[1]) + ");  " + "\n"
    result = result + "    var marker = new kakao.maps.Marker({position: markerPosition}); " + "\n"
    result = result + "    marker.setMap(map); " + "\n"

    result = result + "    var imageSrc_self = 'https://ifh.cc/g/VBcQrN.png';" + "\n"
    result = result + "    var imageSrc_ = 'https://ifh.cc/g/7sq2oA.png';" + "\n"

    result = result + "    for (var i = 0; i < positions.length; i ++) {" + "\n"
    result = result + "        var position = new kakao.maps.LatLng(positions[i][1], positions[i][2]);" + "\n"

    result = result + "        var imageSize = new kakao.maps.Size(40, 40);" + "\n"
    result = result + "        var markerImage_self = new kakao.maps.MarkerImage(imageSrc_self, imageSize);" + "\n"
    result = result + "        var markerImage_ = new kakao.maps.MarkerImage(imageSrc_, imageSize);" + "\n"

    result = result + "        var imageToUse = markerImage_self;" + "\n"
    result = result + "        if (positions[i][0] === '세탁소') {" + "\n"
    result = result + "            imageToUse = markerImage_;" + "\n"
    result = result + "        }" + "\n"

    result = result + "        var marker = new kakao.maps.Marker({" + "\n"
    result = result + "           map: map," + "\n"
    result = result + "           position: position," + "\n"
    result = result + "           title : positions[i][0]," + "\n"
    result = result + "           image : imageToUse" + "\n"
    result = result + "        }); " + "\n"

    result = result + "        var Content = '<div class =\"label\" style=\"padding: 2px; background-color: #FFF; " \
                      "color: black; font-size: 14px; border: 1px solid #8BE8E5; border-radius:10px;\">' + " \
                      "positions[i][0] + '</div>';" + "\n";
    result = result + "        var Position = new kakao.maps.LatLng(positions[i][1], positions[i][2]);" + "\n"
    result = result + "        var customOverlay = new kakao.maps.CustomOverlay({" + "\n"
    result = result + "           position : Position," + "\n"
    result = result + "           content : Content," + "\n"
    result = result + "        }); " + "\n"
    result = result + "        customOverlay.setMap(map); " + "\n"
    result = result + "    }; " + "\n"

    return result


def create_estate_cluster(estate_dict: dict, result):
    javascript_key = "4f4f0002f704a308f73391878f370e5f"

    # 마커 클러스터를 생성합니다
    result = result + "    var clusterer = new kakao.maps.MarkerClusterer({" + "\n"
    result = result + "        map: map," + "\n"
    result = result + "        averageCenter: true," + "\n"
    result = result + "        minLevel: 2," + "\n"
    result = result + "    });" + "\n"

    result = result + "    var estateMarkers = [];" + "\n"
    result = result + "    var estatePositions =" + str(estate_dict['estatePositions']) + ";" + "\n"
    result = result + "    var img_under = 'https://ifh.cc/g/MaHNZd.png';" + "\n"
    result = result + "    var img_over = 'https://ifh.cc/g/ZmXBso.png';" + "\n"

    result = result + "    var imgSize = new kakao.maps.Size(40, 40);" + "\n"
    result = result + "    var markerImg_under = new kakao.maps.MarkerImage(img_under, imgSize);" + "\n"
    result = result + "    var markerImg_over = new kakao.maps.MarkerImage(img_over, imgSize);" + "\n"

    result = result + "    var imgDefault = markerImg_under;" + "\n"

    result = result + "    for (var i = 0; i < estatePositions.length; i ++) {" + "\n"
    result = result + "        (function(index) {" + "\n"
    result = result + "            if (estatePositions[i].type === '이상') {" + "\n"
    result = result + "                imgDefault = markerImg_over;" + "\n"
    result = result + "            }" + "\n"
    result = result + "            var estateMarker = new kakao.maps.Marker({" + "\n"
    result = result + "                 position: new kakao.maps.LatLng(estatePositions[i].lat, estatePositions[i].lng)," + "\n"
    result = result + "                 map : map," + "\n"
    result = result + "                 image : imgDefault" + "\n"
    result = result + "            });" + "\n"

    result = result + "            var content = '<div class=\"wrap\">' +" + "\n"
    result = result + "                    '    <div class=\"info\">' +" + "\n"
    result = result + "                    '     <div class=\"info-content\">' +" + "\n"
    result = result + "                    '         <p>면적 : ' + estatePositions[i].area + '</p>' +" + "\n"
    result = result + "                    '         <p>층수 : ' + estatePositions[i].floor + '</p>' +" + "\n"
    result = result + "                    '         <p>매매가 : ' + estatePositions[i].price + '</p>' +" + "\n"
    result = result + "                    '     </div>' +" + "\n"
    result = result + "                    '    </div>' +" + "\n"
    result = result + "                    '</div>';" + "\n"

    result = result + "            var overlay = new kakao.maps.CustomOverlay({" + "\n"
    result = result + "                 position : new kakao.maps.LatLng(estatePositions[i].lat, estatePositions[i].lng)," + "\n"
    result = result + "                 content : content," + "\n"
    result = result + "                 xAnchor: 0.5," + "\n"
    result = result + "                 yAnchor: 0.5" + "\n"
    result = result + "            });" + "\n"

    result = result + "            kakao.maps.event.addListener(estateMarker, 'click', function() {" + "\n"
    result = result + "                 Roadview (estatePositions[index].lat, estatePositions[index].lng);" + "\n"
    result = result + "            });" + "\n"

    result = result + "            kakao.maps.event.addListener(estateMarker, 'mouseover', function() {" + "\n"
    result = result + "                 overlay.setMap(map);" + "\n"
    result = result + "            });" + "\n"

    result = result + "            kakao.maps.event.addListener(estateMarker, 'mouseout', function() {" + "\n"
    result = result + "                 overlay.setMap(null);" + "\n"
    result = result + "            });" + "\n"

    result = result + "            estateMarkers.push(estateMarker);" + "\n"
    result = result + "        })(i);" + "\n"
    result = result + "    }" + "\n"
    result = result + "    clusterer.addMarkers(estateMarkers); " + "\n"

    result = result + "    var roadviewContainer = document.getElementById('roadview'); " + "\n"
    result = result + "    var roadview = new kakao.maps.Roadview(roadviewContainer);" + "\n"
    result = result + "    var roadviewClient = new kakao.maps.RoadviewClient(); " + "\n"
    result = result + "    var roadview = new kakao.maps.Panorama(container, options); " + "\n"

    result = result + "    function Roadview (lat, lng){" + "\n"
    result = result + "      var position = new kakao.maps.LatLng(lat, lng);" + "\n"
    result = result + "      roadviewClient.getNearestPanoId(position, 50, function(panoId) {" + "\n"
    result = result + "          roadview.setPanoId(panoId, position);" + "\n"
    result = result + "          roadviewContainer.style.display = 'inline-block';" + "\n"
    result = result + "      });" + "\n"
    result = result + "    }" + "\n"

    return result


def create_radius_html(latlng: list, store_dict: dict):
    result = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        html, body {width:800px;height:600px;margin:0;padding:0;}
        .radius_border{border:1px solid #919191;border-radius:5px;}
        .custom_typecontrol {position:absolute;top:10px;right:330px;overflow:hidden;width:130px;height:30px;margin:0;padding:0;z-index:1;font-size:12px;font-family:'Malgun Gothic', '맑은 고딕', sans-serif;}
        .custom_typecontrol span {display:block;width:65px;height:30px;float:left;text-align:center;line-height:30px;cursor:pointer;}
        .custom_typecontrol .btn {background:#fff;background:linear-gradient(#fff,  #e6e6e6);}
        .custom_typecontrol .btn:hover {background:#f5f5f5;background:linear-gradient(#f5f5f5,#e3e3e3);}
        .custom_typecontrol .btn:active {background:#e6e6e6;background:linear-gradient(#e6e6e6, #fff);}
        .custom_typecontrol .selected_btn {color:#fff;background:#425470;background:linear-gradient(#425470, #5b6d8a);}
        .custom_typecontrol .selected_btn:hover {color:#fff;}
        .title {font-weight:bold;display:block;font-size:14px;font-family:'Malgun Gothic', '맑은 고딕', sans-serif;}
        .hAddr {position:absolute;right:10px;bottom:450px;width:375px;border-radius: 2px;background:rgba(255,255,255,255);z-index:10;padding:5px;}
        #centerAddr {display:block;margin-top:2px;font-weight: normal;}
        .bAddr .title {position:absolute;right:-5px;bottom:310px;border-radius: 2px;z-index:1;width:400px;height:136px;background: url('https://ifh.cc/g/9lsq57.png') no-repeat;margin-bottom:8px;}
        #centerBAddr {display:block;margin-top:2px;font-weight: normal;}
    </style>
</head>
<body>
    <div id="map" style='width:800px;height:600px;display:inline-block;'></div>
    <!-- 지도타입 컨트롤 div 입니다 -->
    <div class="custom_typecontrol radius_border">
        <span id="btnRoadmap" class="selected_btn" onclick="setOverlayMapTypeId('roadmap')">지도</span>
        <span id="btnDistrict" class="btn" onclick="setOverlayMapTypeId('use_district')">지적편집도</span>
    </div>
    <div class="hAddr">
        <span class="title">지적편집도(용도지역)</span>
        <span id="centerAddr"></span>
    </div>
    <div class="bAddr">
        <span class="title"></span>
        <span id="centerBAddr"></span>
    </div>
<script type='text/javascript' src='//dapi.kakao.com/v2/maps/sdk.js?appkey=4f4f0002f704a308f73391878f370e5f&libraries=services'></script>
<script>
    var mapContainer = document.getElementById('map');
    var mapOption = {
            center: new kakao.maps.LatLng(""" + str(latlng[0]) + ", " + str(latlng[1]) + """),
            level: 3 // 지도의 확대 레벨
    };
    var map = new kakao.maps.Map(mapContainer, mapOption);
"""
    result = result + "    var Markers = [];" + "\n"
    result = result + "    var markerPosition  = new kakao.maps.LatLng(" + str(latlng[0]) + ", " + str(latlng[1]) + ");" + "\n"
    result = result + "    var marker = new kakao.maps.Marker({position: markerPosition, zIndex:1000}); " + "\n"
    result = result + "    marker.setMap(map); " + "\n"
    result = result + "    var Positions =" + str(store_dict['store_500m']) + ";" + "\n"
    result = result + "\n"
    result = result + "    var img_cafe = 'https://ifh.cc/g/wgM81M.png';" + "\n"
    result = result + "    var img_book = 'https://ifh.cc/g/LNQckq.png';" + "\n"
    result = result + "    var img_pc = 'https://ifh.cc/g/nmpqRF.png';" + "\n"
    result = result + "    var img_hair = 'https://ifh.cc/g/wsYpPt.png';" + "\n"
    result = result + "    var img_convi = 'https://ifh.cc/g/OYAHgk.png';" + "\n"
    result = result + "    var img_tel = 'https://ifh.cc/g/3PYmHW.png';" + "\n"
    result = result + "    var img_sauna = 'https://ifh.cc/g/RxqXqY.png';" + "\n"
    result = result + "    var img_gym = 'https://ifh.cc/g/aoSTlK.png';" + "\n"
    result = result + "    var img_self_laundry = 'https://ifh.cc/g/VBcQrN.png';" + "\n"
    result = result + "    var img_laundry = 'https://ifh.cc/g/7sq2oA.png';" + "\n"
    result = result + "\n"
    result = result + "    var imgSize = new kakao.maps.Size(40, 40);" + "\n"
    result = result + "    var imgDefault = markerImg_cafe;" + "\n"
    result = result + "    var markerImg_cafe = new kakao.maps.MarkerImage(img_cafe, imgSize);" + "\n"
    result = result + "    var markerImg_book = new kakao.maps.MarkerImage(img_book, imgSize);" + "\n"
    result = result + "    var markerImg_pc = new kakao.maps.MarkerImage(img_pc, imgSize);" + "\n"
    result = result + "    var markerImg_hair = new kakao.maps.MarkerImage(img_hair, imgSize);" + "\n"
    result = result + "    var markerImg_convi = new kakao.maps.MarkerImage(img_convi, imgSize);" + "\n"
    result = result + "    var markerImg_tel = new kakao.maps.MarkerImage(img_tel, imgSize);" + "\n"
    result = result + "    var markerImg_sauna = new kakao.maps.MarkerImage(img_sauna, imgSize);" + "\n"
    result = result + "    var markerImg_gym = new kakao.maps.MarkerImage(img_gym, imgSize);" + "\n"
    result = result + "    var markerImg_self_laundry = new kakao.maps.MarkerImage(img_self_laundry, imgSize);" + "\n"
    result = result + "    var markerImg_laundry = new kakao.maps.MarkerImage(img_laundry, imgSize);" + "\n"
    result = result + "\n"
    result = result + "    for (var i = 0; i < Positions.length; i ++) {" + "\n"
    result = result + "        (function(index) {" + "\n"
    result = result + "            var curPosition = Positions[i];" + "\n"
    result = result + "            if (curPosition.apart === '카페') {" + "\n"
    result = result + "                imgDefault = markerImg_cafe;" + "\n"
    result = result + "            }" + "\n"
    result = result + "            else if (curPosition.apart === '서점') {" + "\n"
    result = result + "                imgDefault = markerImg_book;" + "\n"
    result = result + "            }" + "\n"
    result = result + "            else if (curPosition.apart === 'PC방') {" + "\n"
    result = result + "                imgDefault = markerImg_pc;" + "\n"
    result = result + "            }" + "\n"
    result = result + "            else if (curPosition.apart === '미용실') {" + "\n"
    result = result + "                imgDefault = markerImg_hair;" + "\n"
    result = result + "            }" + "\n"
    result = result + "            else if (curPosition.apart === '편의점') {" + "\n"
    result = result + "                imgDefault = markerImg_convi;" + "\n"
    result = result + "            }" + "\n"
    result = result + "            else if (curPosition.apart === '기숙사/고시원') {" + "\n"
    result = result + "                imgDefault = markerImg_tel;" + "\n"
    result = result + "            }" + "\n"
    result = result + "            else if (curPosition.apart === '목욕탕/사우나') {" + "\n"
    result = result + "                imgDefault = markerImg_sauna;" + "\n"
    result = result + "            }" + "\n"
    result = result + "            else if (curPosition.apart === '헬스장') {" + "\n"
    result = result + "                imgDefault = markerImg_gym;" + "\n"
    result = result + "            }" + "\n"
    result = result + "            else if (curPosition.apart === '셀프 빨래방') {" + "\n"
    result = result + "                imgDefault = markerImg_self_laundry;" + "\n"
    result = result + "            }" + "\n"
    result = result + "            else if (curPosition.apart === '세탁소') {" + "\n"
    result = result + "                imgDefault = markerImg_laundry;" + "\n"
    result = result + "            }" + "\n"
    result = result + "            var Marker = new kakao.maps.Marker({" + "\n"
    result = result + "                map : map," + "\n"
    result = result + "                position: new kakao.maps.LatLng(curPosition.lng, curPosition.distance)," + "\n"
    result = result + "                image : imgDefault" + "\n"
    result = result + "            });" + "\n"
    result = result + "            Markers.push(Marker);" + "\n"
    result = result + "        })(i);" + "\n"
    result = result + "    }" + "\n"
    result_ = """
    var currentTypeId;

    // 지도타입 컨트롤버튼을 클릭하면 호출되어 지도타입을 바꾸는 함수
    function setOverlayMapTypeId(maptype) {
        var changeMaptype;
        var districtControl = document.getElementById('btnDistrict');
        var roadmapControl = document.getElementById('btnRoadmap');
        if (maptype === 'use_district') {
            changeMaptype = kakao.maps.MapTypeId.USE_DISTRICT;
            roadmapControl.className = 'btn';
            districtControl.className = 'selected_btn';
            map.addOverlayMapTypeId(changeMaptype);
            currentTypeId = changeMaptype;
        } else if (maptype === 'roadmap') {
            map.setMapTypeId(kakao.maps.MapTypeId.ROADMAP);
            districtControl.className = 'btn';
            roadmapControl.className = 'selected_btn';
            if (currentTypeId) {
                map.removeOverlayMapTypeId(currentTypeId);
            }
        }
    }
    """
    result += result_
    result = result + "    var circle = new kakao.maps.Circle({" + "\n"
    result = result + "        center: new kakao.maps.LatLng(" + str(latlng[0]) + ", " + str(latlng[1]) + "),  " + "\n"
    result = result + "        radius: 500," + "\n"
    result = result + "        strokeWeight: 2," + "\n"
    result = result + "        strokeColor: '#00a0e9'," + "\n"
    result = result + "        strokeOpacity: 0.8," + "\n"
    result = result + "        fillColor: '#00a0e9'," + "\n"
    result = result + "        fillOpacity: 0.5" + "\n"
    result = result + "    });" + "\n"

    result = result + "    circle.setMap(map);" + "\n"

    return result


def complete_html_(result):
    result = result + "</script>" + "\n"
    result = result + "</body>" + "\n"
    result = result + "</html>" + "\n"
    return result


# C:\Users\KDT000\Desktop\ 경로 알맞게 수정 바람
def save_html_(map_html, file_name):
    with open(r"C:\Users\KDT000\Desktop\CorporateProject\HTML" + "\\" + file_name, 'w', encoding="utf-8") as f:
        f.write(map_html)

    url = f'http://localhost:63342/CorporateProject/HTML{file_name}'
    return url

if __name__ == "__main__":
    data = DataClass()

    # dong_address = "서울시 관악구 보라매동"
    # dong_add = dong_address.split(" ")
    # dong_nm = dong_add[2]
    #
    # REST API로 주소 -> 좌표얻음
    # address_latlng = get_dong_latlng(dong_address)

    # 1. 관악구 지도(완료)
    # open_html_()

    # 2. 특정 행정동 지도 (완료)
    # focus_marker(address_latlng[0], address_latlng[1], dong_nm)

    # 3. 특정 행정동 지도 + 세탁업소 마커 (완료)
    # dong_code = data.select_dong_code(dong_nm)
    # dong_wash_positions = data.select_wash_store(dong_code)
    #
    # first_html = wash_store_marker(address_latlng, dong_wash_positions, '4')
    # html_complete = complete_html_(first_html)
    #
    # file_name = "kakao_map_marker.html"
    # save_html_(html_complete, file_name)

    # 3-2. 특정 행정동 지도 + 세탁업소 마커 + 매물 클러스터
    # col_list = ['ESTATE_TYPE', 'ESTATE_LA', 'ESTATE_LO', 'ESTATE_AREA', 'ESTATE_PRICE', 'ESTATE_FLOOR']
    # dong_estate_info = data.select_real_estate_info(dong_nm, col_list)
    # custom_dict = data.create_custom_dict('estatePositions', dong_estate_info)
    # dong_code = data.select_dong_code(dong_nm)
    # dong_wash_positions = data.select_wash_store(dong_code)
    #
    # first_html = wash_store_marker(address_latlng, dong_wash_positions, '5')
    # second_html = create_estate_cluster(custom_dict,first_html)
    # html_complete = complete_html_(second_html)
    #
    # file_name = "kakao_map_marker.html"
    # save_html_(html_complete, file_name)

    # 4. 특정 매물 마커 + 반경 500m + 시설(미용실, 헬스장) + 각 시설 표시제어
    # latlng = data.select_estate_info('서울특별시 관악구 장군봉2길 16', ['ESTATE_LA', 'ESTATE_LO'])[0]
    # tu_latlng = tuple(latlng)
    # radius_dict = data.calculate_distance(tu_latlng)
    # html_script_1 = create_radius_html(latlng, radius_dict)
    # html_script_2 = complete_html_(html_script_1)
    # save_html_(html_script_2, 'kakao_map_radius.html')