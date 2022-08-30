<template>
  <div>
    <h1>Image Application page</h1>

    <div v-for="job in jobs" v-bind:key="job.job_id">
      <h2>job_id : {{ job.job_id }}</h2>
      <P>user_id : {{ job.user_id }}</P>
      <p>path : {{job.path}}</p>
      <p>num_img : {{job.num_img}}</p>
      <p>persent : {{job.persent}}</p>
      <p>status : {{job.job_status}}</p>
      <hr>
    </div>

    <form @submit="handleSubmit()">
      <div>
        <label>job_id : </label>
        <input type="text"
        @change="(e) => setNewJob({ ...newJob, job_id: e.target.value })"
        />
      </div>
      
      <div>
        <label>user_id : </label>            
        <input type="text"
        @change="(e) => setNewJob({ ...newJob, user_id: e.target.value })"
        />
      </div>


      <div>
        <label>path : </label>            
        <input type="text"
        @change="(e) => setNewJob({ ...newJob, path: e.target.value })"
        />
      </div>

      <div>
        <label>num_img : </label>            
        <input type="text"
        @change="(e) => setNewJob({ ...newJob, num_img: e.target.value })"
        />
      </div>


      <div>
        <label>persent : </label>            
        <input type="text"
        @change="(e) => setNewJob({ ...newJob, persent: e.target.value })"
        />
      </div>


      <div>
        <label>job_status : </label>            
        <input type="text"
        @change="(e) => setNewJob({ ...newJob, job_status: e.target.value })"
        />
      </div>



        <input id="submit" type="submit" value="Add Job"/>
      </form>

      {{newJob.job_id}}
      {{newJob.description}}
      {{newJob}}
      {{setNewJob}}
  </div>
</template>


<script>
import { useState } from '../composables/state';

export default {
  name: 'Img_appView',
  data() {
    const [newJob, setNewJob] = useState({
      job_id : "",
      user_id: "",
      path: "",
      num_img: 0,
      persent: 0,
      job_status: 0
    });
    return {
      jobs : [],
      newJob,
      setNewJob,
    }
  },
  methods: {
    handleSubmit() {
      fetch('http://127.0.0.1:8000/api/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
        },
        body: JSON.stringify( this.newJob)
      })
      .then( function( response ){
        if( response.status != 201 ){
          this.fetchError = response.status;
        }else{
          response.json().then( function( data ){
            this.fetchResponse = data;
        }.bind(this));
        }
      }.bind(this));
    },
},
  created(){
    fetch('http://127.0.0.1:8000/api/')     
      .then(async response => await response.json())
      .then(async response => {    
        this.jobs = response
      })
  },
}
</script>
