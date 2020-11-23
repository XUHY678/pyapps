#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests

__URL = "https://raw.githubusercontent.com/LordJX/XueXi/master/update.log"
__Version = "v1.0"

def up_info():
    try:
        update_log = requests.get(__URL).content.decode("utf8")
        update_log = update_log.split('\n')
        if __Version != update_log[1].split('=')[1]:
            print("程序版本为：{}，\n最新版本为：{}".format(
                __Version,
                update_log[1].split("=")[1]))
            print("当前不是最新版本，建议更新")
            print('=' * 80)
            print("更新提要：")
            for i in update_log[2:]:
                print(i)
            print('=' * 80)
        #print("更新显示不会打断之前输入等操作，请继续......（若已输入用户标记直接enter）")
    except:
        #print("获取版本信息时发生网络错误")
        pass

if __name__ == '__main__':
    up_info()
