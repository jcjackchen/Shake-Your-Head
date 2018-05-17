#-*- coding: utf-8 -*-
import cv2
import time
from PIL import Image, ImageTk
# 您需要先注册一个App，并将得到的API key和API secret写在这里。
# You need to register your App first, and enter you API key/secret.
API_KEY = "u8T328HHbUVgZucADi2KvWcEwJOychLM"
API_SECRET = "mfQlsKBmbbTd0UCrkrY8ccr021UCbZs4"

face_one = './demo.jpeg'
headposelist = ('pitch_angle','roll_angle','yaw_angle')
detectrange = (15,15,15)
action = [['up','down'],['右偏头','左偏头'],['turn left','turn right']]

#国际版的服务器地址
#the server of international version
api_server_international = 'https://api-us.faceplusplus.com/facepp/v3/'

# Import system libraries and define helper functions
# 导入系统库并定义辅助函数
from pprint import pformat


def print_result(hit, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(v): encode(k) for (v, k) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hit
    result = encode(result)
    print '\n'.join("  " + i for i in pformat(result, width=75).split('\n'))


# First import the API class from the SDK
# 首先，导入SDK中的API类
from facepp import API, File


#创建一个API对象，如果你是国际版用户，代码为：api = API(API_KEY, API_SECRET, srv=api_server_international)
#Create a API object, if you are an international user,code: api = API(API_KEY, API_SECRET, srv=api_server_international)
def action():
    api = API(API_KEY, API_SECRET)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imwrite('demo.jpeg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 40])

    # detect image
        Face = {}
        res = api.detect(image_file=File(face_one), return_landmark=2, return_attributes
    ='headpose', calculate_all=1)
        try:
            #print_result("person_one", res['time_used'])
            #print_result("person_one", res['faces'][0]['attributes']['headpose'])
            head = res['faces'][0]['attributes']['headpose']
            for i in range(3):
                if head[headposelist[i]] < (-1) * int(detectrange[i]):
                    print action[i][0]
                if head[headposelist[i]] > detectrange[i]:
                    print action[i][1]
        except:
            continue
        for item in res['faces'][0]['landmark']:
            try:
                y = res['faces'][0]['landmark'][item]['x']
                x = res['faces'][0]['landmark'][item]['y']
                frame[x, y] = [0, 0, 255]
                frame[x + 1, y] = [0, 0, 255]
                frame[x, y + 1] = [0, 0, 255]
                frame[x - 1, y] = [0, 0, 255]
                frame[x, y - 1] = [0, 0, 255]
            except:
                continue
        cv2.imshow("capture", frame)
        cv2.waitKey(1)