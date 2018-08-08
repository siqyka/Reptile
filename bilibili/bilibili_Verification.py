import os
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir


uname=''
upwd=''
filepath=''

class bilibili():
    def __init__(self,url,bro,timeout=10):
        self.url=url
        # self.uname=uname
        # self.upwd=upwd
        self.timeout = timeout
        self.bro=bro
        # self.bro=webdriver.Chrome() #chromed B站验站好像比较精确，失败挺多
        self.wait=WebDriverWait(self.bro,self.timeout)
        

    def webbro(self):
        self.bro.get(self.url)
        
    #输入账号密码
    def input_msg(self,uname,upwd):
        name=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#login-username')))
        pwd=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#login-passwd')))
        name.send_keys(uname)
        pwd.send_keys(upwd)
        
    #获取验证图的左上角和右下角坐标（由于b站验证图悬浮于原网页上，所以使用特殊手段
    # （通过原网页一些元素推出）得到图片坐标）
    def get_position(self):
        self.name=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.username')))
        self.pwd=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.password')))
        time.sleep(2)
        location1=self.name.location
        location2=self.pwd.location
        # size1=self.name.size
        size2=self.pwd.size
        top,bottom,left,right=location1['y'],location2['y']+size2['height'],location1['x'],location2['x']+size2['width']
        return(top-20,bottom,left-20,right-130)

    #获取网页截图
    def get_screenshot(self):
        screenshot = self.bro.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        screenshot.save('2.png')
        return screenshot
    
    #1获取完整验证图截图
    def get_jyimage(self, name='captcha.png'):
        jybtn=self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'gt_ready')))
        webdriver.ActionChains(self.bro).move_to_element(jybtn).perform()
        time.sleep(1)
        top, bottom, left, right = self.get_position()
        screenshot = self.get_screenshot()
        self.captcha1 = screenshot.crop((left, top, right, bottom))
        self.captcha1.save(name)

    #2获取带缺口的验证图截图
    def get_q_jyimage(self,name='qcaptcha.png'):
        self.hkbtn=self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'gt_slider_knob')))
        self.hkbtn.click()
        # time.sleep(1)
        top, bottom, left, right = self.get_position()
        screenshot = self.get_screenshot()
        self.captcha2 = screenshot.crop((left, top, right, bottom))
        self.captcha2.save(name)

    #4对比像素点的不同
    def is_pixel_equal(self, image1, image2, x, y):
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True  #像素点是相同的
        else:
            return False
    
    #3获取缺口位置到滑块的偏移量
    def same_image(self):
        # threshold = 0.95# 相似度阈值
        # count = 0
        dif=[]
        fdif=[]
        # imagename1='captcha.png'
        # imagename2='pcaptcha.png'
        # path1=filepath+imagename1
        # path2=filepath+imagename2
        image1=Image.open('captcha.png')#打开完整截图，输入图片的路径filepath
        image2=Image.open('qcaptcha.png')#打开缺口图，输入图片的路径filepath
        for x in range(image1.width):
            for y in range(image1.height):
                # 判断像素是否相同，不同则加入列表
                if not self.is_pixel_equal(image1, image2, x, y):
                    if x not in dif:
                        dif.append(x)
        fdif.append(dif[0])
        # print("0:",dif)
        # print("1:",fdif)
        #通过依次对比，观察验证码的特点，得到滑块起始位置和要移动到的位置
        for i in range(len(dif)-1):
            if dif[i+1]-dif[i]>10:
                fdif.append(dif[i+1])
                break
        # print("2:",fdif)
        distance=fdif[1]-fdif[0]
        print(distance)
        return distance

    #5变速滑动滑块(匀速会失败)
    def track(self,x):
        track=[]
        current=0
        mid=x*4/7   
        t=0.1
        v=0
        while current<x:
            if current<mid:
                a=25
            else:
                a=-25
            v0=v
            v=v0+a*t
            move=v0*t+1/2*a*t*t
            current+=move
            track.append(round(move))
        print(sum(track))
        return track
    
    #6移动滑块
    def move(self):
        distance=self.same_image()
        lis=self.track(distance)
        print(lis)
        ActionChains(self.bro).click_and_hold(self.hkbtn).perform()
        for i in lis:
            ActionChains(self.bro).move_by_offset(xoffset=i, yoffset=0).perform()
        ActionChains(self.bro).move_by_offset(xoffset=-2, yoffset=0).perform()
        time.sleep(0.25)
        ActionChains(self.bro).release().perform()


def main():
    url='https://passport.bilibili.com/login'
    bro=webdriver.Firefox()
    
    a=bilibili(url=url,bro=bro)
    a.webbro()
    a.input_msg(uname,upwd)
    a.get_jyimage()
    a.get_q_jyimage()
    a.move()

if __name__ == '__main__':
    main()