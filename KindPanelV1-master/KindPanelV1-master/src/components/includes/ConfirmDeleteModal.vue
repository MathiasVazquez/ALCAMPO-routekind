<template>
    <q-dialog :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="o_delete" color="primary" text-color="white" />
          <span class="q-ml-sm"><slot/></span>
          <div v-if="error" class="q-pa-sm q-ma-sm bg-red text-white rounded-borders">{{error}}</div>
        </q-card-section>
        <q-card-actions v-if="loading" align="right">
          <q-spinner-pie color="primary" size="2em" />
        </q-card-actions>
        <q-card-actions v-else align="right" class="jusgity-between">
          <q-btn flat label="Cancelar" color="grey-8" v-close-popup />
          <q-btn v-if="preventAutoClose" flat label="Eliminar" color="primary" @click="$emit('confirm', $emit)" />
          <q-btn v-else flat label="Eliminar" color="primary" v-close-popup @click="$emit('confirm', $emit)" />
        </q-card-actions>
      </q-card>
    </q-dialog>
</template>

<script>
import { toRefs } from 'vue';

export default {
    props: ['modelValue', 'preventAutoClose', 'loading', 'error'],
    emits: ['confirm', 'update:modelValue', 'update:error'],
    setup(props) {
        const { modelValue, preventAutoClose, loading, error } = toRefs(props)

        return {
            modelValue,
            preventAutoClose,
            loading,
            error
        }
    },
}
</script>