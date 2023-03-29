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
				<div class="loading" v-if="this.isLoading">Loading&#8230;</div>
				<div class="page-header">
					<div>
						<h1>Feed page</h1>
						<small>ข่าวสาร</small>
					</div>

					
				</div>

				<!-- show all products here -->
				<div class="cards">
					<!-- show each product info here -->
					<div class="card-single" v-for="product in this.productList" v-bind:key="product.product_id"
						@click="goProduct(product.product_id)">
						<div class="card-flex">
							<div class="card-info">
								<div class="card-head">
									<span style="color: #000;">Seller - </span>
									<small style="color: #000;">{{ product.seller }}</small>
								</div>
								<div class="card-img">
									<img :src="`data:image/jpeg;base64,${product.product_img}`"
										alt="{{ product.product_id }}">
								</div>
								<h2 style="color: #000;">{{ product.product_name }}</h2>
								<small style="color: #000;">{{ product.product_type }}</small>
							</div>
						</div>
					</div>
					<!-- end of show each product info here -->
				</div>


			</main>
		</div>
		<label for="sidebar-toggle" class="body-label"></label>
	</div>
</template>

<script>
// @ is an alias to /src
import SlideBar from '@/components/SlideBar'
// import router from '@/router';
import axios from 'axios';
export default {
	name: 'HomeView',
	setup() {
	
	},
	data() {
        return {
            isLoading: true,
            productList: []


        }
    },
	methods: {
        goProduct(product_id) {
            //console.log("enter folder :"+folder_id)
            let path = "/product/" + product_id
            window.location.href = path
        },

    },
	components: {
		SlideBar
	},
	async created() {
		console.log(this.$route.params.keyword)
		axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
		await axios.get('product/home/all')
			.then(res => {
				console.log(res.data)
				this.productList = res.data
				this.isLoading = false;
			})
			.catch(err => {
				this.isLoading = false;
				console.log(err)
			})


	}
}
</script>

