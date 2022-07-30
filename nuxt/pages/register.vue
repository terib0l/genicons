<script setup lang="ts">
const { username, email, password, repeat_password,
        register } = useRegister();
</script>

<template>
  <div class="flex flex-col w-fit mx-auto justify-center">
    <h1 class="font-bold italic text-center text-4xl text-gray-300 m-10 p-10">
      Registration Form
    </h1>

    <form class="flex flex-col mt-4">
      <input
          type="text"
          v-model="username"
          class="text-gray-900 px-4 py-3 w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0 text-sm"
          placeholder="Username"
      />
      <input
          type="text"
          v-model="email"
          class="text-gray-900 px-4 py-3 mt-4 w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0 text-sm"
          placeholder="Email address"
      />
      <input
          type="password"
          v-model="password"
          class="text-gray-900 px-4 py-3 mt-4 w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0 text-sm"
          placeholder="Password"
      />
      <input
          type="password"
          v-model="repeat_password"
          class="text-gray-900 px-4 py-3 mt-4 w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0 text-sm"
          placeholder="Repeat Password"
      />
      <button
          type="button"
          @click="register"
          class="mt-4 px-4 py-3  leading-6 text-base rounded-md border border-transparent text-white focus:outline-none bg-emerald-500 text-white hover:bg-emerald-700 hover:text-white focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 cursor-pointer inline-flex items-center w-full justify-center items-center font-medium focus:outline-none"
      >
        Register
      </button>
      <div class="flex flex-col items-center mt-5">
        <p class="mt-1 text-xs font-light text-gray-500">
          Register already?
          <NuxtLink to="/login" class="ml-1 font-medium text-emerald-400 hover:text-white">Sign in now</NuxtLink>
        </p>
      </div>
    </form>

  </div>
</template>

