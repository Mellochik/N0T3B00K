<script setup>
import { ref, onMounted } from 'vue';
import { marked } from 'marked';

const props = defineProps({
    text: {
        type: String,
        default: '',
    },
    readonly: {
        type: Boolean,
        default: false,
    },
});

defineEmits(['update:description']);

const localText = ref(props.text);
const renderedMarkdown = ref('');
const textareaRef = ref(null);
const edit = ref(true);

function handlePreview() {
    const markdownText = localText.value;
    renderedMarkdown.value = marked(markdownText);
    edit.value = false;
}

function handleEdit() {
    edit.value = true;
}

onMounted(() => {
    textareaRef.value.addEventListener('input', () => {
        textareaRef.value.style.height = 'auto';
        textareaRef.value.style.height = textareaRef.value.scrollHeight - 20 + 'px';
    });

    const markdownText = localText.value;
    renderedMarkdown.value = marked(markdownText);
});
</script>

<template>
    <textarea v-show="edit && !readonly" v-model="localText" ref="textareaRef"
        @input="$emit('update:description', $event.target.value)"></textarea>
    <div class="markdown" v-show="!edit || readonly" v-html="renderedMarkdown"></div>
    <div class="buttons" v-show="!readonly">
        <button v-show="edit" @click="handlePreview">Просмотр</button>
        <button v-show="!edit" @click="handleEdit">Редактирование</button>
    </div>
</template>

<style scoped>
textarea {
    font-size: 20px;
    border-color: transparent;
    border-radius: 10px;
    padding: 10px;
    background-color: #2c2c2c;
    color: #a5a5a5;
    height: auto;
    overflow-y: auto;
    resize: vertical;
}

textarea:focus {
    outline: none;
    border: none;
}

.markdown {
    border-radius: 10px;
    padding: 10px;
    background-color: #2c2c2c;
}

.markdown :deep(h1) {
    font-size: 24px;
    margin: 10px 0px;
    color: #a5a5a5;
}

.markdown :deep(h2) {
    font-size: 20px;
    margin: 10px 0px;
}

.markdown :deep(p) {
    font-size: 16px;
    margin: 0px 0px;
    padding: 0;
}

.markdown :deep(ul) {
    font-size: 16px;
}

.markdown :deep(ol) {
    font-size: 16px;
}

.markdown :deep(a) {
    color: #5c5c5c;
}

.markdown :deep(blockquote) {
    padding: 5px;
    margin: 10px 0px;
    border-left: 5px solid #a5a5a5;
}

.markdown :deep(blockquote > p) {
    padding: 0px;
    margin: 0px 10px;
}

.markdown :deep(code) {
    padding: 2px 2px;
    margin: 0;
    border-radius: 10px;
    background-color: #4c4c4c;
    font-size: 16px;
}

.markdown :deep(pre) {
    padding: 5px;
    margin: 0;
    border-radius: 10px;
    background-color: #4c4c4c;
    font-size: 16px;
}

.markdown :deep(pre > code) {
    padding: 0;
    margin: 0;
    background-color: transparent;
    font-size: 16px;
}

.markdown :deep(table) {
    border-collapse: collapse;
    overflow: hidden;
    margin: 10px 0px;
}

.markdown :deep(th),
.markdown :deep(td) {
    padding: 10px;
    border: 1px solid #4c4c4c;
    background-color: #2c2c2c;
    color: #a5a5a5;
    font-size: 16px;
}

.markdown :deep(th) {
    background-color: #3c3c3c;
}

.markdown :deep(td) {
    border-top: 1px solid #4c4c4c;
}

.markdown :deep(tr:nth-child(even)) {
    background-color: #333;
}

button {
    padding: 5px 10px;
    font-size: 16px;
    color: white;
    background-color: #2c2c2c;
    border: 0px;
    border-radius: 10px;
    float: right;
    width: fit-content;
}

button:hover {
    background-color: #3c3c3c;
}

button:active {
    background-color: #4c4c4c;
}
</style>