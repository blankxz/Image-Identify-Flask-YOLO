import json
from datetime import timedelta, datetime
from yolo import *
from flask import Flask, request, jsonify

import cv2
from PIL import Image

app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
app.debug = True

ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


'''
title: 车流识别(full screen)
input
    type: json
    key: 'img_file'
    value: 图片文件
return
    type: json
    key: 识别物体类别及位置序号
    value: 识别物体类别及位置s
'''


@app.route('/traffic_count_full', methods=["POST"])
def traffic_count():
    if request.method == 'POST':
        img_file = request.files['img_file']
        if not (img_file and allowed_file(img_file.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_path = 'Img-Save/' + file_name + '.png'
        img_file.save(file_path)
        img, res = detect_img(file_path)
        r_back = {}
        j = 1
        for i in res:
            r_back['label_' + str(j)] = str(i[0])
            r_back['location_' + str(j)] = [str(i[1][0]), str(i[1][1]), str(i[2][0]), str(i[2][1])]
            j += 1
        r_back = json.dumps(r_back, ensure_ascii=False)
        print(r_back)
        # img.show()
        img.save(file_path, quality=95)
        return r_back


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
