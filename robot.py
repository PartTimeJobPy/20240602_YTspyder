import requests, time, json, random, gzip, brotli, re
from typing import Union, Mapping, Dict, Any,List
from selenium import webdriver  as webdriver1  #
from seleniumwire import webdriver as webdriver2 # ...可获取浏览器的所有请求
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from seleniumwire.request import Request


# 自定义抛出异常
class valueerror(Exception):
    def __init__(self,err):
          print(err)

# 函数装饰器 随机睡眠几秒
def random_sleep(func):
    def sleep(self,*args):
        func(self,*args)
        time.sleep(random.choice([0.5,0.7,1,1,1,1.5,2,2]))
    return sleep

###################
#####机器人类######
###################

class robot(object):
    '''该类只支持xpath定位'''
    
    def __init__(
            self,
            chrome_driver:str,
            prefs:Mapping[str, Any]={},
            maximize=False,
            is_google=False,
            is_firefox=False,
            is_Ie=False,
            selenium_for_requests=False,
            **kwargs
    ):
        self.kwargs = kwargs
        # 是否最大化窗口
        self.maximize = maximize
        # 类属性
        self.time = time
        self.driver = None
        self.action: ActionChains = None
        self.wait = None
        self.option = None
        self.profile = None
        self.is_google = is_google
        self.is_firefox = is_firefox
        self.is_Ie = is_Ie
        self.prefs = prefs
        # service
        self.service = Service(chrome_driver)
        #
        self.kwargs.update( { "service":self.service } )

        # 切换selenium的webdriver
        self.selenium_for_requests = selenium_for_requests
        if selenium_for_requests:
            self.webdriver = webdriver2
        else:
            self.webdriver = webdriver1
        # 类私有变量
        self._timeout = 10
        # 开始生成机器人的类属性
        self.create_option()
        self.create_driver()
        self.create_action()
        self.create_wait()
        
    @random_sleep
    def __del__(self):
        '''结束销毁类'''
        # self.driver.quit()
        # self.driver.close()
        pass

    def create_option(self):
        if self.is_firefox:
            self.create_firefox_option()
        elif self.is_google:
            self.create_google_option()
        elif self.is_Ie:
            self.create_Ie_option()
            
    def create_firefox_option(self):
        '''
        创建火狐浏览器携带请求头、隐藏selenium特征的option
        '''
        self.option = self.webdriver.FirefoxOptions()
        self.profile = self.webdriver.FirefoxProfile()
        # 火狐--屏蔽selenium特征
        self.option.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"')
        # self.profile.add_argument('--disable-blink-features=AutomationControlled')
        self.profile.set_preference("dom.webdriver.enabled", False)
        self.profile.set_preference('useAutomationExtension', False)
        
    def create_google_option(self):
        '''
        谷歌浏览器 反爬虫设置
        '''
        self.options = self.webdriver.ChromeOptions()
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_experimental_option("detach", True)
        self.options.add_argument('--disable-dev-shm-usage')
        if self.prefs:
            self.options.add_experimental_option('prefs', self.prefs)

    def create_Ie_option(self):
        '''
        IE浏览器 反爬虫设置
        '''
        self.options = self.webdriver.IeOptions()

    def create_driver(self):
        '''
        创建option属性对应的浏览器driver属性、窗口是否最大化
        '''
        if self.option:
            if self.profile:
                if self.is_firefox:
                    self.driver = self.webdriver.Firefox(options=self.option, proxy=self.profile, **self.kwargs)
                elif self.is_google:

                    self.driver = self.webdriver.Chrome(options=self.option, proxy=self.profile, **self.kwargs)
                elif self.is_Ie:
                    self.driver = self.webdriver.Ie(options=self.option, proxy=self.profile, **self.kwargs)
            else:
                if self.is_firefox:
                    self.driver = self.webdriver.Firefox(options=self.option, **self.kwargs)
                if self.is_Ie:
                    self.driver = self.webdriver.Ie(options=self.option, **self.kwargs)
                if self.is_google:
                    self.driver = self.webdriver.Chrome(options=self.option, **self.kwargs)
        else:
                if self.is_firefox:
                    self.driver = self.webdriver.Firefox(**self.kwargs)
                if self.is_Ie:
                    self.driver = self.webdriver.Ie(**self.kwargs)
                if self.is_google:
                    self.driver = self.webdriver.Chrome(**self.kwargs)
        if self.is_google:
            # 修改谷歌浏览器的navigator的值未undefined
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                                  "source": """
                                    Object.defineProperty(navigator, 'webdriver', {
                                      get: () => undefined
                                    })
                                  """
                                })
        if self.maximize:
            self.driver.maximize_window()
        
    def create_action(self):
        self.action = ActionChains(self.driver)
    
    def is_ele_exist(self,xpath,outtime:int=2):
        '''判断元素是否存在，2秒'''
        try:
            WebDriverWait(self.driver,outtime).until(EC.presence_of_element_located((By.XPATH,xpath)))
            return True
        except:
            return False
            
    @property
    def timeout(self):
        return self._timeout
    
    @timeout.setter
    def _(self,timeout):
        '''设置私有变量timeout'''
        if timeout>=0:
            self._timeout = timeout
        else:
            raise ValueError
            
    @timeout.deleter
    def _(self):
        del self._timeout
    
    def create_wait(self):
        self.wait = WebDriverWait(self.driver,self._timeout)
    
    @random_sleep
    def get(self,url):
        self.driver.get(url)
    
    def wait_ele(self,xpath):
        return self.wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
    
    def wait_eles(self,xpath):
        '''返回元素列表'''
        return self.wait.until(EC.presence_of_all_elements_located((By.XPATH,xpath)))
    
    def wait_ele_visibility(self,xpath):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH,xpath)))
    
    @random_sleep
    def wait_click(self,xpath):
        ele = self.wait.until(EC.element_to_be_clickable((By.XPATH,xpath)))
        self.driver.execute_script('arguments[0].click()',ele)
    
    @random_sleep
    def ele_click(self,ele):
        ele.click()
    
    def find_elements(self,xpath):
        self.wait_ele(xpath)
        ele_list = self.driver.find_elements_by_xpath(xpath)
        return ele_list
    
    @random_sleep
    def Specify_number_Click(self,xpath,position):
        '''
        指定元素序号点击
        xpath :
        position :序号
        '''
        ele_list = self.find_eles(xpath)
        ele_list[position].click()
    
    # def is_exist_eles(self,xpath):
    #     '''判断元素是否存在并返回元素列表'''
    #     try:
    #         ele_list = self.find_elements(xpath)
    #         return ele_list
    #     except:
    #         return False
    
    def find_eles(self,xpath):
        self.wait_ele(xpath)
        ele_list = self.driver.find_elements_by_xpath(xpath)
        return ele_list
    
    @random_sleep
    def wait_sendkey(self,xpath,txt):
        ele = self.wait_ele(xpath)
        ele.clear()
        ele.send_keys(txt)

    def Custom_attribute_creation(self):
        '''
        自定义属性创建
        '''
        pass

    def yc(self):
        '''隐蔽selenium的属性'''
        js = 'Object.defineProperty(navigator,"webdriver",{get:() => false,})'
        try:
            self.driver.execute_script(js)
        except:
            pass
    
    def get_cookies(self):
        return self.driver.get_cookies()
    
    def delete_cookies(self):
        self.driver.delete_all_cookies()
        
    def save_cookies_as_json(self,name:str):
        '''
        保存cookies为json，并设置出cookies的最短有效时间
        example: [{...},{...},{'name': 'min_age','value':'...'}]
        '''
        with open(name+'.json','w',encoding='utf-8') as f:
            obj = self.get_cookies()
            expiry_list = [cookie.get('expiry') for cookie in obj if cookie.get('expiry')]
            if expiry_list:
                min_expiry = min(expiry_list)
                key_name = ' '.join( [ cookie.get('name') for cookie in obj if cookie.get('expiry') == min_expiry ] )                                                
                daTe = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime(min_expiry))
                obj.append({'name': 'min_age','key_name':key_name,'value':daTe})
            else:
                obj.append({'name': 'min_age','value':None})
            json.dump(obj, f)
    
    def read_json_and_Forced_return(self,name:str):
        '''读取json，强制返回cookies'''
        cookies_json = json.load(open(name+'.json','r'))
        return cookies_json
        
    def read_the_json_of_cookies(self,name:str):
        '''读取cookies，判断是否过期'''
        cookies_json = json.load(open(name+'.json','r'))
        now = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
        min_expiry = [cookie.get('value') for cookie in cookies_json if cookie.get('name') == 'min_age']
        if min_expiry:
            if min_expiry[0]>now:
                print(f'''
                      -------------------读取的cookies：{name}.json---------------------
                      {cookies_json}
                      ''')
                return cookies_json
            else:
                print(f'''
                  -------------------读取的cookies：{name}.json---------------------
                  已过期 或 不存在最短有效时间
                  min_expiry ： {min_expiry}
                  ''')
                return None
        else:
            print(f'''
                  -------------------读取的cookies：{name}.json---------------------
                  已过期 或 不存在最短有效时间
                  min_expiry ： {min_expiry}
                  ''')
            return None
        
    def input_cookies(self,cookies_list:list):
        '''输入指定的cookies'''
        for cookie in cookies_list:
            self.driver.add_cookie(cookie)
    
    @random_sleep
    def Visit_and_carry_cookies(self,name):
        '''自定义输入cookies的逻辑，'''
        cookies_list = self.read_the_json_of_cookies(name)
        if cookies_list:
            self.delete_cookies()
            self.input_cookies(cookies_list)
            print('''
                  -------------------成功输入cookies---------------------
                  ''')
            return True
        else:
            print('''
                  -------------------erro:输入cookies错误---------------------
                  ''')
            return False
    
    @random_sleep
    def down_image_as_png(self,url:str,path:str):
        img_bytes = requests.get(url).content
        with open(path+'.png','wb') as f:
            f.write(img_bytes)

    def get_handles(self):
        '''机器人获取窗口句柄'''
        return self.driver.window_handles
    
    def Control_new_window(self):
        '''机器人控制弹出的最新窗口'''
        window_handles = self.get_handles()
        self.driver.switch_to.window(window_handles[-1])

    def close_new_window(self):
        '''机器人控制弹出的最新窗口'''
        window_handles = self.get_handles()
        for handle in window_handles[1:]:
            self.driver.switch_to.window(handle)
            self.driver.close()
        self.driver.switch_to.window(window_handles[0])

    @random_sleep
    def Control_new_windows_and_close_old_ones(self):
        '''机器人控制弹出最新窗口并关闭其他窗口'''
        window_handles = self.get_handles()
        for window in window_handles:
            self.driver.switch_to.window(window)
            if list(window_handles).index(window) != len(window_handles) -1:
                # time.sleep(1)
                self.driver.close()
    
    def sleep(self,time):
        '''机器人阻塞代码运行时间'''
        self.time.sleep(time)
    
    @random_sleep
    def execute_script(self,js):
        self.driver.execute_script(js)
    
    ##  !!!需要修改
    @random_sleep
    def Operation_scroll_bar(self):
        '''js滑底部'''
        self.driver.execute_script('var action=document.documentElement.scrollTop=10000')
    
    def Pull_down_n_times(self,num):
        '''滑到底部num次'''
        for i in range(num):
            self.Operation_scroll_bar()
    
    def into_iframe_base(self,id_or_name:str):
        '''通过唯一id或name切换到指定iframe中'''
        self.driver.switch_to.frame(id_or_name)
    
    def into_iframe_by_ele(self,xpath):
        '''通过定位元素，进入指定的iframe'''
        ele = self.wait_ele(xpath)
        self.driver.switch_to.frame(ele)
    
    def out_iframe(self):
        '''返回顶层，退出所有iframe'''
        self.driver.switch_to_default_content()
    
    @random_sleep
    def back_off(self):
        '''后退一次'''
        self.driver.back()
    
    @random_sleep
    def forward(self):
        '''前进一次'''
        self.driver.forward()

    def analysis_responce_of_byte(self,body:bytes):
        data = list()
        try:
            # 尝试直接解码
            data = eval(body.decode())
        except:
            # 使用gzip的decompress函数解析seleniumwire的响应数据，同时用eval还原 gzip解压算法
            try:
                data = eval(gzip.decompress(body).decode('utf-8').replace('true', 'True').replace('false', 'False'))
            except:
                # brotli解压算法
                data = eval(brotli.decompress(body).decode('utf-8').replace('true', 'True').replace('false', 'False'))
        finally:
            return data

    def get_url_responce_of_data(self,url:str)->dict:
        if self.selenium_for_requests:
            for request in self.driver.requests:
                if url in request.url:
                    print(url)
                    responce = request.response
            return self.analysis_responce_of_byte(responce.body)
        else:
            return []

    def get_url_request(self,re_str_of_url:str)->List[Request,]:
        result = list()

        if not self.selenium_for_requests:
            raise AttributeError('robot has`t robot.driver.requests....')

        for request in self.driver.requests:
            if re.findall(re_str_of_url, request.url):
                result.append(request)

        return result