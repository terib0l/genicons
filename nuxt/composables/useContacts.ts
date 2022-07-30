import type { Ref } from 'vue';

const sendMessage = (sent_message: Ref<string>) => async () => {
  const { accessToken, logout } = useAuth();

  if (sent_message.value) {
    if (window.confirm(`${sent_message.value}\n\nこの内容で送信しますか？`)) {
      const formData = new FormData();
      formData.append("contents", sent_message.value);

      const options = {
        method: 'POST',
        headers: {'Authorization': `Bearer ${accessToken.value}`},
        body: formData,
        baseURL: useRuntimeConfig().baseUrl
      }

      const { data, error } = await useAsyncData(
        'contactForm',
        () => $fetch('/send/contact', options)
      );

      if (error.value?.response.status == 401){  // Authentication Error Pattern
        alert('Please one more login!')
        await logout()
      } else if(error.value){                    // Something Error Pattern
        alert('Connection error!')
      } else {                                   // Success Pattern
        alert('Message sent successfully!')
        sent_message.value = '';
      }
    }
  } else {
    alert("Please type your message!!");
  }
}

export const useContacts = () => {
  const sent_message = ref<string>('');

  return {
    sent_message,
    sendMessage: sendMessage(sent_message)
  }
}
