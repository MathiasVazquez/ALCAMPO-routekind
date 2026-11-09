<template>
	<q-layout view="lHh Lpr lFf">
		<EditingPolygonHeader v-if="editingPolygon" />
    <!--<LeftDrawer :miniOnly="true" />-->

    <!-- LEFT OPTIONS -->

    <div class="absolute-top-left overflow-hidden shadow-5 full-height" style="z-index:999">
			<LeftDrawerRouter>
				<template v-slot:top>
					<q-btn flat dense icon="menu" color="grey-8" class="options-btn" @click="toggleLeftDrawer" />
				</template>
			</LeftDrawerRouter>
		</div>

		<!-- BODY -->

		<q-page-container>
			<router-view />
		</q-page-container>

    <AppFrameModal />
    <!-- <SettingsMenuModal /> -->
	</q-layout>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { weekDays } from 'src/utils/statics'
import { usePlanning, usePolygons, useSession } from 'src/context'
import { useRouter } from 'vue-router'
import PolygonList from 'src/components/polygon/PolygonList'
import EditingPolygonHeader from 'src/components/polygon/EditingPolygonHeader'
import LeftDrawer from 'src/pages/includes/LeftDrawer'
import PlanningSelector from 'src/components/planning/PlanningSelector'
import LeftDrawerRouter from 'src/pages/includes/LeftDrawerRouter'
import AppFrameModal from 'src/components/mobileApp/AppFrameModal'
import SettingsMenuModal from 'src/components/includes/SettingsMenuModal'

export default {
	name: 'MainLayout',
	components: {LeftDrawer, PolygonList, SettingsMenuModal, EditingPolygonHeader, PlanningSelector, LeftDrawerRouter, AppFrameModal},
	setup () {
		const { editingPolygon } = usePolygons()
		const { logout } = useSession()
    const toggleLeftDrawer = ref(true)
		const router = useRouter()
		const {
			planning,
			selectPlanning,
			selectedPlanning
		} = usePlanning()

		const selectedDay = ref(weekDays[0])
		const drawerRight = ref(false)
		const attachedFile = ref(null)

		const handleLogout = () => {
			logout()
			router.replace({ path: '/login' })
		}

		/*watch(attachedFile, async () => {
			if (attachedFile.value) {
				await updateCustomers(attachedFile.value)
				console.log('attachedFile:', attachedFile.value)
				attachedFile.value = null
			}
		})*/

		const attachedFileStr = computed(() => attachedFile.value ? JSON.stringify(attachedFile.value) : '')

		return {
			handleLogout,
      toggleLeftDrawer,
			weekDays,
			planning,
			selectedDay,
			drawerRight,
			attachedFile,
			editingPolygon,
			attachedFileStr,
			selectedPlanning,
			selectPlanning,
		}
	}
}
</script>
