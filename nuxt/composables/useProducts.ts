import type { Ref } from 'vue';
import JSZip from "jszip";

type productData = {
  id: string;
  img: string;
}

const fetchProductIds = (productList: Ref<Array<productData>>, productIdsFlag: Ref<boolean>) => async () => {
  const { accessToken, logout } = useAuth();

  const options = {
    method: 'GET',
    headers: {'Authorization': `Bearer ${accessToken.value}`},
    baseURL: useRuntimeConfig().baseUrl,
  };

  const { data, error } = await useAsyncData(
    'productIds',
    () => $fetch('/fetch/product/ids', options)
  );

  if (error.value?.response.status == 401){
    alert('Please one more login!');
    await logout();
  } else if(error.value){
    alert('Connection error!\n\nPlease contact!!');
    navigateTo('/contact');
  } else {
    for (let i = 0; i < data.value?.length; i++){
      productList.value.push({
        id: data.value[i],
        img: ""
      });
    }

    if ( productList.value.length > 0 ){
      productIdsFlag.value = true;
    }
  }
}

const fetchProductOrigins = (productList: Ref<Array<productData>>) => async () => {
  const { accessToken, logout } = useAuth();

  const options = {
    method: 'GET',
    headers: {'Authorization': `Bearer ${accessToken.value}`},
    baseURL: useRuntimeConfig().baseUrl,
  };

  const { data, error } = await useLazyAsyncData(
    'productOrigins',
    () => $fetch('/fetch/product/origins', options)
  );

  if (error.value?.response.status == 401){
    alert("Please one more login!")
    await logout()
  } else if(error.value){
    console.log('Fetch productOrigins error');
  } else {
    JSZip.loadAsync(data.value).then(function(zipData){
      Object.values(zipData.files).forEach(function (value, index) {
        productList.value[index].img = URL.createObjectURL(new Blob([value._data.compressedContent]));
      });
    });
  }
}

const fetchProduct = () => async (productId: string) => {
  const { accessToken, logout } = useAuth();

  if (window.confirm(`Will you download this product??\n\n${productId}`)){
    const options = {
      method: 'GET',
      headers: {'Authorization': `Bearer ${accessToken.value}`},
      params: {
        product_id: productId
      },
      baseURL: useRuntimeConfig().baseUrl,
    };

    const { data, error } = await useAsyncData(
      'product',
      () => $fetch('/fetch/product', options)
    );

    if (error.value?.response.status == 401){
      alert("Please one more login!");
      await logout();
    } else if(error.value){
      alert('Connection error!');
    } else {
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
}

export const useProducts = () => {
  const productList = ref<Array<productData>>([]);
  const productIdsFlag = ref<boolean>(false);

  return {
    productList,
    productIdsFlag,
    fetchProductIds: fetchProductIds(productList, productIdsFlag),
    fetchProductOrigins: fetchProductOrigins(productList),
    fetchProduct: fetchProduct(),
  }
}
