<script setup lang="ts">
import { ref } from 'vue';

// data
const contents = ref('');

// methods
const sendText = async () => {
  if (contents) {
    const res: boolean = window.confirm(`${contents.value}\n\nこの内容で送信しますか？`);

    if (res) {
      const options = {
        method: 'POST',
        body: { contents: contents },
        baseURL: 'http://localhost:8888'
      }

      const { data } = await useAsyncData('contact', () => $fetch('/send/contact', options));

      alert(contents.value);
    }
  } else {
    alert("Please type your consern!!");
  }
};

</script>

<template>
  <div class="flex flex-col w-fit mx-auto justify-center">
    <h1 class="font-bold italic text-center text-4xl text-gray-300 m-10 p-10">Contact Form</h1>
    <div class="py-2 px-4 rounded-t-lg">
      <textarea class="textarea textarea-success" v-model="contents" rows="7" cols="70" placeholder="Type requirements ..."></textarea>
    </div>
    <div class="text-right py-2 px-3 border-t dark:border-gray-600">
      <button @click="sendText" class="btn btn-success inline-flex items-center py-2.5 px-4 text-sm font-medium">
        Send
      </button>
    </div>
  </div>
</template>
