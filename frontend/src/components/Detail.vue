<template>
  <div id="detail">
    <div class="detailtitle bold">Detail</div>
    <div class="detailbox">
      <p class="bold">graph</p>
      <img :src="imgSrc" class="fig_graph" alt="">
    </div>
    <div class="graphtable detailbox">
      <p class="bold">data</p>
    <table>
      <tr>
        <th><span class="whitecolor">ID</span></th>
        <th><span class="whitecolor">日付</span></th>
        <th><span class="whitecolor">就寝時間</span></th>
        <th><span class="whitecolor">起床時間</span></th>
        <th><span class="whitecolor">睡眠時間</span></th>
      </tr>
      <tr v-for="(item,index) in table" :key="index">
        <td><p>{{index+1}}</p></td>
        <td><p>{{item.date}}</p></td>
        <td><p>{{item.startdate}}</p></td>
        <td><p>{{item.stopdate}}</p></td>
        <td class="standoutcolor"><p class="bold">{{item.sleeptime}}</p></td>
      </tr>
    </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data(){
    return{
      table:[
      ],
      imgSrc:"",
      responsedata:""
    };
  },
  created(){
    this.getimg_file()
  }, 
  methods:{
    async getimg_file(){
      // img api
      var date = new Date();
      var dategetTime=String(date.getTime());
      const filename="graph.png";
      this.imgSrc=("/alaimg/"+filename+"/"+dategetTime);
      await axios.get(this.imgSrc)
      .then(response => {console.log("getImage:("+response.config.url+")")})
      .catch(error => {console.log(error);});
      //table api
      const path="/api/graphtable/"
      await axios.get(path)
      .then(response => {this.responsedata=JSON.parse(response.data)})
      .catch(error => {console.log(error);});
      //responsedata→table
      this.responsedata.forEach(element=>{
      this.table.push({
        date:element.date,
        startdate: element.startdate,
        stopdate: element.stopdate,
        sleeptime: element.sleeptime
        })}
      );
    }
  }
};
</script>

<style>
img {
  width: 100%;
  height: 100%;
  display: block;
}

.bold{
  font-weight:bold;
}

#detail{
  background: #c9fffc;
  margin-top:200px;
  width:100%;
  padding:0px;
}

.detailtitle{
  line-height: 150px;
  text-align:center;
  font-size:48px;
}

.detailbox{
padding:20px 0;
}

.detailbox p{
  font-size:16px;
  text-align:center;
}


.fig_graph{
  margin: 0px auto;
  width:50%;
}

table {
  margin: 0 auto;
}


th {
  padding:10px;
  background: #52c2d0;
  border:solid 1px;
}
td {
  padding:10px;
  background: #ffffff;
  border:solid 1px;
}

.whitecolor{
  color:#fff;
}

.standoutcolor{
  background-color:#e5d7f1
}

@media screen and (max-width:768px){
.table,.fig_graph{
  width:100%;
}
}

</style>