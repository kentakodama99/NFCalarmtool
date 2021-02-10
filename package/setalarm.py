# モジュール読み込み
from flask import Flask
import time
import nfc
import datetime
import pygame.mixer
from package import DB

# --------------------------------------
# Alarm01:ピピ！___ピピ！___ピピ！      #
# Alarm02:ﾋﾟﾋﾟﾋﾟﾋﾟ!___ﾋﾟﾋﾟﾋﾟﾋﾟ!___      #
# Alarm03:ﾋﾟﾋﾟﾋﾟﾋﾟﾋﾟﾋﾟﾋﾟﾋﾟﾋﾟ            #
# Alarm04:ﾋﾟｯ___ﾋﾟｯ____ﾋﾟｯ             #
# --------------------------------------

#アラームセット
def setting(s_hours,s_minutes):
  alarm_set=(s_hours.zfill(2)+":"+s_minutes.zfill(2)) #指定した時間をセット
  print(alarm_set+"にセットしました") #セット確認用
  DB.startDB()
  return alarm_set #(時間:分)を返す


#NFCにタッチした時の動作
def connected(tag):
    return False #次の処理に進む。


#アラーム時の動作
def alarm_start():
  print("時間です！")
  pygame.mixer.init() #サウンド初期化
  pygame.mixer.music.load('./mp3/Alarm01.mp3') #読み込み
  pygame.mixer.music.play(-1) #サウンド無限ループ再生(引数で指定した値だけループ)
  clf = nfc.ContactlessFrontend('usb') #RC-S380をUSBから認識
  tag = clf.connect(rdwr={'on-connect': connected}) #ICカード読み込みモード。タッチ時connected実行
  pygame.mixer.music.stop() #サウンド停止
  DB.stopDB() # database整理関数
  return