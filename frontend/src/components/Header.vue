<template>
<header id="top-header">
        <div class="flex">
          <p class="header-logo">目覚まし時計</p>
          <p class="header-time"><Timenow/></p>
        </div>
      </header>
</template>

<script>
import Timenow from "./Timenow"
export default {
  components:{
    Timenow
  }
}
</script>

<style scoped>
.flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  
}

#top-header {
  height: 100px;
  line-height: 100px;
  background: #c9fffc;
  width:100%;
}

.header-logo {
  font-size: 48px;
  margin-left: 35px;
  line-height: 100px;
}

.header-time{
  font-size: 48px;
  margin-right: 35px;
  line-height: 100px;
}

@media screen and (max-width:768px){
  .flex {
  display: block;
  }
#top-header {
  height: 110px;
  line-height: 110px;
  background: #c9fffc;
}

  .header-logo {
  margin-left: 0px;
  text-align:center;
  line-height: 70px;
}

.header-time{
  font-size: 32px;
  margin-right: 0px;
  text-align:center;
  line-height: 30px;
}
}
</style>