<template>
  <div id="main">
    <div class="time-box">
      <p class="timetitle">目覚まし時刻を入力してください</p>
    </div>
    <div class="set-box">
      <select type="number" v-model="alarm.inth" class="time">
        <option>0</option>
      <option v-for="(index) in 23" :key="index">{{index}}</option>
      </select>
      <p>時</p>
      <select type="number" v-model="alarm.intm" class="time">
        <option>0</option>
        <option v-for="(index) in 59" :key="index">{{index}}</option>
      </select>
      <p>分</p>
    </div>
    <Setmenu :parentData="alarm"></Setmenu>
    <Detail></Detail>
  </div>
</template>

<script>
import Setmenu from "../components/Setmenu";
import Detail from "../components/Detail";
export default {
  data(){
    return{
      alarm:{
        inth:0,
        intm:0,
      }
    };
  },
  components:{
    Setmenu,
    Detail
  }
};
</script>

<style scoped>
p{
  font-size:48px;
}

select{
  font-size: 32px;
  text-align: center; 
}

.time-box{
  margin-top:146px;
}

.timetitle{
  text-align: center; 
}

.set-box {
  align-items: center;
  display:flex;
  padding:50px;
  width:250px;
  margin: 0 auto;
  justify-content: space-between;
}

.time{
  width:65px;
  height:65px;
}

@media screen and (max-width:768px){
.timetitle{
  font-size:32px;
  margin: auto 10%;
}
select{
  font-size: 24px;
}
}
</style>