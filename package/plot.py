
#database
import pymysql.cursors
#matplotlib
import matplotlib
matplotlib.use('Agg') #plt前にこの言葉がないとGUIの事情で警告がでる。
import matplotlib.pyplot as plt # pltとしてインポートされるのが慣例です。
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker
import numpy as np
#etc
import os
import datetime 
import numpy as np
import json
#packege
from package import DB

# MySQLに接続する
# def getConnection():
#   return pymysql.connect( #初期設定
#   host='localhost',
#   user='root',
#   password='ouyousql18k',
#   db='alarm-db',
#   charset='utf8',
#   cursorclass=pymysql.cursors.DictCursor 
#   # True=> {'id': id, 'name': name, 'age': age}
#   # False=> (id,name,age}
#   )

# 睡眠時間の計算(startalarm,stopalarm)
def calsleep(start,stop):
  dt1 = start #現在時刻の取得
  dt2 = stop #任意時刻の取得
  dt3=dt2-dt1 #任意の時刻-現在時刻  時刻の差分の計算(睡眠時間)
  dt3=dt3.seconds #睡眠時間の秒数変換
  # print(dt3) ###確認用###
  return dt3

#graphdbの中身を出力
def sql_graph():
  connection=DB.getConnection()
  with connection.cursor() as cursor:  #connection.cursor() カーソルオブジェクトを取得
    sql = "SELECT * FROM graphdb ORDER BY id DESC" #sql構文
    cursor.execute(sql) #SQL実行
    # Select結果を取り出す
    return cursor.fetchall() #fileを全行取得して代入

#graphdbから日付、睡眠時間を配列出力
def plotdata():
  date=[]
  sleeptime=[]
  results=sql_graph() #graphのDBの中身を出力
  #temp(id=6)の削除
  del results[0] 
  for i in range(len(results)): #date,sleeptimeを順に指定
    date.append(results[i]['date'])
    sleeptime.append(calsleep(results[i]['startdate'],results[i]['stopdate']))
  # 平均睡眠時間の文字列設定
  avesleep=int(sum(sleeptime)/len(results)) #平均睡眠時間
  avehour=int(avesleep/3600) #dt3tempから時間のみ抽出(intじゃないと小数点がでる)
  avetemp=avesleep%3600 #dt3tempから時間を除いた秒数を再び格納
  aveminute=int(avetemp/60) #dt3tempから分のみ抽出(intじゃないと小数点がでる)
  avetemp=avetemp%60 #dt3tempから分を除いた秒数を格納(秒数抽出となる)
  avesleep=str(avehour).zfill(2)+":"+str(aveminute).zfill(2)+":"+str(avetemp).zfill(2) #出力
  return date,sleeptime,len(results),avesleep #date:日付、sleeptime:睡眠時間、len(results):data数、avesleep:平均睡眠時間


#mainplot
def exportplot():
  #DB_read
  date,sleeptime,datacount,avesleep=plotdata() #graphdbから日付、睡眠時間 、data数、平均睡眠時間のexport
  #create_plot
  #グラフ初期設定
  plt.clf() #graphの削除。初期化
  x=np.arange(0,datacount,1) #x軸:0から4まで1間隔[0,1,2,3,4](x軸は表記のみdateにしたいため、x間隔は等間隔)
  y=sleeptime #y軸:睡眠時間
  figure_ = plt.figure(1) #図の作成
  axes_=figure_.add_subplot(111) #Axes作成
  plt.title("Average("+str(avesleep)+")",fontsize=(20)) #graphtitle【Average({{平均睡眠時間}})】
  # X軸設定
  xaxis_=axes_.xaxis #XAxis取得
  plt.xlabel('Date') #x軸ラベル
  new_xticks =np.arange(0,datacount,1) #目盛りの場所を等間隔にする
  xaxis_.set_major_locator(ticker.FixedLocator(new_xticks)) #Locator:目盛りを指定。
  xaxis_.set_ticklabels(date) #横軸表記をdateに変更する
  # Y軸設定
  yaxis_=axes_.yaxis #YAxis取得 
  plt.ylabel('time of sleeping[h]') #y軸ラベル
  maxtemp=(int(max(sleeptime)/3600)+1)*3600 #y軸最大値の設定(8000なら9600など)
  #---目盛り指定---#
  new_yticks =np.arange(0,maxtemp+3600,3600) #目盛りの場所を1hごとにする
  yaxis_.set_major_locator(ticker.FixedLocator(new_yticks)) #Locator:目盛りの場所(1hごとに目盛りを指定)
  axes_.grid(which = "major", axis = "y", color = "blue", alpha = 0.8,
        linestyle = "--") #gridの指定
  #---文字列変換---#
  Y_hour_str=[] #(01:00)1hourを文字列表記するための配列
  for i in range (int(maxtemp/3600)+1): #00:00を含むため、(maxtemp/3600)+1
    Y_hour_str.append(str(i)+":00") 
  yaxis_.set_ticklabels(Y_hour_str)#縦軸表記を(xx:yy)に変更する
  # plot and save
  axes_.plot(x, y,'o-') #plot
  # plt.show() ###確認用###
  dir="./img/"
  plt.savefig(os.path.join(dir,"graph.png")) #save


# main_graphdb_out graphdbの中身をjson出力
def graphtable():
  results=sql_graph() #graphのDBの中身を出力
  #temp(id=6)の削除
  del results[0]
  for i in range(len(results)): #date,sleeptimeを文字列指定
    dt3temp=calsleep(results[i]['startdate'],results[i]['stopdate']) #sleeptime
    #sleeptimeを(xx時間yy分zz秒)表記に変換
    dt3hour=int(dt3temp/3600) #dt3tempから時間のみ抽出(intじゃないと小数点がでる)
    dt3temp=dt3temp%3600 #dt3tempから時間を除いた秒数を再び格納
    dt3minute=int(dt3temp/60) #dt3tempから分のみ抽出(intじゃないと小数点がでる)
    dt3seconds=int(dt3temp%60)
    #detetime型をstrに変換 and dt3を辞書型に書き込み
    dt3=str(dt3hour).zfill(2)+":"+str(dt3minute).zfill(2)+":"+str(dt3seconds).zfill(2) #出力
    results[i]['sleeptime']=dt3 #sleeptime
    results[i]['date']=str(results[i]['date']) #date
    results[i]['startdate']=str(results[i]['startdate']) #starttime
    results[i]['stopdate']=str(results[i]['stopdate']) #stoptime
  json_str=json.dumps(results) #辞書型から JSON 形式の文字列へ変換
  return json_str #出力

# if __name__ == "__main__":
  # print( sql_graph())
  # connection=DB.getConnection()
  # a,b,datacount,avesleep=plotdata()
  # print(a,b,datacount,avesleep)
  # exportplot()
  # print(graphtable())