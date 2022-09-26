<template>
  <div>
    <SlideBar></SlideBar>
    <div class="main-home">
      <h1>Image Application page</h1>

      <form style="padding:15px">

        <div>
          <label>app_id :</label>
          <p>
            <input id="app_id" type="text" style="color:black" />
          </p>
        </div>


        <div>
          <label>path :</label>
          <p>
            <input id="path" type="text" style="color:black" />
          </p>
        </div>

        <div>
          <label>num_img :</label>
          <p>
            <input id="num_img" type="text" style="color:black" />
          </p>
        </div>

        <div>
          <label>img_selected :</label>
          <p>
            <input id="img_selected" type="text" style="color:black" />
          </p>
        </div>


        <input @click="add_job()" type="button" value="Add new Job" style="color:black" />


        <div v-for="job in jobs" v-bind:key="job.job_id">
          <h2>job_id : {{ job.job_id }}</h2>
          <p>user_id : {{ job.user_id }}</p>
          <p>path : {{ job.path }}</p>
          <p>num_img : {{ job.num_img }}</p>
          <p>persent : {{ job.persent }}</p>
          <p>status : {{ job.job_status }}</p>
          <hr>
        </div>
      </form>




    </div>
  </div>
</template>


<script>

import SlideBar from '@/components/SlideBar';
import { useCookies } from "vue3-cookies";
import router from '@/router';
import axios from 'axios';
export default {
  name: 'Img_appView',
  setup() {
    const { cookies } = useCookies();
    return { cookies };
  },

  data() {
    return {
      jobs: []
    }
  },
  methods: {
    add_job() {
      axios.post('http://127.0.0.1:8000/api/make_docker_file',
        {
          'jwt': this.cookies.get('jwt'),
          'job_id': Math.random().toString(36).slice(2),
          'app_id': document.getElementById('app_id').value,
          'path': document.getElementById('path').value,
          'num_img': document.getElementById('num_img').value,
          'img_selected': document.getElementById('img_selected').value
        }
      ).then(async (respond) => {
        alert(respond.data.status)
        //console.log(respond)
      })
    }
  },
  created() {
    if (this.cookies.get('jwt') == null) {
      alert("You are not login yet , please login fisrt")
      router.push('login')
    } else {
      console.log("ok")
    }

  },
  components: {
    SlideBar
  },

}
</script>
