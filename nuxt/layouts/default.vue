<template>
  <div class="background">
    <TheHeader />
    <slot />
    <TheFooter />
  </div>
</template>

<style>
.background {
  height: 100vh;
  padding: 20px 20px;
  background-color: #222;
}
</style>
