# coding:utf-8
import psutil
from threading import Timer
import speedtest
import re
import time
import requests
from requests.adapters import HTTPAdapter
import json
from flask import Flask, request
from flask.json import jsonify
from flask_cors import CORS, cross_origin

# 安装包：pip install requests
# # pip install thread6
# pip install -U flask-cors
# pip install wheel
# pip install psutil
# speedtest-cli
app = Flask(__name__)
CORS(app, resources=r'/*')

Filepath="D:/speedData.txt"


class Speed():
    Flag = 0

    def testSpeed(self):
        self.Flag = 1

    #     sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
    #     recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
    #     time.sleep(1)
    #     sent_now = psutil.net_io_counters().bytes_sent
    #     recv_now = psutil.net_io_counters().bytes_recv
    #     sent = (sent_now - sent_before)/1024  # 算出1秒后的差值
    #     recv = (recv_now - recv_before)/1024
    #     upload_speed = format("%.2f" % sent)
    #     download_speed = format("%.2f" % recv)
    # # print(time.strftime(" [%Y-%m-%d %H:%M:%S] ", time.localtime()))
    #     print("上传：{0}KB/s".format("%.2f" % sent))
    #     print("下载：{0}KB/s".format("%.2f" % recv))

        UrlList = [
            "https://www.bilibili.com/",
            "https://www.zhihu.com/",
            "https://gitee.com/",
            "https://cloud.tencent.com/",
            "https://leetcode-cn.com/",
            "https://www.baidu.com/",
            "https://mp.weixin.qq.com/",
            "https://www.ithome.com/",
            "https://www.taobao.com/?from=itab",
            "https://www.csdn.net/",
            "https://wkif-github-io.vercel.app/"
        ]

        print("准备测试ing...")
        # 创建实例对象
        test = speedtest.Speedtest()
        # 获取可用于测试的服务器列表
        test.get_servers()
        # 筛选出最佳服务器
        best = test.get_best_server()
        print("正在测试ing...")
        # 下载速度
        download_speed = int(test.download() / 1024 / 1024)
        # download_speed = 1
        # 上传速度
        upload_speed = int(test.upload() / 1024 / 1024)
        # upload_speed = 1

        print(download_speed, upload_speed)

        TimeList = []
        for url in UrlList:
            count = 0
            retime = 0
            while count < 3:
                try:
                    r = requests.get(url, timeout=5)

                    retime = r.elapsed.total_seconds(),
                    break
                except requests.exceptions.RequestException as e:
                    print(e)
                    retime = 20
                count += 1
            TimeList.append({
                "url": str(url),
                "time": retime[0]
            })
            print(url, r.elapsed.total_seconds())
        speed_info = []
        speed_info.append({
            "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "upload_speed": str(upload_speed) + " Mbs",
            "download_speed": str(download_speed) + " Mbs",
            "Website_response_time": TimeList
        })
        jsonArr = json.dumps(speed_info, ensure_ascii=False)
        file = r'data.txt'
        p = re.compile(r'[[](.*)[]]', re.S)
        with open(Filepath, 'a+') as f:
            x = re.findall(p, str(jsonArr))
            f.write(x[0]+'\n')
            f.close()
        self.Flag = 0

    def checkFlag(self):
        print("查看flag状态: "+str(self.Flag)+'\n')
        if self.Flag == 0:
            print("开始查询。。。")
            self.testSpeed()
            t = Timer(3.0, self.checkFlag)
            t.start()


@app.route('/api', methods=['GET'])
def api():

    file = r'data.txt'
    data = []
    index = 1
    f = open(Filepath)               # 返回一个文件对象
    line = f.readline()               # 调用文件的 readline()方法
    while line:
        if index % 2 == 0:
            if line:
                data.append(json.loads(line))
        
        index += 1
        line = f.readline()
    f.close()
    return jsonify(data)


if __name__ == '__main__':
    t = Timer(3.0, Speed().checkFlag)
    t.start()
    app.run(port=8000, debug=True)
