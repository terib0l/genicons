import type { Ref } from 'vue';

const login = (username: Ref<string>, password: Ref<string>) => async () => {
  if (!username.value || !password.value){
    alert("Please type your username and password!");
    return;
  }

  const formData = new FormData()
  formData.append("username", username.value)
  formData.append("password", password.value)

  const options = {
    method: 'POST',
    body: formData,
    baseURL: useRuntimeConfig().baseUrl
  }

  const { data, error } = await useAsyncData(
    'token',
    () => $fetch('/token', options)
  );

  if (error.value){
    alert("Invalid User");
    return;
  }

  localStorage.setItem("access_token", data.value.access_token)

  const to = useRoute().redirectedFrom?.path || '/';
  navigateTo(to);
}

const logout = () => async () => {
  localStorage.removeItem("access_token")
  return navigateTo('/login')
}

export const useAuth = () => {
  const accessToken = ref<string|null>(localStorage.getItem("access_token"));
  const username = ref<string>('');
  const password = ref<string>('');

  return {
    accessToken,
    username,
    password,
    login: login(username, password),
    logout: logout(),
  }
}
