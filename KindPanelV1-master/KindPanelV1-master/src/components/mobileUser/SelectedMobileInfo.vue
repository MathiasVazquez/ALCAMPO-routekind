<template>
    <div>
        <!-- SELECT MOBILE -->
        <q-item class="q-pa-none">
            <q-item-section>
                <q-item-label header overline class="bg-grey-2">
                    <div class="row justify-between items-center">
                        <div>MÓVIL SELECCIONADO</div>
                    </div>
                </q-item-label>
            </q-item-section>
        </q-item>
        <q-separator/>
        <!-- MOBILE INFO mobileImage: {{mobileImage}} -->
        <q-item>
            <q-item-section avatar>
                <q-avatar color="primary"></q-avatar>
            </q-item-section>
            <q-item-section>
                <q-item-label class="bg-grey-3 rounded-borders">
                    <MobileSelector />
                </q-item-label>
                <q-item-label caption class="q-ml-xs">
                    {{mobileUsername}}
                </q-item-label>
            </q-item-section>
            <q-item-section side>
                <q-btn flat dense round icon="edit" size="12px" />
            </q-item-section>
        </q-item>
        <!--selectedMobile: {{selectedMobile}}-->
    </div>
</template>

<script>
import { computed } from 'vue'
import MobileSelector from 'src/components/mobile/MobileSelector'
import { useMobiles } from 'src/context'

export default {
    components: {MobileSelector},
    setup() {
        const { selectedMobile } = useMobiles()

        const mobileName = computed(_ => selectedMobile.value ? selectedMobile.value.name : '')
        const mobileUser = computed(_ => selectedMobile.value ? selectedMobile.value.user : null)
        const mobileUsername = computed(_ => 
            mobileUser.value ? `@${mobileUser.value.username}` : 'Sin usuario')
        const mobileImage = computed(_ => mobileUser.value ? mobileUser.value.image : '')

        return {
            selectedMobile,
            mobileUsername,
            mobileName,
            mobileImage,
        }
    },
}
</script>