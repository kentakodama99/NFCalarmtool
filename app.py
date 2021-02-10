# from datetime import datetime
# -----------------------------
# request フォームから送信した情報を扱うためのモジュール
# redirect  ページの移動
# url_for アドレス遷移
# send_from_directory 画像のダウンロード
# -------------------------------
from flask import Flask, make_response, jsonify,render_template,request,url_for,redirect,send_file,send_from_directory
import time
import datetime
import pygame.mixer
import threading
from package import setalarm as set
from package import plot as plot
from package import DB
import os


app = Flask(__name__, static_folder="./dist", static_url_path="")
# app = Flask(__name__)

# img----------------
UPLOAD_FOLDER = './img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ------------------------------------


class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread,self).__init__() #super() は親クラスを示すためのメソッド。super().__init__() は  クラスの __init__ メソッドを実行
        
    def stop(self): #中断フラグ
        self.stop=True #stopフラグを有効にする

    def run(self):
        try:
            alarm_set=jobs["alarm_set"] #setting関数でセットした時刻(jobs["alarm_set"])をalarm_setに格納
            #-確認用se-
            pygame.mixer.init() #サウンド初期化
            pygame.mixer.music.load("./mp3/se/on.mp3") 
            pygame.mixer.music.play(1) #サウンド無限ループ再生(引数で指定した値だけループ)
            time.sleep(0.1) #安定してse再生するための待機時間(次の処理が初期化のため)
            #--------
            pygame.mixer.init() #サウンド初期化
            pygame.mixer.music.load("./mp3/wait/nosound_one_millisecond.wav") #無音読み込み
            #セットした時間≠現在時刻ならセット時間までループ
            #stopフラグが有効(中断)時、whileループから脱出。
            while not self.stop==True:  
                dt_now=datetime.datetime.now() #現在時刻生成
                dt_now=dt_now.strftime('%H:%M')#現在時刻を(xx:yy)の形に変換
                if alarm_set==dt_now: #セットした時間＝現在時刻
                    set.alarm_start() #アラーム起動 alarm_start関数
                    break #ループ脱出
                print(dt_now) ####確認用####
                pygame.mixer.music.play(1) #サウンド無限ループ再生(引数で指定した値だけループ)
                time.sleep(1) #1秒間隔で待機

        finally:
            if self.stop==True: #stopフラグが有効(中断)時、無効にする。
                self.stop=False #stopフラグを無効にする
            else:
                del jobs["Thread"] #jobs["Thread"]の削除。※status判定用
                plot.exportplot()
            print("end run")

jobs = {} #辞書型の初期化。セット時間["alarm_set"]、スレッドの管理["Thread"]を行う。


#default(アクセス時の最初の画面)
# @app.route('/')
# def index():
#     return render_template('index.html') #アクセス時の最初の画面

@app.errorhandler(404)
def index(_):
    return send_file("./dist/index.html")

#api
@app.route('/api/start/' , methods=["POST"]) #formから送信された時。スレッドの開始
def start():
    if "Thread" in jobs: #常にセットされている場合、最新の時間に更新する。
        jobs["Thread"].stop() #jobs["Thread"]の削除。※task判定用
        print("削除しました。")
    hours=request.form["inth"] #時間をhoursに格納
    minutes=request.form["intm"] #時間をminutesに格納
    jobs["alarm_set"]=set.setting(hours,minutes) #setting関数によって(xx:yy)に変換し、jobs["alarm_set"]に格納
    task=MyThread() #MyThreadクラスをtaskに格納
    task.start() #スレッド(アラームスクリプト)の実行
    jobs["Thread"]=task #taskをjobs["Thread"](スレッドの管理)に格納
    return make_response('start OK'), 202 #セット時間にreturn

@app.route('/api/reset/') #キャンセルボタンを押した時。スレッドの停止
def reset():
    if not "Thread" in jobs: #セットされていない場合error_messageを返す。
        return  make_response('reset OK'),200
    else:
        jobs["Thread"].stop() #スレッド(アラームスクリプト)のstop()を動かす。#stopフラグを有効にする
        del jobs["Thread"] #jobs["Thread"]の削除。※task判定用
        #-確認用se-
        pygame.mixer.init() #サウンド初期化
        pygame.mixer.music.load("./mp3/se/off.mp3") #off用音声 
        pygame.mixer.music.play(1) #サウンド1回再生
        #--------
        return make_response('reset OK'), 202 #resetをreturn

@app.route('/api/stop/') #キャンセルボタンを押した時。スレッドの停止
def stop():
        jobs["Thread"].stop() #スレッド(アラームスクリプト)のstop()を動かす。#stopフラグを有効にする
        del jobs["Thread"] #jobs["Thread"]の削除。※task判定用
        DB.stopDB()
        plot.exportplot()
        return make_response('reset OK'), 202 #resetをreturn

@app.route('/api/status/') #実行状態の確認
def status():
    if "Thread" in jobs: #jobs["Thread"]の存在状態によって対応したjsonを返す。
        #response(status:実行状態)
        response = {
            "status": True,
        }
        return jsonify(response), 200 #jsonをreturn
    else:
        #response(status:実行状態)
        response = {
            "status":False,
        }
        return jsonify(response), 200 #jsonをreturn

# img生成 URLにtimestampを与えることでキャッシュ回避
@app.route('/alaimg/<filename>/<timestamp>')
def img_file(filename,timestamp):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#graphのdata+sleeptimeをjsonで返す。
@app.route('/api/graphtable/')
def graphteble():
    response=plot.graphtable() #graphdbのdb1~5+sleeptimeをjsonで返す
    return jsonify(response), 200 #jsonをreturn


if __name__ == "__main__":
    app.run(host='localhost')
    # app.run(host='0.0.0.0')