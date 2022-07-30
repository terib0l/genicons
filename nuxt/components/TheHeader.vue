<script setup lang="ts">
const { logout } = useAuth();

const logoutProcess = async () => {
  const currnt_route = useRoute().fullPath;
  if (currnt_route !== '/login' && currnt_route !== '/register'){
    if (window.confirm("Are you sure logout")){
      await logout();
    }
  }
}
</script>

<template>
  <nav class="flex items-center justify-between flex-wrap bg-gray-300 p-6 m-5 rounded">
    <div class="flex items-center flex-shrink-0 text-emerald-500 mr-6">
      <img src="https://www.svgrepo.com/show/352776/hand-lizard.svg" class="w-12 h-12">
      <span class="font-semibold text-xl tracking-tight pl-4">GENICONS</span>
    </div>
    <!-- <div class="w-full block flex-grow lg:flex lg:items-center lg:w-auto mr-4"> -->
    <div class="mr-4 py-2">
      <NuxtLink to="/" class="text-center w-32 inline-block text-base px-4 py-3 leading-none text-white bg-emerald-500 hover:border-transparent hover:text-white hover:bg-emerald-700 mt-4 lg:mt-0">
        HOME
      </NuxtLink>
      <NuxtLink to="/products" class="w-32 text-center inline-block text-base px-4 py-3 leading-none text-white bg-emerald-500 hover:border-transparent hover:text-white hover:bg-emerald-700 mt-4 lg:mt-0">
        PRODUCTS
      </NuxtLink>
      <NuxtLink to="/contacts" class="w-32 text-center inline-block text-base px-4 py-3 leading-none text-white bg-emerald-500 hover:border-transparent hover:text-white hover:bg-emerald-700 mt-4 lg:mt-0">
        CONTACTS
      </NuxtLink>
      <p @click="logoutProcess" class="w-32 text-center inline-block text-base px-4 py-3 leading-none text-white bg-gray-600 hover:border-transparent hover:text-white hover:bg-gray-800 mt-4 lg:mt-0">
        LOGOUT
      </p>
    </div>
  </nav>
</template>
