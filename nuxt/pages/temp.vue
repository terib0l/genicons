<script setup lang="ts">
// data
// const { data } = await useFetch(() => "https://jsonplaceholder.typicode.com/users");
// const users: Array<object> = data._rawValue;

let img: File | null = null

const onImageUploaded = (event: any) => {
  img = event.target.files[0];
}

const createProduct = () => {
  if(img == null) {
    console.log("There is nothing.");
  } else {
    console.log("There is a img"); // request Web API
  }
}
</script>

<template>
  <div class="w-fit mx-auto">
    <h1 class="font-bold italic text-4xl text-gray-300 m-10 p-10">
      Welcome to Genicons!!
    </h1>
    <form class="flex justify-center items-center space-x-6 p-10">
      <div class="shrink-0">
        <img class="h-24 w-24 object-cover rounded-full" src="https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1361&q=80" alt="Current profile photo" />
      </div>
      <label class="block">
        <span class="sr-only">Choose profile photo</span>
        <input type="file" @change="onImageUploaded" class="block w-full text-sm text-slate-500
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
        <button type="button" @click="createProduct" class="inline-block px-6 py-2 border-2 border-emerald-500 text-emerald-500 font-medium text-xs leading-tight uppercase rounded hover:bg-black hover:bg-opacity-5 focus:outline-none focus:ring-0 transition duration-150 ease-in-out">
          Let's create!!
        </button>
      </div>
    </div>
  </div>
  <section class="overflow-hidden text-gray-700">
    <div class="container px-5 py-2 mx-auto lg:pt-12 lg:px-32 border-t border-gray-400 my-10">
      <div class="flex flex-wrap -m-1 md:-m-2">
        <div class="flex flex-wrap w-1/3">
          <div class="w-full p-1 md:p-2">
            <img alt="gallery" class="block object-cover object-center w-full h-full rounded-lg"
              src="https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(73).webp">
          </div>
        </div>
        <div class="flex flex-wrap w-1/3">
          <div class="w-full p-1 md:p-2">
            <img alt="gallery" class="block object-cover object-center w-full h-full rounded-lg"
              src="https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(74).webp">
          </div>
        </div>
        <div class="flex flex-wrap w-1/3">
          <div class="w-full p-1 md:p-2">
            <img alt="gallery" class="block object-cover object-center w-full h-full rounded-lg"
              src="https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(75).webp">
          </div>
        </div>
        <div class="flex flex-wrap w-1/3">
          <div class="w-full p-1 md:p-2">
            <img alt="gallery" class="block object-cover object-center w-full h-full rounded-lg"
              src="https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(70).webp">
          </div>
        </div>
        <div class="flex flex-wrap w-1/3">
          <div class="w-full p-1 md:p-2">
            <img alt="gallery" class="block object-cover object-center w-full h-full rounded-lg"
              src="https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(76).webp">
          </div>
        </div>
        <div class="flex flex-wrap w-1/3">
          <div class="w-full p-1 md:p-2">
            <img alt="gallery" class="block object-cover object-center w-full h-full rounded-lg"
              src="https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(72).webp">
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
