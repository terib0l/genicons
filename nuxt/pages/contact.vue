<script setup lang="ts">
import { ref } from 'vue';

// data
const text = ref('Type your ideas...');

// methods
const sendText = (() => {
  console.log(`Hello ${text.value}`);
  // await useFetch(() => "https://jsonplaceholder.typicode.com/users");
});

</script>

<template>
  <h1>Contact Form</h1>
  <input type="textarea" v-model="text" />
  <button @click="sendText">Click</button>
</template>
