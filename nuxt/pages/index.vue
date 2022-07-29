<script setup lang="ts">
import JSZip from "jszip";

const loading = ref<boolean>(false);

const file = ref<Blob>();
const productId = ref<string>('');

const gallerys = ref<Array<string>>([]);

(async () => {
  const options = {
    method: 'GET',
    params: {
      gallery_num: 9
    },
    baseURL: useRuntimeConfig().baseUrl,
  };

  const { data, pending } = await useLazyAsyncData(
    'gallery',
    () => $fetch('/fetch/gallery', options)
  )

  JSZip.loadAsync(data.value).then(function(zipData){
    Object.values(zipData.files).forEach(function (value) {
      gallerys.value.push(URL.createObjectURL(new Blob([value._data.compressedContent])));
    });

    loading.value = true;
  });
})();

const uploadImage = ( event: any ) => {
  file.value = event.target.files[0];
}

const generateProduct = async () => {
  if(file.value) {
    const formData = new FormData();

    formData.append('img', file.value);

    const options = {
      method: 'POST',
      body: formData,
      params: { user_id: 3 },
      baseURL: useRuntimeConfig().baseUrl
    };

    const { data } = await useAsyncData(
      'generate',
      () => $fetch('/generate/product', options)
    );

    productId.value = data.value.product_id;

    document.getElementById('productDialog').showModal();
  } else {
    alert("Please set JPG!!");
  }
}
</script>

<template>
  <div class="w-fit mx-auto flex flex-col justify-center">

    <dialog id="productDialog" class="bg-gray-300 rounded">
      <div class="p-3">
        <a class="text-lg font-bold text-slate-800">Your Product ID:&nbsp;&nbsp;</a>
        <a class="text-xl font-bold text-violet-700">{{ productId }}</a>
      </div>
      <menu class="flex justify-center">
        <button class="bg-transparent hover:bg-slate-600 text-slate-800 font-semibold hover:text-white py-2 px-4 border border-slate-600 hover:border-transparent rounded" onclick="document.getElementById('productDialog').close()">
          Confirm
        </button>
      </menu>
    </dialog>

    <h1 class="font-bold italic text-center text-4xl text-gray-300 m-10 p-10">
      Welcome to Genicons!!
    </h1>
    <form class="flex justify-center items-center space-x-6 p-10">
      <div class="shrink-0">
        <!-- <img class="h-24 w-24 object-cover rounded-full" src="/favicon.jpg" alt="Current profile photo" /> -->
        <img class="h-24 w-24 object-cover -scale-x-100 scale-y-100 rotate-12" src="/hand.svg" />
      </div>
      <label class="block">
        <input type="file" @change="uploadImage" class="block w-full text-sm text-slate-500
          file:mr-4 file:py-2 file:px-4
          file:rounded-full file:border-0
          file:text-sm file:font-semibold
          file:bg-emerald-50 file:text-emerald-500
          hover:file:bg-emerald-100
        "/>
      </label>
    </form>
    <div class="flex space-x-2 justify-center">
      <div>
        <button @click="generateProduct" class="btn btn-outline btn-success">
          Let's create!!
        </button>
      </div>
    </div>
  </div>

  <div class="border-t border-gray-400 m-10">
    <div v-if="loading">
      <section class="overflow-hidden text-gray-700 w-fit mx-auto justify-center">
        <div class="container px-5 py-2 lg:pt-12 lg:px-32 my-10">
          <div class="flex flex-wrap -m-1 md:-m-2">
            <div v-for="(product, index) in gallerys" :key="index" class="flex flex-wrap w-1/3">
              <div class="w-full p-1 md:p-2 flex justify-center">
                <img alt="gallery" class="block object-cover object-center pointer-events-none touch-none select-none h-60 w-60 my-3 rounded-full"
                  :src="product" />
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
    <div v-else>
      <button class="flex btn loading btn-wide mx-auto btn-success text-xl m-10">
        loading
      </button>
    </div>
  </div>
</template>
