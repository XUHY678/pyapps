import time
import random
from sys import argv
from xuexiqiangguo import version
from xuexiqiangguo import threads
from xuexiqiangguo import users
from xuexiqiangguo import driver
from xuexiqiangguo import dingding
from xuexiqiangguo import score
from xuexiqiangguo import resources

data_path = resources.get_data_location()

def user_status(dd_status, uname):
    if dd_status:
        cookies = dingding.dd_login_status(uname, has_dd=True)
    else:
        #dd_login = input("\n是否保存钉钉账户密码，保存后可免登陆学习（Y/N）")
        dd_login = 'n'
        if dd_login not in ['y', 'Y']:
            driver_login = driver.ChromeDriver(nohead=False)
            cookies = driver_login.login()
        else:
            cookies = dingding.dd_login_status(uname)
    a_log = users.get_a_log(uname)
    v_log = users.get_v_log(uname)
    return cookies, a_log, v_log

def show_score(cookies):
    total, each = score.get_score(cookies)
    today = sum(each.values())
    print("\n今日学习总分：" + str(today))
    print("每日登录：{}/1".format(each["登录"]), end=" ")
    print("阅读文章：{}/6".format(each["阅读文章"]), end=" ")
    print("视听学习：{}/6".format(each["视听学习"]), end=" ")
    print("文章学习时长：{}/6".format(each["文章时长"]), end=" ")
    print("视听学习时长：{}/6".format(each["视听学习时长"]), end=" ")
    print("每日答题：{}/6".format(each["每日答题"]))
    #print("每周答题：{}/5".format(each["每周答题"]))
    #print("专项答题：{}/10".format(each["专项答题"]))
    return total, today, each

def get_argv():
    nohead = True
    lock = False
    stime = False
    if len(argv) > 2:
        if argv[2] == "hidden":
            nohead = True
        elif argv[2] == "show":
            nohead = False
    if len(argv) > 3:
        if argv[3] == "single":
            lock = True
        elif argv[3] == "multithread":
            lock = False
    if len(argv) > 4:
        if argv[4].isdigit():
            stime = argv[4]
    return nohead, lock, stime

def article(cookies, a_log, each):
    if each["阅读文章"] < 6 or each["文章时长"] < 6:
        driver_article = driver.ChromeDriver()
        driver_article.get_url("https://www.xuexi.cn/notFound.html")
        driver_article.set_cookies(cookies)
        links = resources.get_article_links()
        try_count = 0
        while True:
            if each["阅读文章"] < 6 and try_count < 10:
                a_num = 6 - each["阅读文章"]
                for i in range(a_log, a_log + a_num):
                    driver_article.get_url(links[i])
                    time.sleep(random.randint(5, 15))
                    for j in range(120):
                        if random.random() > 0.5:
                            driver_article.go_js('window.scrollTo(0, document.body.scrollHeight/120*{})'.format(j))
                        print("\r文章学习中，文章剩余{}篇,本篇剩余时间{}秒".format(a_log + a_num - i, 120 - j), end="")
                        time.sleep(1)
                    driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, today, each = show_score(cookies)
                    if each["阅读文章"] >= 6:
                        print("\n阅读文章分数已满")
                        break
                a_log += a_num
            else:
                with open("{}/user/{}/a_log".format(data_path, uname), "w", encoding="utf8") as fp:
                    fp.write(str(a_log))
                break
                try_count = 0
        while True:
            if each["文章时长"] < 6 and try_count < 10:
                num_time = 60
                driver_article.get_url(links[a_log - 1])
                time.sleep(random.randint(5, 15))
                remaining = (6 - each["文章时长"]) * 4 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_article.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r文章时长学习中，文章总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % (120) == 0 and i != remaining:
                        total, today, each = show_score(cookies)
                        if each["文章时长"] >= 6:
                            print("\n阅读文章时长分数已满")
                            break
                driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                total, today, each = show_score(cookies)
            else:
                break
        if try_count < 10:
            print("\n完成今日文章学习相关任务")
        else:
            print("\n文章学习出现异常，请检查用户名下a_log文件记录数")
        driver_article.quit()
    else:
        print("\n今日文章学习相关任务已经完成")

def video(cookies, v_log, each):
    if each["视听学习"] < 6 or each["视听学习时长"] < 10:
        driver_video = driver.ChromeDriver()
        driver_video.get_url("https://www.xuexi.cn/notFound.html")
        driver_video.set_cookies(cookies)
        links = resources.get_video_links()
        try_count = 0
        while True:
            if each["视听学习"] < 6 and try_count < 10:
                v_num = 6 - each["视听学习"]
                for i in range(v_log, v_log + v_num):
                    driver_video.get_url(links[i])
                    time.sleep(random.randint(5, 15))
                    for j in range(180):
                        if random.random() > 0.5:
                            driver_video.go_js('window.scrollTo(0, document.body.scrollHeight/180*{})'.format(j))
                        print("\r视频学习中，视频剩余{}个,本次剩余时间{}秒".format(v_log + v_num - i, 180 - j), end="")
                        time.sleep(1)
                    driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                    total, today, each = show_score(cookies)
                    if each["视听学习"] >= 6:
                        print("\n视听学习分数已满")
                        break
                v_log += v_num
            else:
                with open("{}/user/{}/v_log".format(data_path, uname), "w", encoding="utf8") as fp:
                    fp.write(str(v_log))
                break
        try_count = 0
        while True:
            if each["视听学习时长"] < 6 and try_count < 10:
                num_time = 60
                driver_video.get_url(links[v_log-1])
                time.sleep(random.randint(5, 15))
                remaining = (6 - each["视听学习时长"]) * 3 * num_time
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_video.go_js(
                            'window.scrollTo(0, document.body.scrollHeight/{}*{})'.format(remaining, i))
                    print("\r视频学习中，视频总时长剩余{}秒".format(remaining - i), end="")
                    time.sleep(1)
                    if i % (180) == 0 and i != remaining:
                        total, today, each = show_score(cookies)
                        if each["视听学习时长"] >= 6:
                            print("\n视频学习时长分数已满")
                            break
                driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                total, today, each = show_score(cookies)
            else:
                break
        if try_count < 10:
            print("\n完成今日视听学习相关任务")
        else:
            print("\n视听学习出现异常，请检查用户名下v_log文件记录数")
        driver_video.quit()
    else:
        print("\n今日视听学习相关任务已经完成")

if __name__ == '__main__':
    start_time = time.time()

    # get version information
    #info_thread = threads.XueXiThread("", version.up_info)
    #info_thread.start()

    # get user information
    dd_status, uname = users.get_user()

    # login and get history record
    cookies, a_log, v_log = user_status(dd_status, uname)
    total, today, each = show_score(cookies)

    # get parameters
    nohead, lock, stime = get_argv()

    # task1: read articles
    article_thread = threads.XueXiThread("文章学习", article, cookies, a_log, each, lock=lock)
    article_thread.start()
    article_thread.join()

    # task2: watch videos
    video_thread = threads.XueXiThread("视频学习", video, cookies, v_log, each, lock=lock)
    video_thread.start()
    video_thread.join()

    print("\n总计用时" + str(int(time.time() - start_time) / 60) + "分钟")
