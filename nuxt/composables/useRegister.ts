import type { Ref } from 'vue';

const register = (
  username: Ref<string>, email: Ref<string>, password: Ref<string>, repeat_password: Ref<string>
) => async () => {
  if (!username.value || !email.value || !password.value || !repeat_password.value){
    alert("Please type your username, email and password!");
    return;
  }

  if(password.value !== repeat_password.value){
    alert("Two passwords is difference!");
    return;
  }

  if(password.value.length < 9 && password.value.length > 60){
    alert("This password is too long or too short!");
    return;
  }

  const emailReg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
  if (!emailReg.test(email.value)){
    alert("This email is invalid!");
    return;
  }

  if (username.value.length > 50){
    alert("This username is too long!");
    return;
  }

  const usernameReg = /^[a-z0-9]+$/;
  if (!usernameReg.test(username.value)){
    alert("This username is invalid!\n\n Username's regex is that /^[a-z]+$/");
    return;
  }

  const formData = new FormData()
  formData.append("username", username.value)
  formData.append("email", email.value)
  formData.append("password", password.value)

  const options = {
    method: 'POST',
    body: formData,
    baseURL: useRuntimeConfig().baseUrl
  }

  const { data, error } = await useAsyncData(
    'generateUser',
    () => $fetch('/generate/user', options)
  );

  if (error.value){
    alert("Registration Failure!");
    username.value = '';
    email.value = '';
    password.value = '';
    repeat_password.value = '';
    return;
  } else {
    alert("Registration Sucess!!");
    navigateTo('/login');
  }
}

export const useRegister = () => {
  const username = ref<string>('');
  const email = ref<string>('');
  const password = ref<string>('');
  const repeat_password = ref<string>('');

  return {
    username,
    email,
    password,
    repeat_password,
    register: register(username, email, password, repeat_password),
  }
}
