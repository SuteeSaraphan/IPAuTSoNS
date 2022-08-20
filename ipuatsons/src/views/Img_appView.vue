<template>
  <div>
    <h1>Image Application page</h1>

    <div v-for="job in jobs" v-bind:key="job.job_id">
    <h2>{{ job.job_id }}</h2>
    {{ job.description }}
  </div>

  <form>

  <div>

    <label>Job_id : </label>

    <input

      type="text"

    />

  </div>

  <div>

    <label>Description : </label>            

    <textarea rows="4"/>

  </div>

  <input id="submit" type="submit" value="Add Job"/>

</form>

  </div>
</template>

<script>

export default {
  name: 'Img_appView',
  data() {
    return {
      jobs : [],
    }
  },
  methods: {
    
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
