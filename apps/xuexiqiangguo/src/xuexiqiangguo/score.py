import requests
from requests.cookies import RequestsCookieJar
import json

__TOTAL_URL = "https://pc-api.xuexi.cn/open/api/score/get"
__EACH_URL = "https://pc-api.xuexi.cn/open/api/score/today/queryrate"

def get_score(cookies):
    try:
        jar = RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
        total = requests.get(__TOTAL_URL, cookies=jar).content.decode("utf8")
        total = int(json.loads(total)["data"]["score"])
        each = requests.get(__EACH_URL, cookies=jar).content.decode("utf8")
        each = json.loads(each)["data"]["dayScoreDtos"]
        each = [(i["name"], int(i["currentScore"]))
                for i in each if i["ruleId"] in [9, 1, 2, 1002, 1003, 6, 5, 4]]
        return total, dict(each)
    except:
        print("=" * 120)
        print("get_video_links获取失败")
        print("=" * 120)
        raise
