<template>
  <div>
    <h1>Image Application page</h1>

    <div v-for="job in jobs" v-bind:key="job.job_id">
      <h2>{{ job.job_id }}</h2>
      {{ job.description }}
    </div>

    <form @submit="handleSubmit()">
      <div>
        <label>Job_id : </label>
        <input type="text"
        @change="(e) => setNewJob({ ...newJob, job_id: e.target.value })"
        />
      </div>
      
      <div>
        <label>Description : </label>            
        <textarea rows="4"
        @change="(e) => setNewJob({ ...newJob, description: e.target.value })"
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
      description : "",
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
