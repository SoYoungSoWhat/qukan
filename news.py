#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import time
import datetime
import adbShell
# import logger


FUN_PACKAGE = "com.jifen.qukan"
FUN_MAIN_PAGE = "com.jifen.qkbase.main.MainActivity"
FUN_ARTICLE_PAGE = ".content.newsdetail.news.NewsDetailNewActivity"
FUN_VIDEO_NEWS_PAGE = ".content.newsdetail.video.VideoNewsDetailNewActivity"

NewsCount = 10
ShortVideoCount  = 6
LongVideoCount  = 4

MODE_WATCH_NEWS = 0
MODE_WATCH_SHORT_VIDEO = 1
MODE_WATCH_LONG_VIDEO = 2

mMode = 0
mShortVideoCount = 0
mLongVideoCount = 0

mNewsCount = 0
mIsOnLine = True
isFirstNewsRun = True
isFirstVideoRun = True
mCurentHour = -1
mCurrentPackage = ''
mCurrentActivity = ''

def isDeviceAlive():
  result = adbShell.getAllDevices()
  if result.find('device') == -1:
    return False
  return True

def refreashStateInfo():
  global mCurrentPackage
  global mCurrentActivity
  global mIsOnLine

  mIsOnLine = isDeviceAlive();
  if mIsOnLine == False:
    return

  result = adbShell.getTopActivity()
  print(result)
  if result.find("ACTIVITY") == -1:
    return False
  resList = result.split(' ')
  if len(resList) != 4:
    return
  appInfo = resList[1]
  appInfoList = appInfo.split('/')
  if len(appInfoList) != 2:
    return
  mCurrentPackage = appInfoList[0]
  mCurrentActivity = appInfoList[1]
  return False;

def schedule():
  global mMode
  global mNewsCount
  global mShortVideoCount
  global mLongVideoCount
  if mMode == MODE_WATCH_NEWS:
    if mNewsCount < NewsCount:
      return
    print('切换到浏览短视频模式')
    mMode = MODE_WATCH_SHORT_VIDEO
    mShortVideoCount = 0
    return

  if mMode == MODE_WATCH_SHORT_VIDEO:
    if mShortVideoCount < ShortVideoCount:
      return
    print('切换到浏览长视频模式')
    mMode = MODE_WATCH_LONG_VIDEO
    mLongVideoCount = 0
    return

  if mMode == MODE_WATCH_LONG_VIDEO:
    if mLongVideoCount < LongVideoCount:
      return
    print('切换到浏览新闻模式')
    mMode = MODE_WATCH_NEWS
    mNewsCount = 0
    return
  
def onAppDie():
  adbShell.startApp()

# 获取当前小时
def getCurrentHour():
  now = datetime.datetime.now()
  return now.hour

# //领取每小时的金币
def getHourReward():
  global mCurentHour
  curHour = getCurrentHour()
  print('当前时间:' + str(curHour))
  if mCurentHour != curHour:
    adbShell.switchTabBar(0)
    time.sleep(3)
    adbShell.clickHourReward();
    time.sleep(1)
    adbShell.back()
    mCurentHour = curHour
    return

def watchNews():
  global mNewsCount
  global isFirstNewsRun
  print ('watchNews')
  adbShell.switchTabBar(0)
  time.sleep(1)

  if isFirstNewsRun == True:
    adbShell.switchNewsType()
    isFirstNewsRun = False

  time.sleep(3)
  adbShell.chooseAnArticle();
  refreashStateInfo();

  time.sleep(1)
  if (mCurrentActivity == FUN_ARTICLE_PAGE or 
    mCurrentActivity == FUN_VIDEO_NEWS_PAGE):
    onNewsPage()
    adbShell.getNewNews()
    time.sleep(2)


def watchShortVideo():
  global mShortVideoCount
  global isFirstVideoRun

  adbShell.switchTabBar(1)
  time.sleep(1)

  if isFirstVideoRun == True:
    adbShell.switchVideosType()
    isFirstVideoRun = False
    time.sleep(2)

  adbShell.chooseAnArticle();
  delay = random.randint(8,20);
  time.sleep(delay)

  mShortVideoCount += 1
  print('浏览小视频数：' + str(mShortVideoCount) )

def watchLongVideo():
  global mLongVideoCount

  adbShell.switchTabBar(2)
  time.sleep(1)

  adbShell.getNewNews();
  time.sleep(2)
  delay = random.randint(8,20);
  time.sleep(delay)

  mLongVideoCount += 1
  print('浏览长视频数：' + str(mLongVideoCount) )


def onMainPage():
  global mShortVideoCount
  getHourReward()
  print ('mMode = ' + str(mMode))

  if mMode == MODE_WATCH_NEWS:
    watchNews()
    return

  if mMode == MODE_WATCH_SHORT_VIDEO:
    watchShortVideo()
    return

  if mMode == MODE_WATCH_LONG_VIDEO:
    watchLongVideo()
    return

 # //文章详细界面，滑动阅读
def onNewsPage():
  global mNewsCount
  global mMode
  global mCurrentActivity

  refreashStateInfo();

  if (mCurrentActivity != FUN_ARTICLE_PAGE and 
    mCurrentActivity != FUN_VIDEO_NEWS_PAGE):
    return
  if mMode != MODE_WATCH_NEWS:
    adbShell.back()
    time.sleep(1)
    return

  print('往下滑动...')
  for i in range(1,9):
    adbShell.scrollDown();
    time.sleep(0.7)
  print('往上滑动...')
  for i in range(1,5):
    adbShell.scrollUp();
    time.sleep(0.7)

  if (mCurrentActivity == FUN_ARTICLE_PAGE or 
    mCurrentActivity == FUN_VIDEO_NEWS_PAGE):
    time.sleep(0.5)
    mNewsCount += 1
    print('浏览新闻数：' + str(mNewsCount))
    adbShell.back()

def onOtherPage():
  adbShell.back()

def earnMoney():

  global mCurrentPackage
  global mCurrentActivity
  while True:
    refreashStateInfo()
    if mIsOnLine == False:
      print('设备不在线!')
      break
    schedule()

    print (mCurrentActivity)

    if mCurrentPackage != FUN_PACKAGE:
      onAppDie()
      continue
    if mCurrentActivity == FUN_MAIN_PAGE:
      onMainPage()
      continue
    onOtherPage();

# clickVideoBtn()
if __name__=='__main__':
  earnMoney()
