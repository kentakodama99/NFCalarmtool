<template>
  <div id="Setmenu">
    <div class="button-submit">
    <!-- button -->
    <button @click="setting(); openModal()" class="button"><p>set</p></button>
    <!-- モーダルウィンドウ -->
    <transition name="fade">
      <div id="overlay" v-if="Modal.show">
        <!-- 設定画面:set -->
        <div v-if="swich">
          <div class="Modalbox-true">
            <p>アラーム設定中です</p>
            <div class="Modalsettext">
              <p>設定時刻</p>
              <p>{{this.alarm.temp}}</p>
            </div>
            <button @click="getreset(); closeModal()" class="alarm-button"><p>Cansel</p></button>
            <!-- 30分後に早起き用のstopボタン -->
            <div>
              <button @click="getealrybottom()" class="earlystop"><span class="earlystop_text">STOP amarm!!</span></button>
            </div>
          </div>
        </div>
        <!-- 設定画面:alarm -->
      <div v-else>
        <div class="Modalbox-false">
          <p>時間です！</p>
        </div>
      </div>
      </div>
    </transition>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  props: ["parentData","timenowText"],
  data(){
    return{
      alarm:{
        inth:0,
        intm:0,
        item:"",
        outth:"",
        temp:"",
        time_start:false
      },
      Modal:{
        show:false
      },
      swich:true,
      justtime:false,
      itemstatus:""
    };
  },
  created(){
    this.getreset();
    setInterval(this.getjuststatus, 1000); 
    setInterval(this.timer, 1000);
  }, 
  methods:{
    async setting(){
      this.status=false;
      //Home.vueから受け取ったinputの値の処理
      this.item=this.parentData;
      this.alarm.inth=this.item.inth;
      this.alarm.intm=this.item.intm;
      // start_api
      const path='/api/start/'
      let params=new FormData()
      params.append('inth',this.alarm.inth)
      params.append('intm',this.alarm.intm)
      console.log(params)
      await axios.post(path,params)
      .then(response => {console.log(response);})
      .catch(error => {console.log(error);});
      //set時刻を(xx:yy)に変換
      this.alarm.intm=('0' + this.alarm.intm).slice(-2);
      this.alarm.temp=(this.alarm.inth+":"+this.alarm.intm) //tempに(xx:yy)を保存
      console.log("set:",this.alarm.temp)
    },
    async getreset(){
      //初期化
      this.alarm.outth="" //時間の初期化
      this.alarm.temp=""
      this.alarm.inth=0
      this.alarm.inth=0
      //resetapi
      const path=`/api/reset/`
      await axios.get(path)
      .then(response => {console.log(response);})
      .catch(error => {console.log(error);});
    },
    async getealrybottom(){
      //api
      const path=`/api/stop/`
      await axios.get(path)
      .then(response => {console.log(response);})
      .catch(error => {console.log(error);});
      //初期化、結果画面に遷移
      this.justtime=false;
      this.alarm.time_start=false;
      this.$router.push({ name: "Result" });
    },
    openModal(){
      this.swich=true;
      this.Modal.show=true;
      this.alarm.time_start=true;
      console.log("open_time_start:",this.alarm.time_start)
    },
    closeModal(){
      this.justtime=false;
      this.Modal.show=false;
      this.alarm.time_start=false;
      console.log("close_time_start:",this.alarm.time_start)
    },
    timer(){
      if(this.alarm.time_start==true){
        var date = new Date();
        var house= date.getHours()
        var minutes=date.getMinutes()
        minutes=('0' + minutes).slice(-2);
        this.now = (house+ ':' +minutes);
        /*設定時間処理*/
        if(this.alarm.temp==this.now){ 
          this.swich=false;
          this.alarm.time_start=false;
          this.justtime=true;
        }
      }
    },
    async getjuststatus(){
      // 1秒おきに関数を実行しているが、アラーム時のみif以下動作
      // api
      if(this.justtime==true){
        const path=`/api/status/`
        await axios.get(path)
        .then(response => {this.itemstatus=response.data;})
        .catch(error => {console.log(error);});
        // スレッドが停止していれば結果画面に遷移
        if(this.itemstatus.status==false){
          this.justtime=false;
          this.alarm.time_start=false;
          this.$router.push({ name: "Result" });
        }
      }
    }
  }
};
</script>

<style>
p{
  font-size:36px;
}

.button-submit{
  text-align:center
}

.button {
  background: #c9fffc;
  margin: 30px 0;
  width:150px;
  border-radius:50px;
  cursor: pointer;
}

.button p{
  font-size:36px;
}

/*Modal*/
.fade-enter-active,.fade-leave-active{
  transition:0.5s;
}
.fade-enter,.fade-leave-to{ /*0→1,1→0にするトリガ*/
  opacity:0;
}

#overlay{
  z-index:1;
  position:fixed;
  top:0;
  left:0;
  width:100%;
  height:100%;
  background-color:rgba(0,0,0,0.8);
  display: flex;
  align-items: center;
  justify-content: center;
}

.Modalbox-true{
  color:#fff;
  text-align:center;
  z-index:2;
  padding:20px;
  background-color:#003A47;
  border:1px solid #fff;
}

.alarm-button{
  margin: 30px 0;
  width:150px;
  border-radius:50px;
  cursor: pointer;
  width:200px;
  background:#fff;
}

.earlystop{
  margin: 10px 0;
  border-radius:50px;
  cursor: pointer;
  width:130px;
  background:gray;
  font-size:16px;
}

.earlystop_text{
  font-size:16px;
}

.Modalsettext{
  line-height:1;
  padding:20px;
}

.Modalsettext p{
  font-size:24px;
}

.Modalbox-false{
  color:#fff;
  text-align:center;
  z-index:2;
  padding:20px;
  background-color:red;
  border:1px solid #fff;
}

@media screen and (max-width:768px){
.Modalbox{
  width:100%;
}
}
</style>