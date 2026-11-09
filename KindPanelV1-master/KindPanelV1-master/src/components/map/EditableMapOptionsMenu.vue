<template>
  <q-list class="q-pa-none q-ma-none">

    <!-- VIEW SCOPE -->
    <div class="row">
      <div class="bg-primary text-white q-px-xs q-py-xs q-mx-xs q-mt-sm rounded-borders text-caption">
        <strong>{{viewScopeName}}</strong>
      </div>
    </div>

    <!-- VISUALIZATIONS -->

    <div v-for="visualization of visualizations" :key="visualization.title">
      <q-item-label class="q-px-xs" header>{{visualization.title}}</q-item-label>

      <q-btn-dropdown no-caps auto-close flat class="q-mx-none q-mb-md">
        <template #label>
          <q-item style="width:225px" class="q-pa-none">
            <!-- <q-item-section avatar st>

            </q-item-section> -->
            <q-item-section class="text-left">
              <q-item-label style="white-space:normal" class="row no-wrap q-gutter-x-xs items-center">
                <q-avatar rounded :icon="visualization.selected.value.icon"
                  :color="visualization.selected.value.color"
                  text-color="white" size="28px"
                />
                <div>{{visualization.selected.value.title}}</div>
              </q-item-label>
              <q-item-label caption style="white-space:normal">
                {{visualization.selected.value.description}}
              </q-item-label>
            </q-item-section>
          </q-item>
        </template>
        <q-list separator>
          <q-item v-for="option of visualization.options.value" :key="option.value"
            clickable @click="visualization.selected.value=option"
            class="full-width"
          >
            <q-item-section avatar style="max-width:300px">
              <q-avatar :icon="option.icon" :color="option.color" text-color="white" size="32px" />
            </q-item-section>
            <q-item-section style="max-width:300px">
              <q-item-label style="white-space:normal">{{option.title}}</q-item-label>
              <q-item-label caption style="white-space:normal">{{option.description}}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>

      <q-separator spaced />
    </div>
  </q-list>
</template>

<script>
import { ref, computed } from 'vue'
import { useSettings } from 'src/context'

export default {
  setup() {
    const { polygonVisualization, eventVisualization, addressesVisualization, orderVisualization, viewScope } = useSettings()

    const viewScopeName = computed(() => {
      switch(viewScope.value) {
        case "zones":
          return "ZONAS"
        case "orders":
          return "PEDIDOS"
        case "events":
          return "EVENTOS"
        case "editmode":
          return "EDICIÓN DE FIGURAS"
      }
    })

    const polygonOptions = ref([{
      title: 'Mostrar las figuras de los móviles seleccionados',
      description: 'Se muestran las figuras de todas las zonas pertenencientes a los móviles seleccionados en la planificación actual',
      value: 'all',
      icon: 'done_all',
      color: 'green',
    }, {
      title: 'Mostrar solo las figuras de la zona seleccionada',
      description: 'Se muestran todas las figuras de la zona seleccionada',
      value: 'zone',
      icon: 'route',
      color: 'purple',
    }, {
      title: 'Mostrar solo la figura seleccionada',
      description: 'Se ocultan del mapa todas las figuras que no estén seleccionadas',
      value: 'figure',
      icon: 'pentagon',
      color: 'orange',
    }, {
      title: 'Ocultar todas las figuras',
      description: 'Ninguna figura será visible en el mapa',
      value: 'none',
      icon: 'close',
      color: 'red',
    }])
    const selectedPolygonVisualization = computed({
      get: () => polygonOptions.value.find(o => o.value === polygonVisualization.value),
      set: option => polygonVisualization.value = option.value
    })

    const orderOptions = ref([{
      title: 'Mostrar los pedidos de los móviles seleccionados',
      description: 'Se mostrarán todos los pedidos que hayan sido asignados a los móviles seleccionados junto con los pedidos no asignados a ningún móvil',
      value: 'all',
      icon: 'done_all',
      color: 'green',
    }, {
      title: 'Ocultar todos los pedidos',
      description: 'Ningún pedido será visible en el mapa',
      value: 'none',
      icon: 'close',
      color: 'red',
    }])
    const selectedOrderVisualization = computed({
      get: () => orderOptions.value.find(o => o.value === orderVisualization.value),
      set: option => orderVisualization.value = option.value
    })

    const addressOptions = ref([{
      title: 'Mostrar todos los clientes',
      description: 'Todos los clientes del sistema serán visibles en el mapa',
      value: 'all',
      icon: 'done_all',
      color: 'green',
    }, {
      title: 'Mostrar solo los clientes de la zona actual',
      description: 'Todos los clientes incluidos de la zona seleccionada serán visibles (no recomendado)',
      value: 'zone',
      icon: 'switch_account',
      color: 'purple',
    }, {
      title: 'Mostrar solo los clientes de la figura actual',
      description: 'Solo los clientes de la figura seleccionada serán visibles (no recomendado)',
      value: 'polygon',
      icon: 'supervised_user_circle',
      color: 'orange',
    }, {
      title: 'Ocultar todos los clientes',
      description: 'Todos los clientes del sistema se ocultarán (recomendado para una mayor fluidez)',
      value: 'none',
      icon: 'close',
      color: 'red',
    }])
    const selectedAddressVisualization = computed({
      get: () => addressOptions.value.find(o => o.value === addressesVisualization.value),
      set: option => addressesVisualization.value = option.value
    })

    const eventOptions = ref([{
      title: 'Mostrar los eventos de los móviles seleccionados',
      description: 'Se mostrarán todos los eventos que hayan sido realizados a los móviles seleccionados',
      value: 'all',
      icon: 'done_all',
      color: 'green',
    }, {
      title: 'Ocultar todos los eventos',
      description: 'Ningún los evento será visible',
      value: 'none',
      icon: 'close',
      color: 'red',
    }])
    const selectedEventVisualization = computed({
      get: () => eventOptions.value.find(o => o.value === eventVisualization.value),
      set: option => eventVisualization.value = option.value
    })

    const visualizations = computed(() => {
      return [{
        title: 'Visualización de clientes',
        options: addressOptions,
        selected: selectedAddressVisualization,
      }, {
        title: 'Visualización de pedidos',
        options: orderOptions,
        selected: selectedOrderVisualization,
      }, {
        title: 'Visualización de polígonos',
        options: polygonOptions,
        selected: selectedPolygonVisualization,
      }, {
        title: 'Visualización de eventos',
        options: eventOptions,
        selected: selectedEventVisualization,
      }]
    })

    return {
      orderOptions,
      viewScopeName,
      polygonOptions,
      visualizations,
      orderVisualization,
      polygonVisualization,
      addressesVisualization,
      selectedOrderVisualization,
      selectedPolygonVisualization,
    }
  },
}
</script>
