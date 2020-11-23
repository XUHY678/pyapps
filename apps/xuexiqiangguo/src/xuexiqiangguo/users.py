import os
from time import sleep
from sys import argv
from xuexiqiangguo import resources

data_path = resources.get_data_location()

def get_user():
    if len(argv) > 1:
        uname = argv[1]
    else:
        #uname = input("输入用户标记名：")
        uname = "18616855696"
    if check_uname(uname):
        dd = check_dd(uname)
    else:
        os.makedirs("{}/user/{}".format(data_path, uname))
        dd = False
    return dd, uname

def check_uname(uname):
    __check_status = False
    if os.path.exists("{}/user/{}".format(data_path, uname)):
        __check_status = True
    return __check_status

def check_dd(uname):
    __dd_status = False
    if os.path.exists("{}/user/{}/dingding".format(data_path, uname)):
        __dd_status = True
    return __dd_status

def get_a_log(uname):
    __a_log = 0
    log_file_name = "{}/user/{}/a_log".format(data_path, uname)
    if os.path.exists(log_file_name):
        with open(log_file_name, 'r', encoding="utf8") as fp:
            __a_log = int(fp.read())
    else:
        with open(log_file_name, 'w', encoding="utf8") as fp:
            fp.write(str(__a_log))
    return __a_log

def get_v_log(uname):
    __v_log = 0
    log_file_name = "{}/user/{}/v_log".format(data_path, uname)
    if os.path.exists(log_file_name):
        with open(log_file_name, 'r', encoding="utf8") as fp:
            __v_log = int(fp.read())
    else:
        with open(log_file_name, 'w', encoding="utf8") as fp:
            fp.write(str(__v_log))
    return __v_log

def shutdown(stime):
    if stime:
        stime = int(stime)
        os.system("shutdown -s -t {}".format(stime))
        for i in range(stime):
            print("\r{}秒后关机".format(stime-i), end="")
            sleep(1)
    else:
        print("无自动关机任务，已释放程序内存，10分钟后窗口将自动关闭")
        sleep(600)


