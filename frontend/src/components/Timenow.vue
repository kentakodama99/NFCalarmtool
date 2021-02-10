<template>
  <div id="timenow">
    <p>{{now}}</p>
  </div>
</template>

<script>
export default {
  data(){
    return{
      now:""
    };
  },

  created(){
    setInterval(this.updateTime, 1000); 
    }, 
    methods:{
      updateTime(){
      var date = new Date();
      var house= date.getHours()
      var minutes=date.getMinutes()
      minutes=('0' + minutes).slice(-2);
      this.now = (house+ ':' +minutes);
      }
    }
  }
</script>