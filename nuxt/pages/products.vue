<script setup lang="ts">
const productIdsBool = ref<boolean>(false);
const productIds = ref<Array<string>>([]);

// Immediate Func
(async () => {
  const options = {
    method: 'GET',
    params: {
      user_id: 3
    },
    baseURL: useRuntimeConfig().baseUrl,
  };

  const { data } = await useAsyncData(
    'productIds',
    () => $fetch('/fetch/product/ids', options)
  );

  for (let i = 0; i < data.value.length; i++){
    productIds.value.push(data.value[i]);
  }

  if ( productIds.value.length > 0 ){
    productIdsBool.value = true;
  }
})();

const fetchProduct = async (productId: string) => {
  const res: boolean = window.confirm(
    `Will you download this product??\n\n${productId}`
  );

  if (res) {
    const options = {
      method: 'GET',
      params: {
        product_id: productId
      },
      baseURL: useRuntimeConfig().baseUrl,
    };

    const { data } = await useAsyncData(
      'product',
      () => $fetch('/fetch/product', options)
    );

    if (data.value && data.value instanceof Blob){
      const uri = URL.createObjectURL(data.value);
      const link = document.createElement('a');
      link.download = `${productId}.zip`;
      link.href = uri;
      link.click();
    } else {
      alert(`This product is not created yet, so wait some minutes!!\n\n${productId}`)
    }
  }
}
</script>

<template>
  <div class="w-fit mx-auto flex flex-col justify-center">
    <h1 class="font-bold italic text-center text-4xl text-gray-300 m-10 p-10">
      Your Products
    </h1>
    <div v-if="productIdsBool">
      <table class="table w-full">
        <thead>
          <tr class="text-center">
            <th class="text-xl">Num</th>
            <th class="text-xl">Product ID</th>
          </tr>
        </thead>
        <tbody v-for="(productId, index) in productIds" :key="index">
          <tr class="hover text-center" @click="fetchProduct(productId)">
            <th class="text-emerald-400">{{ index }}</th>
            <td class="text-emerald-500 text-lg font-semibold font-mono">{{ productId }}</td>
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
