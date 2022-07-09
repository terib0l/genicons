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
  <div class="halloween mx-10 my-5 justify-center">
    <div>
      <h1>Contact Form</h1>
    </div>
    <div>
      <textarea class="textarea textarea-success p-10" v-model="text"></textarea>
      <button @click="sendText" class="btn btn-success mx-5">Click</button>
    </div>
  </div>
</template>
