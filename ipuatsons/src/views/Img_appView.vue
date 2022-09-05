<template>
  <div class="main-home">
    <h1>Image Application page</h1>

    <form @submit="add_job(), do_job()" style="padding:15px">
      <div>
        <label>job_id :</label>
        <p>
          <input type="text" @change="(e) => setNewJob({ ...newJob, job_id: e.target.value })" />
        </p>
      </div>

      <div>
        <label>user_id :</label>
        <p>
          <input type="text" @change="(e) => setNewJob({ ...newJob, user_id: e.target.value })" />
        </p>
      </div>

      <div>
        <label>app_id :</label>
        <p>
          <input type="text" @change="(e) => setNewJob({ ...newJob, app_id: e.target.value })" />
        </p>
      </div>


      <div>
        <label>path :</label>
        <p>
          <input type="text" @change="(e) => setNewJob({ ...newJob, path: e.target.value })" />
        </p>
      </div>

      <div>
        <label>num_img :</label>
        <p>
          <input type="text" @change="(e) => setNewJob({ ...newJob, num_img: e.target.value })" />
        </p>
      </div>

      <div>
        <label>img_selected :</label>
        <p>
          <input type="text" @change="(e) => setNewJob({ ...newJob, img_selected: e.target.value })" />
        </p>
      </div>


      <div>
        <label>persent :</label>
        <p>
          <input type="text" @change="(e) => setNewJob({ ...newJob, persent: e.target.value })" />
        </p>
      </div>


      <div>
        <label>job_status :</label>
        <p>
          <input type="text" @change="(e) => setNewJob({ ...newJob, job_status: e.target.value })" />
        </p>
      </div>




      <input id="submit" type="submit" value="Add Job" />
    </form>

    <div v-for="job in jobs" v-bind:key="job.job_id">
      <h2>job_id : {{ job.job_id }}</h2>
      <p>user_id : {{ job.user_id }}</p>
      <p>path : {{ job.path }}</p>
      <p>num_img : {{ job.num_img }}</p>
      <p>persent : {{ job.persent }}</p>
      <p>status : {{ job.job_status }}</p>
      <button @click="do_job(job.job_id)">{{ job.job_id }}</button>
      <hr>

    </div>



  </div>
</template>


<script>
import { useState } from '../composables/state';

export default {
  name: 'Img_appView',
  mounted() {

  },


  data() {
    const [newJob, setNewJob] = useState({
      job_id: "",
      user_id: "",
      path: "",
      num_img: 0,
      persent: 0,
      job_status: 0,
      create_time: null
    });
    return {
      jobs: [],
      newJob,
      setNewJob,
      job_id: ""
    }
  },
  methods: {
    add_job() {
      console.log(this.newJob)
      fetch('http://127.0.0.1:8000/api/', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json;charset=utf-8',
        },
        body: JSON.stringify(this.newJob)
      })
        .then(function (response) {
          if (response.status != 201) {
            this.fetchError = response.status;
          } else {
            response.json().then(function (data) {
              this.fetchResponse = data;
            }.bind(this));
          }
        }.bind(this));
    },

    do_job(job_id) {
      console.log(job_id)
      fetch('http://127.0.0.1:8000/api/do_job')
        .then(async response => await response.json())
        .then(async response => {
          this.jobs = response
          console.log(response)
        })
    },


  },
  created() {
    fetch('http://127.0.0.1:8000/api/')
      .then(async response => await response.json())
      .then(async response => {
        this.jobs = response
      })
  },
}
</script>
