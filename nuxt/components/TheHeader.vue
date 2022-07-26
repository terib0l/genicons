<template>
  <nav class="flex items-center justify-between flex-wrap bg-gray-300 p-6 m-5 rounded">
    <div class="flex items-center flex-shrink-0 text-emerald-500 mr-6">
      <img src="https://www.svgrepo.com/show/352776/hand-lizard.svg" class="w-12 h-12">
      <span class="font-semibold text-xl tracking-tight pl-4">GENICONS</span>
    </div>
    <!-- <div class="w-full block flex-grow lg:flex lg:items-center lg:w-auto mr-4"> -->
    <div class="mr-4 py-2">
      <NuxtLink to="/" class="inline-block text-base px-4 py-2 leading-none text-white bg-emerald-500 hover:border-transparent hover:text-white hover:bg-gray-900 mt-4 mr-2 lg:mt-0">
        HOME
      </NuxtLink>
      <NuxtLink to="/products" class="inline-block text-base px-4 py-2 leading-none text-white bg-emerald-500 hover:border-transparent hover:text-white hover:bg-gray-900 mt-4 mr-2 lg:mt-0">
        PRODUCTS
      </NuxtLink>
      <NuxtLink to="/contacts" class="inline-block text-base px-4 py-2 leading-none text-white bg-emerald-500 hover:border-transparent hover:text-white hover:bg-gray-900 mt-4 lg:mt-0">
        CONTACTS
      </NuxtLink>
    </div>
  </nav>
</template>
