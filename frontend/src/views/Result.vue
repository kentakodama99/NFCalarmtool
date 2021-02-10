<template>
  <div id="result">
  <div v-bind:class="weatherImg" class="background_img">
    <div class="current_weather">
      <p ><span class="bold">{{this.weather.city}}</span></p>
      <p>天気：{{this.weather.weather}}</p>
      <p>気温：{{this.weather.temperature}}℃</p>
    </div>
    <div class="after">
      <p class="morning-text">おはようございます</p>
      <div class="after-time">
        <p>本日の睡眠時間</p>
        <p>{{this.cursleeptime}}</p>
        </div>
        <button @click="transition()" class="toppage_button"><p>終了する</p></button>
      </div>
  </div>
  </div>
</template>

<script>
import axios from 'axios'
export default{
  data(){
    return{
      weather:{
        city:"",
        weather:"",
        temperature:"0"
      },
      cursleeptime:"",
      OWdata:"",
      weatherImg:""
    };
  },
  created(){
    this.getweather()
  },
  methods:{
    async getweather(){
      //OpenWeatherAPI
      this.weather.city="funabashi"
      await axios.get(`https://api.openweathermap.org/data/2.5/weather?q=${this.weather.city},jp&units=metric&appid=24dc8e7a9194dd0696722fc728772ae2`)
      .then(response => {this.OWdata=response;})
      .catch(error => {console.log(error);});
      console.log(this.OWdata)
      this.weather.weather=this.OWdata.data.weather[0].main
      this.weather.temperature=this.OWdata.data.main.temp
      //change_backgroundimage
      if(this.weather.weather=="Sun"){
        this.weatherImg="Sun";
      }else if(this.weather.weather=="Clouds"){
        this.weatherImg="Clouds";
      }else if(this.weather.weather=="Rain"){
        this.weatherImg="Rain";
      }else if(this.weather.weather=="Snow"){
        this.weatherImg="Snow";
      }else{
        this.weatherImg="Etc";
      }
      console.log("Change:"+this.weather.weather)
      //graph ID5の睡眠時間(最新の時間)を参照
      //table api
      const path="/api/graphtable/"
      await axios.get(path)
      .then(response => {this.cursleeptime=JSON.parse(response.data)})
      .catch(error => {console.log(error);});
      this.cursleeptime=this.cursleeptime[0].sleeptime
    },
    transition() {
      this.$router.push({ name: "Home" });
    }
  }
};
</script>

<style>

#result{
  text-align:center;
}
.Sun{
    background-image: url(../assets/Sun.jpg);
}

.Rain{
  background-image: url(../assets/Rain.jpg);
}

.Clouds{
    background-image: url(../assets/Clouds.jpg);
}

.Snow{
    background-image: url(../assets/Snow.jpg);
}

.Etc{
    background-image: url(../assets/Etc.jpg);
}

.background_img{
  width: 100%;
  min-height:calc(100vh - 130px ); 
  background-size: cover;
  background-position: center;
  padding-top:30px;
  display:block;
}

.current_weather{
  border-radius:20px;
  width:25%;
  margin: 0 auto;
  padding: 10px;
  background:white;
  opacity:0.8;
  margin-bottom:50px;
}

.current_weather p{
  font-size:24px;
  color:black;
}

.bold{
  font-weight:bold;
}

.after{
  color:black;
  font-weight:bold;
  text-shadow:2px 2px gray;
}

.morning-text{
  text-align:center;
  font-size:64px;
  color:white;
  font-weight:bold;
}

.after-time{
  margin:30px;
}

.toppage_button {
  background: #fff;
  width:200px;
  border-radius:50px;
  cursor: pointer;
}

.toppage_button p{
  font-size:24px;
}

@media screen and (max-width:768px){
  .background_img{
    height:calc(100vh - 140px);
  }

  .current_weather{
  width:80%;
  /* margin-bottom:20px; */
}

.current_weather p{
  font-size:24px;
}

.morning-text{
  font-size:32px;
}

.toppage_button {
  background: #fff;
  margin:70px;
  width:200px;
  border-radius:50px;
  cursor: pointer;
}
}
</style>