<script setup lang="ts">
// import JSZip from 'jszip';
// import JSZipUtils from 'jszip-utils';

// import AssetsImage from '@/assets/images/c_81940681-204c-47a2-9eb0-2e4b516edb3d.jpg';

let image: Blob = null;
const productId = ref<string>('');
const initGallery = async () => {
  const options = {
    method: 'GET',
    params: { num: 6 },
    baseURL: 'http://localhost:8888'
  };

  const { data } = await useLazyAsyncData('gallery', () => $fetch('/fetch/gallery', options));

  // const urls: Array<string> = 
}
const urls: Array<string> = [
  "https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(73).webp",
  "https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(74).webp",
  "https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(75).webp",
  "https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(70).webp",
  "https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(76).webp",
  "https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(72).webp",
]

const uploadImage = (event: any) => {
  image = event.target.files[0];
}

const generateProduct = async () => {
  if(image) {
    const bodyImg = new FormData();
    bodyImg.append('img', image);

    const options = {
      method: 'POST',
      body: bodyImg,
      params: { user_id: 2 },
      baseURL: 'http://localhost:8888'
    };

    const { data } = await useAsyncData('generate', () => $fetch('/generate/product', options));

    productId.value = data._rawValue.product_id;

    const productDialog = document.getElementById('productDialog');
    productDialog.showModal();
  } else {
    alert("Please set JPG!!");
  }
}
</script>

<template>
  <div class="w-fit mx-auto">
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
    <h1 class="font-bold italic text-4xl text-gray-300 m-10 p-10">
      Welcome to Genicons!!
    </h1>
    <form class="flex justify-center items-center space-x-6 p-10">
      <div class="shrink-0">
        <img class="h-24 w-24 object-cover rounded-full" src="https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1361&q=80" alt="Current profile photo" />
      </div>
      <label class="block">
        <span class="sr-only">Choose profile photo</span>
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
        <button type="button" @click="generateProduct" class="inline-block px-6 py-2 border-2 border-emerald-500 text-emerald-500 font-medium text-sm leading-tight uppercase rounded hover:bg-black hover:bg-opacity-5 focus:outline-none focus:ring-0 transition duration-150 ease-in-out">
          Let's create!!
        </button>
      </div>
    </div>
  </div>
  <section class="overflow-hidden text-gray-700">
    <div class="container px-5 py-2 mx-auto lg:pt-12 lg:px-32 border-t border-gray-400 my-10">
      <div class="flex flex-wrap -m-1 md:-m-2">
        <div v-for="url in urls" :key="url" class="flex flex-wrap w-1/3">
          <div class="w-full p-1 md:p-2">
            <img alt="gallery" class="block object-cover object-center w-full h-full rounded-lg"
              :src="url">
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
