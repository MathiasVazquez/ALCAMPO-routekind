<template>
	<!-- DRAWER -->
	<q-drawer v-if="!showDrawer || onlyMini"
		bordered
		show-if-above 
		:width="50"
		:breakpoint="1"
		class="bg-white text-black"
	>
		<div class="absolute-top-left full-height">
			<LeftDrawerRouter>
				<template v-slot:top>
					<q-btn flat dense icon="menu" class="options-btn" @click="toggleLeftDrawer" />
				</template>
			</LeftDrawerRouter>
		</div>
	</q-drawer>
	<q-drawer v-else
		show-if-above
		v-model="showDrawer"
		:width="340"
		:breakpoint="700"
		class="bg-white text-black"
	>
		<div class="absolute-top-left full-height">
			<LeftDrawerRouter>
				<template v-slot:top>
					<q-btn flat dense icon="menu" class="options-btn" @click="toggleLeftDrawer" />
				</template>
			</LeftDrawerRouter>
		</div>
		<!-- Drawer content by route -->
		<RouteDrawerContent v-if="pageNameIs('Index')" />
		<SecurityDrawerContent v-if="pageNameIs('Security')"/>
		<MobileDrawerContent v-if="pageNameIs('Mobiles')"/>
		<PlanningDrawerContent v-if="pageNameIs('Planning')"/>
	</q-drawer>
</template>

<script>
import { ref, toRefs } from 'vue'
import LeftDrawerRouter from './LeftDrawerRouter'
import RouteDrawerContent from 'src/drawers/RouteDrawerContent'
import SecurityDrawerContent from 'src/drawers/SecurityDrawerContent'
import MobileDrawerContent from 'src/drawers/MobileDrawerContent'
import PlanningDrawerContent from 'src/drawers/PlanningDrawerContent'
import { useRoute } from 'vue-router'
import { usePolygons } from 'src/context'

export default {
	name: 'MainLayout',
	components: {LeftDrawerRouter, RouteDrawerContent, SecurityDrawerContent, MobileDrawerContent, PlanningDrawerContent},
	props: ['onlyMini'],
	setup (props) {
		const { editingPolygon } = usePolygons()
		const { onlyMini } = toRefs(props)
    const route = useRoute()

		const showDrawer = ref(true)
		const toggleLeftDrawer = () => (showDrawer.value = !showDrawer.value)
    const pageNameIs = name => route.name === name

		return {
			onlyMini,
			showDrawer,
			editingPolygon,
			toggleLeftDrawer,
      pageNameIs,
		}
	}
}
</script>

<style>
.drawer-header {
	height:121px;
	max-height:121px;
	min-height:121px;
}
.options-btn {
	width:50px;
	height:50px;
	border-radius:0;
}
</style>