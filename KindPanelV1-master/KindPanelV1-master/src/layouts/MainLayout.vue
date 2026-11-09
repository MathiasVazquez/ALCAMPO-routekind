<template>
	<q-layout view="lHh Lpr lFf" class="bg-transparent">
		<!--<EditingPolygonHeader v-if="editingPolygon" />-->
		<!-- HEADER -->
		<q-header class="bg-transparent text-black">
			<q-toolbar class="bg-transparent">
				<!-- SELECT PLAN -->
				<!--<PlanningSelector />-->
				<q-space/>

				<!-- ATTACH FILE -->
				<q-file v-if="false" dense outlined v-model="attachedFile" label="Cargar lista de clientes">
					<template v-slot:prepend>
						<q-icon name="attach_file" />
					</template>
					<template v-slot:append>
						<q-btn flat dense round icon="close" @click="attachedFile=null" />
					</template>
				</q-file>
        <SessionOptions :hideMapOptions="true" />
			</q-toolbar>
		</q-header>

		<LeftDrawer />

		<!-- BODY -->
		<q-page-container>
			<router-view />
		</q-page-container>

    <AppFrameModal />
	</q-layout>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { usePlanning, usePolygons, useSession } from 'src/context'
import { weekDays } from 'src/utils/statics'
import { useRouter } from 'vue-router'
import PolygonList from 'src/components/polygon/PolygonList'
import ZoneSelector from 'src/components/zone/ZoneSelector'
import EditingPolygonHeader from 'src/components/polygon/EditingPolygonHeader'
import LeftDrawer from 'src/pages/includes/LeftDrawer'
import PlanningSelector from 'src/components/planning/PlanningSelector'
import SessionOptions from 'src/components/security/SessionOptions'
import AppFrameModal from 'src/components/mobileApp/AppFrameModal'

export default {
	name: 'MainLayout',
	components: {LeftDrawer, PolygonList, ZoneSelector, EditingPolygonHeader, PlanningSelector, SessionOptions, AppFrameModal},
	setup () {
		const { editingPolygon } = usePolygons()
		const { logout } = useSession()
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
