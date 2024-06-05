from robot import robot
from config import *
from until import *
import os, time, traceback, threading
from Crypto.Cipher import AES

print('start selenium...')

robot = robot( **robot_param )

robot.create_action()

# 访问网站
robot.get(url)

# 手动登录
robot.wait_click('//p[text()="登录注册"]')
# robot.wait_sendkey('//input[@id="regmobile"]', username)
for i in range(30*10):
    if robot.is_ele_exist('//p[@id="dropdown"]'):
        print('登录成功...')
        break
    else:
        print('等待完成手动登录...')
else:
    raise Exception('手动登录时间超过10分钟...')




url1 = 'https://www.kaoyanvip.cn/appmanage/learnDetail?my_delivery_id=195668801&delivery_outline_id=10705410&course_section=13495101&unit_id=OT11130402&outlineMode=true'
url2 = 'https://www.kaoyanvip.cn/appmanage/learnDetail?my_delivery_id=195668801&delivery_outline_id=10705410&course_section=13342201&unit_id=OT11130802&outlineMode=true'
url3 = 'https://www.kaoyanvip.cn/appmanage/learnDetail?my_delivery_id=195668801&delivery_outline_id=10705410&course_section=13342601&unit_id=OT11130802&outlineMode=true'

# 写入视频连接
url_list = [
url1,
url2,
url3,
]

# 循环访问课程视频页面
for url in [url1, url2]:
# for url in [url3]:

    # 访问视频页面
    robot.get(url)
    ele = robot.wait_ele('//header')
    mp4_filename = ele.text + f'_{time.time()}.mp4'
    mp4_file = os.path.join(mp4_file_path, mp4_filename)
    robot.sleep(3)

    # 获取m3u8
    request_ = robot.get_url_request(r'https://hls.videocc.net/.*_1.m3u8')
    response = request_[-1].response.body.decode('utf-8')

    # 获取key
    method, key_url, ts_list = parse_m3u8_text(response)
    key = requests.get(key_url, headers=headers).content

    ## MODE_CBC模式，解密器
    decrypter = AES.new(key, AES.MODE_CBC)

    # 删除旧文件
    for file in os.listdir(response_file_path):
        file_path = os.path.join(response_file_path, file)
        os.remove(file_path)

    print(len(ts_list))
    # 获取ts文件
    for ts_url in ts_list:

        content = requests.get(ts_url, headers).content
        file_name = ts_url.split('?')[0].split('/')[-1]
        file_path = os.path.join( response_file_path, file_name )
        open(file_path, 'wb').write(decrypter.decrypt(content))

        # 使用线程执行
        # threading.Thread(target=run).start()

        # 每隔五十个停10秒
        # if ts_list.index(ts_url) % 50 == 0:
        #     robot.sleep(10)

    # 合并ts为mp4,并命名mp4文件
    ts_file_list = [ os.path.join(response_file_path, file) for file in os.listdir( response_file_path ) ]
    # ts文件名排序
    ts_dict = {
        int(ts.split('_')[-1].replace('.ts', '')):ts
        for ts in ts_file_list
    }
    ts_dict = dict(sorted(ts_dict.items(), key=lambda item: item[0]))
    print(mp4_file)

    merge_ts_to_mp4(mp4_file,ts_dict.values())

robot.driver.quit()