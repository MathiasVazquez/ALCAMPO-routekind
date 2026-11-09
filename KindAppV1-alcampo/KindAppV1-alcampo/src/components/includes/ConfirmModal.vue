<template>
  <q-dialog v-model="showModal" persistent>
    <q-card>
      <q-card-section class="column flex-center q-gutter-y-md">
        <q-avatar :icon="confirmOptions.icon || 'o_delete'" :color="confirmOptions.color || 'primary'" text-color="white" />
        <span class="q-ml-sm">{{confirmOptions.text}}</span>
        <div v-if="hasError" class="q-pa-sm q-ma-sm bg-red text-white rounded-borders">{{confirmOptions.errorMessage}}</div>
      </q-card-section>
      <q-card-actions v-if="loadingConfirmModal" align="right">
      <q-spinner-pie :color="confirmOptions.color || 'primary'" size="2em" />
      </q-card-actions>
      <q-card-actions v-else>
        <q-btn flat label="Cancelar" color="grey-8" v-close-popup />
        <q-space />
        <q-btn flat :label="confirmOptions.confirmButtonMessange" :color="confirmOptions.color || 'primary'" @click="onConfirm" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { computed } from 'vue'
import { useConfirmModal } from 'src/context'

export default {
  setup() {
    const {
      hasError,
      onConfirm,
      confirmOptions,
      loadingConfirmModal,
      hideConfirModal,
    } = useConfirmModal()

    const showModal = computed({
      get() { return !!confirmOptions.value },
      set(value) { if (!value) hideConfirModal() }
    })

    return {
      onConfirm,
      hasError,
      showModal,
      confirmOptions,
      loadingConfirmModal,
    }
  },
}
</script>
