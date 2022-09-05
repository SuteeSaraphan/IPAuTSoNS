<template>
  <div class="main-home">

    <h1>
      Model and application lastest update
    </h1>

    <!-- Start newest news upadate -->
    <div class="lastest-update">
      <div>
        <router-link to="/"><img src="../img/664e3012-0a0c-43f1-a6cf-9f7003a77ca2.jpg" alt=""></router-link>
        <div class="lastest-update-info">Yhaa tub sein</div>
        <div class="lastest-update-info">Last update : 04/03/2022</div>
      </div>

    </div>
    <!-- End newest news upadate -->
    
    <h2>Feed</h2>
    <!-- Start Feed  -->
    <div class="main-posts">

      <div class="post-box">
        <div class="post-box-head">
          <a href="index.html"><router-link to="/" ><img src="../img/profile.jpg" alt=""></router-link></a>
          <div class="post-info">
            <router-link to="/" >
              <h3>PEACH</h3>
            </router-link>
            <div>2 Houses ago</div>
            <div>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras tellus orci, luctus id ultricies non,
              malesuada vitae mi. Aliquam in semper quam. Mauris porta lorem quis sem dapibus, non volutpat tortor
              pulvinar. Nam molestie non arcu nec laoreet. Aliquam congue tincidunt erat, non sodales est iaculis ac.
              Suspendisse potenti. Morbi non mattis felis, nec lobortis enim. Pellentesque lectus nibh, maximus ac
              gravida eu, venenatis ac lorem. Proin tempor felis felis, quis hendrerit velit pulvinar id. Nam venenatis
              et ligula sit amet dictum. Vestibulum ullamcorper ante eget nunc facilisis, id vehicula velit viverra.
              Morbi congue, tellus ornare dapibus hendrerit, velit diam molestie est, non mattis diam leo sed nibh. Sed
              dictum lacus vel elit elementum hendrerit. Cras finibus orci vel blandit tempor. Suspendisse commodo
              suscipit posuere.
            </div>
          </div>
        </div>
      </div>



    </div>
    <!--  End Feed  -->

  </div>
</template>

<script>
// @ is an alias to /src
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  
}
</script>
