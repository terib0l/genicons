<script setup lang="ts">
import { ref } from 'vue';

// data
const text = ref('');

// methods
const sendText = (() => {
  const res: boolean = window.confirm(`${text.value}\n\nこの内容で送信しますか？`);

  if (res) {
    console.log(`Hello ${text.value}`);
    // await useFetch(() => "https://jsonplaceholder.typicode.com/users");
  } else {
    ;
  }
});

</script>

<template>
  <div class="flex flex-col w-fit mx-auto justify-center">
    <h1 class="font-bold italic text-center text-4xl text-gray-300 m-10 p-10">Contact Form</h1>
    <div class="py-2 px-4 rounded-t-lg">
      <textarea class="textarea textarea-success" v-model="text" rows="7" cols="70" placeholder="Type requirements ..."></textarea>
    </div>
    <div class="text-right py-2 px-3 border-t dark:border-gray-600">
      <button @click="sendText" class="btn btn-success inline-flex items-center py-2.5 px-4 text-sm font-medium">
        Send
      </button>
    </div>
  </div>
</template>
