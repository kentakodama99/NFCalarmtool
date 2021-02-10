# モジュール読み込み
import pymysql.cursors
import datetime

#-----------------------------------------------------------------------------------------------------------------------------#
# graphdb(id,date(XXXX-YY-ZZ),startdate(XXXX-YY-ZZ xx:yy:xx.aaaaaa),stopdate(XXXX-YY-ZZ xx:yy:xx.aaaaaa))                     #
# totaldb(id,date(XXXX-YY-ZZ),startdate(XXXX-YY-ZZ xx:yy:xx.aaaaaa),stopdate(XXXX-YY-ZZ xx:yy:xx.aaaaaa))                     #
#                                                                                                                             #
# CREATE TABLE totaldb(id int auto_increment,date DATE,startdate DATETIME(0),stopdate DATETIME(0),index(id),primary key(id)); #
# CREATE TABLE graphdb(id int,date DATE,startdate DATETIME(0) ,stopdate DATETIME(0) ,primary key(id));                        #
#                                                                                                                             #
# id1~5:グラフ格納用                                                                                                           #
# id6:temp用                                                                                                                  #
#-----------------------------------------------------------------------------------------------------------------------------#


# MySQLに接続する
def getConnection():
  return pymysql.connect( #初期設定
  host='localhost',
  user='root',
  password='ouyousql18k',
  db='alarm-db',
  charset='utf8',
  cursorclass=pymysql.cursors.DictCursor 
  # True=> {'id': id, 'name': name, 'age': age}
  # False=> (id,name,age}
  )


#startdateのDB格納
def startDB():
  connection=getConnection() # MySQLに接続する
  start_dt = datetime.datetime.now() #現在時刻の取得
  start_dt_temp =start_dt.strftime("%Y-%m-%d %H:%M:%S") #DBに格納できるformatに変換
  # Insert処理
  with connection.cursor() as cursor: #connection.cursor() カーソルオブジェクトを取得
    # id6の中身がNULLならdate,startdateをpush,それ以外はid6のdate,startdateの更新
    sql = "INSERT INTO graphdb (id, date, startdate) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE id = VALUES(id),date = VALUES(date),startdate = VALUES(startdate)"
    cursor.execute(sql, (6, start_dt.date(), start_dt_temp)) #SQLの実行
    connection.commit() # autocommitではないので、明示的にコミットする


#stopdateのDB格納＆グラフの更新
def stopDB():
  connection=getConnection() # MySQLに接続する
  stop_dt = datetime.datetime.now() #現在時刻の取得 #DBに格納できるformatに変換
  stop_dt=stop_dt.strftime("%Y-%m-%d %H:%M:%S")
  # Insert処理
  with connection.cursor() as cursor: #connection.cursor() カーソルオブジェクトを取得
    # id6の中身がNULLならstopdateをpush,それ以外はid6のstopdateの更新
    sql = "INSERT INTO graphdb (id,stopdate) VALUES (%s, %s) ON DUPLICATE KEY UPDATE id = VALUES(id),stopdate = VALUES(stopdate)"
    cursor.execute(sql, (6,stop_dt)) #SQLの実行 結果をrに格納
    connection.commit() # autocommitではないので、明示的にコミットする
    DBupdate(connection) # DBupdate()の実行。graphdbの整理を行う。


# graphdbの整理
def DBupdate(connection):
  with connection.cursor() as cursor: #connection.cursor() カーソルオブジェクトを取得
    totalDATA(connection) #id6(temp)のDB情報をtoaldbにpush
    #id1~5の間で中身にデータがなければ、そのidにid6のDB情報をpushする。
    sql = "SELECT * FROM graphdb WHERE id=6" #id6のDB情報を抽出
    cursor.execute(sql) #SQLの実行(id=6)
    temp=cursor.fetchall() #id6のDB情報を出力。tempに格納
    sql = "SELECT COUNT(*) FROM graphdb" #COUNT(*)によってデータの存在の判定 例:id=6のみの場合COUNT=1=>id=1にpush
    cursor.execute(sql) #SQLの実行 (COUNT(*))
    count=cursor.fetchall() #COUNT(*)の出力。存在状態の判定
    #id1~5の中身にデータがなければ、idの小さい場所にpush
    if not count[0]['COUNT(*)']==6:
      sql = "INSERT INTO graphdb (id,date,startdate,stopdate) VALUES (%s, %s,%s,%s)"
      cursor.execute(sql, (count[0]['COUNT(*)'],temp[0]['date'],temp[0]['startdate'],temp[0]['stopdate'])) #SQLの実行 結果をrに格納
      connection.commit() #autocommitではないので、明示的にコミットする
    #id1~5の中身にデータがあれば、id2~6を繰り下げて更新。
    else:
      for i in range(1,count[0]['COUNT(*)']): #1,2,3,4,5のforループ
        sql = "SELECT * FROM graphdb WHERE id=%s" #id(i+1)【2,3,4,5,6】のDB情報を抽出
        cursor.execute(sql,(i+1)) #SQLの実行(i+1注意)
        temp_up=cursor.fetchall() #id(i+1)【2,3,4,5,6】のDB情報を出力。temp_upに格納
        # id(i)にid(i+1)のDB情報の更新
        sql = "INSERT INTO graphdb (id,date,startdate,stopdate) VALUES (%s, %s,%s,%s) ON DUPLICATE KEY UPDATE id = VALUES(id),date = VALUES(date),startdate = VALUES(startdate),stopdate = VALUES(stopdate)"
        cursor.execute(sql, (i,temp_up[0]['date'],temp_up[0]['startdate'],temp_up[0]['stopdate'])) #SQLの実行 結果をrに格納
        connection.commit() #autocommitではないので、明示的にコミットする


# id6のDB情報をtoaldbにpush
def totalDATA(connection):
  with connection.cursor() as cursor: #connection.cursor() カーソルオブジェクトを取得
    sql = "SELECT * FROM graphdb WHERE id=6" #graphdbのid6のDB情報を抽出
    cursor.execute(sql) #SQLの実行
    temp=cursor.fetchall() #graphdbのid1のDB情報を出力。tempに格納
    # totaldbにgraphdbのid1のDB情報をpush
    sql = "INSERT INTO totaldb (date,startdate,stopdate) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE date = VALUES(date),startdate = VALUES(startdate),stopdate = VALUES(stopdate)"
    cursor.execute(sql, (temp[0]['date'],temp[0]['startdate'],temp[0]['stopdate'])) #SQLの実行 結果をrに格納
    connection.commit() #autocommitではないので、明示的にコミットする


# if __name__ == "__main__":
#   connection=getConnection()
  # startDB()
  # stopDB()
  # test(connection)
  # DBupdate(connection)
  # totalDATA(connection)