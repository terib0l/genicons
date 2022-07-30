<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
});

const { sent_message, sendMessage } = useContacts();
</script>

<template>
  <div class="flex flex-col w-fit mx-auto justify-center">
    <h1 class="font-bold italic text-center text-4xl text-gray-300 m-10 p-10">
      Contact Form
    </h1>
    <div class="py-2 px-4 rounded-t-lg">
      <textarea class="textarea textarea-success" v-model="sent_message" rows="7" cols="70" placeholder="Type requirements ..."></textarea>
    </div>
    <div class="text-right py-2 px-3 border-t dark:border-gray-600">
      <button @click="sendMessage" class="btn btn-success inline-flex items-center py-2.5 px-4 text-sm font-medium">
        Send
      </button>
    </div>
  </div>
</template>
