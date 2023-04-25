<template>

    <div>
        <SlideBar></SlideBar>



        <div class="main-content">

            <header>
                <div class="menu-toggle">
                    <label for="sidebar-toggle">
                        <span style="color:#000 ;" class="las la-bars"></span>
                    </label>
                </div>
                <span class="bars"></span>

                <div style="color:#000 ;">
                    Job history
                </div>
            </header>


            <main>
                <div class="loading" v-if="this.isLoading">Loading&#8230;</div>
                <h1>Job history</h1>

                
                <!-- filter history here  -->
                <div class="sort-btn" style="padding:5px;">
                    <button type="button" @click="goSort('1')" >sort by newest </button>
                    <button type="button" @click="goSort('2')" >sort by oldest</button>
                    <input type="date" id="search_by_date" @change="goSearch">
                </div>
                
                


                <!-- folder image list show here -->
                <div style="background:#e7e5e6">
                    <table style="width: 100%; padding:1%" >
                    
                        
                        <tr style="margin-top: 5px;margin-bottom: 5px; background-color: #ccc; text-align: center;">
                            <!-- <div style="display : flex; 
                             flex-direction : row;
                             justify-content: space-between;
                             align-items : center;

                             background:#ccc;"> -->
                                <td style="color:black;padding:10px; ">
                                    Job_id
                                </td>
                                <td style="color:black;padding:10px; justify-self: center;">
                                    Folder on process
                                </td>
                                <td style="color:black;padding:10px; justify-self: center;">
                                    status
                                </td>
                                <td style="color:black;padding:10px;">
                                    create_time
                                </td>

                        </tr>
                        <tr v-if="jobs < 1" 
                        style="text-align: center;
                            align-items: center;
                            color: #000;
                            background:#ccc;">
                            <td colspan="5">!!! You do not have any record !!!</td>
                        </tr>

                        <tr v-for="job in jobs" v-bind:key="job.id" style="margin-top: 5px;margin-bottom: 5px;background:#ccc; text-align: center; ">

                            <!-- <div style="display : flex; 
                             flex-direction : row;
                             justify-content: space-between;
                             align-items : center;
                             padding-right: 15px;
                             background:#ccc;"> -->


                                <td style="color:black;padding:10px;">
                                    {{ job.job_id }}
                                </td>
                                <td style="color:black;padding:10px; justify-self: center;">
                                    {{ pathCut(job.path) }} 
                                </td>
                                <td style="color:black;padding:10px; justify-self: center;">
                                    {{ statusShow(job.job_status) }} 
                                </td>
                                <td style="color:black;padding:10px;">
                                    {{ job.create_time }} 
                                </td>
                               

                            
                        </tr>

                    
                </table>
                </div>


            </main>
        </div>
    </div>
</template>
<style>
    .sort-btn button{
        color: black;
        padding: 0.5%;
        margin-right: 0.5%;
    }
    .sort-btn input{
        color: black;
        padding: 0.5%;
        margin-right: 0.5%;
    }
</style>

<script>
import SlideBar from '@/components/SlideBar'
//import router from '@/router';
import axios from 'axios';
//import VueSlideBar from 'vue-slide-bar';
const URL_JOB_HISTORY = "job_history"




export default {
    name: "JobHistoryView",
    setup() {



    },
    data() {
        return {
            isLoading: true,
            jobs : null

        }
    },
    methods: {

        goSort(type){
            if (type == "1"){
                let path = "/job_history/" + "newest"
                window.location.href = path;
            }else if(type == "2"){
                let path = "/job_history/" + "oldest"
                window.location.href = path;
            }

        },

        goSearch(){
            let path = "/job_history/" + document.getElementById("search_by_date").value
            window.location.href = path;
        },

        pathCut(pathName){
            let tempName = pathName.split("/");
            return tempName[tempName.length - 1]
        },

        statusShow(jobStatus){
            if(jobStatus == 0){
                return "On process"
            }else if(jobStatus == 1){
                return "Success"
            }else if(jobStatus == 2){
                return "Job Error"
            }else{
                return "Unknow"
            }
            
        }
        





    }
    ,
    components: {
        SlideBar,
        //VueSlideBar
    },
    async created() {
            axios.defaults.headers.get['jwt'] = this.$store.state.jwt
            await axios.get(URL_JOB_HISTORY+"/"+this.$route.params.type)
                .then(res => {
                    this.jobs = res.data;
                    this.isLoading = false; 
                    //console.log(this.jobs[0])
                })
                .catch(err => {
                    this.isLoading = false
                    console.log(err)
                })
        

    }
};
</script>
