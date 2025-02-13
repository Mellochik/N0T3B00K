<script setup>
import { ref, onMounted } from 'vue';
import CloseIcon from '../icons/CloseIcon.vue';

const props = defineProps({
  labels: {
    type: Array,
    default: () => []
  },
});

const emit = defineEmits(['update:selectedLabels']);

const allLabels = ref([]);
const selectedLabels = ref(props.labels);

onMounted(async () => {
  const responseLabels = await fetch('http://127.0.0.1:8000/tasks/labels')
  const dataLabels = await responseLabels.json()
  allLabels.value = dataLabels

  selectedLabels.value.forEach((selectedLabel) => {
    allLabels.value = allLabels.value.filter(label => label.id !== parseInt(selectedLabel.id))
  })

  emit('update:selectedLabels', selectedLabels.value.map(label => label.id));
})

function handleSelectChange(event) {
  const selectedId = event.target.value
  const selectedLabel = allLabels.value.find(label => label.id === parseInt(selectedId))
  if (selectedLabel) {
    selectedLabels.value.push(selectedLabel)
    allLabels.value = allLabels.value.filter(label => label.id !== parseInt(selectedId))
  }

  emit('update:selectedLabels', selectedLabels.value.map(label => label.id));
}

function handleDeleteLabel(label) {
  const index = selectedLabels.value.indexOf(label)
  if (index !== -1) {
    selectedLabels.value.splice(index, 1)
    allLabels.value.push(label)
  }

  emit('update:selectedLabels', selectedLabels.value.map(label => label.id));
}
</script>

<template>
  <div class="labels">
    <select @change="handleSelectChange" v-if="allLabels.length > 0">
      <option></option>
      <option v-for="label in allLabels" :key="label.id" :value="label.id">{{ label.name }} </option>
    </select>
    <div class="label-container">
      <div v-for="label in selectedLabels" :key="label.id" class="label">
        {{ label.name }}
        <CloseIcon :size="20" :color="'#a5a5a5'" @click="handleDeleteLabel(label)" />
      </div>
    </div>
  </div>
</template>

<style scoped>
select {
  font-size: 20px;
  border-color: transparent;
  border-radius: 10px;
  color: #a5a5a5;
  background-color: #2c2c2c;
  max-width: fit-content;
  padding: 2px 10px;
}

select:focus {
  outline: none;
  border-color: transparent;
  box-shadow: none;
}

.labels {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.label-container {
  flex-grow: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.label {
  padding: 5px 10px;
  background-color: #2c2c2c;
  border-radius: 10px;
  display: flex;
  align-items: center;
}
</style>