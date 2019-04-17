#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os 
import time
import random
# import logger

isEmulator = True

# 屏幕的尺寸
size = {'width': 1080,'height': 1920}

def execute(cmd):
  return os.popen('adb shell "{}"'.format(cmd)).read()

def rand(x):
  return random.randint(1,x);

# 执行点击
def execTap(x, y):
  execute('input tap {} {}'.format(x, y))

# 执行滑动
def execSwip(sx, sy, ex, ey, duration = 500):
  execute('input swipe {} {} {} {} {}'.format(sx, sy, ex, ey, duration))

# 启动趣头条
def startApp():
  package = 'com.jifen.qukan'
  result = execute('monkey -p {} 1'.format(package))
  time.sleep(4)
  result = execute('ps | grep {}'.format(package))
  if result.find(package) != -1:
    return True
  return False

# 点击左下角的头条按钮
# x: [60 : 115]
# y: [1850 : 1908]
def clickTopTitle():
  execTap(100 + rand(75),size["height"] - 70 + rand(58))
  print('点击左下角的头条按钮.')
  return True

# 切换Tabbar
def switchTabBar(index):
  execTap((size["width"] / 5) * index + 80 + rand(20), size["height"] - 70 + rand(58))
  print('切换到第{}个Tabbar.'.format(index))

# 点击领取小时金币奖励按钮
# x: [945 : 964]
# y: [106 : 116]
def clickHourReward():
  if isEmulator == True:
    #模拟器的新闻位置
    execTap(size["width"] - 135 + rand(19),84 + rand(20))
  else:
    execTap(size["width"] - 135 + rand(19),106 + rand(20))
  # 
  print('点击领取小时金币奖励按钮.')

# 发送back键
def back():
  print('点击返回.')
  execute('input keyevent 4')

# 选择一个文章(就是第一个文章)
def chooseAnArticle():
  #手机的新闻位置
  if isEmulator:
    execTap(586 + rand(100),300 + rand(10))
  else:
    execTap(586 + rand(100),520 + rand(10))
  print('选择第一篇新闻.')

# 往上滑动
def scrollUp():
  startX = 190 + rand(100);
  startY = 1000 + rand(100);
  endX = startX + 100;
  endY = startY + 300;
  execSwip(startX,startY,endX,endY)

# 往下滑动
def scrollDown():
  startX = 300 - rand(100);
  startY = 1300 + rand(100);
  endX = startX - 100;
  endY = startY - 300;
  execSwip(startX,startY,endX,endY)

# 获取最新的数据
def getNewNews():
  startX = size["width"] / 2 + 80 + rand(100);
  startY = size["height"] / 2 - 220 + rand(100);
  endX = startX;
  endY = startY + 600;
  execSwip(startX,startY,endX,endY)
  print('获取最新的数据...')


# 切换头条文章类型，因为默认第一个是政治类新闻，我选了第三个类型
# x:360~ 540
def switchNewsType():
  startX = 250 + rand(5);
  startY = 280 + rand(5);

  endX = startX + 800;
  endY = startY + 2;
  execSwip(startX,startY,endX,endY)
  if isEmulator:
    execTap(size["width"] / (9 / 2) + 28 + rand(5),160 + rand(5))
  else:
    execTap(size["width"] / (6 / 2) + 56 + rand(5),285 + rand(5))

  print('切换到第三个文章类型...')

def switchVideosType():
  execTap(size["width"] / (6 / 2) + 56 + rand(5),80 + rand(5))
  print('切换到第三个视频类型...')

#显示顶层的Activity
def getTopActivity():
  print('显示顶层的Activity')
  return execute('dumpsys activity top | grep pid').strip()

def getAllDevices():
  print('获取所有的devices')
  return os.popen('adb devices').read()

# chooseAnArticle()

# 滑动：adb shell input swipe 500 1000 500 400

# 点击：adb shell input tap 972 1260
# 查看一个文章 550 480

# 启动：adb shell "monkey -p com.jifen.qukan 1"

# 返回：adb shell input keyevent 4
# adb shell dumpsys activity top | grep pid
