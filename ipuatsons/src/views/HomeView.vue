<template>
  <div>
    <SlideBar></SlideBar>

    <div class="main-content">
		<header style="color: #000;">
			<div class="menu-toggle">
				<label for="sidebar-toggle">
					<span class="las la-bars"></span>
				</label>
			</div>
			<span class="bars"></span>

			<div style="color: #000;">
				asd
			</div>
		</header>

		<main>
			<div class="page-header">
				<div>
					<h1>Ana</h1>
					<small>asdasdsafasf</small>
				</div>

				<div class="header-actions">
					<button>
						<span class="las la-file-export"></span>
						ปุ่มอะไรสักอย่าง
					</button>
				</div>
			</div>

			<div class="cards" >
				<div class="card-single"> 
					<div class="card-flex">
						<div class="card-info">
							<div class="card-head">
								<span style="color: #000;">อิอิย์เร็ว</span>
								<small style="color: #000;">asdgggg</small>
							</div>
							<h2 style="color: #000;">1123123</h2>
							<small style="color: #000;">2%</small>
						</div>
					</div>
				</div>

				<div class="card-single"> 
					<div class="card-flex">
						<div class="card-info">
							<div class="card-head">
								<span style="color: #000;">ไอ้โอมมันเลว</span>
								<small style="color: #000;">asEEEEEdgggg</small>
							</div>
							<h2 style="color: #000;">1123123</h2>
							<small style="color: #000;">2%</small>
						</div>
					</div>
				</div>

				<div class="card-single"> 
					<div class="card-flex">
						<div class="card-info">
							<div class="card-head">
								<span style="color: #000;">EIE</span>
								<small style="color: #000;">asdgggg</small>
							</div>
							<h2 style="color: #000;">1123123</h2>
							<small style="color: #000;">2%</small>
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
export default {
  name: 'HomeView',
  setup() {
    const { cookies } = useCookies();
    return { cookies };
  },
  components: {
    SlideBar
  },
  created() {
    if (this.cookies.get('jwt') == null) {
      alert("You are not login yet , please login fisrt")
      router.push('login')
    }
  }
}
</script>

