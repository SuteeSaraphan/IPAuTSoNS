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
                    Image processing application
                </div>
            </header>


            <main>
                <!-- loading -->
                <div v-if="this.isLoading" @mousewheel="addPresent">
                    <div style="
                        padding-left: 15px;
                        padding-right: 20px;
                        padding-top: 15px;
                        display: flex;
                        height: 810px;
                        flex-direction: row;
                        justify-content:center;
                        align-items: center;
                        align-content:center;
                        background-color: #4B5162;">

                    
                            



                            <radial-progress-bar 
                                :diameter="500" 
                                :completed-steps="completedSteps"
                                :total-steps="totalSteps"
                                :startColor="this.barColor"
                                :stopColor="this.barColor"
                                
                                style="
                                align-items: center;
                                justify-content:center;
                                
                                "
                                >
                                <h2>On Process</h2>
                                <h1 >Completed : {{ completedSteps }} %</h1>
                                <button style="
                                border: 0;
                                padding: 15px;
                                background-color: red;
                                font-weight: bold;">cancel</button>
                            </radial-progress-bar>

                            


                    </div>
                </div>
                <!-- loading -->



                <!-- image show -->
                <div v-if="!(this.isLoading)">
                    <div style="
                    padding-left: 15px;
                    padding-right: 20px;
                    padding-top: 15px;
                    display: flex;
                    flex-direction: column;
                    background-color: #4B5162;">
                        <h1>Export Done !!!</h1>

                        <div style="
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    align-items: center;
                    padding:20px;">
                            <img :src="this.imgShowSrc" width="900">

                        </div>

                        <div style="
                        display: flex;
                        flex-direction: row;
                        justify-content: flex-end;
                        padding:20px;">
                            <button type="button"  style="
                                font-weight: bold;
                                background-color: #5294e2;
                                border: 0;
                                padding: 10px;">
                                Download
                            </button>
                        </div>







                    </div>



                </div>
                <!-- image show -->
            </main>

        </div>
    </div>
</template>

<script>
import SlideBar from '@/components/SlideBar'
import { useCookies } from "vue3-cookies";
import router from '@/router';
import RadialProgressBar from 'vue-radial-progress';





export default {



    name: "DemoExportView",
    setup() {
        const { cookies } = useCookies();
        return { cookies };



    },
    data() {
        return {
            completedSteps: 0,
            totalSteps: 100,
            barColor :"#5294e2",

            filterNoneCpu: ['Black and White', 'ASCII'],
            filterOnCpu: ['Mosaic', 'PixelArt'],
            isLoading: true,
            imgShowSrc: require('@/img/for_demo/DSC01577-pixie.jpg')

        }
    },
    methods: {
        addPresent(){
            if( this.completedSteps < 100){
                this.completedSteps += 2
            }else{
                this.isLoading=false
            }
            
        }
        
        








    }
    ,
    components: {
        SlideBar,
        RadialProgressBar
    },
    created() {

        if (this.cookies.get('jwt') == null) {
            alert("You are not login yet , please login fisrt")
            router.push('/login')
        }
        
        

        




    }
};
</script>

