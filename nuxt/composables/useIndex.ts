import type { Ref } from 'vue';
import JSZip from "jszip";

const fetchGallery = (gallerys: Ref<Array<string>>, loading: Ref<boolean>) => async () => {
  const options = {
    method: 'GET',
    params: {
      gallery_num: 9
    },
    baseURL: useRuntimeConfig().baseUrl,
  };

  const { data, error } = await useLazyAsyncData(
    'gallery',
    () => $fetch('/fetch/gallery', options)
  )

  if (error.value){
    console.log("Connection Error!");
    return;
  } else {
    JSZip.loadAsync(data.value).then(function(zipData){
      Object.values(zipData.files).forEach(function (value) {
        gallerys.value.push(URL.createObjectURL(new Blob([value._data.compressedContent])));
      });
      loading.value = true;
    });
  }
}

const uploadImage = (file: Ref<Blob|null>) => (event: any) => {
  file.value = event.target.files[0];
}

const generateProduct = (file: Ref<Blob|null>, productId: Ref<string>) => async () => {
  const { accessToken, logout } = useAuth();

  if(file.value) {
    const formData = new FormData();
    formData.append('image', file.value);

    const options = {
      method: 'POST',
      headers: {'Authorization': `Bearer ${accessToken.value}`},
      body: formData,
      baseURL: useRuntimeConfig().baseUrl
    };

    const { data, error } = await useAsyncData(
      'generateProduct',
      () => $fetch('/generate/product', options)
    );

    if (error.value?.response.status == 401){
      alert('Please one more login!');
      await logout();
    } else if(error.value) {
      alert('Connection error');
    } else {
      productId.value = data.value.product_id;
      document.getElementById('productDialog').showModal();
    }
  } else {
    alert("Please set JPG!!");
  }
}

export const useIndex = () => {
  const loading = ref<boolean>(false);
  const gallerys = ref<Array<string>>([]);

  const file = ref<Blob|null>(null);
  const productId = ref<string>('');

  return {
    loading, 
    gallerys, 
    productId, 
    fetchGallery: fetchGallery(gallerys, loading),
    uploadImage: uploadImage(file),
    generateProduct: generateProduct(file, productId),
  }
}
