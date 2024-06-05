# -*- coding:UTF-8 -*-
import os.path

robot_param = {
    "chrome_driver":r'chromedriver.exe',
    "maximize":True,
    "is_google":True,
    "selenium_for_requests":True,
}

url = 'https://www.kaoyanvip.cn/'

base_path = os.path.split(__file__)[0]
response_file_path = os.path.join(base_path, 'data', 'response')
mp4_file_path = os.path.join(base_path, 'data', 'mp4')


# 请求头ua列表
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'Accept-Encoding': 'gzip, deflate, br, zstd',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
'Sec-Ch-Ua-Mobile': '?0',
'Sec-Ch-Ua-Platform': '"Windows"',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'none',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}