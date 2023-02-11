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
					asd
				</div>
			</header>

			<main>
				<div class="page-header">
					<div>
						<h1>Feed page</h1>
						<small>ข่าวสาร</small>
					</div>

					<div class="header-actions">
						<button>
							<span class="las la-file-export"></span>
							Coming Soon
						</button>
					</div>
				</div>

				<div class="cards">
					<div class="card-single">
						<div class="card-flex">
							<div class="card-info">
								<div class="card-head">
									<span style="color: #000;">Coming Soon</span>
									<small style="color: #000;">Coming Soon</small>
								</div>
								<h2 style="color: #000;">Coming Soon</h2>
								<small style="color: #000;">Coming Soon</small>
							</div>
						</div>
					</div>
					<div class="card-single">
						<div class="card-flex">
							<div class="card-info">
								<div class="card-head">
									<span style="color: #000;">Coming Soon</span>
									<small style="color: #000;">Coming Soon</small>
								</div>
								<h2 style="color: #000;">Coming Soon</h2>
								<small style="color: #000;">Coming Soon</small>
							</div>
						</div>
					</div>
					<div class="card-single">
						<div class="card-flex">
							<div class="card-info">
								<div class="card-head">
									<span style="color: #000;">Coming Soon</span>
									<small style="color: #000;">Coming Soon</small>
								</div>
								<h2 style="color: #000;">Coming Soon</h2>
								<small style="color: #000;">Coming Soon</small>
							</div>
						</div>
					</div>
					<div class="card-single">
						<div class="card-flex">
							<div class="card-info">
								<div class="card-head">
									<span style="color: #000;">Coming Soon</span>
									<small style="color: #000;">Coming Soon</small>
								</div>
								<h2 style="color: #000;">Coming Soon</h2>
								<small style="color: #000;">Coming Soon</small>
							</div>
						</div>
					</div>
					<div class="card-single">
						<div class="card-flex">
							<div class="card-info">
								<div class="card-head">
									<span style="color: #000;">Coming Soon</span>
									<small style="color: #000;">Coming Soon</small>
								</div>
								<h2 style="color: #000;">Coming Soon</h2>
								<small style="color: #000;">Coming Soon</small>
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

