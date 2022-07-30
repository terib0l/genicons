<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
});

const { productList, productIdsFlag,
        fetchProductIds, fetchProductOrigins, fetchProduct } = useProducts();

fetchProductIds();
fetchProductOrigins();
</script>

<template>
  <div class="w-fit mx-auto flex flex-col justify-center">
    <h1 class="font-bold italic text-center text-4xl text-gray-300 m-10 p-10">
      Your Products
    </h1>
    <div v-if="productIdsFlag">
      <table class="table w-full">
        <thead>
          <tr class="text-center">
            <th class="text-xl">Num</th>
            <th class="text-xl">Product ID</th>
            <th class="text-xl">Origin Img</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(productData, index) in productList" :key="index" class="hover text-center" @click="fetchProduct(productData.id)">
            <td class="text-emerald-400">{{ index+1 }}</td>
            <td class="text-emerald-500 text-lg font-semibold font-mono">{{ productData.id }}</td>
            <td class="flex justify-center">
              <img class="h-10 w-10" :src="productData.img" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <div class="alert alert-success shadow-lg">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current flex-shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <span class="text-lg font-bold">Your products is nothing!</span>
        </div>
      </div>
    </div>
  </div>
</template>
