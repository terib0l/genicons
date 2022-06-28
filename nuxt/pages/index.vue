<script setup lang="ts">
</script>

<template>
  <div class="main">
    <h1>Welcome!!</h1>
    <NuxtLink class="nl" to="/making">&gt;&gt; Making</NuxtLink>
    <NuxtLink class="nl" to="/square">&gt;&gt; Garally</NuxtLink>
    <NuxtLink class="nl" to="/contact">&gt;&gt; Contact</NuxtLink>
  </div>
</template>

<style>
.main {
  text-align: center;
}

h1 {
  color: white;
}

.nl:link {
  padding: 20px 20px;
  font-size: 20px;
  text-decoration: none;
}

.nl:visited {
  color: aquamarine;
}
</style>
