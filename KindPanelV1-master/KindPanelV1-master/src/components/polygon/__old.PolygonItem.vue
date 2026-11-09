<template>
    <!-- PLYGON DELETE CONFIRMATION -->
    <ConfirmDeleteModal 
        v-model="showConfirmRemovePolygon" 
        @confirm="handleRemovePolygon"
        :preventAutoClose="true"
        :loading="removing"
        :error="removingErrorMessage"
    >
        ¿Estás seguro/a de que quieres eliminar la figura <strong>{{polygonName}}</strong>?
    </ConfirmDeleteModal>
    <!-- POLYGON ITEM -->
    <q-item 
        clickable 
        class="relative-position"
        @click="selectPolygon(poly)"
        :class="isSelectedPolygon?'bg-grey-2 shadow-2':selectedToShow?'bg-grey-2':'bg-white'"
        style="margin:5px;border-radius:4px;overflow:hidden"
        :style="isSelectedPolygon?`border:1px solid ${poly.color}`:'border:1px solid #ccc'"
    >
        <!-- POLYGON PROPS -->
        <q-item-section>
            <div class="absolute-left full-height" 
                style="width:10px" 
                :style="`background-color:${poly.color}`"
            >
                <!-- POLYGON COLOR -->
                <q-menu v-model="selectedToShowColorSelector" class="q-pa-md row">
                    <div v-for="(type, index) of colors" :key="index" class="column">
                        <div v-for="color of type" :key="color" style="padding:1px">
                            <q-avatar size="24px" class="handler"
                                :style="`background-color:`+color" 
                                @click="setSelectedPolygonColor(color)"
                            />
                        </div>
                    </div>
                </q-menu>
            </div>
            <!-- POLYGON NAME INPUT -->
            <PolygonNameInput
                :currentItem="poly" 
                v-model:focus="focusPolygonNameInput" 
            />
        </q-item-section>
        <!-- POLYGON OPTIONS -->
        <q-item-section side v-if="isSelectedPolygon">
            <div class="row q-gutter-x-xs">
                <q-btn flat round dense size="11px" icon="edit"
                    :class="{'text-white bg-primary': editingPolygon}"
                    @click="setEditingPolygon(!editingPolygon)"
                >
                    <q-tooltip>Editar figura</q-tooltip>
                </q-btn>
                <ItemOptionsBtn :options="polygonOptions" />
            </div>
        </q-item-section>
    </q-item>
</template>

<script>
import { ref, computed, toRefs, nextTick } from 'vue'
import { weekDays, colors } from 'src/utils/statics'
import PolygonNameInput from 'src/components/polygon/PolygonNameInput'
import ConfirmDeleteModal from 'src/components/includes/ConfirmDeleteModal'
import ItemOptionsBtn from 'src/components/includes/ItemOptionsBtn'
import { usePolygons } from 'src/context'

export default {
    components: {PolygonNameInput, ConfirmDeleteModal, ItemOptionsBtn},
    props: ['poly'],
    setup(props) {
        const {
            selectedPolygon, 
            showAllPolygons,
            editingPolygon,
            selectPolygon, 
            setEditingPolygon,
            removeSelectedPolygon,
            setSelectedPolygonColor,
            setSelectedPolygonDisabled,
        } = usePolygons()

        const { poly } = toRefs(props)

        // Polygon color and input focus
        const selectedToShowColorSelector = ref(false)
        const focusPolygonNameInput = ref(false)

        // Polygon show and selections
        const isSelectedPolygon = computed(() => selectedPolygon.value && poly.value.id === selectedPolygon.value.id)
        const selectedToShow = computed(() => showAllPolygons.value || isSelectedPolygon.value)
        
        //
        // HANDLE REMOVE POLYGON
        //
        const showConfirmRemovePolygon = ref(false)
        const removing = ref(false)
        const removingErrorMessage = ref('')
        const handleRemovePolygon = async () => {
            removing.value = true
            const { error } = await removeSelectedPolygon()
            if (error) removingErrorMessage.value = "No fue posible remover la figura, por favor vuelva a intentarlo."
            else showConfirmRemovePolygon.value = false
            removing.value = false
        }
        //
        // Polygon options
        //
        const polygonOptions = computed(() => [{
            text: 'Cambiar nombre',
            icon: 'o_mode_edit_outline',
            onClick: () => focusPolygonNameInput.value = true,
        }, {
            text: 'Cambiar color',
            icon: 'o_palette',
            onClick: () => selectedToShowColorSelector.value = true,
        }, {
            text: 'Enfocar en el mapa',
            hidden: true,
            icon: 'o_pin_drop',
            onClick: () => {}
        }, {
            text: poly.value.disabled ? 'Habilitar' : 'Deshabilitar',
            icon: poly.value.disabled ? 'o_visibility' : 'o_visibility_off',
            onClick: () => setSelectedPolygonDisabled(!poly.value.disabled),
        }, {
            text: 'Eliminar',
            icon: 'o_delete',
            onClick: () => showConfirmRemovePolygon.value = true,
        }])

        // Polygon name
        const polygonName = computed(_ => poly.value ? poly.value.name || `Figura ${poly.value.id}` : '')

        return {
            poly,
            polygonName,
            selectedPolygon,
            editingPolygon,
            colors,
            selectedToShowColorSelector,
            focusPolygonNameInput,
            polygonOptions,
            showConfirmRemovePolygon,
            selectPolygon,
            selectedToShow,
            setEditingPolygon,
            isSelectedPolygon,
            setSelectedPolygonColor,
            handleRemovePolygon,
            removing,
            removingErrorMessage
        }
    },
}
</script>