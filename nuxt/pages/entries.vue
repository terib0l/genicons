<script setup lang="ts">
// data
const { data } = await useFetch(() => "https://jsonplaceholder.typicode.com/users");
const users: Array<object> = data._rawValue;

</script>

<template>
  <div class="main">
    <h1>Garally</h1>
  </div>
  <div class="list">
    <ul v-for="user in users" :key="user.id">
      <li>{{ user.id }} - {{ user.username }} - {{ user.email }}</li>
    </ul>
  </div>
</template>

<style>
.list {
  text-align: left;
  padding: 20px 0;
  color: aquamarine;
}
</style>
