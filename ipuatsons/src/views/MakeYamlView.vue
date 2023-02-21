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
					Making YAML file test
				</div>
			</header>

			<main>
				<div class="page-header">
					<div>
						<h1>Making YAML file test</h1>
						<small>ลองสร้างไฟล์ YAML</small>
					</div>

					<div class="header-actions">
						<button>
							<span class="las la-file-export"></span>
							click here to create ymal file
						</button>
					</div>
				</div>

				<div class="cards">
					<div class="card-single" @click="createyamlfile">
						<div class="card-flex">
							<div class="card-info">
								<div class="card-head">
									<span style="color: #000;">click here to create yaml file</span>
									<small style="color: #000;">click here to create yaml file</small>
								</div>
								<h2 style="color: #000;">click here to create yaml file</h2>
								<small style="color: #000;">click here to create yaml file</small>
							</div>
						</div>
					</div>



				</div>
			</main>
		</div>
		<label for="sidebar-toggle" class="body-label"></label>
	</div>
</template>

<script>
// @ is an alias to /src
import SlideBar from '@/components/SlideBar'
import { useCookies } from "vue3-cookies";
import router from '@/router';
import axios from 'axios';
const URL_MAKE_YAML_FILE = 'http://127.0.0.1:8000/api/make_docker_file';

export default {
	name: 'MakeYamlView',
	setup() {
		const { cookies } = useCookies();
		return { cookies };
	},
	components: {
		SlideBar
	},

    methods: {
        createyamlfile(){
            console.log('make file')
            let data_yaml = new FormData();
            data_yaml.append('jwt',this.cookies.get('jwt'))
            data_yaml.append('job_id',Math.random().toString(36).slice(2))
            let config = {
                    header: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            axios.post(URL_MAKE_YAML_FILE,data_yaml,config)
            .then(async res=>{
                console.log(res)
            })
        },
    },
	created() {
		if (this.cookies.get('jwt') == null) {
			alert("You are not login yet , please login fisrt")
			router.push('login')
		}
	}
}
</script>

